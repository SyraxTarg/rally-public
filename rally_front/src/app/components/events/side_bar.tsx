"use client";
import React, { useState, useEffect, useCallback } from "react";
import styles from "./side_bar.module.css";
import CustomDatePicker from "./date_picker";
import { useCookies } from "react-cookie";
import { fetchTypesApi } from "@/app/server_components/api";

type SidebarProps = {
  children: React.ReactNode;
  onSelect: (type_id: number) => void;
  selectedTypes: number[];
  onDateAvantChange: (date: Date | null) => void;
  dateAvant: Date;
  onDateApresChange: (date: Date | null) => void;
  dateApres: Date;
  city: string;
  onCityChange: (city: string | null) => void;
  country: string;
  onCountryChange: (country: string | null) => void;
  popular: boolean;
  onPopularToggle: (popular: boolean | null) => void;
  recent: boolean;
  onRecentToggle: (recent: boolean | null) => void;
};

type EventType = {
  id: number;
  type: string;
};

export default function Sidebar({
  children,
  onSelect,
  selectedTypes,
  onDateAvantChange,
  dateAvant,
  onDateApresChange,
  dateApres,
  city,
  onCityChange,
  country,
  onCountryChange,
  popular,
  onPopularToggle,
  recent,
  onRecentToggle,
}: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [eventTypes, setEventTypes] = useState<EventType[]>([]);
  const [cookies] = useCookies(["user_access_token", "user_refresh_token", "user_connected_id"]);

  const fetchTypes = useCallback(async () => {
    try {
      const res = await fetchTypesApi();
      if (!res.ok) return;

      const data = await res.json();
      setEventTypes(data.data);
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  }, []);

  useEffect(() => {
    fetchTypes();
  }, [fetchTypes]);

  return (
    <div className="flex min-h-screen bg-gray-50 pt-16"> {/* décalé sous le header fixe */}
      {/* Sidebar */}
      <div
        className={`${
          styles.sidebar
        } ${isOpen ? styles.sidebarOpen : styles.sidebarClosed} w-72 sm:relative fixed top-16 left-0 z-40 sm:top-0 sm:static bg-white shadow-md transition-all`}
      >
        {isOpen && (
          <div className="p-4 relative">
            <button
              className="sm:hidden absolute top-2 right-2 p-2 rounded-md bg-gray-200 hover:bg-gray-300 z-50"
              onClick={() => setIsOpen(false)}
              aria-label="Fermer la barre latérale"
            >
              ✕
            </button>
            <h2 className="text-xl font-semibold mb-6">Filtres</h2>

            {/* Types */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Types</h3>
              <ul className="flex flex-wrap gap-2">
                {eventTypes.map((eventType, index) => (
                  <li key={index}>
                    <button
                      onClick={() => onSelect(eventType.id)}
                      className={`px-3 py-1 rounded-full text-sm transition ${
                        selectedTypes.includes(eventType.id)
                          ? styles.selected_type
                          : styles.unselected_type
                      }`}
                    >
                      {eventType.type}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            {/* Dates */}
            <div className="mb-6 space-y-4">
              <div>
                <CustomDatePicker
                  label="Date avant"
                  value={dateAvant}
                  onChange={(newDate) => onDateAvantChange(newDate)}
                />
                <button
                  onClick={() => onDateAvantChange(null)}
                  className="mt-1 text-sm text-blue-600 hover:underline"
                >
                  Réinitialiser la date
                </button>
              </div>
              <div>
                <CustomDatePicker
                  label="Date après"
                  value={dateApres}
                  onChange={(newDate) => onDateApresChange(newDate)}
                />
                <button
                  onClick={() => onDateApresChange(null)}
                  className="mt-1 text-sm text-blue-600 hover:underline"
                >
                  Réinitialiser la date
                </button>
              </div>
            </div>

            {/* Localisation */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Localisation</h3>
              <div className="space-y-4">
                <div>
                  <label htmlFor="city" className="block text-sm text-gray-600 mb-1">
                    Ville
                  </label>
                  <input
                    type="text"
                    name="city"
                    id="city"
                    placeholder="Ex : Paris"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    onChange={(e) => onCityChange(e.target.value)}
                  />
                </div>

                <div>
                  <label htmlFor="country" className="block text-sm text-gray-600 mb-1">
                    Pays
                  </label>
                  <input
                    type="text"
                    name="country"
                    id="country"
                    placeholder="Ex : France"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    onChange={(e) => onCountryChange(e.target.value)}
                  />
                </div>
              </div>
            </div>

            {/* Tri */}
            <div className="mt-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Trier par</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => onPopularToggle(!popular)}
                  className={`px-3 py-1 rounded-full text-sm transition ${
                    popular ? styles.selected_type : styles.unselected_type
                  }`}
                >
                  Les plus populaires
                </button>
                <button
                  onClick={() => onRecentToggle(!recent)}
                  className={`px-3 py-1 rounded-full text-sm transition ${
                    recent ? styles.selected_type : styles.unselected_type
                  }`}
                >
                  Les plus récents
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main content */}
      <div
          className={`content flex-1 p-4 transition-margin duration-300 
            ${isOpen ? 'ml-64' : 'ml-0'} sm:ml-0`}
        >
      <button
          className={`
            ${styles.toggleButton}
            sm:relative fixed top-20 left-4 sm:top-auto sm:left-0
            bg-[#123c69] text-white p-2 rounded-md shadow-md
          `}
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? (
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" className="w-6 h-6" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" className="w-6 h-6" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          )}
        </button>

        {children}
      </div>
    </div>
  );
};
