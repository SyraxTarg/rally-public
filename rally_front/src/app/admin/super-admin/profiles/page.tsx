"use client";

import React, { useEffect, useState } from "react";
import { fetchProfilesApi } from "@/app/server_components/api";
import RoleModal from "@/app/components/admin/profiles/role_modal";
import ProfilesFiltersModal from "@/app/components/admin/profiles/filters_modal";

type Profile = {
  id: number;
  first_name: string;
  last_name: string;
  photo: string;
  nb_like: number;
  user: {
    id: number;
    email: string;
    phone_number: string;
    is_planner: boolean;
    account_id: string | null;
    role: {
        id: number;
        role: string;
    }
  };
  created_at: Date;
  updated_at: Date;
};

const PAGE_SIZE = 10;

const ProfileBackOffice: React.FC = () => {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [isRoleOpen, setIsRoleOpen] = useState<boolean>(false);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [filters, setFilters] = useState({});

  const fetchProfiles = async (page: number) => {
    setLoading(true);
    setError(null);
    try {
      const offset = (page - 1) * PAGE_SIZE;
      const response = await fetchProfilesApi(PAGE_SIZE, offset, filters);
      const data = await response?.json();
      setProfiles(data.data);
      setTotal(data.total);
    } catch (err) {
      setError("Failed to load profiles");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfiles(currentPage);
  }, [currentPage, filters]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (loading) return (
    <div className="flex justify-center items-center p-10 text-gray-600 text-lg font-semibold">
      Chargement...
    </div>
  );
  if (error) return (
    <div className="p-6 bg-red-100 text-red-700 rounded-md font-medium">
      {error}
    </div>
  );

  return (
    <>
      {/* Filtres */}
      <div className="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white">Liste des Profils</h1>
        <button
          onClick={() => setIsFiltersOpen(true)}
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 text-white font-semibold px-5 py-2 rounded-md shadow transition"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L15 13.414V19a1 1 0 01-1.447.894l-4-2A1 1 0 019 17v-3.586L3.293 6.707A1 1 0 013 6V4z" />
          </svg>
          Filtres
        </button>
      </div>

      {/* Desktop table */}
      <div className="hidden sm:block relative overflow-x-auto p-6 bg-white dark:bg-gray-900 rounded-lg shadow-md">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {["ID", "Utilisateur", "Email", "Rôle", "Organisateur", "Créé le", "Téléphone", "Changer de rôle"].map((header) => (
                <th
                  key={header}
                  className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider dark:text-gray-300"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200 dark:bg-gray-900 dark:divide-gray-700">
            {profiles.map((profile) => (
              <tr key={profile.id} className="hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">{profile.id}</td>
                <td className="px-6 py-4 text-blue-600 dark:text-blue-400 hover:underline">
                  <a href={`/profiles/${profile.id}`}>
                    {profile.first_name} {profile.last_name}
                  </a>
                </td>
                <td className="px-6 py-4 text-gray-700 dark:text-gray-300">{profile.user.email}</td>
                <td className="px-6 py-4 text-gray-700 dark:text-gray-300">{profile.user.role.role}</td>
                <td className="px-6 py-4">
                  <span className={`inline-block px-2 py-0.5 text-xs font-semibold rounded-full
                    ${profile.user.is_planner
                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                      : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"}`}>
                    {profile.user.is_planner ? "Oui" : "Non"}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-600 dark:text-gray-400">
                  {new Date(profile.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-gray-700 dark:text-gray-300">{profile.user.phone_number}</td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => {
                      setSelectedUserId(profile.user.id);
                      setIsRoleOpen(true);
                    }}
                    className="text-blue-600 hover:text-blue-800 font-semibold"
                  >
                    Modifier
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Cards */}
      <div className="sm:hidden p-4 space-y-4">
        {profiles.map((profile) => (
          <div key={profile.id} className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-4 space-y-2">
            <div className="text-lg font-semibold text-gray-900 dark:text-white">
              {profile.first_name} {profile.last_name}
            </div>
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <strong>Email :</strong> {profile.user.email}
            </div>
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <strong>Rôle :</strong> {profile.user.role.role}
            </div>
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <strong>Organisateur :</strong>{" "}
              <span className={`inline-block px-2 py-0.5 text-xs font-semibold rounded-full
                ${profile.user.is_planner
                  ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                  : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"}`}>
                {profile.user.is_planner ? "Oui" : "Non"}
              </span>
            </div>
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <strong>Créé le :</strong> {new Date(profile.created_at).toLocaleDateString()}
            </div>
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <strong>Téléphone :</strong> {profile.user.phone_number}
            </div>
            <button
              onClick={() => {
                setSelectedUserId(profile.user.id);
                setIsRoleOpen(true);
              }}
              className="mt-2 inline-block text-blue-600 hover:text-blue-800 font-semibold text-sm"
            >
              Modifier le rôle
            </button>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <nav className="flex flex-col sm:flex-row sm:items-center justify-between mt-6 px-6" aria-label="Pagination">
        <p className="text-sm text-gray-700 dark:text-gray-300 mb-3 sm:mb-0">
          Affiche <span className="font-semibold text-gray-900 dark:text-white">
            {(currentPage - 1) * PAGE_SIZE + 1}–{Math.min(currentPage * PAGE_SIZE, total)}
          </span> sur <span className="font-semibold text-gray-900 dark:text-white">{total}</span> profils
        </p>
        <ul className="inline-flex -space-x-px text-sm h-8">
          <li>
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-l-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700 dark:hover:bg-gray-700"
            >
              Précédent
            </button>
          </li>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <li key={page}>
              <button
                onClick={() => setCurrentPage(page)}
                className={`flex items-center justify-center px-3 h-8 leading-tight border ${
                  page === currentPage
                    ? "text-blue-600 bg-blue-50 border-blue-300 dark:bg-blue-900 dark:text-blue-300"
                    : "text-gray-500 bg-white border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700 dark:hover:bg-gray-700"
                }`}
              >
                {page}
              </button>
            </li>
          ))}
          <li>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-r-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700 dark:hover:bg-gray-700"
            >
              Suivant
            </button>
          </li>
        </ul>
      </nav>

      {/* Modales */}
      <ProfilesFiltersModal
        isOpen={isFiltersOpen}
        onClose={() => setIsFiltersOpen(false)}
        onApply={(newFilters) => {
          setFilters(newFilters);
          setCurrentPage(1);
        }}
        initialFilters={filters}
      />
      <RoleModal
        isOpen={isRoleOpen}
        onClose={() => setIsRoleOpen(false)}
        user_id={selectedUserId}
        onSuccess={() => fetchProfiles(currentPage)}
      />
    </>
  );

};

export default ProfileBackOffice;
