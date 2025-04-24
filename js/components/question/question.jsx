import { useEffect, useRef, useState } from "react";
import { Toast } from "primereact/toast";
import { ToastContext } from "../../contexts/toast_context.jsx";
import Sidebar from "../common/side_bar.jsx";
import Verify from "../auth/verify.jsx";
import Solution from "./solution.jsx";
import DescriptionTab from "./description_tab.jsx";
import SolutionTab from "./solutions_tab.jsx";
import { getReqHeader } from "../../utils/utils.js";

export default function Question() {
  const [question, setQuestion] = useState("");
  const [curSolution, setCurSolution] = useState(null);
  const [solutions, setSolutions] = useState([]);
  const [activeTab, setActiveTab] = useState("");
  const [isAdmin, setIsAdmin] = useState(true);
  const [toastReady, setToastReady] = useState(false);

  const questionPanel = useRef(null);
  const horDragBar = useRef(null);
  const verDragBar = useRef(null);
  const toastRef = useRef(null);

  useEffect(() => {
    const req = {
      method: "GET",
      headers: getReqHeader(),
    }

    fetch(`/api/questions/${document.title}`, req)
      .then(res => res.json())
      .then(data => {
        document.title = data.title;
        setSolutions(data.solutions);
        setQuestion(data);
        if (data.solutions.length !== 0) setCurSolution(data.solutions[0]);
        setActiveTab("Description");
      })
      .catch(err => {
        throw err;
      });

    // Set up window resizers
    // horDragBar.current.addEventListener("mousedown", () => {
    //   document.addEventListener("mousemove", resizeHor);
    // });

    // verDragBar.current.addEventListener("mousedown", () => {
    //   document.addEventListener("mousemove", resizeVer);
    // });

    // document.addEventListener("mouseup", () => {
    //   document.removeEventListener("mousemove", resizeHor);
    //   document.removeEventListener("mousemove", resizeVer);
    // });
  }, []);

  useEffect(() => {
    if (toastRef.current) {
      setToastReady(true);
    }
  }, [toastRef.current]);

  const updateQuestion = (newData) => {
    setQuestion(newData);
  }

  const displaySolution = (data) => {
    setCurSolution(data);
  }

  const addSolution = (data) => {
    const updated = [...solutions, data];
    setSolutions(updated)
    setCurSolution(updated[updated.length - 1]);
  }

  const removeSolution = (id) => {
    const removed = solutions.filter(solution => solution.id !== id)
    setSolutions(removed);
    setCurSolution(removed.length !== 0 ? removed[0] : null);
  }

  const updateSolution = (sId, newData) => {
    const updated = solutions.map(sln => sln.id === sId ? newData : sln);
    setSolutions(updated);
    setCurSolution(newData)
  }

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
      <ToastContext.Provider value={toastRef}>
        {toastReady && <>
          <Sidebar open={false} />
          <div className="w-full h-full text-sm bg-white
            flex flex-row max-md:flex-col justify-between items-center">
            <div className="w-3/7 h-full max-md:w-full max-md:h-2/5 p-8 pt-2 overflow-y-auto hide-scrollbar" ref={questionPanel}>
              <div className="flex justify-around items-center mb-4">{
                ["Description", "Solutions"].map((label) => {
                  return (
                    <button key={`tab-${label}`}
                      className={`bg-transparent rounded-none text-black h-full
                        ${activeTab === label ? "text-primary border-b-2 border-b-primary" : ""}`}
                        onClick={() => setActiveTab(label)}>
                        {label}
                    </button>
                  );
              })}</div>
              {activeTab === "Description"
                && <DescriptionTab data={question} setIsAdmin={setIsAdmin} updateQuestion={updateQuestion} />}
              {activeTab === "Solutions"
                && (<SolutionTab question={question} solutions={solutions}
                  setIsAdmin={(b) => setIsAdmin(b)} displaySolution={displaySolution} addSolution={addSolution} />)}
            </div>
            <div className="border-gray-300 w-0 h-full border-2 max-md:hidden"
              ref={horDragBar}></div>
            <div className="border-gray-300 w-full h-0 border-2 md:hidden"
              ref={verDragBar}></div>
            <div className="flex-1 w-full h-full bg-white p-8 overflow-y-auto">
              <Solution question={question} data={curSolution} setIsAdmin={(b) => setIsAdmin(b)}
                removeSolution={removeSolution} updateSolution={updateSolution} />
            </div>
          </div>

          {!isAdmin
            ? <Verify closable={true} closeComponent={() => setIsAdmin(true)}
            positionStyle="fixed top-0 right-0 m-8" className="text-base" />
            : null}
        </>}
      </ToastContext.Provider>
      <Toast ref={toastRef} position="bottom-right" />
    </div>
  );
}