import { useState } from "react";
import { Tooltip } from "react-tooltip";
import { faRotate, faTrash, faPen, faLightbulb, faHashtag } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ModalContainer from "../common/modal.jsx";
import QuestionForm from "./question_form.jsx";
import TextDisplay from "../common/text_display.jsx";
import { getStatusIcon, getDifficultyStyle } from "../../utils/assets.jsx";
import { formatDate, capitalizeFirst, getReqHeader } from "../../utils/utils.js";

export default function DescriptionTab(props) {
  const [openModal, setOpenModal] = useState(false);

  const handleDelete = () => {
    if (!window.confirm("Are you sure you want to delete the question?")) {
      return;
    }

    const req = {
      method: "DELETE",
      headers: getReqHeader(),
    };

    fetch(`/api/questions/${props.data.id}`, req)
      .then(response => {
        if (response.ok) {
          window.location.href = "/";
        } else if (response.status == 401 || response.status === 403) {
          alert("ur not admin lmao");
          props.setIsAdmin(false);
        } else {
          alert("handle error del q");
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const handleUpdate = (newData) => {
    setOpenModal(false);
    props.updateQuestion(newData);
  };

  return (
    <div className="flex flex-col justify-between items-start gap-16 w-full h-full">
      <div className="w-full flex-1">
        <div className="flex justify-start items-center gap-4 mb-2">
          {getStatusIcon(props.data.status, 0, false)}
          <h1 className="text-xl text-wrap">{props.data.title}</h1>
        </div>
        <div className="flex justify-start items-center gap-2 text-xs mb-8">
          <div className="chip" style={getDifficultyStyle(props.data.difficulty)}>{capitalizeFirst(props.data.difficulty)}</div>
          <div className="chip">{capitalizeFirst(props.data.source)}</div>
          <div className="chip text-nowrap">{formatDate(props.data.created_at)}</div>
          <button className="chip p-1 hover:bg-gray-300 text-black"
            onClick={() => setOpenModal(true)}
            data-tooltip-id="edit-question" data-tooltip-content="Edit question">
            <FontAwesomeIcon icon={faRotate} />
            <Tooltip id="edit-question" />
          </button>
          <button className="chip p-1 hover:bg-gray-300 text-black"
            onClick={handleDelete}
            data-tooltip-id="delete-question" data-tooltip-content="Delete question">
            <FontAwesomeIcon icon={faTrash} />
            <Tooltip id="delete-question" />
          </button>
        </div>
        <TextDisplay content={props.data.prompt} />
      </div>
      <div>
        {props.data.tags.length !== 0
          ? <AccordianItem title={"Tags"} icon={faHashtag} content={
              <div className="flex justify-start items-center gap-1 flex-wrap">
                {props.data.tags.map((tag, i) => {
                  return (<div key={tag + i}
                      className="chip w-fit text-md">{`# ${tag}`}
                    </div>);
                })}
              </div>}
            />
          : null}
        {props.data.notes.map((note, i) => {
          return (
            <AccordianItem title={"Note " + (i + 1)} icon={faPen}
              content={<p className="text-xs font-light">{note}</p>} />
          );
        })}
        {props.data.hints.map((hint, i) => {
          return (
            <AccordianItem title={"Hint " + (i + 1)} icon={faLightbulb}
              content={<p className="text-xs font-light">{hint}</p>} />
          );
        })}
      </div>
      {openModal
        ? <ModalContainer closeModal={() => setOpenModal(false)} title="Edit Question"
            content={
              <QuestionForm create={false} link={props.data.link} source={props.data.source} difficulty={props.data.difficulty}
                status={props.data.status} tags={props.data.tags} title={props.data.title} prompt={props.data.prompt} notes={props.data.notes}
                hints={props.data.hints} questionId={props.data.id} updateSuccessful={handleUpdate} />
            } />
        : null}
    </div>
  );
}

function AccordianItem(props) {
  return (
    <details className="w-full mb-3">
      <summary className="cursor-pointer w-full mb-1 first-letter:text-primary">
        <label className="ml-1 mr-2 text-xs">{props.title}</label>
        <FontAwesomeIcon icon={props.icon} size="xs" />
      </summary>
      {props.content}
    </details>
  );
}