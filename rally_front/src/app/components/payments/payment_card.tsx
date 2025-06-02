"use client";

import React from "react";

interface Payment {
  id: number;
  event_id: number;
  event_title: string;
  buyer_id: number;
  buyer_email: string;
  organizer_id: number;
  organizer_email: string;
  brut_amount: number;
  status: string;
  created_at: string;
}

export default function PaymentCard({ payment }: { payment: Payment }) {
  const date = new Date(payment.created_at).toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const statusColor =
    payment.status === "success"
      ? "text-green-600 bg-green-100"
      : "text-red-600 bg-red-100";

  return (
    <div className="rounded-2xl border border-gray-200 shadow-sm p-4 bg-white w-full max-w-md mx-auto">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">
            {payment.event_title}
          </h2>
          <p className="text-sm text-gray-500">
            Acheteur : {payment.buyer_email}
          </p>
          <p className="text-sm text-gray-500">
            Organisateur : {payment.organizer_email}
          </p>
        </div>
        <span
          className={`text-sm px-2 py-1 rounded-full font-medium ${statusColor}`}
        >
          {payment.status === "success" ? "Succès" : payment.status}
        </span>
      </div>

      <div className="mt-4 flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-500">Montant</p>
          <p className="text-lg font-bold text-gray-800">
            {payment.brut_amount.toFixed(2)} €
          </p>
        </div>
        <div className="text-sm text-gray-500 text-right">
          <p>Payé le</p>
          <p>{date}</p>
        </div>
      </div>
    </div>
  );
}
