import { Sidebar } from "../common/side_bar.jsx";

export function Home() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">yo</div>
    </div>
  );
}