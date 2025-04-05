import Sidebar from "../common/side_bar.jsx";

export default function Page({ pageTitle, content, openSidebar }) {
  const Content = content

  return (
    <div className="flex">
    <Sidebar open={(openSidebar || JSON.parse(localStorage.getItem("openSidebar"))) && window.innerWidth >= 768} />
      <div className="flex-1 py-4 px-6 max-md:px-4">
        <h1 className="text-6xl font-medium max-md:text-4xl">{pageTitle}</h1>
        <Content />
      </div>
    </div>
  );
}