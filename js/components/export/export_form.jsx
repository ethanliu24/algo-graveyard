import { useState } from "react";
import { Dropdown } from "../common/drop_down";
import { MultiSelect } from "../common/drop_down";

export default function ExportForm(props) {
  const [exportGroup, setExportGroup] = useState("");
  const [selectedSlns, setSelectedSlns] = useState([]);

  return (
    <div className="flex flex-col justify-between items-start gap-4 w-full h-full">
      <div className="w-full h-full">
        <p className="italic mt-3 mb-2 text-[12px]">* Select solutions to export them</p>
        <div className="flex justify-start items-stretch gap-4 w-full">
          <MultiSelect title="Solutions" selected={selectedSlns}
            options={props.question.solutions.map(sln => sln.summary)}
            values={props.question.solutions.map(sln => sln.id)}
            updateValue={(t) => setSelectedSlns(t)} />
          <Dropdown title="Group options" value={exportGroup}
            options={["Export all", "Export accpted only", "Export denied only"]}
            values={[0, 1, 2]}
            updateValue={(e) => setExportGroup(e)} />
        </div>
      </div>
      <div>
        <button>Download</button>
        <p className="italic mt-3 text-[12px]">* Choosing a export group value will override manually selected solutions</p>
      </div>
    </div>
  );
}