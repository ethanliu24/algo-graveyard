import { useState } from "react";
import ModalContainer from "../common/modal";
import SolutionForm from "./solution_form";
import { useToastContext } from "../../contexts/toast_context";
import { formatDate } from "../../utils/utils";
import { getLanguageIcon, getAcceptedIcon } from "../../utils/assets";

export default function SolutionTab(props) {
  const [openForm, setOpenForm] = useState(false);
  const toast = useToastContext();

  const creationSucess = (slnData) => {
    setOpenForm(false);
    props.addSolution(slnData);
    toast.show({ severity: "success", summary: "Success", className: "success", detail: "Solution created!" });
  }

  return (
    <div className="flex flex-col justify-start items-start w-full">
      <button className="mb-2" onClick={() => setOpenForm(true)}>Add solution</button>
      {props.solutions.map((sln, i) => {
        return (
          <div className="flex justify-start items-center gap-4 min-w-full w-fit hover:bg-gray-200 cursor-pointer
            px-4 py-2 text-[12px] rounded select-none"
            onClick={() => props.displaySolution(sln)}>
            <div className="text-gray-500">{i + 1}</div>
            {getAcceptedIcon(sln.accepted)}
            <div className="flex-1">
              <h1 className="text-base">{sln.summary}</h1>
              <h2 className="text-nowrap truncate">{formatDate(sln.last_modified)}</h2>
            </div>
            {getLanguageIcon(sln.language)}
          </div>
        );
      })}
      {openForm
        ? <ModalContainer closeModal={() => setOpenForm(false)} title="Add Solution"
            content={<SolutionForm create={true} data={{}} questionId={props.question.id}
            questionTitle={props.question.title} questionPrompt={props.question.prompt}
              methodSuccessful={(d) => creationSucess(d)} />} />
        : null
      }
    </div>
  );
}