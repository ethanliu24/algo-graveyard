import React from "react";
import { createRoot } from "react-dom/client";
import About from "./about.jsx";
import Page from "../common/page.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("aboutDiv");
  const root = createRoot(container);
  root.render(React.createElement(Page, { pageTitle: "About", content: About, openSidebar: false }));
});
