import ReactMarkdown from "react-markdown";
import { faRotate, faTrash, faPen, faLightbulb, faHashtag } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getStatusIcon, getDifficultyStyle } from "../../utils/assets";
import { formatDate, capitalizeFirst } from "../../utils/utils";

export function QuestionTab({ data }) {
  return (
    <div className="flex flex-col justify-between items-start w-full overflow-y-auto">
      <div className="flex justify-start items-center gap-4 mb-2">
        {getStatusIcon(data.status, 0, false)}
        <h1 className="text-xl text-wrap">{data.title}</h1>
      </div>
      <div className="flex justify-start items-center gap-2 text-xs mb-8">
        <div className="chip" style={getDifficultyStyle(data.difficulty)}>{capitalizeFirst(data.difficulty)}</div>
        <div className="chip">{capitalizeFirst(data.source)}</div>
        <div className="chip text-nowrap">{formatDate(data.created_at)}</div>
        <button className="chip p-1 hover:bg-gray-300 text-black"><FontAwesomeIcon icon={faRotate} /></button>
        <button className="chip p-1 hover:bg-gray-300 text-black"><FontAwesomeIcon icon={faTrash} /></button>
      </div>
      <div className="prompt-container text-xs mb-32">
        <ReactMarkdown children={data.prompt} />
      </div>
      <div>
        <AccordianItem title={"Tags"} icon={faHashtag} content={
          <div className="flex justify-start items-center gap-1 flex-wrap">
            {data.tags.map((tag, i) => {
              return (<div key={tag + i}
                  className="chip w-fit text-md">{`# ${tag}`}
                </div>);
            })}
          </div>}
        />
        {data.notes.map((note, i) => {
          return (
            <AccordianItem title={"Note " + (i + 1)} icon={faPen}
              content={<p className="text-xs font-light">{note}</p>} />
          );
        })}
        {data.hints.map((hint, i) => {
          return (
            <AccordianItem title={"Hint " + (i + 1)} icon={faLightbulb}
              content={<p className="text-xs font-light">{hint}</p>} />
          );
        })}
      </div>
    </div>
  );
}

function AccordianItem(props) {
  return (
    <details className="w-full mb-3">
      <summary className="cursor-pointer w-full mb-1 first-letter:text-primary">
        <label className="ml-1 mr-2 text-xs">{props.title}</label>
        <FontAwesomeIcon icon={props.icon} size="xs" />
      </summary>
      {props.content}
    </details>
  );
}