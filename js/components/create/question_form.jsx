import { useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { faPlus, faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getReqHeader, formatQueries } from "../../utils/utils";
import { StatusDropdown, DifficultyDropdown, SourceDropdown, TagsDropdown } from "../common/drop_down.jsx";

export default function QuestionForm(props) {
  const [source, setSource] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [status, setStatus] = useState("");
  const [tags, setTags] = useState([]);
  const [title, setTitle] = useState("");
  const [prompt, setPrompt] = useState("");
  const [notes, setNotes] = useState([]);
  const [metadata, setMetadata] = useState({});

  useEffect(async () => {
    const req = {
      method: "GET",
      header: getReqHeader()
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
        console.log("hi")
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
    const updated = formatHelperList(notes, val, idx, remove);
    setNotes(updated);
  };

  const formatHelperList = (lst, val, idx, remove) => {
    const updated = lst.slice(0, idx);
    if (!remove) updated.push(val);
    updated.push(...lst.slice(idx + 1));
    return updated;
  }

  const handleSubmit = (e) => {
    e.prevenDefault();
  };

  return (
    <div className="flex flex-col justify-start items-start gap-4 text-[18px]">
      <div className="form-section">
        <label className="section-title">Title</label>
        <InputText placeholder="" value={title} onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded-xs" />
      </div>
      <div className="flex flex-col justiify-start items-start">
        <label className="section-title">Category</label>
        <div className="flex justify-start items-center gap-4 flex-wrap grow w-full">
          <TagsDropdown tags={metadata.tags || []} updateValue={(t) => setTags(t)} />
          <SourceDropdown sources={metadata.sources || []} updateValue={(s) => setSource(s)} className="p-0" />
          <DifficultyDropdown difficulties={metadata.difficulties || []} updateValue={(d) => setDifficulty(d)} />
          <StatusDropdown statuses={metadata.statuses || []} updateValue={(s) => setStatus(s)} />
        </div>
      </div>
      <div className="form-section">
        <label className="section-title">Prompt</label>
        <InputTextarea placeholder="" value={prompt} autoResize onChange={(e) => setPrompt(e.target.value)}
          className="border-1 rounded-xs border-gray-300 w-full" />
      </div>
      <div className="form-section">
        <details open className="w-full">
          <summary className="section-title cursor-pointer">
            <label className="ml-1">Notes</label>
          </summary>
          <button onClick={() => setNotes([...notes, ""])}
            className="text-[14px] p-0 w-4 h-4 my-2 flex justify-center items-center">+</button>
          <div className="flex flex-col gap-2">
            {notes.map((n, i) => {
              return (<div className="flex justify-between items-center gap-2">
                  <FontAwesomeIcon icon={faX} size="xs" className="cursor-pointer" style={{ color: "#a0a0a0" }}
                    onClick={() => updateNotes("", i, true)} />
                  <InputText value={n} onChange={(e) => updateNotes(e.target.value, i)}
                    className="border-0 border-b-1 rounded-[0%] text-[14px] w-full focus:outline-none flex-1" />
                </div>);
            })}
          </div>
        </details>
      </div>
      <button onClick={handleSubmit}>
        {props.create
          ? <FontAwesomeIcon icon={faPlus} className="mr-2" />
          : <FontAwesomeIcon icon={faPlus} className="mr-2" />}
        {props.create ? "Create" : "Update"}
      </button>
    </div>
  )
}
