"use client";

import Image from "next/image";
import { useUser } from "../../context/auth_context";
import Card from "@/app/components/events/event_card";
import { Accordion, AccordionItem } from "@heroui/accordion";
import { useState, useEffect } from "react";
import Pagination from "@/app/components/pagination";
import { useRouter } from 'next/navigation';
import { Chip } from "@heroui/chip";
import UpdateProfileModal from "../../components/profiles/update_profile_modal";
import { useDisclosure } from "@heroui/modal";
import RegistrationCard from "@/app/components/registrations/registration_card";
import { fetchMyEvents } from "./server_components/fetch_my_events";
import { fetchMyRegistrations } from "./server_components/fetch_my_registrations";
import { useCookies } from "react-cookie";
import StripeAccountButton from "@/app/components/profiles/stripe_account_button";
import { useSearchParams } from "next/navigation";
import { toast } from "react-toastify";
import { fetchMyPayments } from "./server_components/fetch_my_payments";
import PaymentCard from "@/app/components/payments/payment_card";


export default function MePage() {
  const user = useUser()?.user;
  const router = useRouter();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const limit = 5;

  const [currentPageEvents, setCurrentPageEvents] = useState(1);
  const [currentPageRegistrations, setCurrentPageRegistrations] = useState(1);
  const [currentPagePayments, setCurrentPagePayments] = useState(1);

  const [myEvents, setMyEvents] = useState([]);
  const [totalPagesEvents, setTotalPagesEvents] = useState(1);

  const [myRegistrations, setMyRegistrations] = useState([]);
  const [totalPagesRegistrations, setTotalPagesRegistrations] = useState(1);

  const [myPayments, setMyPayments] = useState([]);
  const [totalPagesPayments, setTotalPagesPayments] = useState(1);

  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);
  const searchParams = useSearchParams();

  useEffect(() => {
    if (!user) return;
    fetchMyEvents(user.id, currentPageEvents, limit, cookies.user_access_token).then(({ data, totalPagesEvents }) => {
      setMyEvents(data);
      setTotalPagesEvents(totalPagesEvents);
    });
  }, [user, currentPageEvents]);

  useEffect(() => {
    fetchMyPayments(currentPagePayments, limit, cookies.user_access_token).then(({ data, totalPagesPayments }) => {
      setMyPayments(data);
      setTotalPagesPayments(totalPagesPayments);
    });
  }, [currentPagePayments]);

  useEffect(() => {
    fetchMyRegistrations(currentPageRegistrations, limit, cookies.user_access_token).then(({ data, totalPagesRegistrations }) => {
      setMyRegistrations(data);
      setTotalPagesRegistrations(totalPagesRegistrations);
    });
  }, [currentPageRegistrations]);

  useEffect(() => {
    const accountStatus = searchParams.get("account");
    if (accountStatus === "success") {
      toast.success("Le compte stripe a été créé avec succès !");
      const url = new URL(window.location.href);
      url.searchParams.delete("account");
      window.history.replaceState({}, document.title, url.pathname);
    } else if (accountStatus === "error") {
      toast.error("Erreur le compte stripe n'a pas été créé");
      const url = new URL(window.location.href);
      url.searchParams.delete("account");
      window.history.replaceState({}, document.title, url.pathname);
    }
  }, []);

  if (!user) {
    return (
      <p className="text-center text-lg text-gray-600 mt-10">
        Vous n'êtes pas connecté.
      </p>
    );
  }

  return (
    <>
      <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-12">
        {/* Profil */}
        <div className="relative flex flex-col md:flex-row items-center justify-between p-8 bg-white shadow-lg rounded-2xl">
          {user.is_planner && (
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

          <div className="flex-shrink-0">
            <Image
              className="w-40 h-40 rounded-full bg-gray-300 object-cover"
              src={user.photo}
              alt="Photo de profil"
              width={160}
              height={160}
              priority
            />
          </div>

          <div className="flex-1 mt-6 md:mt-0 md:ml-10 space-y-4 text-center md:text-left">
            <p className="text-3xl font-bold text-gray-900">
              {user.first_name} {user.last_name}
            </p>
            <div className="space-y-1 text-gray-600">
              <p><span className="font-semibold text-gray-700">Email :</span> {user.user.email}</p>
              <p><span className="font-semibold text-gray-700">Contact :</span> {user.user.phone_number}</p>
            </div>
            <div className="flex flex-wrap gap-4 justify-center md:justify-start pt-2">
              <Chip
                variant="solid"
                color="rose"
                className="text-sm font-medium bg-rose-100 text-rose-600 px-3 py-1 rounded-full"
              >
                ❤️ {user.nb_like} likes
              </Chip>

              <Chip
                variant="solid"
                color="gray"
                className="text-sm font-medium bg-gray-100 text-gray-700 px-3 py-1 rounded-full"
              >
                📅 {myEvents.length} évènement{myEvents.length > 1 ? "s" : ""}
              </Chip>
            </div>
          </div>

          <div className="mt-10 flex gap-6 flex-wrap justify-center">
            {user.user.account_id == null &&
              <StripeAccountButton profile_id={user.id}/>
            }
            <button className="px-6 py-2 bg-[#123c69] text-white rounded-full hover:bg-[#0e2c4d] transition cursor-pointer" onClick={onOpen}>
              Modifier mon profil
            </button>
            <button className="px-6 py-2 bg-[#edc7b7] text-[#123c69] rounded-full hover:bg-[#f0c1ad] transition cursor-pointer" onClick={() => router.push("/events/new")}>
              Ajouter un évènement
            </button>
          </div>
        </div>

        {/* Accordion Mes événements */}
        <div className="w-full">
          <Accordion className="border-t border-gray-200 divide-y divide-gray-200 dark:divide-gray-700 dark:border-gray-700">
            <AccordionItem
              key="1"
              aria-label="Mes évènements"
              title={<div className="text-[#123c69] dark:text-white font-semibold text-lg">Mes évènements</div>}
              className="p-0"
            >
              <div className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-8 w-full mt-6">
                {myEvents.map((event) => (
                  <Card
                    key={event.id}
                    title={event.title}
                    username={`${user.first_name} ${user.last_name}`}
                    price={event.price}
                    nb_likes={event.nb_likes}
                    pictureUrl={"/no_pic.jpg"}
                    isLoggedIn={true}
                    event_id={event.id}
                    description={event.description}
                    address={`${event.address.number}, ${event.address.street}, ${event.address.city}, ${event.address.country}`}
                    types={event.types}
                  />
                ))}
                {totalPagesEvents > 0 && (
                  <div className="col-span-full flex justify-center mt-8">
                    <Pagination
                      currentPage={currentPageEvents}
                      totalPages={totalPagesEvents}
                      onPageChange={setCurrentPageEvents}
                    />
                  </div>
                )}
                
              </div>
            </AccordionItem>
          </Accordion>
        </div>

        {/* Accordion Mes inscriptions */}
        <div className="w-full">
          <Accordion className="border-t border-gray-200 divide-y divide-gray-200 dark:divide-gray-700 dark:border-gray-700">
            <AccordionItem
              key="2"
              aria-label="Mes inscriptions"
              title={<div className="text-[#123c69] dark:text-white font-semibold text-lg">Mes inscriptions</div>}
              className="p-0"
            >
              <div className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-8 w-full mt-6">
                {myRegistrations.map((registration) => (
                  <RegistrationCard registration={registration} key={registration.id} />
                ))}
                {totalPagesRegistrations > 0 && (
                  <div className="col-span-full flex justify-center mt-8">
                    <Pagination
                      currentPage={currentPageRegistrations}
                      totalPages={totalPagesRegistrations}
                      onPageChange={setCurrentPageRegistrations}
                    />
                  </div>
                )}
              </div>
            </AccordionItem>
          </Accordion>
        </div>
        {/* Accordion Mes payments */}
        <div className="w-full">
          <Accordion className="border-t border-gray-200 divide-y divide-gray-200 dark:divide-gray-700 dark:border-gray-700">
            <AccordionItem
              key="2"
              aria-label="Mes paiements"
              title={<div className="text-[#123c69] dark:text-white font-semibold text-lg">Mes paiements</div>}
              className="p-0"
            >
              <div className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-8 w-full mt-6">
                {myPayments.map((payment) => (
                  <PaymentCard payment={payment} key={payment.id} />
                ))}
                {totalPagesPayments > 0 && (
                    <div className="col-span-full flex justify-center mt-8">
                      <Pagination
                        currentPage={currentPagePayments}
                        totalPages={totalPagesPayments}
                        onPageChange={setCurrentPagePayments}
                      />
                    </div>
                  )}
              </div>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
      <UpdateProfileModal isOpen={isOpen} onClose={onClose} />
    </>
  );
}
