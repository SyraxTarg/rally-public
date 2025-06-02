"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchProfileApi, grantRoleApi } from "@/app/server_components/api";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  user_id: number;
  onSuccess?: () => void;
};

export interface Profile {
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
    role: {
      id: number;
      role: string;
    };
  };
  created_at: string;
  updated_at: string;
}

const Roles = [
  { name: "Utilisateur", value: "ROLE_USER" },
  { name: "Administrateur", value: "ROLE_ADMIN" },
  { name: "Super-administrateur", value: "ROLE_SUPER_ADMIN" },
];

export default function RoleModal({ isOpen, onClose, user_id, onSuccess }: Props) {
  const [selectedRole, setSelectedRole] = useState<string>("");
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);

  const getProfile = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetchProfileApi(user_id);
      const profile = await response?.json();
      setProfile(profile);
      setSelectedRole(profile.user.role.role);
    } catch (err) {
      console.error("Erreur lors du chargement du profil :", err);
    } finally {
      setLoading(false);
    }
  }, [user_id]);

  const handleRoleChange = async () => {
    try {
      setSaving(true);
      await grantRoleApi(user_id, selectedRole);
      if (onSuccess) onSuccess(); // <-- Rafraîchir la liste après succès
      onClose(); // Ferme la modale
    } catch (err) {
      console.error("Erreur lors de la mise à jour du rôle :", err);
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      getProfile();
    }
  }, [getProfile, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4 py-6">
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

        <div className="relative z-50 w-full max-w-md bg-white rounded-xl shadow-xl p-6 max-h-[90vh] overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6 border-b border-gray-200 pb-3">
            Modifier le rôle de l’utilisateur {profile?.user.email}
        </h2>

        {loading ? (
            <p className="text-center text-gray-500">Chargement du profil...</p>
        ) : profile ? (
            <>
            <div className="mb-6">
                <label
                htmlFor="roles"
                className="block text-sm font-semibold text-gray-700 mb-2"
                >
                Rôle actuel
                </label>
                <select
                name="roles"
                id="roles"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="block w-full rounded-md border border-gray-300 px-4 py-3 text-gray-900 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                >
                <option value="" disabled>
                    -- Sélectionnez un rôle --
                </option>
                {Roles.map((role) => (
                    <option key={role.value} value={role.value}>
                    {role.name}
                    </option>
                ))}
                </select>
            </div>

            <div className="flex justify-end gap-4">
                <button
                onClick={onClose}
                disabled={saving}
                className="px-5 py-3 rounded-lg bg-gray-100 text-gray-700 font-semibold hover:bg-gray-200 transition disabled:opacity-50"
                >
                Annuler
                </button>
                <button
                onClick={handleRoleChange}
                disabled={saving || selectedRole === ""}
                className="px-5 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50"
                >
                {saving ? "Enregistrement..." : "Enregistrer"}
                </button>
            </div>
            </>
        ) : (
            <p className="text-center text-red-500">Profil introuvable.</p>
        )}
        </div>

    </div>
  );
}
