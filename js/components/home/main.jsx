import { createRoot } from "react-dom/client";
import { Home } from "./home.jsx";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("homeDiv");
  const root = createRoot(container);
  root.render(<Home />);
});
