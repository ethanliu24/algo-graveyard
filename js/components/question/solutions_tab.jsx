import { useState } from "react";
import { faCheck, faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ModalContainer from "../common/modal";
import SolutionForm from "./solution_form";
import { formatDate } from "../../utils/utils";
import { getLanguageIcon } from "../../utils/assets";

export default function SolutionTab(props) {
  const [solutions, setSolutions] = useState(props.solutions || []);
  const [openForm, setOpenForm] = useState(false);

  const creationSucess = (slnData) => {
    setOpenForm(false);
    setSolutions([...solutions, slnData]);
  }

  return (
    <div className="flex flex-col justify-start items-start w-full">
      <button className="mb-2" onClick={() => setOpenForm(true)}>Add solution</button>
      {solutions.map((sln, i) => {
        return (
          <div className="flex justify-start items-center gap-4 min-w-full w-fit hover:bg-gray-200 cursor-pointer
            px-4 py-2 text-[12px] rounded">
            <div className="text-gray-500">{i + 1}</div>
            <FontAwesomeIcon icon={sln.accepted ? faCheck : faX} color={sln.accepted ? "#6bd177" : "#eb4b63"} />
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
            content={<SolutionForm create={true} questionId={props.questionId} methodSuccessful={(d) => creationSucess(d)} />} />
        : null
      }
    </div>
  );
}