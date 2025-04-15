import { useEffect, useRef } from "react";
import Sidebar from "../common/side_bar";

export default function Question() {
  const questionPanel = useRef(null);
  const horDragBar = useRef(null);
  const verDragBar = useRef(null);

  useEffect(() => {
    // Set up window resizers
    horDragBar.current.addEventListener("mousedown", () => {
      document.addEventListener("mousemove", resizeHor);
    });

    verDragBar.current.addEventListener("mousedown", () => {
      document.addEventListener("mousemove", resizeVer);
    });

    document.addEventListener("mouseup", () => {
      document.removeEventListener("mousemove", resizeHor);
      document.removeEventListener("mousemove", resizeVer);
    });
  }, []);

  const resizeHor = (e) => {
    const containerLeft = questionPanel.current.getBoundingClientRect().left;
    const width = Math.max(
      0.2 * window.innerWidth,
      Math.min(0.8 * window.innerWidth, e.clientX - containerLeft)
    );
    questionPanel.current.style.width = `${width}px`;
  };

  const resizeVer = (e) => {
    const containerTop = questionPanel.current.getBoundingClientRect().top;
    const height = Math.max(
      0.2 * window.innerHeight,
      Math.min(0.8 * window.innerHeight, e.clientY + containerTop)
    );
    questionPanel.current.style.height = `${height}px`;
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
          ref={verDragBar}></div>
        <div className="flex-1"></div>
      </div>
    </div>
  );
}