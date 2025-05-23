import { useEffect, useState } from 'react';
import { Password } from 'primereact/password';
import { useToastContext } from '../../contexts/toast_context';
import { getReqHeader } from '../../utils/utils';
import { faXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

/**
 * This component is closable. To make it closable, set "props.closable" to true and provide a
 * function at "props.closeComponent" that unmounts the component.
 */
export default function Verify(props) {
  const [secret, setSecret] = useState("");
  const [show, setShow] = useState(true);
  const verificationRes = useToastContext();

  const toastLife = 3000;

  useEffect(() => {
    const toast = { severity: "info", life: 5000, className: "info",
      summary: "Info", detail: "Only admins are allowed to manage questions." }
    setTimeout(() => verificationRes.show(toast), 100);
  }, []);

  const handleVerification = async () => {
    let result = { severity: "danger", summary: "Error", detail: "Something went wrong.", life: toastLife, className: "error" };

    if (secret === "") {
      result = { severity: "warning", summary: "Warning", detail: "Please enter app secret.", life: toastLife, className: "warning" };
    } else {
      const req = {
        method: "POST",
        headers: getReqHeader(),
        body: JSON.stringify({ secret: secret })
      }

      await fetch("/api/auth", req)
        .then(response => {
          if (response.ok) {
            result = { severity: "success", summary: "Success", detail: "You are authenticated!", life: toastLife, className: "success" };
            setSecret("");
            if (props.closable) {
              setShow(false);
              setTimeout(() => props.closeComponent(), toastLife + 1000);
            }
          } else {
            result = { severity: "danger", summary: "Error", detail: "Authentication Failed.", life: toastLife, className: "error" };
          }
        })
        .catch(err => {
          throw err;
        });
    }

    verificationRes.show(result);
  };  

  return (
    <div className={`flex flex-col justify-center items-center w-fit h-fit rounded-sm
      bg-gray-50 shadow-sm z-100
      ${props.positionStyle ? props.positionStyle : "relative"}
      ${props.className ? props.className : ""}`}>
      <div className={`${show ? "" : "hidden"}`}>
        <h2 className="w-full rounded-t-sm p-0.5 bg-primary text-white text-center relative">Authenticate
          {props.closable
            ? <FontAwesomeIcon icon={faXmark} size="md" className="absolute top-1/2 right-0 -translate-y-1/2 cursor-pointer mr-2"
                onClick={() => setTimeout(props.closeComponent(), toastLife)} />
            : null}
        </h2>
        <div className="flex-1 flex flex-col justify-around items-center gap-4 p-4">
          <Password value={secret} onChange={(e) => setSecret(e.target.value)} feedback={false} tabIndex={1}
            placeholder="Super secret secret" className="w-full" />
          <button className="w-full p-0.5 cursor-pointer" onClick={handleVerification}>Verify</button>
        </div>
      </div>
    </div>
  )
}
