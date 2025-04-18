import { useState, useEffect } from "react";
import { MultiSelect } from 'primereact/multiselect';
import { capitalizeFirst } from "../../utils/utils";


export function Dropdown(props) {
  const handleChange = (e) => {
    const val = e.target.value === "clear" ? "" : e.target.value;
    props.updateValue(val);
  };

  return (
    <select value={props.value ? props.value : ""} onChange={handleChange}
      className={`drop-down ${props.className}`}
    >
      {!props.value ? <option value="" disabled>{props.title}</option> : null}
      {props.options.map((option, index) => {
        return <option key={index} value={option}>{capitalizeFirst(option)}</option>
      })}
      <option value="clear">Clear</option>
    </select>
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


