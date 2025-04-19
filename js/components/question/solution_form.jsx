import { useState, useEffect } from "react";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { Dropdown } from "../common/drop_down.jsx";
import { formatQueries, getReqHeader } from "../../utils/utils.js";

export default function SolutionForm(props) {
  const [summary, setSummary] = useState(props.summary || "");
  const [explanation, setExplanation] = useState(props.explanation || "");
  const [language, setLanguage] = useState(props.language || "");
  const [timeComplexity, setTimeComplexity] = useState(props.timeComplexity || "");
  const [spaceComplexity, setSpaceComplexity] = useState(props.spaceComplexity || "");
  const [code, setCode] = useState(props.code || "");
  const [accepted, setAccepted] = useState(props.accepted || true);
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
          <Dropdown title="Language" value={"Accepted"} options={["Accepted", "Denied"]} updateValue={(a) => setAccepted(a === "Y")} />
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
        {/* <InputTextarea placeholder="" value={code} autoResize onChange={(e) => setCode(e.target.value)}
          className="border-1 rounded-xs border-gray-300 w-full min-h-[20rem]" /> */}
      </div>
    </div>
  );
}