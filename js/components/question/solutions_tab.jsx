import { useState } from "react";
import ModalContainer from "../common/modal";
import SolutionForm from "./solution_form";

export default function SolutionTab(props) {
  const [solutions, setSolutions] = useState(props.solutions || []);
  const [openForm, setOpenForm] = useState(false);

  const creationSucess = (slnData) => {
    setOpenForm(false);
    setSolutions([...solutions, slnData]);
    console.log(slnData)
  }

  return (
    <div className="flex flex-col justify-start items-start w-full">
      <button onClick={() => setOpenForm(true)}>Add solution</button>
      {openForm
        ? <ModalContainer closeModal={() => setOpenForm(false)} title="Add Solution"
            content={<SolutionForm create={true} questionId={props.questionId} methodSuccessful={(d) => creationSucess(d)} />} />
        : null
      }
    </div>
  );
}