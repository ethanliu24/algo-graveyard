import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faHourglassEnd, faClock, faMinus } from "@fortawesome/free-solid-svg-icons";
import { Tooltip } from "react-tooltip";
import { getReqHeader } from "../../utils/api.js";

export default function QuestionList() {
  const [questions, setQuestions] = useState([]);

  useEffect(async () => {
    const req = {
      method: "GET",
      header: getReqHeader(),
    }

    const data = await getQuestions(req);
    setQuestions(data.data.data);  // lol
  }, []);

  const getQuestions = async (req, queries) => {
    return await fetch(`/api/questions?${queries}`, req)
      .then(res => res.json())
      .catch(err => {
        throw err;
      })
  };

  return (
    <div>
      <div className="text-sm w-[100%]">
        {questions.map((q, i) => {
          return (<ListItem key={"q" + i}
            idx={i + 1} title={q.title} status={q.status} source={q.source}
            difficulty={q.difficulty} createdAt={q.created_at} tags={q.tags}
          />)
        })
      }</div>
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
      <div data-tooltip-id={tooltipId} data-tooltip-content={tooltip} data-tooltip-place="left">
        {statusIcon[status] || <FontAwesomeIcon icon={faMinus} color="#c7c7c7" />}
        <Tooltip id={tooltipId} />
      </div>);
  };

  return (
    <div className="flex justify-between items-center gap-4 text-center mt-4
      bg-transparent px-4 py-2 cursor-pointer rounded hover:bg-gray-200">
      <div className="text-[12px] text-gray-500">{props.idx}</div>
      {getStatusIcon(props.status, props.idx)}
      <div className="flex-8 flex flex-col justify-between items-start">
        <div className="text-sm">{props.title}</div>
        <div className="flex justify-start items-center gap-2 text-[12px] text-gray-500">
          <div className="">{props.createdAt}</div>
          <div className="">{props.source}</div>
          <div className="">{props.difficulty}</div>
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

// idstring
// sourceExpand allstring
// difficultyExpand allstring
// statusExpand allstring
// titlestring
// tagsExpand allarray<string>
// created_atstringdate-time
// last_modifiedstringdate-time