import { InputText } from "primereact/inputtext";
import { InputTextarea } from 'primereact/inputtextarea';
import { faX, faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function QuestionHelper(props) {
  const HelperTemplate = props.helperTemplate;

  return (
    <div className="form-section">
      <details className="w-full">
        <summary className="section-title cursor-pointer">
          <label className="ml-1">{props.title}</label>
        </summary>
        <button onClick={() => props.setList([...props.list, props.defaultValue])}
          className="text-[14px] p-0 w-4 h-4 my-2 flex justify-center items-center">+</button>
        <div className="flex flex-col gap-2">
          {props.list.map((c, i) => {
            return <HelperTemplate content={c} idx={i} updateList={props.updateList} />
          })}
        </div>
      </details>
    </div>
  );
}

export function HelperStrTemplate(props) {
  return (
    <div className="flex justify-between items-center gap-2">
      <FontAwesomeIcon icon={faX} className="cursor-pointer" style={{ color: "#a0a0a0" }}
        onClick={() => props.updateList(null, props.idx, true)} />
      <InputText value={props.content} onChange={(e) => props.updateList(e.target.value, props.idx, false)}
        className="border-0 border-b-1 rounded-[0%] text-[14px] w-full focus:outline-none flex-1 p-1" />
    </div>
  );
}

export function HelperTestCaseTemplate(props) {
  const handleChange = (params, ex) => {
    props.updateList({ parameters: params, explanation: ex }, props.idx, false);
  };

  const handleParamChange = (e, field, idx) => {
    let newParams = [...props.content.parameters];
    newParams[idx][field] = e.target.value;
    handleChange(newParams, props.content.explanation);
  }

  return (
    <div className="flex flex-col justify-start items-center gap-2 w-full mt-4">
      <div className="flex flex-col justify-start items-start gap-2 w-full">
        {props.content.parameters.map(({ parameter, value }, i) => {
          return (<div className="flex justify-start items-center gap-2 w-full">
            <FontAwesomeIcon icon={faMinus} className="cursor-pointer" style={{ color: "#a0a0a0" }}
              onClick={() => {
                let newParams = [...props.content.parameters]
                newParams.splice(i, 1)
                handleChange(newParams, props.content.explanation);
              }} />
            <div className="flex gap-2 flex-wrap grow w-full">
              <InputText placeholder="Parameter" value={parameter} className="py-0.5 grow max-w-[10rem]"
                onChange={(e) => handleParamChange(e, "parameter", i)} />
              <InputText placeholder="Value" value={value} className="py-0.5 flex-1 grow"
                onChange={(e) => handleParamChange(e, "value", i)} />
            </div>
          </div>);
        })}
        <FontAwesomeIcon icon={faPlus} className="cursor-pointer" style={{ color: "#a0a0a0" }}
          onClick={() => handleChange([...props.content.parameters, { parameter: "", value: null }], props.content.explanation)} />
      </div>
      <div className="flex gap-2 items-center w-full">
        <FontAwesomeIcon icon={faX} className="cursor-pointer" style={{ color: "#a0a0a0" }}
          onClick={() => props.updateList(null, props.idx, true)} />
        <InputTextarea placeholder="Explanation of test case" value={props.content.explanation} autoResize
          onChange={(e) => handleChange(props.content.parameters, e.target.value)}
          className="border-gray-300 w-full flex-1" />
      </div>
    </div>
  );
}