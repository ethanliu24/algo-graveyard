import { useEffect, useState } from "react";
import { Tooltip } from "react-tooltip";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChevronRight,
  faChevronLeft,
  faHouse,
  faSquarePlus,
  faChartSimple,
  faCode,
  faCircleInfo
} from "@fortawesome/free-solid-svg-icons";
import tombstone from "../../../static/res/tombstone.svg";

export function Sidebar(props) {
  const [isOpen, setIsOpen] = useState(props.open || window.innerWidth >= 768)

  useEffect(() => {
    window.addEventListener("resize", () => {
      setIsOpen(window.innerWidth > 768);
    });

    return () => {
      window.removeEventListener("resize", () => {});
    }
  }, []);

  return (
    <div className={`
      h-screen py-4 ${isOpen ? "w-47 px-2.5 " : "w-12 px-0"}
      border-r-1 rounded border-r-gray-300
      flex flex-col justify-between items-center
      `}>
      <div className={`w-[100%] gap-1 flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <div className="flex justify-center items-center w-[100%]">
          <img src={tombstone} alt="rip" className={`${isOpen ? "w-16 h-16" : "w-8 h-8"}`} />
        </div>
        <SidebarItem title="Home" icon={faHouse} link="/"
          isOpen={isOpen} className={`${isOpen ? "-ml-[2px]" : ""}`} />
        <SidebarItem title="Create" icon={faSquarePlus} link="/create"
          isOpen={isOpen} size="l" />
        <SidebarItem title="Analytics" icon={faChartSimple} link="/analytics"
          isOpen={isOpen} size="l" />
        <SidebarItem title="Source" icon={faCode} link="https://github.com/ethanliu24/algo-graveyard"
          isOpen={isOpen} className={`${isOpen ? "-ml-[2px]" : ""}`} />
        <SidebarItem title="About" icon={faCircleInfo} link="/about"
          isOpen={isOpen} size="l" />
      </div>

      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <div className={`flex flex-col ${isOpen ? "items-end" : "items-center"} w-[100%]`}>
          <div className="flex justify-center items-center rounded-[50%] w-8 h-8
            bg-transparent hover:bg-gray-200 transition-colors cursor-pointer"
            onClick={() => setIsOpen(!isOpen && window.innerWidth >= 768)} /* Temp solution for mobile */ >
            <FontAwesomeIcon icon={window.innerWidth >= 768 ? (isOpen ? faChevronLeft : faChevronRight) : ""} />
          </div>
        </div>
      </div>
    </div>
  );
}

function SidebarItem(props) {
  return (
    <a href={props.link}
      className={`w-[100%] flex justify-${props.isOpen ? "start" : "center"} items-center gap-4
        cursor-pointer select-none my-0.5 py-1 ${props.isOpen ? "px-3 rounded-2xl" : "px-0"}
      hover:bg-sky-100 hover:ring-1 hover:ring-sky-200`}>
      <span data-tooltip-id={props.title} data-tooltip-content={props.title}
        className={`${props.isOpen ? "w-[1.2rem]" : ""} ${props.className}`}>
        <FontAwesomeIcon icon={props.icon} size={props.size || ""} />
      </span>
      <Tooltip id={props.isOpen ? "" : props.title} className="ml-5" />
      {props.isOpen ?
        <div>{props.title}</div>
        : null
      }
    </a>
  );
}
