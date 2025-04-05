import Sidebar from "../common/side_bar.jsx";

export default function Page({ pageTitle, content, openSidebar }) {
  const Content = content

  return (
    <div className="flex">
      <Sidebar open={openSidebar || window.innerWidth >= 768} />
      <div className="flex-1 py-4 px-8">
        <h1 className="text-6xl font-medium">{pageTitle}</h1>
        <Content />
      </div>
    </div>
  );
}