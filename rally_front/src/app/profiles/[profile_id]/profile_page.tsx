"use client";

import Image from "next/image";
import Card from "@/app/components/events/event_card";
import { Accordion, AccordionItem } from "@heroui/accordion";
import Pagination from "@/app/components/pagination";
import { Chip } from "@heroui/chip";
import { useDisclosure } from "@heroui/modal";
import SignalUserModal from "@/app/components/profiles/SignalingUsers";


export interface Profile {
    id: number;
    first_name: string;
    last_name: string;
    photo: string;
    nb_like: number;
    user: {
      id: number;
      email: string;
      phone_number: string;
      is_planner: boolean;
    };
    created_at: string;
    updated_at: string;
  }


export default function ProfilePage({profile, profileEvents, totalPages, currentPage, user}) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  if (!profile) {
    return <div>Chargement du profil...</div>;
  }


  return (
    <>
      <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-12">
        {/* Profil */}
        <div className="relative flex flex-col md:flex-row items-center justify-between p-8 bg-white shadow-lg rounded-2xl">
            {/* Badge Organisateur en haut à droite */}
            {profile.user.is_planner && (
              <div className="absolute top-4 right-4">
                <Chip
                  variant="solid"
                  color="warning"
                  className="text-xs font-semibold bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full"
                >
                  🛠️ Organisateur
                </Chip>
              </div>
            )}

            {/* Avatar */}
            <div className="flex-shrink-0">
              <Image
                className="w-40 h-40 rounded-full bg-gray-300 object-cover"
                src={profile.photo}
                alt="Photo de profil"
                width={160}
                height={160}
                priority
              />
            </div>

            {/* Infos */}
            <div className="flex-1 mt-6 md:mt-0 md:ml-10 space-y-4 text-center md:text-left">
              {/* Nom */}
              <p className="text-3xl font-bold text-gray-900">
                {profile.first_name} {profile.last_name}
              </p>

              {/* Email et Téléphone */}
              <div className="space-y-1 text-gray-600">
                <p><span className="font-semibold text-gray-700">Email :</span> {profile.user.email}</p>
                <p><span className="font-semibold text-gray-700">Contact :</span> {profile.user.phone_number}</p>
              </div>

              {/* Chips Likes & Évènements */}
              <div className="flex flex-wrap gap-4 justify-center md:justify-start pt-2">
                <Chip
                  variant="solid"
                  color="rose"
                  className="text-sm font-medium bg-rose-100 text-rose-600 px-3 py-1 rounded-full"
                >
                  ❤️ {profile.nb_like} likes
                </Chip>

                <Chip
                  variant="solid"
                  color="gray"
                  className="text-sm font-medium bg-gray-100 text-gray-700 px-3 py-1 rounded-full"
                >
                  📅 {profileEvents.length} évènement{profileEvents.length > 1 ? "s" : ""}
                </Chip>
              </div>
            </div>
            {user && (
                <button
                  onClick={onOpen}
                  title="Signaler"
                  aria-label="Signaler l’évènement"
                  className="flex items-center justify-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-6 h-6 block translate-y-[1px] hover:text-red-500 transition-colors"
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
          </div>

        {/* Accordion avec événements */}
        <div className="w-full">
          <Accordion className="border-t border-gray-200 divide-y divide-gray-200 dark:divide-gray-700 dark:border-gray-700">
            <AccordionItem
              key="1"
              aria-label="Mes évènements"
              title={
                <div className="text-[#123c69] dark:text-white font-semibold text-lg">
                  Evènements
                </div>
              }
              className="p-0"
            >
              <div className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-8 w-full mt-6">
                {profileEvents.map((event) => (
                  <Card
                    key={event.id}
                    title={event.title}
                    username={`${profile.first_name} ${profile.last_name}`}
                    price={event.price}
                    nb_likes={event.nb_likes}
                    pictureUrl={"/no_pic.jpg"}
                    isLoggedIn={!!user}
                    event_id={event.id}
                    description={event.description}
                    address={`${event.address.number}, ${event.address.street}, ${event.address.city}, ${event.address.country}`}
                    types={event.types}
                  />
                ))}

                {/* Pagination */}
                <div className="col-span-full flex justify-center mt-8">
                  <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={(page) => setCurrentPage(page)}
                  />
                </div>
              </div>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
      <SignalUserModal isOpen={isOpen} onClose={onClose} user_id={profile.id} />
      </>
  );
}
