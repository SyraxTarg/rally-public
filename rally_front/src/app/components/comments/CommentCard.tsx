"use client";
import Image from "next/image";
import SignalCommentModal from "./SignalingComment";
import { useDisclosure } from "@heroui/modal";
import DeleteCommentButton from "./delete_comment_button";
import ConfirmDeleteModal from "../confirm_delete_modal";
import { useState } from "react";

type CommentCardProps = {
  comment_id: number;
  profile: {
    first_name: string;
    last_name: string;
    photo: string;
  };
  content: string;
  created_at: string;
  user_id?: number;
  by_user_id: number;
  onDeleteComment: (_:number) => void;
};

export default function CommentCard({
  profile,
  content,
  created_at,
  user_id,
  comment_id,
  by_user_id,
  onDeleteComment
}: CommentCardProps) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [confirmOpen, setConfirmOpen] = useState(false);
  const isOwner = user_id === by_user_id;

  const handleDelete = async () => {
    setConfirmOpen(false);
    await onDeleteComment(comment_id);
  };

  return (
    <>
      <div className="bg-white rounded-xl shadow p-4 flex flex-col sm:flex-row gap-4 sm:gap-6">
        {/* Photo de profil */}
        <div className="flex-shrink-0 flex justify-center sm:block">
          <Image
            src={"/pfps/default.jpg"}
            alt={`${profile.first_name} ${profile.last_name}`}
            width={48}
            height={48}
            className="rounded-full object-cover"
          />
        </div>

        {/* Contenu du commentaire + actions */}
        <div className="flex-1 flex flex-col sm:flex-row justify-between gap-4">
          {/* Texte */}
          <div className="flex-1 space-y-1">
            <div className="flex justify-between items-center">
              <p className="font-semibold text-[#123c69]">
                {profile.first_name} {profile.last_name}
              </p>
              <p className="text-xs text-gray-400">
                {new Date(created_at).toLocaleDateString('fr-FR', {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                              </p>
            </div>
            <p className="text-gray-700 whitespace-pre-line">{content}</p>
          </div>

          {/* Actions */}
          <div className="flex flex-row sm:flex-col justify-end items-center gap-4 sm:gap-2 text-gray-600">
            {user_id && (
              <button
                onClick={onOpen}
                title="Signaler"
                aria-label="Signaler le commentaire"
                className="hover:text-red-500 transition-colors"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3 3v1.5M3 21v-6m0 0 2.77-.693a9 9 0 0 1 6.208.682l.108.054a9 9 0 0 0 6.086.71l3.114-.732a48.524 48.524 0 0 1-.005-10.499l-3.11.732a9 9 0 0 1-6.085-.711l-.108-.054a9 9 0 0 0-6.208-.682L3 4.5M3 15V4.5"
                  />
                </svg>
              </button>
            )}
            {isOwner && (
              <DeleteCommentButton
                onClick={() => setConfirmOpen(true)}
              />
            )}
          </div>
        </div>
      </div>

      {/* Modale de signalement */}
      <SignalCommentModal
        isOpen={isOpen}
        comment_id={comment_id}
        onClose={onClose}
      />
      <ConfirmDeleteModal
        isOpen={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        onConfirm={handleDelete}
      />

    </>
  );
}
