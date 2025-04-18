import { useEffect, useRef } from "react";

export default function TextDisplay(props) {
  const containerRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    const heightObserver = new ResizeObserver(() => adjustHeight());
    heightObserver.observe(containerRef.current);
    adjustHeight();
    return () => heightObserver.disconnect();
  }, [props.content])

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight + 20}px`;
  }

  return (
    <div className="w-full h-fit" ref={containerRef}>
      <textarea className="w-full border-0 p-0 focus:outline-none resize-none text-xs"
        value={props.content} ref={textareaRef} readOnly />
    </div>
  );
}
