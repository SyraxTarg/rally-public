"use client";

import { useEffect } from "react";

type LogoutModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onLogout: () => void;
};

export default function LogoutModal({ isOpen, onClose, onLogout }: LogoutModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal content */}
      <div className="relative bg-white rounded-xl shadow-xl z-50 p-6 w-full max-w-md mx-4">
        <h2 className="text-lg font-semibold mb-4">
          Voulez-vous vous déconnecter ?
        </h2>
        <div className="flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded border hover:bg-gray-100"
          >
            Annuler
          </button>
          <button
            onClick={onLogout}
            className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-500"
          >
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  );
}
