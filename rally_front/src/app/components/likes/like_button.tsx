"use client";

import { useEffect, useState } from "react";
import {postLikeApi, deleteLikeApi, fetchIsLiked} from "@/app/server_components/api";
import { useCookies } from "react-cookie";

type LikeProps = {
  event_id: number;
  isLoggedIn: boolean;
  nb_likes: number;
};

export default function LikeButton({
  event_id,
  nb_likes,
  isLoggedIn,
}: LikeProps) {
  const [likes, setLikes] = useState(nb_likes);
  const [liked, setLiked] = useState(false);
  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);


  const isLikedByUser = async () => {
    try {
      const liked = await fetchIsLiked(event_id);
      // const data = await liked.json();
      console.log(`OMGGGG`, liked);
      setLiked(liked.is_liked);
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  };

  const handleLike = async () => {
    if (liked) return;

    try {
      const res = await postLikeApi(event_id, cookies.user_access_token);
      if (res.ok) {
        setLikes(likes + 1);
        setLiked(true);
      } else {
        console.error("Échec du like");
      }
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  };

  const handleRemoveLike = async () => {
    if (!liked) return;

    try {
      const res = await deleteLikeApi(event_id, cookies.user_access_token);
      if (res.ok) {
        setLikes(likes - 1);
        setLiked(false);
      } else {
        console.error("Échec du remove like");
      }
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      isLikedByUser();
    }
  }, [event_id, isLoggedIn]); // Appelle la fonction seulement quand event_id ou isLoggedIn change

  return (
    <div className="flex items-center mt-3 gap-1 text-pink-600">
      {isLoggedIn ? (
        <button
          onClick={liked ? handleRemoveLike : handleLike}
          className="hover:text-pink-800 transition-colors flex items-center gap-1"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-4 h-4 transition-all duration-300 ease-in-out"
            fill={`${liked ? "red" : "white"}`}
            stroke="red"
            viewBox="0 0 24 24"
          >
            <path d="M3.172 5.172a4.001 4.001 0 015.656 0L12 8.343l3.172-3.171a4.001 4.001 0 015.656 5.656L12 21.657 3.172 10.828a4.001 4.001 0 010-5.656z" />
          </svg>
          <span className="text-black">{likes}</span>
        </button>
      ) : (
        <div
          title="Connectez-vous pour liker"
          className="flex items-center gap-1 text-gray-400 cursor-not-allowed"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="red"
            strokeWidth="1.5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3.172 5.172a4.001 4.001 0 015.656 0L12 8.343l3.172-3.171a4.001 4.001 0 015.656 5.656L12 21.657 3.172 10.828a4.001 4.001 0 010-5.656z"
            />
          </svg>
          <span className="text-black">{likes}</span>
        </div>
      )}
    </div>
  );
}
