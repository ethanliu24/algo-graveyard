import Sidebar from "../common/side_bar";

export default function Question() {
  return (
    <div className="flex justify-center items-center gap-0 w-full h-full">
      <Sidebar open={false} />
      <div className="flex-1">
        hi
      </div>
    </div>
  );
}