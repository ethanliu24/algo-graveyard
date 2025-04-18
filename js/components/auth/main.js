import React from "react";
import { createRoot } from "react-dom/client";
import Authenticate from "./authenticate.jsx";
import Page from "../common/page.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("authDiv");
  const root = createRoot(container);
  root.render(React.createElement(Page, { pageTitle: "Admin Login", content: Authenticate, openSidebar: false }));
});