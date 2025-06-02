"use client";
import { useCallback } from "react";
import { registerToEventFreeApi, registerToEventPaymentApi } from "@/app/server_components/api";
import { toast } from "react-toastify";

interface RegisterButtonProps {
  event_id: number;
  isRegistered: boolean;
  isLoggedIn: boolean;
  onRegistered: () => void;
  nb_places: number;
  places_taken: number;
  date: string;
  cloture_billets: string;
  is_stripe_needed: boolean | null;
  is_free: boolean;
}

export default function RegisterButton({
  event_id,
  isRegistered,
  isLoggedIn,
  onRegistered,
  nb_places,
  places_taken,
  date,
  cloture_billets,
  is_stripe_needed,
  is_free
}: RegisterButtonProps) {
  const handleClickFree = useCallback(async () => {
    const result = await registerToEventFreeApi(event_id);
    if (result) {
      onRegistered();
      toast.success("Inscription enregistrée");
    } else{
      toast.error("Erreur lors de l'inscription");
    }
  }, [event_id, onRegistered]);

  const handleClickPayment = useCallback(async () => {
    const result = await registerToEventPaymentApi(event_id);
    const data = await result?.json()
    if (data) {
      window.location.href = data.session_url;
    } else{
      toast.error("Erreur lors de l'inscription");
    }
  }, [event_id, onRegistered]);

  const now = new Date();
  const eventDate = new Date(date);
  const clotureDate = new Date(cloture_billets);

  const isEventPast = eventDate < now;
  const isCloturePast = clotureDate < now;
  const isFull = nb_places === places_taken;

  const isDisabled = isRegistered || !isLoggedIn || isEventPast || isCloturePast || isFull;

  let buttonText = "Réserver";
  if (isRegistered) buttonText = "Inscrit";
  else if (isEventPast) buttonText = "Événement passé";
  else if (isCloturePast) buttonText = "Clôturé";
  else if (isFull) buttonText = "Complet";
  // else if (is_stripe_needed) buttonText = "Créez votre compte stripe"

  return (
    <button
      type="button"
      onClick={is_free ? handleClickFree : handleClickPayment}
      disabled={isDisabled}
      className={`py-2 px-6 rounded-xl transition whitespace-nowrap mt-4 md:mt-0
        ${isDisabled ? "bg-gray-400 cursor-not-allowed text-white" : "bg-[#123c69] hover:bg-[#0e2e50] text-white"}`}
    >
      {buttonText}
    </button>
  );
}
