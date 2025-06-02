"use client";
import { useParams } from "next/navigation";
import { useState, useEffect, useCallback } from "react";
import LikeButton from "../../components/likes/like_button";
import { useUser } from "../../context/auth_context";
import {Accordion, AccordionItem} from "@heroui/accordion"
import CommentCard from "@/app/components/comments/CommentCard";
import { useDisclosure } from "@heroui/modal";
import SignalEventModal from "../../components/events/SignalingEvent";
import Caroussel from "../../components/events/Caroussel";
import CommentForm from "../../components/comments/CommentForm";
import RegisterButton from "../../components/events/RegisterButton";
import { useRouter } from 'next/navigation'
import Link from "next/link";
import UpdateEventModal from "@/app/components/events/update_event_modal";
import {fetchApi, isRegisteredApi, fetchCommentsEventApi, deleteCommentApi, deleteEventApi} from "@/app/server_components/api";
import { useCookies } from "react-cookie";
import TopBanner from "@/app/components/top_banner";
import { useSearchParams } from "next/navigation";
import { toast } from "react-toastify";
import DeleteButton from "@/app/components/events/delete_event_button";
import ConfirmDeleteModal from "@/app/components/confirm_delete_modal";
import { Chip } from "@heroui/chip";

interface Event {
  id: number;
  title: string;
  description: string;
  nb_places: number;
  price: number;
  date: string;
  cloture_billets: string;
  created_at: string;
  updated_at: string;
  nb_likes: number;
  nb_comments: number;
  profile: {
    id: number;
    first_name: string;
    last_name: string;
    photo: string;
    nb_like: number;
    email: string;
    created_at: string;
  };
  types: {
    id: number;
    type: string;
  }[];
  address: {
    id: number;
    city: string;
    zipcode: string;
    number: string;
    street: string;
    country: string;
  };
  pictures: {
    id: number;
    photo: string;
  }[];
}

export interface Comment {
    id: number;
    profile: {
      id: number;
      first_name: string;
      last_name: string;
      photo: string;
      nb_like: number;
      email: string;
      created_at: string;
    };
    event_id: number;
    content: string;
    created_at: string;
  }


