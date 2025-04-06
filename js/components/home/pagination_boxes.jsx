import { useEffect, useState } from "react";
import { faAnglesLeft, faAngleLeft, faAngleRight, faAnglesRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function PaginationBoxes(props) {
  const [boxes, setBoxes] = useState([]);

  useEffect(() => {
    // Maximum of 9 boxes, should be an odd number for style
    const numBoxes = Math.min(props.totalPages, 9);
    let front = [];
    let back = [];
    let res = [];

    for (let i = 0; i < numBoxes; i++) {
      if (front.length + back.length + 1 < numBoxes) {
        if (props.page - i - 1 >= 1) {
          front.unshift(props.page - i - 1);
        }

        if (props.page + i + 1 <= props.totalPages) {
          back.push(props.page + i + 1);
        }
      }
    }

    res.push(...front, props.page, ...back);
    setBoxes(res);
  }, [props.page, props.totalPages]);

  return (
    <div className="flex justify-center items-center gap-3 mb-4">
      <Box page={1} fetchForPage={props.fetchForPage} icon={faAnglesLeft} />
      <Box page={Math.max(props.page - 1, 1)} fetchForPage={props.fetchForPage} icon={faAngleLeft}
        className="mr-4" />
      {boxes.map(boxNum => {
        return <Box page={boxNum} curPage={props.page} fetchForPage={props.fetchForPage} />;
      })}
      <Box page={Math.min(props.page + 1, props.totalPages)} fetchForPage={props.fetchForPage} icon={faAngleRight}
        className="ml-4" />
      <Box page={props.totalPages} fetchForPage={props.fetchForPage} icon={faAnglesRight} />
    </div>
  );
}

function Box(props) {
  return (
    <div className={`flex justify-center items-center
      cursor-pointer w-4 h-4 rounded-xs text-xs p-2 shadow-[1px_1px_2px_rgba(0,0,0,0.2)] bg-gray-100
      ${props.curPage && props.curPage == props.page ? "bg-primary" : ""}
      ${props.className ? props.className : ""}`}
      onClick={() => props.fetchForPage(props.page)}>
      {props.icon
        ? <FontAwesomeIcon icon={props.icon} size="xs" />
        : props.page}
    </div>
  );
}
