"use client";

import React, { useState, useEffect } from "react";
import { Select, SelectItem } from "@heroui/select";

type Filters = {
  search?: string;
  role?: string;
  is_planner?: boolean;
  nb_like?: string;
};

type Props = {
  isOpen: boolean;
  onClose: () => void;
  onApply: (filters: Filters) => void;
  initialFilters: Filters;
};

export default function ProfilesFiltersModal({
  isOpen,
  onClose,
  onApply,
  initialFilters,
}: Props) {
  const [filters, setFilters] = useState<Filters>({});

  useEffect(() => {
    if (isOpen) {
      setFilters(initialFilters || {});
    }
  }, [isOpen, initialFilters]);

  if (!isOpen) return null;

  const handleApply = (e: React.FormEvent) => {
    e.preventDefault();
    onApply(filters);
    onClose();
  };

  const handleClear = () => {
    setFilters({});
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4 py-6">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

      <form
        onSubmit={handleApply}
        className="relative z-50 max-w-4xl w-full bg-white rounded-2xl shadow p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {/* Recherche */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-800">Recherche</label>
          <input
            type="text"
            placeholder="Nom, email..."
            className="border border-gray-300 p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            value={filters.search || ""}
            onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))}
          />
        </div>

        {/* Rôle */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-800">Rôle</label>
          <Select
            className="max-w-full"
            aria-label="Rôle"
            placeholder="Sélectionnez un rôle"
            selectedKeys={filters.role ? new Set([filters.role]) : new Set()}
            onSelectionChange={(selectedKeys) => {
              const roles = Array.from(selectedKeys);
              setFilters((f) => ({ ...f, role: roles[0] || "" }));
            }}
          >
            <SelectItem key="ROLE_USER" value="ROLE_USER">
              Utilisateur
            </SelectItem>
            <SelectItem key="ROLE_ADMIN" value="ROLE_ADMIN">
              Administrateur
            </SelectItem>
            <SelectItem key="ROLE_SUPER_ADMIN" value="ROLE_SUPER_ADMIN">
              Super-administrateur
            </SelectItem>
          </Select>
        </div>

        {/* Statut */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-800">Statut</label>
          <Select
            className="max-w-full"
            aria-label="Statut"
            placeholder="Statut"
            selectedKeys={
              filters.is_planner === true
                ? new Set(["True"])
                : filters.is_planner === false
                ? new Set(["False"])
                : new Set()
            }
            onSelectionChange={(selected) => {
              const [value] = Array.from(selected);
              setFilters((f) => ({
                ...f,
                is_planner:
                  value === "True" ? true : value === "False" ? false : undefined,
              }));
            }}
          >
            <SelectItem key="True" value="True">
              Organisateur
            </SelectItem>
            <SelectItem key="False" value="False">
              Non-organisateur
            </SelectItem>
          </Select>
        </div>

        {/* Nombre de likes */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-800">Nombre de likes</label>
          <input
            type="text"
            placeholder="Ex: gte:10"
            className="border border-gray-300 p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            value={filters.nb_like || ""}
            onChange={(e) => setFilters((f) => ({ ...f, nb_like: e.target.value }))}
          />
        </div>

        {/* Boutons */}
        <div className="md:col-span-2 lg:col-span-4 flex justify-end gap-4 pt-4">
          <button
            type="button"
            onClick={handleClear}
            className="bg-gray-300 hover:bg-gray-400 text-gray-700 font-semibold px-6 py-2 rounded-lg transition shadow"
          >
            Réinitialiser
          </button>
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition shadow"
          >
            Filtrer
          </button>
        </div>
      </form>
    </div>
  );
}
