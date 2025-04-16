import Sidebar from "../common/side_bar.jsx";

export default function Page({ pageTitle, content, openSidebar }) {
  const Content = content;
  const presevedSidebarState = JSON.parse(localStorage.getItem("openSidebar"));

  return (
    <div className="flex">
      <Sidebar open={typeof openSidebar === "boolean"
        ? openSidebar
        : (typeof presevedSidebarState === "boolean" ? presevedSidebarState : window.innerWidth >= 768)} />
      <div className="flex-1 flex flex-col h-screen overflow-y-auto py-4 px-16 max-md:px-4">
        <h1 className="text-4xl font-bold mb-6 first-letter:text-primary first-letter:text-5xl">{pageTitle}</h1>
        <Content />
      </div>
    </div>
  );
}