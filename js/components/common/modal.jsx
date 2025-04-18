import { useEffect, useRef } from "react";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function ModalContainer(props) {
  const dialogRef = useRef(null);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    dialogRef.current.showModal();
    dialogRef.current.addEventListener("close", closeModal);

    return () => closeModal();
  }, []);

  const closeModal = () => {
    document.body.style.overflow = "";
    props.closeModal();
    if (dialogRef) {
      dialogRef.current.removeEventListener("close", closeModal)
      dialogRef.current.close();
    }
  };

  return (
    <dialog ref={dialogRef} className="backdrop:bg-black/60">
      <div className="w-[90vw] h-[95vh] fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
        overflow-y-auto z-0 flex flex-col justify-start items-start gap-2 rounded p-8 bg-white">
        <span className="absolute top-0 right-0 cursor-pointer w-6 h-6 p-1 rounded-full m-2
          flex justify-center items-center hover:bg-gray-300"
          onClick={() => closeModal()}>
          <FontAwesomeIcon icon={faX} size="xs" />
        </span>
        <h1 className="section-title first-letter:text-4xl text-3xl">{props.title}</h1>
        {props.content}
      </div>
    </dialog>
  );
}