import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faHourglassEnd, faClock, faMinus } from "@fortawesome/free-solid-svg-icons";
import { Tooltip } from "react-tooltip";
import { capitalizeFirst } from "../../utils/utils.js";

export default function QuestionList(props) {
  return (
    <div className="mt-4 text-sm w-[100%] flex flex-col justify-start items-center">
      {props.questions.map((q, i) => {
        return (<ListItem key={"q" + i}
          idx={i + 1} title={q.title} status={q.status} source={q.source}
          difficulty={q.difficulty} timestamp={q.last_modified} tags={q.tags}
        />);
      })}
    </div>
  );
}

function ListItem(props) {
  const getStatusIcon = (status, idx) => {
    const statusIcon = {
      "completed": <FontAwesomeIcon icon={faCheck} color="#6bd177" />,
      "unoptimized": <FontAwesomeIcon icon={faClock} color="#3b82f7" />,
      "attempted": <FontAwesomeIcon icon={faHourglassEnd} color="#f5cd3d" />
    };

    const tooltip = statusIcon[status] ? status : "unknown";
    const tooltipId = `${tooltip}-${idx}`;

    return (
      <div data-tooltip-id={tooltipId} data-tooltip-content={capitalizeFirst(tooltip)} data-tooltip-place="left">
        {statusIcon[status] || <FontAwesomeIcon icon={faMinus} color="#c7c7c7" />}
        <Tooltip id={tooltipId} />
      </div>);
  };

  const formatDate = (dateStr) => {
    const options = { month: 'short', day: 'numeric', year: 'numeric' };
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', options);
  };

  const getDifficultyStyle = (difficulty) => {
    const colorMap = {
      "easy": "#6bd177",
      "medium": "#f5cd3d",
      "hard": "#eb4b63"
    };

    return {
      color: colorMap[difficulty] || "#c7c7c7"
    };
  };

  return (
    <div className="flex justify-between items-center gap-4 text-center w-[100%]
      bg-transparent px-4 py-3 cursor-pointer rounded hover:bg-gray-200">
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
              className="bg-gray-300 px-1 rounded-3xl">{`#${tag}`}
            </div>);
        })}
      </div>
    </div>
  );
}
