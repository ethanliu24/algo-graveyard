import Sidebar from "../common/side_bar.jsx";

export default function Page({ pageTitle, content, openSidebar }) {
  const Content = content;

  return (
    <div className="flex">
      <Sidebar open={typeof openSidebar === "boolean"
        ? openSidebar
        : JSON.parse(localStorage.getItem("openSidebar")) || window.innerWidth >= 768} />
      <div className="flex-1 flex flex-col h-screen overflow-y-scroll py-4 px-16 max-md:px-4">
        <h1 className="text-4xl font-bold mb-6 first-letter:text-primary first-letter:text-5xl">{pageTitle}</h1>
        <Content />
      </div>
    </div>
  );
}