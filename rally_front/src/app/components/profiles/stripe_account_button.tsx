"use client";
import { useCallback } from "react";
import { createStripeAccountApi } from "@/app/server_components/api";
import { redirect } from "next/navigation";
import { toast } from "react-toastify";


interface StripeAccountButton {
    profile_id: number;
}

export default function StripeAccountButton({
  profile_id
}: StripeAccountButton) {
  const handleClick = useCallback(async () => {
    try{
      const res = await createStripeAccountApi();
      const data = await res.json();
      window.location.href = data.onboarding_url;
    } catch {
      toast.error("Une erreur est survenue, le compte n'a pas été crée");
    }

  }, []);

  return (
    <button
      type="button"
      onClick={handleClick}
      className={`py-2 px-6 rounded-xl transition whitespace-nowrap mt-4 md:mt-0 bg-[#123c69] hover:bg-[#0e2e50] text-white`}
    >
      Créer mon compte stripe
    </button>
  );
}
