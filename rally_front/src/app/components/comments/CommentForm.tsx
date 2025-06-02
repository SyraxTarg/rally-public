"use client";

import { useCallback, useState } from "react";
import { useCookies } from "react-cookie";
import { postCommentApi } from "@/app/server_components/api";
import { toast } from "react-toastify";

type CommentFormProps = {
  event_id: number;
  onNewComment: (comment: Comment) => void;
};

export default function CommentForm({ event_id, onNewComment }: CommentFormProps) {
  const [newComment, setNewComment] = useState("");
  const [cookies] = useCookies(['user_access_token']);

  const addComment = useCallback(async () => {
    if (!newComment.trim()) return;

    try {
      const res = await postCommentApi(
        JSON.stringify({
          event_id,
          content: newComment.trim(),
        }),
        cookies.user_access_token
      );

      onNewComment(res);
      setNewComment("");
      toast.success("Commentaire ajouté");
    } catch (error) {
      console.error("Erreur réseau :", error);
      toast.error(`Erreur lors de l'ajout : ${error}`)
    }
  }, [newComment, event_id]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await addComment();
  };


  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl bg-white p-4 rounded-xl shadow space-y-4">
      <label htmlFor="comment" className="block text-sm font-medium text-gray-700">
        Laisser un commentaire
      </label>
      <div className="flex items-center space-x-2">
        <input
          id="comment"
          name="comment"
          type="text"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Écrivez un commentaire..."
          className="flex-1 block w-full px-4 py-2 text-sm text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#0e2e50] focus:border-[#0e2e50"
        />
        <button
          type="submit"
          className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#123c69] border border-transparent rounded-lg hover:bg-[#0e2e50] focus:outline-none focus:ring-2 focus:ring-[#0e2e50]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
          </svg>
          Envoyer
        </button>
      </div>
    </form>
  );
}
