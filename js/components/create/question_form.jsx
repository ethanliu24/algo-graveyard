import { useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { faPlus } from "@fortawesome/free-solid-svg-icons";
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

  const handleSubmit = (e) => {
    e.prevenDefault();
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col justify-start items-start gap-4 text-[18px]">
      <div className="w-full">
        <h1 className="section-title">Title</h1>
        <InputText placeholder="" value={title} onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded-xs" />
      </div>
      <div className="flex flex-col justiify-start items-start">
        <h2 className="section-title">Category</h2>
        <div className="flex justify-start items-center gap-4">
          <SourceDropdown sources={metadata.sources || []} updateValue={(s) => setSource(s)} className="p-0" />
          <DifficultyDropdown difficulties={metadata.difficulties || []} updateValue={(d) => setDifficulty(d)} />
          <StatusDropdown statuses={metadata.statuses || []} updateValue={(s) => setStatus(s)} />
          <TagsDropdown tags={metadata.tags || []} updateValue={(t) => setTags(t)} />
        </div>
      </div>
      <div className="w-full">
        <h3 className="section-title">Prompt</h3>
        <InputTextarea placeholder="" value={prompt} autoResize onChange={(e) => setPrompt(e.target.value)}
          className="border-1 rounded-xs border-gray-300 w-full" />
      </div>
      <button>
        {props.create
          ? <FontAwesomeIcon icon={faPlus} className="mr-2" />
          : <FontAwesomeIcon icon={faPlus} className="mr-2" />}
        {props.create ? "Create" : "Update"}
      </button>
    </form>
  )
}
