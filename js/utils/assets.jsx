import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faHourglassEnd, faClock, faMinus } from "@fortawesome/free-solid-svg-icons";
import { Tooltip } from "react-tooltip";
import { capitalizeFirst } from "./utils";

export function getStatusIcon(status, id, enableTooltip = true) {
  const statusIcon = {
    "completed": <FontAwesomeIcon icon={faCheck} color="#6bd177" />,
    "unoptimized": <FontAwesomeIcon icon={faClock} color="#3b82f7" />,
    "attempted": <FontAwesomeIcon icon={faHourglassEnd} color="#f5cd3d" />
  };

  const tooltip = statusIcon[status] ? status : "unknown";
  const tooltipId = `${tooltip}-${id}`;

  return (
    <div data-tooltip-id={tooltipId} data-tooltip-content={capitalizeFirst(tooltip)} data-tooltip-place="left">
      {statusIcon[status] || <FontAwesomeIcon icon={faMinus} color="#c7c7c7" />}
      {enableTooltip ? <Tooltip id={tooltipId} /> : null}
    </div>);
};

export function getDifficultyStyle (difficulty) {
  const colorMap = {
    "easy": "#6bd177",
    "medium": "#f5cd3d",
    "hard": "#eb4b63"
  };

  return {
    color: colorMap[difficulty] || "#c7c7c7"
  };
};