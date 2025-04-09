import { useEffect, useState } from "react";
import { Tooltip } from "react-tooltip";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChevronRight,
  faChevronLeft,
  faHouse,
  faSquarePlus,
  faLock,
  faChartSimple,
  faCode,
  faCircleInfo
} from "@fortawesome/free-solid-svg-icons";
import tombstone from "../../../static/res/tombstone.svg";

export default function Sidebar(props) {
  const [isOpen, setIsOpen] = useState(props.open)

  useEffect(() => {
    localStorage.setItem("openSidebar", JSON.stringify(props.open));

    window.addEventListener("resize", () => {
      setIsOpen(window.innerWidth > 768);
    });

    return () => {
      window.removeEventListener("resize", () => {});
    }
  }, []);

  const handleSidebarExpand = () => {
    setIsOpen((i) => {
      const openState = !i && window.innerWidth >= 768;
      localStorage.setItem("openSidebar", JSON.stringify(openState));
      return openState;
    });
  }

  return (
    <div className={`
      h-screen overflow-y-scroll py-4 ${isOpen ? "w-50 px-2.5 " : "w-12 px-0"}
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
        <SidebarItem title="Authenticate" icon={faLock} link="/authenticate"
          isOpen={isOpen} size="l" />
        <SidebarItem title="Analytics" icon={faChartSimple} link="/analytics"
          isOpen={isOpen} size="l" />
        <SidebarItem title="Source" icon={faCode} link="https://github.com/ethanliu24/algo-graveyard"
          isOpen={isOpen} className={`${isOpen ? "-ml-[2px]" : ""}`} />
        <SidebarItem title="About" icon={faCircleInfo} link="/about"
          isOpen={isOpen} size="l" />
      </div>

      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        {window.innerWidth >= 768 ? <div className={`flex flex-col ${isOpen ? "items-end" : "items-center"} w-[100%]`}>
          <div className="flex justify-center items-center rounded-[50%] w-8 h-8
            bg-transparent transition-colors hover:bg-gray-200 cursor-pointer"
            onClick={handleSidebarExpand} >
            <FontAwesomeIcon icon={isOpen ? faChevronLeft : faChevronRight} />
          </div>
        </div> : null /* Temp solution for mobile */}
      </div>
    </div>
  );
}

function SidebarItem(props) {
  return (
    <a href={props.link} data-tooltip-id={props.title} data-tooltip-content={props.title}
      className={`w-[100%] flex justify-${props.isOpen ? "start" : "center"} items-center gap-4
        cursor-pointer select-none text-sm my-0.5 py-1 ${props.isOpen ? "px-3 rounded-2xl" : "px-0"}
      hover:bg-primary/20 hover:ring-1 hover:ring-primary/50`}>
      <span className={`${props.isOpen ? "w-[1.2rem]" : ""} ${props.className}`}>
        <FontAwesomeIcon icon={props.icon} size={props.size || ""} />
      </span>
      {props.isOpen ? null : <Tooltip id={props.title} className="ml-1 z-50" />}
      {props.isOpen ? <div>{props.title}</div> : null }
    </a>
  );
}
