import { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import { faPlus, faRotate } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import Verify from "../auth/verify.jsx";
import { Dropdown } from "../common/drop_down.jsx";
import { formatQueries, getReqHeader, getLanguageHighlighter } from "../../utils/utils.js";

export default function SolutionForm(props) {
  const [summary, setSummary] = useState(props.data.summary || "");
  const [explanation, setExplanation] = useState(props.data.explanation || "");
  const [language, setLanguage] = useState(props.data.language || "");
  const [timeComplexity, setTimeComplexity] = useState(props.data.timeComplexity || "");
  const [spaceComplexity, setSpaceComplexity] = useState(props.data.spaceComplexity || "");
  const [code, setCode] = useState(props.data.code || "");
  const [accepted, setAccepted] = useState(props.data.accepted || true);
  const [languages, setLanguages] = useState([]);
  const [showVerify, setShowVerify] = useState(false);

  useEffect(() => {
    const req = {
      method: "GET",
      headers: getReqHeader()
    };

    fetch(`/api/metadata?${formatQueries({ languages: true })}`, req)
      .then(res => res.json())
      .then(data => {
        setLanguages(data.languages);
      })
      .catch(err => {
        throw err;
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      summary: summary,
      explanation: explanation,
      language: language,
      time_complexity: timeComplexity,
      space_complexity: spaceComplexity,
      code: code,
      accepted: accepted
    };

    if (isFormValid(data)) {
      props.create ? createSolution(data) : updateSolution(data);
    }
  };

  const isFormValid = (data) => {
    if (!data.language || !data.summary || data.summary.length >= 50) {
      alert("invalid data");
      return false;
    }

    return true;
  };

  const createSolution = (data) => {
    const req = {
      method: "POST",
      headers: getReqHeader(),
      body: JSON.stringify(data)
    };

    fetch(`/api/questions/${props.questionId}/solutions`, req)
      .then(response => {
        if (!response.ok) {
          if (response.status == 401) {
            alert("Show unauthed Toast");
            setShowVerify(true);
          } else {
            alert("Error handling");
          }
        }

        return response;
      })
      .then(res => res.json())
      .then(json => {
        if (!json.id) {  // This means creation was successful
          alert("print errors in toast");
        } else {
          props.methodSuccessful(json);
        }
      })
      .catch(err => {
        throw err;
      });
  };

  const updateSolution = (data) => {
    const req = {
      method: "PUT",
      headers: getReqHeader(),
      body: JSON.stringify(data)
    };

    fetch(`/api/questions/${props.questionId}/solutions/${props.data.id}`, req)
      .then(response => {
        if (response.ok) {
          alert("show successful toast");
          return response;
        } else {
          if (response.status == 401) {
            alert("show unauthed toast");
            setShowVerify(true);
          } else {
            alert(response.status);
          }

          return null;
        }
      })
      .then(res => res ? res.json() : null)
      .then(json => {
        if (json) props.methodSuccessful(json);
      })
      .catch(err => {
        throw err;
      })
  };

  return (
    <div className="flex flex-col justify-start items-start gap-4 w-full text-[14px]">
      {showVerify
        ? <Verify closable={true} closeComponent={() => setShowVerify(false)}
            positionStyle="fixed top-0 right-0 m-8" className="text-base" />
        : null}
      <div className="form-section">
        <label className="section-title">Summary</label>
        <InputText placeholder="" value={summary} onChange={(e) => setSummary(e.target.value)}
          className="rounded-xs py-1 w-full" />
      </div>
      <div className="form-section">
        <label className="section-title">Information</label>
        <div className="space-x-4">
          <Dropdown title="Language" value={accepted ? "Accepted" : "Denied"} options={["Accepted", "Denied"]} updateValue={(a) => setAccepted(a === "Accepted")} />
          <Dropdown title="Language" value={language} options={languages} updateValue={(l) => setLanguage(l)} />
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Complexity</label>
        <div className="space-y-2">
          <span className="flex justify-start items-stretch">Time: O&#40;
            <InputTextarea value={timeComplexity} autoResize onChange={(e) => setTimeComplexity(e.target.value)}
              className="py-0 px-1 w-20 min-w-8 h-4 max-h-4 overflow-x-auto" />
          &#41;</span>
          <span className="flex justify-start items-stretch">Space: O&#40;
            <InputTextarea value={spaceComplexity} autoResize onChange={(e) => setSpaceComplexity(e.target.value)}
              className="py-0 px-1 w-20 min-w-8 h-4 max-h-4 overflow-x-auto" />
          &#41;</span>
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Explanation</label>
        <InputTextarea placeholder="" value={explanation} autoResize onChange={(e) => setExplanation(e.target.value)}
          className="border-1 rounded-xs border-gray-300 w-full min-h-[10rem]" />
      </div>
      <div className="form-section">
        <label className="section-title">Implementation</label>
        <Editor height="400px" language={getLanguageHighlighter(language) || "plaintext"}
          onChange={(c) => setCode(c)} value={code} options={{ wordWrap: "on" }} theme="vs-dark" />
      </div>
      <button onClick={handleSubmit} className="my-3 text-base">
        <FontAwesomeIcon icon={props.create ? faPlus : faRotate} className="mr-2" />
        {props.create ? "Create" : "Update"}
      </button>
    </div>
  );
}