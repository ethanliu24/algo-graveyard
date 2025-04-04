import { useEffect, useState } from "react"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronRight, faChevronLeft } from '@fortawesome/free-solid-svg-icons'

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
      h-screen p-6 ${isOpen ? "w-50" : "w-12 px-0"}
      border-r-1 rounded border-r-gray-300
      flex flex-col justify-between items-center
      `}>
      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <div>hi</div>
      </div>

      <div className={`w-[100%] flex flex-col ${isOpen ? "items-start" : "items-center"}`}>
        <div className={`flex flex-col ${isOpen ? "items-end" : "items-center"} w-[100%]`}>
          <div className="flex justify-center items-center rounded-[50%] w-8 h-8
            bg-transparent hover:bg-gray-200 transition-colors cursor-pointer"
            onClick={() => setIsOpen(!isOpen)}>
            <FontAwesomeIcon icon={isOpen ? faChevronLeft : faChevronRight} />
          </div>
        </div>
      </div>
    </div>
  )
}