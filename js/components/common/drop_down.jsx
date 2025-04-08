import { useState, useEffect } from "react";
import { Dropdown } from "primereact/dropdown";
import { MultiSelect } from 'primereact/multiselect';
import { capitalizeFirst } from "../../utils/utils";
import { getDifficultyStyle, getStatusIcon } from "../../utils/assets";

const CLEAR = "clear";


const valueTemplate = (option, props) => {
  return (<div className="mr-1">
      {capitalizeFirst(!option || option === CLEAR ? props.placeholder : option)}
    </div>
  );
};


export function SourceDropdown(props) {
  const [source, setSource] = useState("");

  const sourceTemplate = (option) => {
    return <div className="drop-down-item"><span className="px-2">{capitalizeFirst(option)}</span></div>
  };

  const handleChange = (e) => {
    const val = e.value === CLEAR ? "" : e.value;
    setSource(val);
    props.updateValue(val);
  };

  return (
    <Dropdown placeholder="Source" options={props.sources.concat(CLEAR)} value={source} optionLabel="source"
      valueTemplate={valueTemplate} itemTemplate={sourceTemplate}
      className={`drop-down ${props.className}`} panelClassName="drop-down-panel"
      onChange={handleChange} />
  );
}


export function DifficultyDropdown(props) {
  const [difficulty, setDifficulty] = useState("");

  const difficultyTemplate = (option) => {
    return (
      <div className="drop-down-item" style={getDifficultyStyle(option)}><span className="px-2">
        {capitalizeFirst(option)}
      </span></div>
    );
  };

  const handleChange = (e) => {
    const val = e.value === CLEAR ? "" : e.value;
    setDifficulty(val);
    props.updateValue(val);
  };

  return (
    <Dropdown placeholder="Difficulty" options={props.difficulties.concat(CLEAR)} value={difficulty} optionLabel="difficulty"
      valueTemplate={valueTemplate} itemTemplate={difficultyTemplate}
      className={`drop-down ${props.className}`} panelClassName="drop-down-panel"
      onChange={handleChange} />
  );
}


export function StatusDropdown(props) {
  const [status, setStatus] = useState("");

  const statusTemplate = (option) => {
    return (
      <div className="drop-down-item"><span className="px-2 flex justify-start items-center gap-2 text-xs">
        {getStatusIcon(option, option, false)}
        {capitalizeFirst(option)}
      </span></div>
    );
  };

  const handleChange = (e) => {
    const val = e.value === CLEAR ? "" : e.value;
    setStatus(val);
    props.updateValue(val);
  };

  return (
    <Dropdown placeholder="Status" options={props.statuses.concat(CLEAR)} value={status} optionLabel="status"
      valueTemplate={valueTemplate} itemTemplate={statusTemplate}
      className={`drop-down ${props.className}`} panelClassName="drop-down-panel"
      onChange={handleChange} />
  );
}


export function TagsDropdown(props) {
  const [tags, setTags] = useState([]);
  const [tagOpts, setTagOpts] = useState([]);  // formatted for Multiselect

  useEffect(() => {
    const formattedTags = props.tags.map((tag) => ({
      label: tag,
      value: tag
    }));
    setTagOpts(formattedTags);
  }, [props.tags]);

  const tagsTemplate = (option) => {
    return (
      <div className="w-full"><span className="ml-2">
        {capitalizeFirst(option.label)}
      </span></div>
    );
  };

  const tagsFooterTemplate = () => {
    const length = tags ? tags.length : 0;

    return (
        <div className="py-2 px-3 text-[10px] bg-gray-100">
            <b>{length}</b> item{length > 1 ? 's' : ''} selected.
        </div>
    );
  };

  const handleChange = (e) => {
    const val = e.value;
    setTags(val);
    props.updateValue(val);
  };

  return (
    <MultiSelect placeholder="Tags" options={tagOpts} value={tags} optionLabel="label" display="chip"
      onChange={handleChange} filter
      itemTemplate={tagsTemplate} panelFooterTemplate={tagsFooterTemplate}
      className={`drop-down max-w-[12rem] ${props.className}`} panelClassName="drop-down-panel" />
  );
}


