import React from "react";
import { createRoot } from "react-dom/client";
import Create from "./create.jsx";
import Page from "../common/page.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("createDiv");
  const root = createRoot(container);
  root.render(React.createElement(Page, { pageTitle: "Create", content: Create, openSidebar: false }));
});