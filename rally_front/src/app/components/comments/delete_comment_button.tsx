import { Trash2 } from "lucide-react";

export default function DeleteCommentButton({ onClick, disabled = false }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-2xl shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
    >
      <Trash2 size={18} />
    </button>
  );
}
