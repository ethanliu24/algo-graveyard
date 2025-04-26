import { useState, useEffect, useRef } from "react";
import { Editor } from "@monaco-editor/react";
import { faRotate, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Tooltip } from "react-tooltip";
import Markdown from "react-markdown";
import ModalContainer from "../common/modal";
import SolutionForm from "./solution_form";
import { useToastContext } from "../../contexts/toast_context";
import { formatDate, getLanguageHighlighter, getReqHeader } from "../../utils/utils";
import { getAcceptedIcon } from "../../utils/assets";

export default function Solution(props) {
  const [openForm, setOpenForm] = useState(false);
  const [editorHeight, setEditorHeight] = useState(500);
  const toast = useToastContext();

  const containerRef = useRef(null);
  const editorRef = useRef(null);

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

    fetch(`/api/questions/${props.question.id}/solutions/${props.data.id}`, req)
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

  const formatExplanation = (data) => {
    let res = [];
    res.push("### Explaination");
    res.push(`- Time: O(${data.time_complexity})`);
    res.push(`- Space: O(${data.space_complexity})`);
    res.push(`\n${data.explanation}`);
    res.push("### AI Analysis");
    res.push(`- Time: O(${data.ai_analysis.time_complexity})`);
    res.push(`- Space: O(${data.ai_analysis.space_complexity})`);
    res.push(`\n${data.ai_analysis.feedback}`);
    return res.join("\n");
  }

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

  return (!props.data
    ? (
      <div className="flex justify-center items-center w-full h-full">
        <h1 className="text-xs font-light italic">No solutions available</h1>
      </div>
    )
    : (
      <div>
        <div className="flex justify-start items-center gap-4 mb-2">
          {getAcceptedIcon(props.data.accepted)}
          <h1 className="text-xl text-wrap">{props.data.summary}</h1>
        </div>
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
        <div className="markdown-content">
          <Markdown children={
            formatExplanation(props.data)
          } />
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