import Image from "next/image";
import LikeButton from "../likes/like_button";
import { useRouter } from 'next/navigation'
import Link from "next/link";
import { Chip } from "@heroui/chip";
// import { types } from "util";

type CardProps = {
  title: string;
  username: string;
  address: string;
  price: number;
  nb_likes: number;
  pictureUrl?: string;
  description: string;
  isLoggedIn: boolean;
  event_id: number;
  organizer_id: number;
  types: {
    id: number;
    type: string;
  }[];
};


export default function Card({
  title,
  username,
  address,
  price,
  nb_likes,
  pictureUrl,
  isLoggedIn,
  event_id,
  organizer_id,
  description,
  types
}: CardProps) {
  const router = useRouter();
  return (
    <>
    <div
      className="rounded-2xl shadow-md bg-white overflow-hidden max-w-xs transition-shadow hover:shadow-lg"
    >
      {/* Image */}
      <div className="w-full h-32 relative">
        <Image
          src={`${pictureUrl}` || "/no_pic.jpg"}
          alt={title}
          fill
          className="object-cover"
        />
      </div>

      {/* Contenu */}
      <div className="p-4">
        <h2 className="text-lg font-bold">{title}</h2>
        <p className="text-gray-400 italic text-sm">
          <Link
            href={`/profiles/${organizer_id}`}
            className="text-[#123c69] hover:text-[#0e2e50] hover:underline transition-colors"
          >
            @{username}
          </Link>
        </p>
        <p className="text-sm text-gray-700 mt-2 line-clamp-2">
          {address}
        </p>
        <p className="text-sm text-gray-700 mt-2 line-clamp-3">
          {description}
        </p>

        {/* Prix avec icône ticket */}
        <div className="flex items-center mt-2 gap-2 text-red-600 font-semibold">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-4 h-4 text-red-600"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M21 10V8a2 2 0 0 0-2-2h-1V4a1 1 0 0 0-1-1h-2v2h-4V3H8a1 1 0 0 0-1 1v2H6a2 2 0 0 0-2 2v2h2v4H4v2a2 2 0 0 0 2 2h1v2a1 1 0 0 0 1 1h2v-2h4v2h2a1 1 0 0 0 1-1v-2h1a2 2 0 0 0 2-2v-2h-2v-4h2z" />
          </svg>
          <span>{price}€</span>
        </div>

        {/* Likes avec icône cœur */}
        <LikeButton
          event_id={event_id}
          nb_likes={nb_likes}
          isLoggedIn={isLoggedIn}
        />
      </div>
      <div className="flex flex-wrap gap-2 sm:gap-3 p-2">
        {
          types.map((type) => (
            <Chip
              key={type.id}
              variant="solid"
              color="default"
              className="text-xs font-semibold bg-blue-100 text-blue-800 px-3 py-1 rounded-full"
            >
              {type.type}
            </Chip>
          ))
        }
      </div>
      <div className="px-4 pb-4">
        <button
          onClick={() => router.push(`/events/${event_id}`)}
          className="w-full bg-[#123c69] hover:bg-[#29527e] text-white font-semibold py-2 px-4 rounded-xl mt-2 transition-colors duration-200"
        >
          Voir plus
        </button>
      </div>

    </div>
    </>
  );
}
