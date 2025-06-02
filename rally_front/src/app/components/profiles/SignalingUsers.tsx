"use client";

import { useEffect, useCallback, useState } from "react";
import React from "react";
import { Select, SelectItem } from "@heroui/select";
import { fetchReasonsApi, postSignaledUserApi } from "@/app/server_components/api";
import { toast } from "react-toastify";

interface SignalUserModalProps {
  isOpen: boolean;
  user_id: number;
  onClose: () => void;
}

interface Reason {
  id: number;
  reason: string;
}

export default function SignalUserModal({ isOpen, user_id, onClose }: SignalUserModalProps) {
  const [reasons, setReasons] = useState<Reason[]>([]);
  const [selectedReason, setSelectedReason] = useState<Reason | null>(null);
  console.log(selectedReason);

  const fetchReasons = useCallback(async () => {
    if (!user_id) return;

    try {
      const response = await fetchReasonsApi()
        const data = await response?.json();
      if (Array.isArray(data.data)) {
        setReasons(data.data);
      } else {
        console.error("Les données reçues ne sont pas un tableau :", data);
        setReasons([]);
      }
    } catch (err) {
      console.error("Erreur réseau :", err);
      setReasons([]);
    }
  }, [user_id]);

  useEffect(() => {
    if (isOpen) fetchReasons();
  }, [fetchReasons, isOpen]);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "auto";
  }, [isOpen]);

  const onSignal = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selectedReason) return;

    try {
      await postSignaledUserApi(JSON.stringify({
        "reason_id": selectedReason.id,
        "user_signaled_id": user_id
      }))
      toast.success(`Utilisateur signalé pour la raison : ${selectedReason.reason}`)
      onClose();
    } catch (error) {
      console.error("Erreur lors du signalement :", error);
      toast.error(`Erreur lors du signalement : ${error}`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

      {/* Modal */}
      <form
        onSubmit={onSignal}
        className="relative bg-white rounded-xl shadow-xl z-50 p-6 w-full max-w-md mx-4"
      >
        <h2 className="text-lg font-semibold mb-4">
          Pourquoi signaler cet utilisateur ?
        </h2>

        <div className="flex w-full flex-col gap-2 mb-6">
          <label htmlFor="reason" className="text-sm font-medium text-gray-700">
            Raison du signalement
          </label>
          <div className="relative">
            <Select
              id="reason"
              className="w-full"
              placeholder="Sélectionnez une raison"
              selectedKeys={new Set(selectedReason ? [selectedReason.id.toString()] : [])}
              aria-label="Sélectionnez une raison"
              variant="bordered"
              onSelectionChange={(key) => {
                const selectedId = Array.from(key)[0];
                const found = reasons.find((r) => r.id.toString() === selectedId);
                setSelectedReason(found || null);
              }}
              classNames={{
                trigger:
                  "bg-white text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#123c69] focus:border-[#123c69] transition-all",
                listboxWrapper: "rounded-lg border border-gray-200 shadow-md bg-white",
                listbox: "p-1",
                popoverContent: "z-50",
              }}
            >
              {reasons.map((reason) => (
                <SelectItem
                  aria-label={reason.reason}
                  key={reason.id.toString()}
                  className="hover:bg-gray-100 text-sm px-2 py-1 cursor-pointer rounded"
                >
                  {reason.reason}
                </SelectItem>
              ))}
            </Select>
          </div>
        </div>

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded border hover:bg-gray-100"
          >
            Annuler
          </button>
          <button
            type="submit"
            className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-500 disabled:bg-gray-300"
            disabled={!selectedReason}
          >
            Signaler
          </button>
        </div>
      </form>
    </div>
  );
}
