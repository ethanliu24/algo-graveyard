import { useState, useRef } from 'react';
import { Password } from 'primereact/password';
import { Toast } from 'primereact/toast';

export default function Verify(props) {
  const [secret, setSecret] = useState("");
  const verificationRes = useRef(null);

  const handleVerification = () => {
    let result = { severity: "info", summary: "Info", detail: "Content", sticky: true, className: "info" };
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
