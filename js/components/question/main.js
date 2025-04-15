import React from "react";
import { createRoot } from "react-dom/client";
import Question from "./question.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("questionDiv");
  const root = createRoot(container);
  root.render(React.createElement(Question));
});