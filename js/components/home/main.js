import React from "react";
import { createRoot } from "react-dom/client";
import Home from "./home.jsx";
import Page from "../common/page.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("homeDiv");
  const root = createRoot(container);
  root.render(React.createElement(Page, { pageTitle: "Home", content: Home, openSidebar: true }));
});