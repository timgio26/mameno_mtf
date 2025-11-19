import { type ReactNode } from "react";

type PopupModalProp = {
  visible: boolean;
  // setVisible: React.Dispatch<React.SetStateAction<boolean>>;
  // onConfirm: () => void;
  // confirmText: string;
  children: ReactNode;
};

export function PopupModal({visible,children}: PopupModalProp) {
  return (
    <>
      {visible && (
        <div
          className={
            "fixed inset-0 z-50 flex items-center justify-center bg-white/10 backdrop-blur-sm transition-all"
          }
        >
          <div className="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 transform transition-all duration-300 scale-100">

            {children}


          </div>
        </div>
      )}
    </>
  );
}