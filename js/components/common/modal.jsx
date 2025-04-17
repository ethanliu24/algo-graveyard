import { useEffect, useRef } from "react";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function ModalContainer(props) {
  const dialogRef = useRef(null);

  useEffect(() => {
    dialogRef.current.showModal();
    document.body.style.overflow = "hidden";
  }, []);

  const closeModal = () => {
    document.body.style.overflow = "";
    dialogRef.current.close();
    props.closeModal();
  };

  return (
    <dialog ref={dialogRef} className="backdrop:bg-black/60">
      <div className="w-[95vw] h-[95vh] fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 overflow-y-auto
        rounded p-8 pt-14 bg-white">
        <span className="absolute -ml-5 -mt-11 cursor-pointer w-6 h-6 p-1 rounded-[50%]
          flex justify-center items-center hover:bg-gray-300"
          onClick={closeModal}>
          <FontAwesomeIcon icon={faX} size="xs" />
        </span>
        hi
        {/* {props.content} */}
      </div>
    </dialog>
  );
}