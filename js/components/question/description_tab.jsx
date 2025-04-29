import { useState } from "react";
import { Tooltip } from "react-tooltip";
import {
  faRotate, faTrash, faPen, faLightbulb, faHashtag, faPenToSquare, faUpRightFromSquare, faDownload
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Markdown from "react-markdown";
import ModalContainer from "../common/modal.jsx";
import QuestionForm from "./question_form.jsx";
import ExportForm from "../export/export_form.jsx";
import { useToastContext } from "../../contexts/toast_context.jsx";
import { getStatusIcon, getDifficultyStyle } from "../../utils/assets.jsx";
import { formatDate, capitalizeFirst, getReqHeader } from "../../utils/utils.js";

export default function DescriptionTab(props) {
  const [openQuestionForm, setOpenQuestionForm] = useState(false);
  const [openExportForm, setOpenExportForm] = useState(false);

  const toast = useToastContext();

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
          toast.show({ severity: "danger", summary: "Error", className: "error", detail: "Ur not admin lol" })
          props.setIsAdmin(false);
        } else if (response.status >= 500) {
          toast.show({ severity: "warning", summary: "Warning", className: "warning", detail: `Internal server error ${response.status}` })
        } else {
          toast.show({ severity: "danger", summary: "Error", className: "error", detail: `Error: ${response.status}` })
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const handleUpdate = (newData) => {
    setOpenQuestionForm(false);
    props.updateQuestion(newData);
    toast.show({ severity: "success", summary: "Success", className: "success", detail: "Question updated!" });
  };

  const handleReparse = () => {
    props.setIsLoading(true);

    const req = {
      method: "PUT",
      headers: getReqHeader()
    };

    fetch(`/api/questions/${props.data.id}/parse`, req)
      .then(response => {
        if (response.status == 401 || response.status === 403) {
          props.setIsAdmin(false);
        }

        return response.json();
      })
      .then(data => {
        if (data.id) {
          toast.show({ severity: "success", summary: "Success", className: "success", detail: "Reparsed successful." });
          props.updateQuestion(data);
        }

        if (data.detail) {
          toast.show({ severity: "danger", summary: "Error", life: 7000, className: "error", detail: data.detail });
        }
      })
      .catch(err => {
        throw err
      }).finally(() => {
        props.setIsLoading(false);
      });
  }

  return (
    <div className="flex flex-col justify-start items-stretch gap-8 w-full h-full">
      <div className="w-full h-fit">
        <div className="flex justify-start items-center gap-4 mb-2">
          {getStatusIcon(props.data.status, 0, false)}
          <h1 className="text-xl truncate"
            data-tooltip-id="title-tooltip" data-tooltip-content={props.data.title}>
            {props.data.title}
          </h1>
          <Tooltip id="title-tooltip" />
        </div>
        <div className="flex justify-start items-center gap-2 text-xs mb-4 overflow-x-auto">
          <div className="chip" style={getDifficultyStyle(props.data.difficulty)}>{capitalizeFirst(props.data.difficulty)}</div>
          <div className="chip">{capitalizeFirst(props.data.source)}</div>
          <div className="chip text-nowrap">{formatDate(props.data.created_at)}</div>
          <button className="chip chip-btn"
            onClick={() => setOpenQuestionForm(true)}
            data-tooltip-id="edit-question" data-tooltip-content="Edit question">
            <FontAwesomeIcon icon={faPenToSquare} />
            <Tooltip id="edit-question" />
          </button>
          <button className="chip chip-btn"
            onClick={handleDelete}
            data-tooltip-id="delete-question" data-tooltip-content="Delete question">
            <FontAwesomeIcon icon={faTrash} />
            <Tooltip id="delete-question" />
          </button>
          <button className="chip chip-btn"
            onClick={handleReparse}
            data-tooltip-id="reparse-question" data-tooltip-content="Reparse question">
            <FontAwesomeIcon icon={faRotate} />
            <Tooltip id="reparse-question" />
          </button>
          <button className="chip chip-btn"
            onClick={() => setOpenExportForm(true)}
            data-tooltip-id="download-report" data-tooltip-content="Download report">
            <FontAwesomeIcon icon={faDownload} />
            <Tooltip id="download-report" />
          </button>
          <a href={props.data.link} target="_blank" rel="noreferrer noopener" className="chip chip-btn"
            data-tooltip-id="navigate-to-source" data-tooltip-content="Navigate to source">
            <FontAwesomeIcon icon={faUpRightFromSquare} />
            <Tooltip id="navigate-to-source" />
          </a>
        </div>
        <div className="markdown-content"><Markdown children={props.data.prompt} /></div>
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
      {openQuestionForm
        ? <ModalContainer closeModal={() => setOpenQuestionForm(false) } title="Edit Question"
            content={
              <QuestionForm create={false} link={props.data.link} source={props.data.source} difficulty={props.data.difficulty}
                status={props.data.status} tags={props.data.tags} title={props.data.title} prompt={props.data.prompt} notes={props.data.notes}
                hints={props.data.hints} questionId={props.data.id} updateSuccessful={handleUpdate} />
            } />
        : null}
      {openExportForm
        ? <ModalContainer closeModal={() => setOpenExportForm(false) } title="Download"
            content={
              <ExportForm question={props.data}
                solutionSummaries={props.data.solutions.map(sln => sln.summary)}
                exportSuccessful={() => setOpenExportForm(false)}
            />} />
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