export default function SingleEventPage() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [event, setEvent] = useState<Event | null>(null);
  const [placesTaken, setPlacesTaken] = useState(0);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentCount, setCommentCount] = useState(0);
  const [isRegistered, setIsRegistered] = useState(false);
  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);
  const { event_id } = useParams();
  const user = useUser().user;
  const [showBanner, setShowBanner] = useState(false);
  const router = useRouter();

  const searchParams = useSearchParams();

  const fetchData = useCallback(async () => {
    if (!event_id) return;
    return await fetchApi(`/events/${event_id}`, cookies.user_access_token, "GET")
  }, [event_id, isUpdateModalOpen]);

  const fetchTakenPlaces = useCallback(async () => {
    if (!event_id) return;

    return await fetchApi(`/registrations/places/${event_id}`, cookies.user_access_token, "GET")
  }, [event_id, isUpdateModalOpen, isRegistered]);

  const fetchComments = useCallback(async () => {
    if (!event_id) return;

    return await fetchCommentsEventApi(event_id);
  }, [event_id, isUpdateModalOpen, commentCount]);

  const handleNewComment = (comment: Comment) => {
    setComments((prev) => [comment, ...prev]);
    setCommentCount((prev) => prev + 1);
  };

  const handleRegistered = useCallback(async () => {
    const places = await fetchTakenPlaces();
    setPlacesTaken(places.number);
    setIsRegistered(true);
  }, [fetchTakenPlaces]);


  const handleDeleteComment = useCallback(async (comment_id: number) => {
    const confirmDelete = window.confirm("Voulez-vous supprimer ce commentaire ?");
    if (!confirmDelete) return;

    try {
      await deleteCommentApi(comment_id);
      setCommentCount((prev) => prev - 1);
    } catch (error) {
      console.error("Erreur lors de la suppression du commentaire :", error);
    }
  }, [deleteCommentApi]);


  const handleDeleteEvent = useCallback(async (event_id: number) => {
    try {
      await deleteEventApi(event_id);
      router.push("/events");
    } catch (error) {
      console.error("Erreur lors de la suppression de l'évènement :", error);
    }
  }, [deleteEventApi]);



  useEffect(() => {
    const onboardingStatus = searchParams.get("onboarding");
    if (onboardingStatus === "success") {
      toast.success("Paiement effectué créé avec succès !");
      const url = new URL(window.location.href);
      url.searchParams.delete("onboarding");
      window.history.replaceState({}, document.title, url.pathname);
    } else if (onboardingStatus === "error") {
      toast.error("Erreur le paiement n'a pas été pris en compte");
      const url = new URL(window.location.href);
      url.searchParams.delete("onboarding");
      window.history.replaceState({}, document.title, url.pathname);
    }
  }, []);

  useEffect(() => {
    const loadEvent = async () => {
      if (!event_id) return;

      try {
        const eventData = await fetchData();
        setEvent(eventData);

        const places = await fetchTakenPlaces();
        setPlacesTaken(places.number);

        const commentData = await fetchComments();
        setComments(commentData.data);
        setCommentCount(commentData.count);

        if (user?.id) {
          const is_registered = await isRegisteredApi(event_id);
          setIsRegistered(is_registered.registered)
        }
      } catch (error) {
        console.error("Error loading event data:", error);
      }
    };

    loadEvent();
  }, [fetchData, fetchTakenPlaces, fetchComments, user?.id]);

  useEffect(() => {
    if (!user?.user?.account_id && (event && event.price > 0)) {
      setShowBanner(true);
    } else {
      setShowBanner(false);
    }
  }, [user, event]);

  if (!event) return <div className="p-4 text-gray-600">Chargement...</div>;

  return (
    <>
    {showBanner && (
        <TopBanner
          headline="Attention"
          text="Pour vous inscrire à des évènements payants, merci de créer votre compte Stripe."
          buttonText="Créer un compte Stripe"
          buttonLink="/profiles/me"
          height="auto"
          maxHeight="200px"
          backgroundColor="#fee2e2"
          buttonBackgroundColor="#f87171"
          closeButtonClicked={() => setShowBanner(false)}
        />
      )}
    <div className="p-6 max-w-3xl mx-auto space-y-6">
      <Caroussel event_id={event_id} photos={event.pictures} />
      {/* Titre & Auteur */}
        <div className="bg-white p-6 rounded-2xl shadow-md space-y-2">
            <h1 className="text-3xl font-bold text-[#123c69] text-center">{event.title}</h1>
        </div>
        <div className="flex flex-col md:flex-row justify-between items-start gap-4">
            <div>
            <p className="text-sm text-gray-500">
              par{" "}
              <Link
                href={`/profiles/${event.profile.id}`}
                className="text-[#123c69] font-medium hover:underline hover:text-[#0e2e50] transition-colors"
              >
                {event.profile.first_name} {event.profile.last_name}
              </Link>
            </p>

                <div>
                    <p className="text-xs text-gray-400">
                        Créé le {new Date(event.created_at).toLocaleDateString('fr-FR', {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                    </p>
                    <p className="text-xs text-gray-400">
                        Mis à jour le {new Date(event.updated_at).toLocaleDateString('fr-FR', {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                    </p>
                </div>

            </div>
            <div className="flex items-center space-x-4 text-gray-600">
              <LikeButton event_id={event.id} nb_likes={event.nb_likes} isLoggedIn={!!user} />

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
              {!!user && user.id === event.profile.id && (
                <div className="flex flex-wrap items-center gap-2">
                  <button
                    onClick={() => setIsUpdateModalOpen(true)}
                    className="flex items-center gap-2 bg-yellow-400 hover:bg-yellow-500 text-white px-4 py-2 rounded-2xl shadow transition-all font-semibold"
                    title="Modifier l’évènement"
                  >
                    Modifier
                  </button>

                  <DeleteButton
                    onClick={() => setIsDeleteModalOpen(true)}
                    label="Supprimer"
                  />

                </div>


              )}
            </div>
        </div>

        {/* Infos de l'événement */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white p-6 rounded-xl shadow-md gap-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 w-full">
                <div>
                    <h3 className="font-semibold text-[#123c69]">Places</h3>
                    <p>{placesTaken} / {event.nb_places}</p>
                </div>
                <div>
                    <h3 className="font-semibold text-[#123c69]">Date</h3>
                    <p>{new Date(event.date).toLocaleDateString('fr-FR', {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}</p>
                </div>
                <div>
                    <h3 className="font-semibold text-[#123c69]">Prix</h3>
                    <p>{!event.price ? "gratuit" : `${event.price}€`}</p>
                </div>
                <div>
                    <h3 className="font-semibold text-[#123c69]">Adresse</h3>
                    <p>
                        {event.address.number} {event.address.street},<br />
                        {event.address.zipcode} {event.address.city}
                    </p>
                </div>
            </div>

                {/* Réserver button */}
                  <RegisterButton
                    event_id={Number(event_id)}
                    isRegistered={isRegistered}
                    isLoggedIn={!!user}
                    onRegistered={handleRegistered}
                    nb_places={event.nb_places}
                    places_taken={placesTaken}
                    date={event.date}
                    cloture_billets={event.cloture_billets}
                    is_stripe_needed={user && !user.user.account_id && event.price > 0 }
                    is_free={event.price == 0}
                  />
        </div>

        <div className="w-full max-w-3xl mx-auto">
          <Accordion className="border-t border-gray-200 divide-y divide-gray-200 rounded-md shadow-sm">
            <AccordionItem
              key="1"
              aria-label="Types"
              title={
                <div className="text-[#123c69] font-semibold text-lg">
                  Types
                </div>
              }
              className="p-0"
            >
              <div className="flex flex-wrap gap-2 p-4 bg-gray-50">
                {event.types.map((type) => (
                  <Chip
                    key={type.id}
                    variant="solid"
                    color="default"
                    className="text-xs font-semibold bg-blue-100 text-blue-800 px-3 py-1 rounded-full shadow-sm hover:bg-blue-200 transition-colors"
                  >
                    {type.type}
                  </Chip>
                ))}
              </div>
            </AccordionItem>
          </Accordion>
        </div>

        {/* Description */}
        <div className="bg-white p-6 rounded-xl shadow">
            <h3 className="text-xl font-semibold text-[#123c69] mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-line">{event.description}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow space-y-6">
          {event.nb_comments > 0 ? (
            <Accordion className="border-t border-gray-200 divide-y divide-gray-200">
              <AccordionItem
                key="1"
                aria-label="Commentaires"
                title={
                  <div className="text-[#123c69] font-semibold text-lg">
                    {commentCount} commentaire{commentCount > 1 ? "s" : ""}
                  </div>
                }
                className="p-0"
              >
                <div className="space-y-4 p-4">
                  {comments.map((comment) => (
                    <CommentCard
                      key={comment.id}
                      comment_id={comment.id}
                      profile={comment.profile}
                      content={comment.content}
                      created_at={comment.created_at}
                      user_id={user?.id ?? null}
                      by_user_id={comment.profile.id}
                      onDeleteComment={handleDeleteComment}
                    />
                  ))}
                </div>
              </AccordionItem>
            </Accordion>
          ) : (
            <p className="text-gray-500">Pas de commentaires</p>
          )}

          {!!user ? (
            <CommentForm
              event_id={event_id}
              onNewComment={handleNewComment}
            />

          ) : (
            <div className="flex flex-col items-center justify-center mt-4 text-center">
              <p className="text-gray-700 text-base mb-3">
                Pour laisser un commentaire, veuillez vous connecter.
              </p>
              <button
                onClick={() => router.push("/auth/login")}
                className="px-6 py-2 bg-[#123c69] text-white rounded-full hover:bg-[#0e2e50] transition"
              >
                Se connecter
              </button>
            </div>
          )}
        </div>

    </div>
    <SignalEventModal isOpen={isOpen} onClose={onClose} event_id={event.id} />
    <UpdateEventModal
      event={event}
      isOpen={isUpdateModalOpen}
      onClose={() => setIsUpdateModalOpen(false)}
    />
    <ConfirmDeleteModal
      isOpen={isDeleteModalOpen}
      onClose={() => setIsDeleteModalOpen(false)}
      onConfirm={() => handleDeleteEvent(event.id)}
      title="Supprimer cet évènement"
      description="Cette action est irréversible. Voulez-vous vraiment supprimer cet évènement ?"
    />

    </>
  );
}
