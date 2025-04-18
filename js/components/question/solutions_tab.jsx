import { useState } from "react";
import ModalContainer from "../common/modal";

export default function SolutionTab(props) {
  const [solutions, setSolutions] = useState(props.solutions || []);
  const [openForm, setOpenForm] = useState(false);

  return (
    <div className="flex flex-col justify-start items-start w-full">
      <button onClick={() => setOpenForm(true)}>Add solution</button>
      {openForm
        ? <ModalContainer closeModal={() => setOpenForm(false)} title="Add Solution" />
        : null
      }
    </div>
  );
}