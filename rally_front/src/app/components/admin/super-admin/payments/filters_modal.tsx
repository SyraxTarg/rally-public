"use client";

import { useState, useEffect } from "react";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  onApply: (filters: Filters) => void;
  initialFilters: Filters;
};

type Filters = {
  buyer_email?: string;
  date_avant?: string;
  date_apres?: string;
  brut_amount_min?: number;
  brut_amount_max?: number;
  status?: string;
  organizer_email?: string;
};

const statuses = ["pending", "success"];

export default function PaymentFiltersModal({ isOpen, onClose, onApply, initialFilters }: Props) {
  const [filters, setFilters] = useState<Filters>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value === "" ? undefined : Number(value) }));
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
          <div>
            <label className="block text-sm font-medium text-gray-700">Acheteur</label>
            <input
              type="text"
              name="buyer_email"
              value={filters.buyer_email || ""}
              onChange={handleChange}
              placeholder="Ex: Dupont"
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Organisateur</label>
            <input
              type="text"
              name="organizer_email"
              value={filters.organizer_email || ""}
              onChange={handleChange}
              placeholder="Ex: Dupont"
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Montant min (€)</label>
              <input
                type="number"
                name="brut_amount_min"
                min={0}
                value={filters.brut_amount_min ?? ""}
                onChange={handleNumberChange}
                className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Montant max (€)</label>
              <input
                type="number"
                name="brut_amount_max"
                min={0}
                value={filters.brut_amount_max ?? ""}
                onChange={handleNumberChange}
                className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Date début</label>
              <input
                type="date"
                name="date_avant"
                value={filters.date_avant || ""}
                onChange={handleChange}
                className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Date fin</label>
              <input
                type="date"
                name="date_apres"
                value={filters.date_apres || ""}
                onChange={handleChange}
                className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Statut</label>
            <select
              name="status"
              value={filters.status || ""}
              onChange={handleChange}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm"
            >
              <option value="">-- Tous les statuts --</option>
              {statuses.map((status) => (
                <option key={status} value={status}>
                  {status}
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
