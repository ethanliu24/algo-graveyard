import Verify from "../auth/verify.jsx";

export default function Authenticate() {
  return (
    <div className="flex justify-center items-center w-full h-full">
      <Verify closable={false} className="mt-[-15%]" />
    </div>
  );
}