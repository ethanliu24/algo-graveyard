import { useEffect, useRef, useState } from "react";
import Sidebar from "../common/side_bar.jsx";
import { QuestionTab } from "./tabs.jsx";

export default function Question() {
  const [questionData, setQuestionData] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

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

  const tabs = [
    { label: "Question", content: <QuestionTab data={questionData} /> }
  ];

  return (
    <div className="flex justify-center items-center gap-0 w-full h-screen">
      <Sidebar open={false} />
      <div className="flex-1 w-full h-full text-sm
        flex flex-row max-md:flex-col justify-between items-center">
        <div className="w-1/2 h-full max-md:w-full max-md:h-1/2 p-4" ref={questionPanel}>
          <div className="flex justify-around items-center">{
            tabs.map(({ label }, i) => {
              return (
                <button key={`tab-${label}-${i}`}
                  className={`bg-transparent rounded-none text-black h-full
                    ${activeTab === i ? "text-primary border-b-2 border-b-primary" : ""}`}
                    onClick={() => setActiveTab(i)}>
                    {label}
                </button>
              );
          })}</div>
          {tabs[activeTab].content}
        </div>
        <div className="border-gray-300 hover:border-primary w-0 h-full border-2 cursor-ew-resize max-md:hidden"
          ref={horDragBar}></div>
        <div className="border-gray-300 hover:border-primary w-full h-0 border-2 cursor-ns-resize md:hidden"
          ref={verDragBar}></div>
        <div className="flex-1"></div>
      </div>
    </div>
  );
}