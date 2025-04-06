import { useEffect, useState, useRef } from 'react';
import { Password } from 'primereact/password';
import { Toast } from 'primereact/toast';
import { getReqHeader } from '../../utils/utils';

export default function Verify(props) {
  const [secret, setSecret] = useState("");
  const verificationRes = useRef(null);

  useEffect(() => {
    const toast = { severity: "info", life: 5000, className: "info",
      summary: "Info", detail: "Enter the app secret to manage questions." }
    verificationRes.current.show(toast);
  }, []);

  const handleVerification = async () => {
    let result = { severity: "danger", summary: "Error", detail: "Something went wrong.", className: "error" };

    if (secret === "") {
      result = { severity: "warning", summary: "Warning", detail: "Please enter app secret.", className: "warning" };
    } else {
      const req = {
        method: "POST",
        header: getReqHeader(),
        body: JSON.stringify({ secret: secret })
      }

      await fetch("api/auth", req)
        .then(response => {
          if (response.ok) {
            result = { severity: "success", summary: "Success", detail: "You are authenticated!", className: "success" };
          } else {
            result = { severity: "danger", summary: "Error", detail: "Authentication Failed.", className: "error" };
          }
        })
        .catch(err => {
          throw err;
        });
    }

    verificationRes.current.show(result);
  };

  return (
    <div className={`flex flex-col justify-center items-center w-fit h-fit rounded-sm
      bg-gray-50 shadow-sm
      ${props.className ? props.className : ""}`}>
      <h2 className="w-full rounded-t-sm p-0.5 bg-primary text-white text-center">Authenticate</h2>
      <div className="flex-1 flex flex-col justify-around items-center gap-4 p-4">
        <Password value={secret} onChange={(e) => setSecret(e.target.value)} feedback={false} tabIndex={1}
          placeholder="Secret" className="w-full" />
        <Toast ref={verificationRes} position="bottom-right" />
        <button className="w-full p-0.5 cursor-pointer" onClick={handleVerification}>Verify</button>
      </div>
    </div>
  )
}
