"use client";

import { useState, useEffect } from "react";
import { updateProfile } from "../../profiles/me/server_components/update_profile";
import { useUser } from "../../context/auth_context";
import { uploadPhoto } from "@/app/events/new/server_components/upload_photo";
import { useCookies } from "react-cookie";
import { toast } from "react-toastify";
import { useRouter } from "next/navigation";

type UpdateProfileModalProps = {
  isOpen: boolean;
  onClose: () => void;
};

export default function UpdateProfileModal({ isOpen, onClose }: UpdateProfileModalProps) {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [phone, setPhone] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [photo, setPhoto] = useState<File | null>(null);
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const router = useRouter();
  const { user, refetchUser } = useUser();
  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      let uploadedPhotoUrl = "/default.jpg";
      if (photo) {
        uploadedPhotoUrl = await uploadPhoto(photo, cookies.user_access_token);
      }
      await updateProfile(first_name, last_name, phone, uploadedPhotoUrl, cookies.user_access_token);
      await refetchUser();
      router.refresh();
      toast.success("Profil modifié");
      onClose();
    } catch (error) {
      setErrorMessage("Erreur lors de la mise à jour du profil.");
      console.error(error);
      toast.error(`Erreur lors de la modification`)
    }
  };

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setPhoto(e.target.files[0]);
    }
  };

  const removeSelectedImage = () => {
    setPhoto(null);
  };

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }, [isOpen]);

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name || "");
      setLastName(user.last_name || "");
      setPhone(user.user.phone_number || "");
      setPhotoUrl(user.photo || null);
    }
  }, [user]);


  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center">
      <div className="w-full max-w-sm sm:max-w-md max-h-[90vh] overflow-y-auto bg-white rounded-xl shadow-xl p-6 m-4">
        <h2 className="text-xl font-bold text-center text-[#123c69] mb-6">
          Modifier mon profil
        </h2>

        {(photo || photoUrl) && (
          <div className="mt-4 flex flex-col items-center gap-3 border border-gray-300 rounded-md bg-gray-50 p-4">
            <div className="relative w-40 h-40">
              <img
                src={photo ? URL.createObjectURL(photo) : photoUrl!}
                alt="Preview"
                className="w-40 h-40 object-cover rounded-full shadow-md"
              />
              {photo && (
                <button
                  onClick={removeSelectedImage}
                  className="absolute top-1 right-1 bg-black/60 hover:bg-black/80 text-white rounded-full p-1 text-xs"
                  aria-label="Supprimer l'image"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
        )}
          <form onSubmit={handleSubmit} className="space-y-4 mt-4">
            <div>
              <label htmlFor="picture" className="block text-sm font-medium text-gray-700">
                Photo de profil
              </label>
              <input
                id="picture"
                name="picture"
                type="file"
                onChange={handleFile}
                className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">
                Prénom
              </label>
              <input
                id="firstName"
                name="firstName"
                type="text"
                value={first_name}
                required
                onChange={(e) => setFirstName(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                Nom
              </label>
              <input
                id="last_name"
                name="last_name"
                type="text"
                value={last_name}
                required
                onChange={(e) => setLastName(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 text-sm"
              />
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                N° de téléphone
              </label>
              <input
                id="phone"
                name="phone"
                type="tel"
                value={phone}
                required
                onChange={(e) => setPhone(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 text-sm"
              />
            </div>

            {errorMessage && (
              <p className="text-sm text-red-600">{errorMessage}</p>
            )}

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded border hover:bg-gray-100"
              >
                Annuler
              </button>
              <button
                type="submit"
                className="px-4 py-2 rounded bg-[#123c69] text-white hover:bg-[#0f2f54] transition-colors"
              >
                Modifier
              </button>
            </div>
          </form>
        </div>
      </div>
  );
}
