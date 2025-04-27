import React from "react";
import { createRoot } from "react-dom/client";
import NotFound from "./not_found.jsx";
import Page from "../common/page.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("notFoundDiv");
  const root = createRoot(container);
  root.render(React.createElement(Page, { pageTitle: "Not Found", content: NotFound, openSidebar: false }));
});
