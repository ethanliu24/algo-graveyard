import { useEffect, useState, useRef } from "react";
import { Dropdown } from "primereact/dropdown";
import { MultiSelect } from 'primereact/multiselect';
import { capitalizeFirst } from "../../utils/utils";
import { getDifficultyStyle, getStatusIcon } from "../../utils/assets";

export default function FilterBar(props) {
  const [source, setSource] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [status, setStatus] = useState("");
  const [tags, setTags] = useState([]);
  const [tagOpts, setTagOpts] = useState([]);  // formatted for Multiselect

  useEffect(() => {
    const formattedTags = props.tags.map((tag) => ({
      label: tag,
      value: tag
    }));
    setTagOpts(formattedTags);
  }, [props.tags]);

  const CLEAR = "clear"

  const valueTemplate = (option, props) => {
    return (<div className="">{
        capitalizeFirst(!option || option === CLEAR ? props.placeholder : option)
      }</div>
    );
  };

  const sourceTemplate = (option) => {
    return <div className="drop-down-item"><span className="px-2">{capitalizeFirst(option)}</span></div>
  };

  const difficultyTemplate = (option) => {
    return (
      <div className="drop-down-item" style={getDifficultyStyle(option)}><span className="px-2">
        {capitalizeFirst(option)}
      </span></div>
    );
  };

  const statusTemplate = (option) => {
    return (
      <div className="drop-down-item"><span className="px-2 flex justify-start items-center gap-2 text-xs">
        {getStatusIcon(option, option, false)}
        {capitalizeFirst(option)}
      </span></div>
    );
  };

  const tagsTemplate = (option) => {
    return (
      <div className="w-full"><span className="ml-2">
        {capitalizeFirst(option.label)}
      </span></div>
    );
  }

  const tagsFooterTemplate = () => {
    const length = tags ? tags.length : 0;

    return (
        <div className="py-2 px-3 text-[10px] bg-gray-100">
            <b>{length}</b> item{length > 1 ? 's' : ''} selected.
        </div>
    );
  };

  return (
    <div className="flex flex-row justify-center items-center gap-4 flex-wrap gap-y-2 w-[100%] text-md">
      <Dropdown placeholder="Source" options={props.sources.concat(CLEAR)} value={source} optionLabel="source"
        valueTemplate={valueTemplate} itemTemplate={sourceTemplate}
        className="drop-down" panelClassName="drop-down-panel"
        onChange={(e) => setSource(e.value === CLEAR ? "" : e.value)} />
      <Dropdown placeholder="Difficulty" options={props.difficulties.concat(CLEAR)} value={difficulty} optionLabel="difficulty"
        valueTemplate={valueTemplate} itemTemplate={difficultyTemplate}
        className="drop-down" panelClassName="drop-down-panel"
        onChange={(e) => setDifficulty(e.value === CLEAR ? "" : e.value)} />
      <Dropdown placeholder="Status" options={props.statuses.concat(CLEAR)} value={status} optionLabel="status"
        valueTemplate={valueTemplate} itemTemplate={statusTemplate}
        className="drop-down" panelClassName="drop-down-panel"
        onChange={(e) => setStatus(e.value === CLEAR ? "" : e.value)} />
      <MultiSelect placeholder="Tags" options={tagOpts} value={tags} optionLabel="label" display="chip"
        onChange={(e) => setTags(e.value)} filter
        itemTemplate={tagsTemplate} panelFooterTemplate={tagsFooterTemplate}
        className="drop-down" panelClassName="drop-down-panel" />
    </div>
  );
}