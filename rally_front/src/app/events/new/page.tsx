"use client";
import { useState } from "react";
import NewEventForm from "../../components/events/NewEventForm";
import { useUser } from "@/app/context/auth_context";
import TopBanner from "@/app/components/top_banner";

export default function NewEvent() {
  const user = useUser().user;
  const [showBanner, setShowBanner] = useState(!user?.user?.account_id);

  return (
    <div className="relative bg-gray-100 ">
      {showBanner && (
        <TopBanner
          headline="Attention"
          text="Pour ajouter des évènements payants, merci de créer votre compte Stripe."
          buttonText="Créer un compte Stripe"
          buttonLink="/profiles/me"
          height="auto"
          maxHeight="200px"
          backgroundColor="#fee2e2"
          buttonBackgroundColor="#f87171"
          closeButtonClicked={() => setShowBanner(false)}
        />
      )}

      <div className={`p-4`}>
        <NewEventForm />
      </div>
    </div>
  );
}
