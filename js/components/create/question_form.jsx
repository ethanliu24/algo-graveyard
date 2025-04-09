import { useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getReqHeader, formatQueries } from "../../utils/utils";
import { StatusDropdown, DifficultyDropdown, SourceDropdown, TagsDropdown } from "../common/drop_down.jsx";
import QuestionHelper, { HelperStrTemplate, HelperTestCaseTemplate } from "./question_helper.jsx";
import Verify from "../auth/verify.jsx";

export default function QuestionForm(props) {
  const [link, setLink] = useState("");
  const [source, setSource] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [status, setStatus] = useState("");
  const [tags, setTags] = useState([]);
  const [title, setTitle] = useState("");
  const [prompt, setPrompt] = useState("");
  const [notes, setNotes] = useState([]);
  const [hints, setHints] = useState([]);
  const [testCases, setTestCases] = useState([]);
  const [metadata, setMetadata] = useState({});
  const [showVerify, setShowVerify] = useState(false);

  useEffect(async () => {
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

    fetch(`api/metadata?${formatQueries(metadataQuery)}`, req)
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
  }, []);

  const updateNotes = (val, idx, remove) => {
    const updated = updateHelper(notes, val, idx, remove);
    setNotes(updated);
  };

  const updateHints = (val, idx, remove) => {
    const updated = updateHelper(hints, val, idx, remove);
    setHints(updated);
  };

  const updateTestCases = (val, idx, remove) => {
    const updated = updateHelper(testCases, val, idx, remove);
    setTestCases(updated);
  }

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
      test_cases: testCases,
      notes: notes,
      hints: hints,
      tags: tags
    };

    if (isFormValid(data)) {
      props.create ? createQuestion(data) : updateQuestion(data);
    }
  };

  const isFormValid = (data) => {
    // TODO show toast here
    if (data.link !== "") {
      alert("handle source is valid");
      return data.source !== "";
    }

    if (!data.difficulty || !data.status || !data.source ||
        data.title.length === 0 || data.title.length > 50 ||
        data.prompt.length === 0) {
      alert("invalid data");
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

    fetch("api/questions", req)
      .then(response => {
        if (response.ok) {
          alert("redirect not implemented");
        } else if (response.status == 401) {
          alert("Show unauthed Toast");
          setShowVerify(true);
        } else {
          alert("Error handling");
          return response;
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const updateQuestion = (data) => {
    alert("Not Implemented yet");
  };

  return (
    <div className="flex flex-col justify-start items-start gap-4 text-[14px]">
      {showVerify
        ? <Verify closable={true} closeComponent={() => setShowVerify(false)}
            positionStyle="fixed top-0 right-0 m-8" className="text-base" />
        : null}
      <div className="form-section">
        <label className="section-title">Link</label>
        <div className="flex justify-between items-center gap-4 w-full">
          <InputText placeholder="" value={link} onChange={(e) => setLink(e.target.value)}
            className="flex-1 rounded-xs py-1" />
          <SourceDropdown sources={metadata.sources || []} updateValue={(s) => setSource(s)} className="py-1" />
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Title</label>
        <InputText placeholder="" value={title} onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded-xs py-1" />
      </div>
      <div className="flex flex-col justify-start items-start">
        <label className="section-title">Category</label>
        <div className="flex justify-start items-center gap-4 gap-y-1 flex-wrap grow w-full">
          <TagsDropdown tags={metadata.tags || []} updateValue={(t) => setTags(t)} />
          <DifficultyDropdown difficulties={metadata.difficulties || []} updateValue={(d) => setDifficulty(d)} />
          <StatusDropdown statuses={metadata.statuses || []} updateValue={(s) => setStatus(s)} />
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
      <QuestionHelper title="Test Cases" helperTemplate={HelperTestCaseTemplate} defaultValue={{ parameters: [], explanation: "" }}
        list={testCases} updateList={updateTestCases} setList={(l) => setTestCases(l)} />
      <button onClick={handleSubmit} className="my-3 text-base">
        <FontAwesomeIcon icon={faPlus} className="mr-2" />
        {props.create ? "Create" : "Update"}
      </button>
    </div>
  )
}
