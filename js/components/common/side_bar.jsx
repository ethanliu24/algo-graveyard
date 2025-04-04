import { useEffect, useState } from "react"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronRight, faChevronLeft, faCross, faHouse } from '@fortawesome/free-solid-svg-icons'

export function Sidebar(props) {
  const [isOpen, setIsOpen] = useState(props.open || screen.width >= 768)

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
      h-screen py-4 ${isOpen ? "w-50 px-3 " : "w-12 px-0"}
      border-r-1 rounded border-r-gray-300
      flex flex-col justify-between items-center
      `}>
      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <FontAwesomeIcon icon={faCross} size="2x" className="mb-4" />
        <SidebarItem title="Home" />
      </div>

      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <div className={`flex flex-col ${isOpen ? "items-end" : "items-center"} w-[100%]`}>
          <div className="flex justify-center items-center rounded-[50%] w-8 h-8
            bg-transparent hover:bg-gray-200 transition-colors cursor-pointer"
            onClick={() => setIsOpen(!isOpen && window.innerWidth >= 768)} /* Temp solution for mobile */ >
            <FontAwesomeIcon icon={isOpen ? (window.innerWidth >= 768 ? faChevronLeft : faChevronRight) : ""} />
          </div>
        </div>
      </div>
    </div>
  );
}

function SidebarItem(props) {
  return (
    <div className="w-[100%] flex justify-start items-center gap-4 cursor-pointer
      px-3 py-1 rounded-2xl select-none
      hover:bg-blue-200 hover:ring-2 hover:ring-offset-1 hover:ring-blue-400">
      <FontAwesomeIcon icon={faHouse} />
      <div>{props.title}</div>
    </div>
  );
}
