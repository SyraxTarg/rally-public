"use client";
import { useState, useCallback, useEffect } from "react";
import { useRouter } from 'next/navigation';
import {Select, SelectItem} from "@heroui/select";
import { createEvent } from "../../events/new/server_components/create_new_event";
import { Textarea } from "@heroui/input";
import { uploadPhoto } from "@/app/events/new/server_components/upload_photo";
import { fetchTypesApi } from "@/app/server_components/api";
import { useCookies } from "react-cookie";
import { toast } from "react-toastify";
import { useUser } from "@/app/context/auth_context";


type EventType = {
    id: number;
    type: string;
};

export default function NewEventForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [places, setPlaces] = useState(0);
  const [price, setPrice] = useState(0.0);
  const [eventTypes, setEventTypes] = useState<EventType[]>([])
  const [date, setDate] = useState("");
  const [clotureBillets, setClotureBillets] = useState("");
  const [types, setTypes] = useState<number[]>([]);
  const [photos, setPhotos] = useState<File[]>([]);
  const [address, setAddress] = useState({
    city: "",
    zipcode: "",
    number: "",
    street: "",
    country: ""
  });
  console.log(types, date, clotureBillets);
  const [errorMessage, setErrorMessage] = useState("");
  const router = useRouter();
  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);
  const user = useUser().user;


  const getTypes = useCallback(async () => {
    const types = await fetchTypesApi()
    const data = await types.json()
    setEventTypes(data.data)
  }, []);

  useEffect(() => {
    getTypes();
  }, [getTypes]);

  if (errorMessage){
    toast.error(errorMessage);
  }
  // Mise à jour des champs d'adresse
  const handleAddressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setAddress(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const uploadedUrls: string[] = [];

      for (const photo of photos) {
        const url = await uploadPhoto(photo, cookies.user_access_token);
        uploadedUrls.push(url);
      }

      const new_event = await createEvent({
        titre: title,
        description,
        date,
        cloture_billets: clotureBillets,
        types,
        country: address.country,
        city: address.city,
        zipcode: address.zipcode,
        number: address.number,
        street: address.street,
        price,
        nb_places: places,
        photos: uploadedUrls,
        token: cookies.user_access_token
      });

      router.push(`/events/${new_event}`);
      toast.success("Evenement créé avec succès");
    } catch (error) {
      setErrorMessage("Erreur lors de la création de l'événement.");
      console.error(error);
      toast.error(`Erreur lors de la création de l'évènement : ${errorMessage}`)
    }
  };

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;
    const newFiles = Array.from(files);
    setPhotos(newFiles);
  };

  const removeSelectedImage = (index: number) => {
    setPhotos(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <>
      <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4 py-12 sm:px-6 lg:px-8">
      {errorMessage && (
        <p className="text-red-500 text-sm">{errorMessage}</p>
      )}

        <div className="w-full max-w-md bg-white rounded-lg shadow-lg">
          <div className="w-full bg-[#123c69] text-[#edc7b7] text-center py-4 rounded-t-lg">
            <h2 className="text-2xl font-bold">Ajouter un évènement</h2>
          </div>
          <div className="pb-8 pl-8 pr-8">
            <form action="#" method="POST" className="mt-8 space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-4">
              {photos && (
                <div className="mt-4 max-h-48 overflow-x-auto overflow-y-hidden border border-gray-300 rounded-md bg-gray-50 p-2">
                  <div className="flex flex-row items-start gap-3">
                    {photos.map((photo, index) => (
                      <div key={index} className="relative flex-shrink-0 w-32 h-32">
                        <img
                          src={URL.createObjectURL(photo)}
                          alt="Preview"
                          className="w-full h-full object-cover rounded-md shadow-md"
                        />
                        <button
                          type="button"
                          onClick={() => removeSelectedImage(index)}
                          className="absolute top-1 right-1 bg-black/60 hover:bg-black/80 text-white rounded-full p-1 text-xs"
                          aria-label="Supprimer l'image"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

              )}


                <div>
                  <label htmlFor="pictures" className="block text-sm font-medium text-gray-700">Photos</label>
                  <input
                    id="pictures"
                    name="pictures"
                    type="file"
                    multiple
                    onChange={(e) => handleFile(e)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">Titre</label>
                  <input
                    id="title"
                    name="title"
                    type="text"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">Description</label>
                    <Textarea
                        placeholder="Décrivez votre évènement"
                        variant="bordered"
                        id="description"
                        name="description"
                        required
                        onChange={(e) => setDescription(e.target.value)}
                        disableAnimation
                        maxRows={4}
                        classNames={{
                            base: "w-full",
                            inputWrapper:
                            "w-full min-h-[120px] resize-none overflow-y-auto rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500",
                            input: "text-gray-900 px-3 py-2 text-sm",
                            label: "text-sm font-medium text-gray-700 mb-1",
                        }}
                    />

                </div>

                <div>
                  <label htmlFor="places" className="block text-sm font-medium text-gray-700">Places</label>
                  <input
                    id="places"
                    name="places"
                    type="number"
                    required
                    onChange={(e) => setPlaces(e.target.valueAsNumber)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label htmlFor="price" className="block text-sm font-medium text-gray-700">Prix</label>
                  <input
                    id="price"
                    name="price"
                    type="number"
                    step="0.01"
                    min="0"
                    disabled={!user || !user.user.account_id}
                    value={!user || !user.user.account_id ? 0 : price}
                    required
                    onChange={(e) => setPrice(e.target.valueAsNumber || 0)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                {/* Champs dates */}
                <div>
                  <label htmlFor="date" className="block text-sm font-medium text-gray-700">Date de l'événement</label>
                  <input
                    id="date"
                    name="date"
                    type="date"
                    required
                    onChange={(e) => setDate(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label htmlFor="clotureBillets" className="block text-sm font-medium text-gray-700">Date de clôture des billets</label>
                  <input
                    id="clotureBillets"
                    name="clotureBillets"
                    type="date"
                    required
                    onChange={(e) => setClotureBillets(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>

                {/* Types - Select */}
                <div className="flex w-full max-w-xs flex-col gap-2">
                    <Select
                        className="max-w-xs"
                        aria-label="Sélectionnez des types"
                        placeholder="Sélectionnez des types"
                        selectionMode="multiple"
                        selectedKeys={new Set(types.map(String))}
                        onSelectionChange={(selectedKeys: Set<string>) => {
                            const selectedIds = Array.from(selectedKeys).map(Number);
                            setTypes(selectedIds);
                        }}
                        >
                        {eventTypes.map((type) => (
                            <SelectItem key={type.id} value={type.id.toString()} aria-label={type.type}>
                            {type.type}
                            </SelectItem>
                        ))}
                    </Select>

                </div>

                {/* Address */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Adresse</label>
                  <input
                    name="number"
                    type="text"
                    placeholder="Numéro"
                    value={address.number}
                    onChange={handleAddressChange}
                    className="mb-2 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <input
                    name="street"
                    type="text"
                    placeholder="Rue"
                    value={address.street}
                    onChange={handleAddressChange}
                    className="mb-2 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <input
                    name="city"
                    type="text"
                    placeholder="Ville"
                    value={address.city}
                    onChange={handleAddressChange}
                    className="mb-2 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <input
                    name="zipcode"
                    type="text"
                    placeholder="Code postal"
                    value={address.zipcode}
                    onChange={handleAddressChange}
                    className="mb-2 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <input
                    name="country"
                    type="text"
                    placeholder="Pays"
                    value={address.country}
                    onChange={handleAddressChange}
                    className="block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <button className="w-full py-2 px-4 bg-[#123c69] text-[#edc7b7] rounded-md hover:bg-[#0f2a4a] transition">
                Ajouter
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
