import { useState } from "react";
import { InputText } from 'primereact/inputtext';
import { faMagnifyingGlass, faCaretUp, faCaretDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Dropdown, MultiSelect } from "../common/drop_down.jsx";

export default function FilterBar(props) {
  const [source, setSource] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [status, setStatus] = useState("");
  const [tags, setTags] = useState([]);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("");
  const [asc, setAsc] = useState(true);

  const handleSearch = () => {
    // Since react deals with states asynchronously, there may be delays in when the states are updated,
    // which causes outdated information to fetch. Shouldn't be much of an issue in this case,
    // but smth to keep in mind.
    let query = {};
    if (source) query = { ...query, source: source };
    if (difficulty) query = { ...query, difficulty: difficulty };
    if (status) query = { ...query, status: status };
    if (tags.length !== 0) query = { ...query, tags: tags };
    if (search) query = { ...query, search: search };
    if (sortBy) query = { ...query, sort_by: sortBy };
    query = { ...query, order: asc ? "asc" : "desc" };

    props.searchQuestions(query);
  };

  return (
    <div className="flex justify-center items-stretch gap-2 flex-wrap gap-y-2 text-sm mb-4 w-full h-full">
      <button className="drop-down hover:bg-gray-50 flex justify-center items-center" onClick={() => setAsc(!asc)} >
        <FontAwesomeIcon icon={asc ? faCaretUp : faCaretDown} className="text-black" />
      </button>
      <Dropdown title="Sort" value={sortBy} options={props.sortOptions} values={props.sortOptions} updateValue={(s) => setSortBy(s)} />
      <Dropdown title="Source" value={source} options={props.sources} values={props.sources} updateValue={(s) => setSource(s)} />
      <Dropdown title="Difficulty" value={difficulty} options={props.difficulties} values={props.difficulties} updateValue={(d) => setDifficulty(d)} />
      <Dropdown title="Status" value={status} options={props.statuses} values={props.statuses} updateValue={(s) => setStatus(s)} />
      <MultiSelect title="Tags" selected={tags} options={props.tags} values={props.tags} updateValue={(t) => setTags(t)} />
      <span className="relative flex-1">
        <InputText placeholder="Search" value={search} onChange={(e) => setSearch(e.target.value)}
          className="drop-down min-w-48 w-full pl-8 cursor-text border-none"/>
        <FontAwesomeIcon icon={faMagnifyingGlass} size="sm" className="absolute top-1/2 left-0 -translate-y-1/2 ml-2" />
      </span>
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}