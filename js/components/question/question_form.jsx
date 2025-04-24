import { useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { faPlus, faRotate } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Dropdown, MultiSelect } from "../common/drop_down.jsx";
import { getReqHeader, formatQueries } from "../../utils/utils";
import QuestionHelper, { HelperStrTemplate } from "./question_helpers.jsx";
import { useToastContext } from "../../contexts/toast_context.jsx";
import Verify from "../auth/verify.jsx";

export default function QuestionForm(props) {
  const [link, setLink] = useState(props.link || "");
  const [source, setSource] = useState(props.source || "");
  const [difficulty, setDifficulty] = useState(props.difficulty || "");
  const [status, setStatus] = useState(props.status || "");
  const [tags, setTags] = useState(props.tags || []);
  const [title, setTitle] = useState(props.title || "");
  const [prompt, setPrompt] = useState(props.prompt || "");
  const [notes, setNotes] = useState(props.notes || []);
  const [hints, setHints] = useState(props.hints || []);
  // const [testCases, setTestCases] = useState([]);
  const [metadata, setMetadata] = useState({});
  const [showVerify, setShowVerify] = useState(false);

  const toast = useToastContext();

  useEffect(() => {
    getMetadata();
  }, []);

  const getMetadata = () => {
    const req = {
      method: "GET",
      headers: getReqHeader()
    };

    const metadataQuery = {
      sources: true,
      difficulties: true,
      statuses: true,
      tags: true
    };

    fetch(`/api/metadata?${formatQueries(metadataQuery)}`, req)
      .then(res => res.json())
      .then(data => {
        setMetadata({
          sources: data.sources,
          difficulties: data.difficulties,
          statuses: data.statuses,
          tags: data.tags,
        });
      })
      .catch(err => {
        throw err;
      });
  }

  const updateNotes = (val, idx, remove) => {
    const updated = updateHelper(notes, val, idx, remove);
    setNotes(updated);
  };

  const updateHints = (val, idx, remove) => {
    const updated = updateHelper(hints, val, idx, remove);
    setHints(updated);
  };

  // const updateTestCases = (val, idx, remove) => {
  //   const updated = updateHelper(testCases, val, idx, remove);
  //   setTestCases(updated);
  // }

  const updateHelper = (lst, val, idx, remove) => {
    const updated = lst.slice(0, idx);
    if (!remove) updated.push(val);
    updated.push(...lst.slice(idx + 1));
    return updated;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      source: source,
      link: link,
      difficulty: difficulty,
      status: status,
      title: title,
      prompt: prompt,
      notes: notes,
      hints: hints,
      tags: tags
    };

    if (isFormValid(data)) {
      props.create ? createQuestion(data) : updateQuestion(data);
    }
  };

  const isFormValid = (data) => {
    if (data.link !== "") {
      if (!data.source) {
        toast.show({ severity: "danger", summary: "Error", className: "error", detail: "Source must be selected" });
      }

      return data.source !== "";
    }

    if (!data.difficulty || !data.status || !data.source) {
      let msg = [
        !data.source && "Source",
        !data.difficulty && "Difficulty",
        !data.status && "Status"
      ].filter(Boolean).join(", ");
      msg += " must be selected."

      toast.show({ severity: "danger", summary: "Error", className: "error", detail:  msg });
      return false;
    }

    if (data.title.length === 0 || data.title.length > 70) {
      toast.show({ severity: "danger", summary: "Error", className: "error", detail: "There must be a title and should be under 70 characters." });
      return false;
    }

    if (data.prompt.length === 0) {
      toast.show({ severity: "danger", summary: "Error", className: "error", detail: "Question prompt must be entered." });
      return false;
    }

    return true;
  };

  const createQuestion = (data) => {
    const req = {
      method: "POST",
      headers: getReqHeader(),
      body: JSON.stringify(data)
    };

    fetch("/api/questions", req)
      .then(response => {
        if (!response.ok) {
          if (response.status == 401 || response.status === 403) {
            toast.show({ severity: "danger", summary: "Error", className: "error", detail: "You are not authorized to perform this action." });
            setShowVerify(true);
          }
        }

        return response;
      })
      .then(res => res.json())
      .then(data => {
        if (data.id) {  // This means creation was successful
          window.location.href = `/questions/${data.id}`;
        } else {
          toast.show({ severity: "danger", summary: "Error", className: "error", detail: data.detail });
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const updateQuestion = (data) => {
    const req = {
      method: "PUT",
      headers: getReqHeader(),
      body: JSON.stringify(data)
    };

    fetch(`/api/questions/${props.questionId}`, req)
      .then(response => {
        if (response.status == 401 || response.status === 403) {
          setShowVerify(true);
        }

        return response;
      })
      .then(res => res.json())
      .then(data => {
        if (data.id) {
          toast.show({ severity: "success", summary: "Success", className: "success", detail: "Question updated!" });
          props.updateSuccessful(data);
        }

        if (data.detail) {
          toast.show({ severity: "danger", summary: "Error", className: "error", detail: data.detail });
        }
      })
      .catch(err => {
        throw err
      })
  };

  return (
    <div className="flex flex-col justify-start items-start gap-4 w-full text-[14px]">
      {showVerify
        ? <Verify closable={true} closeComponent={() => setShowVerify(false)}
            positionStyle="fixed top-0 right-0 m-8" className="text-base" />
        : null}
      <div className="form-section">
        <label className="section-title">Link</label>
        <div className="flex justify-between items-center gap-4 w-full">
          <InputText placeholder="" value={link} onChange={(e) => setLink(e.target.value)}
            className="flex-1 rounded-xs py-1" />
          <Dropdown title="Source" className="grow-0" value={source} options={metadata.sources || []} updateValue={(s) => setSource(s)} />
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Title</label>
        <InputText placeholder="" value={title} onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded-xs py-1" />
      </div>
      <div className="flex flex-col justify-start items-start">
        <label className="section-title">Category</label>
        <div className="flex justify-start items-stretch gap-4 gap-y-2 flex-wrap grow w-full">
          <Dropdown title="Difficulty" value={difficulty} options={metadata.difficulties || []} updateValue={(s) => setDifficulty(s)} />
          <Dropdown title="Status" value={status} options={metadata.statuses || []} updateValue={(s) => setStatus(s)} />
          <MultiSelect title="Tags" selected={tags} options={metadata.tags || []} updateValue={(t) => setTags(t)} />
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Prompt</label>
        <InputTextarea placeholder="" value={prompt} autoResize onChange={(e) => setPrompt(e.target.value)}
          className="border-1 rounded-xs border-gray-300 w-full min-h-[20rem]" />
      </div>
      <QuestionHelper title="Notes" helperTemplate={HelperStrTemplate} defaultValue=""
        list={notes} updateList={updateNotes} setList={(l) => setNotes(l)} />
      <QuestionHelper title="Hints" helperTemplate={HelperStrTemplate} defaultValue=""
        list={hints} updateList={updateHints} setList={(l) => setHints(l)} />
      {/* <QuestionHelper title="Test Cases" helperTemplate={HelperTestCaseTemplate} defaultValue={{ parameters: [], explanation: "" }}
        list={testCases} updateList={updateTestCases} setList={(l) => setTestCases(l)} /> */}
      <button onClick={handleSubmit} className="my-3 text-base">
        <FontAwesomeIcon icon={props.create ? faPlus : faRotate} className="mr-2" />
        {props.create ? "Create" : "Update"}
      </button>
    </div>
  )
}
