import { useState } from 'react';
import { Password } from 'primereact/password';

export default function Verify(props) {
  const [secret, setSecret] = useState("");

  return (
    <div className={`flex flex-col justify-center items-center w-fit h-fit rounded-sm
      bg-gray-50 shadow-sm
      ${props.classNames}`}>
      <h2 className="w-full rounded-t-sm bg-primary text-white text-center">Authenticate</h2>
      <div className="flex flex-col justify-around items-center gap-4 p-4">
        <Password value={secret} onChange={(e) => setSecret(e.target.value)} feedback={false} tabIndex={1}
          placeholder="Secret" className="p-0.5" />
        <button className="w-full p-0.5 cursor-pointer">Verify</button>
      </div>
    </div>
  )
}
