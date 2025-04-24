import { useState, useEffect, useRef } from "react";
import { Editor } from "@monaco-editor/react";
import { faRotate, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Tooltip } from "react-tooltip";
import TextDisplay from "../common/text_display";
import ModalContainer from "../common/modal";
import SolutionForm from "./solution_form";
import { useToastContext } from "../../contexts/toast_context";
import { formatDate, getLanguageHighlighter, getReqHeader } from "../../utils/utils";

export default function Solution(props) {
  const [openForm, setOpenForm] = useState(false);
  const [editorHeight, setEditorHeight] = useState(200);
  const toast = useToastContext();

  const containerRef = useRef(null);
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;

    const updateHeight = () => {
      const contentHeight = editor.getContentHeight();
      setEditorHeight(contentHeight);
      editor.layout(); // re-layout the editor
    };

    // Update height on mount
    updateHeight();

    // Update height on content change
    editor.onDidContentSizeChange(() => {
      updateHeight();
    });
  };

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.layout();
    }
  }, [editorHeight]);

  const handleDelete = () => {
    if (!window.confirm("Are you sure you want to delete this solution?")) {
      return;
    }

    const req = {
      method: "DELETE",
      headers: getReqHeader(),
    };

    fetch(`/api/questions/${props.questionId}/solutions/${props.data.id}`, req)
      .then(response => {
        if (response.status == 401 || response.status === 403) {
          props.setIsAdmin(false);
        }

        return response.json();
      })
      .then(json => {
        if (json === null) {  // delete successful
          toast.show({ severity: "success", summary: "Success", className: "success", detail: "Solution deleted!" });
          props.removeSolution(props.data.id);
        } else if (json.detail) {
          toast.show({ severity: "danger", summary: "Error", className: "error", detail: json.detail });
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const updateSuccess = (newData) => {
    props.updateSolution(newData.id, newData);
    setOpenForm(false);
    toast.show({ severity: "success", summary: "Success", className: "success", detail: "Solution updated!" });
  };

  return (!props.data
    ? (
      <div className="flex justify-center items-center w-full h-full">
        <h1 className="text-xs font-light italic">No solutions available</h1>
      </div>
    )
    : (
      <div>
        <h1 className="text-xl text-wrap mb-2">{props.data.summary}</h1>
        <div className="flex justify-start items-stretch gap-2 mb-4">
          <div className="chip w-fit text-nowrap">{formatDate(props.data.last_modified)}</div>
          <button className="chip p-1 hover:bg-gray-300 text-black"
            onClick={() => setOpenForm(true)}
            data-tooltip-id="edit-solution" data-tooltip-content="Edit solution">
            <FontAwesomeIcon icon={faRotate} />
            <Tooltip id="edit-solution" />
          </button>
          <button className="chip p-1 hover:bg-gray-300 text-black"
            onClick={handleDelete}
            data-tooltip-id="delete-solution" data-tooltip-content="Delete solution">
            <FontAwesomeIcon icon={faTrash} />
            <Tooltip id="delete-solution" />
          </button>
        </div>
        <h2 className="text-md first-letter:text-primary">{`Time: O(${props.data.time_complexity})`}</h2>
        <h2 className="text-md first-letter:text-primary mb-4">{`Space: O(${props.data.space_complexity})`}</h2>
        <TextDisplay content={props.data.explanation} />
        <div className="text-[14px] mb-8">
          <h1 className="text-[18px] mb-2 first-letter:text-primary">Ai Analysis</h1>
          <p>{`Time: O(${props.data.ai_analysis.time_complexity}) Space: O(${props.data.ai_analysis.space_complexity})`}</p>
          <p>{props.data.ai_analysis.feedback}</p>
        </div>
        <div ref={containerRef} className="w-full">
          <Editor
            height={editorHeight}
            width="100%"
            language={getLanguageHighlighter(props.data.language) || "plaintext"}
            options={{
              readOnly: true,
              domReadOnly: true,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              wordWrap: "on"
            }}
            value={props.data.code}
            theme="vs-dark"
            // onMount={handleEditorDidMount}
          />
        </div>
        {openForm
          ? <ModalContainer closeModal={() => setOpenForm(false)} title="Edit Question"
              content={<SolutionForm create={false} data={props.data} methodSuccessful={(d) => updateSuccess(d)}
                questionId={props.question.id} questionTitle={props.question.title} questionPrompt={props.question.prompt} />} />
          : null}
      </div>
    )
  );
}