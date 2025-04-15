import { useEffect, useRef } from "react";
import Sidebar from "../common/side_bar";

export default function Question() {
  const questionPanel = useRef(null);
  const horDragBar = useRef(null);

  useEffect(() => {
    horDragBar.current.addEventListener("mousedown", () => {
      document.addEventListener("mousemove", resizeHor);
    });

    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", resizeHor);
    });
  }, []);

  const resizeHor = (e) => {
    const containerLeft = questionPanel.current.getBoundingClientRect().left;
    const width = Math.max(
      0.2 * window.innerWidth,
      Math.min(0.7 * window.innerWidth, e.clientX - containerLeft)
    );
    questionPanel.current.style.width = `${width}px`;
  };

  return (
    <div className="flex justify-center items-center gap-0 w-full h-screen">
      <Sidebar open={false} />
      <div className="flex-1 w-full h-full
        flex flex-row max-md:flex-col justify-between items-center">
        <div className="w-1/2 h-full max-md:w-full max-md:h-1/2" ref={questionPanel}></div>
        <div className="border-gray-300 hover:border-primary w-0 h-full border-2 cursor-ew-resize max-md:hidden"
          ref={horDragBar}></div>
        <div className="border-gray-300 hover:border-primary w-full h-0 border-2 cursor-ns-resize md:hidden"
          ></div>
        <div className="flex-1"></div>
      </div>
    </div>
  );
}