"use client";

import { useState, useEffect } from "react";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  onApply: (filters: Filters) => void;
  initialFilters: Filters;
};

type Filters = {
  date?: string;
  action_type?: string;
  log_type?: string;
};

export const action_types = [
    "login",
    "registration",
    "logout",
    "event_created",
    "event_updated",
    "event_deleted",
    "event_registered",
    "event_unregistered",
    "user_banned",
    "payment_failed",
    "user_signaled",
    "user_unsignaled",
    "comment_signaled",
    "comment_banned",
    "comment_unsignaled",
    "event_signaled",
    "event_unsignaled",
    "event_banned",
    "profile_updated",
    "type_created",
    "type_deleted",
    "reason_created",
    "reason_deleted",
    "email_unbanned"
  ];

  const log_types = ["info", "warning", "error", "critical"];

export default function LogsFiltersModal({ isOpen, onClose, onApply, initialFilters }: Props) {
  const [filters, setFilters] = useState<Filters>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onApply(filters);
    onClose();
  };

  const handleClear = () => {
    setFilters({});
  };

  useEffect(() => {
    if (isOpen && initialFilters) {
      setFilters(initialFilters);
    }
  }, [isOpen, initialFilters]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4 py-6">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

      <div className="relative z-50 w-full max-w-md bg-white rounded-xl shadow-xl p-6 max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-1 right-1 text-black-700 hover:text-gray-500 rounded-full p-1 text-xs"
          aria-label="Fermer la modale de filtres"
        >
          ✕
        </button>

        <h2 className="text-lg font-semibold mb-4">Filtres de paiements</h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Date début</label>
              <input
                type="date"
                name="date_avant"
                value={filters.date || ""}
                onChange={handleChange}
                className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Statut</label>
            <select
              name="action_type"
              value={filters.action_type || ""}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
            >
              <option value="">-- types d'actions --</option>
              {action_types.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
            <select
              name="log_type"
              value={filters.log_type || ""}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
            >
              <option value="">-- types de log --</option>
              {log_types.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div className="flex justify-between gap-2 mt-4">
            <button
              type="button"
              onClick={handleClear}
              className="w-1/2 border border-gray-400 text-gray-700 py-2 rounded-md hover:bg-gray-100"
            >
              Réinitialiser
            </button>
            <button
              type="submit"
              className="w-1/2 bg-[#123c69] text-[#edc7b7] py-2 rounded-md shadow hover:bg-[#0f2a4a]"
            >
              Appliquer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
