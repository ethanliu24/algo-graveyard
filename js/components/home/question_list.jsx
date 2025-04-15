import { getStatusIcon, getDifficultyStyle } from "../../utils/assets.jsx";
import { capitalizeFirst, formatDate } from "../../utils/utils.js";

export default function QuestionList(props) {
  return (
    <div className="text-sm w-[100%] mb-12 flex flex-col justify-start items-center">
      {props.questions.map((q, i) => {
        return (<ListItem key={"q" + i}
          idx={i + 1} id={q.id} title={q.title} status={q.status} source={q.source}
          difficulty={q.difficulty} timestamp={q.last_modified} tags={q.tags}
        />);
      })}
    </div>
  );
}

function ListItem(props) {
  return (
    <div className="flex justify-between items-center gap-4 text-center w-[100%]
      bg-transparent px-4 py-3 cursor-pointer rounded hover:bg-gray-200"
      onClick={() => window.location.href = `/questions/${props.id}`}>
      <div className="text-[12px] text-gray-500">{props.idx}</div>
      {getStatusIcon(props.status, props.idx)}
      <div className="flex-8 flex flex-col justify-between items-start">
        <div className="text-sm">{capitalizeFirst(props.title)}</div>
        <div className="flex justify-start items-center gap-2 text-[12px] text-gray-500">
          <div>{formatDate(props.timestamp)}</div>
          <div className="-mx-1">·</div>
          <div>{capitalizeFirst(props.source)}</div>
          <div className="-mx-1">·</div>
          <div style={getDifficultyStyle(props.difficulty)}>{capitalizeFirst(props.difficulty)}</div>
        </div>
      </div>
      <div className="flex justify-end items-center gap-2 w-48 overflow-x-scroll text-xs max-md:hidden">
        {props.tags.map((tag, i) => {
          return (<div key={tag + props.idx + i}
              className="chip text-md">{`# ${tag}`}
            </div>);
        })}
      </div>
    </div>
  );
}
