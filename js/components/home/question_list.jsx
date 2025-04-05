export default function QuestionList() {
  return (
    <div>
      <div className="text-sm w-[100%]">
        <ListItem idx={1} title="Title" status="status" source="source" difficulty="diff" createdAt="Mar 21, 2020" tags={["graph", "bfs", "ass", "aaa"]} />
        <ListItem idx={1} title="Title" status="status" source="source" difficulty="diff" createdAt="Mar 21, 2020" tags={["graph", "bfs", "ass", "aaa"]} />
        <ListItem idx={1} title="Title" status="status" source="source" difficulty="diff" createdAt="Mar 21, 2020" tags={["graph", "bfs", "ass", "aaa"]} />
        <ListItem idx={1} title="Title" status="status" source="source" difficulty="diff" createdAt="Mar 21, 2020" tags={["graph", "bfs", "ass", "aaa"]} />
      </div>
    </div>
  );
}

function ListItem(props) {
  return (
    <div className="flex justify-between items-center gap-4 text-center mt-4
      bg-transparent px-4 py-2 cursor-pointer rounded hover:bg-gray-200">
      <div className="text-[12px] text-gray-500">{props.idx}</div>
      <div>{props.status}</div>
      <div className="flex-8 flex flex-col justify-between items-start">
        <div className="text-sm">{props.title}</div>
        <div className="flex justify-start items-center gap-2 text-[12px] text-gray-500">
          <div className="">{props.createdAt}</div>
          <div className="">{props.source}</div>
          <div className="">{props.difficulty}</div>
        </div>
      </div>
      <div className="flex justify-end items-center gap-2 w-48 overflow-x-scroll text-xs max-md:hidden">
        {props.tags.map((tag, i) => {
          return (<div key={tag + props.idx + i}
              className="bg-gray-300 px-1 rounded-3xl">{`#${tag}`}
            </div>);
        })}
      </div>
    </div>
  );
}

// idstring
// sourceExpand allstring
// difficultyExpand allstring
// statusExpand allstring
// titlestring
// tagsExpand allarray<string>
// created_atstringdate-time
// last_modifiedstringdate-time