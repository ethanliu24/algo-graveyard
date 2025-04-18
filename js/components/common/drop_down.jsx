import { useState, useEffect } from "react";
import { faChevronDown, faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { capitalizeFirst } from "../../utils/utils";


export function Dropdown(props) {
  const handleChange = (e) => {
    const val = e.target.value === "clear" ? "" : e.target.value;
    props.updateValue(val);
  };

  return (
    <select value={props.value ? props.value : ""} onChange={handleChange}
      className="drop-down cursor-pointer">
      {!props.value ? <option value="" disabled>{props.title}</option> : null}
      {props.options.map((option, index) => {
        return <option key={index} value={option}>{capitalizeFirst(option)}</option>
      })}
      <option value="clear">Clear</option>
    </select>
  );
}


export function MultiSelect(props) {
  const [selected, setSelected] = useState([]);
  const [itemStates, setItemStates] = useState([]);  // 1 means selected, 0 means not
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setItemStates(Array(props.options.length).fill(0));
  }, [props.options])

  const handleItemClick = (e, value, idx) => {
    e.stopPropagation();
    let selectStates = [...itemStates];
    let newSelected = [...selected];

    if (selectStates[idx] === 1) {  // Selcted to not selected
      const itemIdx = newSelected.indexOf(value);
      if (itemIdx > -1) newSelected.splice(itemIdx, 1);
      selectStates[idx] = 0;
    } else {  // not selected to selected
      newSelected.push(value)
      selectStates[idx] = 1;
    }

    updateSelection(newSelected, selectStates)
  }

  const removeSelected = (val) => {
    let selectStates = [...itemStates];
    let newSelected = [...selected];
    const itemIdx = newSelected.indexOf(val);
    if (itemIdx > -1) newSelected.splice(itemIdx, 1);
    selectStates[itemIdx] = 0;

    updateSelection(newSelected, selectStates)
  }

  const updateSelection = (newSelected, newStates) => {
    setItemStates(newStates);
    setSelected(() => {
      props.updateValue(newSelected);
      return newSelected;
    });
  }

  return (
    <div className="flex justify-between items-center gap-4 relative drop-down max-w-[12rem] cursor-pointer select-none"
      onClick={() => setOpen(!open)}>
        <div className="flex justify-start items-center gap-1 overflow-x-auto">
          {selected.length === 0
            ? props.title
            : selected.map(val => {
              return (
                <div className="chip text-nowrap text-primary bg-primary/20 text-xs">
                  {val}
                  <div className="flex justify-center items-center rounded-full border-1 w-[0.8rem] h-[0.8rem] border-primary"
                    onClick={() => removeSelected(val)}>
                    <FontAwesomeIcon icon={faX} size="2xs" className="text-primary"
                       />
                  </div>
                </div>
              );
            })}
        </div>
      <div className={`absolute top-full left-0 flex flex-col justify-start items-stretch z-100
        bg-white shadow-md rounded text-sm max-h-50 overflow-x-auto ${open ? "" : "hidden"}`}>{
          props.options.map((val, i) => {
            return (
              <div className={`text-nowrap py-2 px-4 hover:bg-gray-200
                ${itemStates[i] === 1 ? "text-primary" : "" }`}
                onClick={(e) => handleItemClick(e, val, i)}>
                {val}
              </div>
            );
          })
        }</div>
      <FontAwesomeIcon icon={faChevronDown} size="2xs" />
    </div>
  );
}

