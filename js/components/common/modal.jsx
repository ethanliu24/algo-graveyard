import { useEffect, useState, useRef } from "react";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Toast } from "primereact/toast";
import { ToastContext } from "../../contexts/toast_context";

export default function ModalContainer(props) {
  const [toastReady, setToastReady] = useState(false);
  const dialogRef = useRef(null);
  const toastRef = useRef(null);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    dialogRef.current.showModal();
    dialogRef.current.addEventListener("close", closeModal);
    return () => closeModal();
  }, []);

  useEffect(() => {
    if (toastRef.current) {
      setToastReady(true);
    }
  }, [toastRef.current]);

  const closeModal = () => {
    document.body.style.overflow = "";
    if (dialogRef.current) {
      dialogRef.current.removeEventListener("close", closeModal)
      dialogRef.current.close();
    }
    props.closeModal();
  };

  return (
    // https://mui.com/material-ui/react-modal/  Use this instead
    <dialog ref={dialogRef} className="backdrop:bg-black/60 fixed z-[99]">
      <ToastContext.Provider value={toastRef} >
        {toastReady && <div className="w-[90vw] h-[95vh] fixed inset-0 m-auto z-0
          overflow-y-auto scrollbar-hide flex flex-col justify-start items-start gap-2 rounded p-8 bg-white">
          <span className="absolute top-0 right-0 cursor-pointer w-6 h-6 p-1 rounded-full m-2
            flex justify-center items-center hover:bg-gray-300"
            onClick={() => closeModal()}>
            <FontAwesomeIcon icon={faX} size="xs" />
          </span>
          <h1 className="section-title first-letter:text-4xl text-3xl">{props.title}</h1>
          {props.content}
        </div>}
      </ToastContext.Provider>
      <Toast ref={toastRef} position="bottom-right" />
    </dialog>
  );
}