import { useState, useEffect } from "react";
import { Dropdown } from "../common/drop_down";
import { MultiSelect } from "../common/drop_down";

export default function ExportForm(props) {
  const [exportGroup, setExportGroup] = useState(0);
  const [selectedSlnSummaries, setSelectedSlnSummaries] = useState([]);

  useEffect(() => {
    setExportGroup(1);  // export all by default
  }, []);

  useEffect(() => {
    if (exportGroup === 0) {  // clear
      setSelectedSlnSummaries([]);
    } else if (exportGroup === 1) {  // export all
      setSelectedSlnSummaries(props.solutionSummaries);
    } else if (exportGroup === 2) {  // export accepted only
      let slnSummaries = [];
      for (let i = 0; i < props.question.solutions.length; i++) {
        let s = props.question.solutions[i];
        if (s.accepted) {
          slnSummaries.push(s.summary);
        }
      }
      setSelectedSlnSummaries(slnSummaries);
    } else if (exportGroup === 3) {  // export denined only
      let slnSummaries = [];
      for (let i = 0; i < props.question.solutions.length; i++) {
        let s = props.question.solutions[i];
        if (!s.accepted) {
          slnSummaries.push(s.summary);
        }
      }
      setSelectedSlnSummaries(slnSummaries);
    }
  }, [exportGroup]);

  const handleExportGroupSelection = (e) => {
    e = !e ? 0 : parseInt(e);
    setExportGroup(e);
  }

  const exportQuestion = () => {
    
  }

  return (
    <div className="flex flex-col justify-between items-start gap-4 w-full h-full">
      <div className="w-full h-full">
        <p className="italic mt-3 mb-2 text-[12px]">* Select solutions to export them</p>
        <div className="flex justify-start items-stretch gap-4 w-full">
          <MultiSelect title="Solutions" selected={selectedSlnSummaries}
            options={props.solutionSummaries}
            values={props.solutionSummaries}
            updateValue={(s) => setSelectedSlnSummaries(s)} />
          <Dropdown title="Group options" value={exportGroup}
            options={["Export all", "Export accpted only", "Export denied only"]}
            values={[1, 2, 3]}
            updateValue={(e) => handleExportGroupSelection(e)} />
        </div>
      </div>
      <div>
        <button onClick={exportQuestion}>Download</button>
        <p className="italic mt-3 text-[12px]">* Choosing a export group value will override manually selected solutions</p>
      </div>
    </div>
  );
}