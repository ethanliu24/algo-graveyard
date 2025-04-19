import { createContext, useContext } from "react";

export const ToastContext = createContext(null);  // contains a dom reference to toast

export function useToastContext() {
  const toastRef = useContext(ToastContext);

  if (!toastRef || !toastRef.current) {
    throw new Error("There's no reference to a Toast DOM element.");
  }

  return toastRef.current;
}