import { faX } from "@fortawesome/free-solid-svg-icons";

export default function QuestionHelper(props) {
  const HelperTemplate = props.helperTemplate;

  return (
    <div className="form-section">
      <details className="w-full">
        <summary className="section-title cursor-pointer">
          <label className="ml-1">{props.title}</label>
        </summary>
        <button onClick={() => props.setList([...props.list, ""])}
          className="text-[14px] p-0 w-4 h-4 my-2 flex justify-center items-center">+</button>
        <div className="flex flex-col gap-2">
          {props.list.map((item, i) => {
            return <HelperContent item={item} idx={i} />
          })}
        </div>
      </details>
    </div>
  );
}

export function HelperStrTemplate(props) {
  return (<div className="flex justify-between items-center gap-2">
    <FontAwesomeIcon icon={faX} size="xs" className="cursor-pointer" style={{ color: "#a0a0a0" }}
      onClick={() => props.updateList("", props.idx, true)} />
    <InputText value={props.item} onChange={(e) => props.updateList(e.target.value, props.idx, false)}
      className="border-0 border-b-1 rounded-[0%] text-[14px] w-full focus:outline-none flex-1 p-1" />
  </div>);
}