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
    <div>
      <Box page={1} icon={faAnglesLeft} />
      <Box page={Math.max(props.page - 1, 1)} icon={faAngleLeft} />
      {boxes.map(boxNum => {
        return <Box page={boxNum} />;
      })}
      <Box page={Math.min(props.page + 1, props.totalPages)} icon={faAngleRight} />
      <Box page={props.totalPages} icon={faAnglesRight} />
    </div>
  );
}

function Box(props) {
  return (
    <div>
      {props.icon
        ? <FontAwesomeIcon icon={props.icon} />
        : props.page}
    </div>
  );
}
