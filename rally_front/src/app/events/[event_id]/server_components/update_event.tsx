
import { updateEventApi } from "@/app/server_components/api";
interface CreateEventProp{
    event_id: number;
    titre: string;
    description: string;
    date: string;
    cloture_billets: string;
    types: number[];
    country: string;
    city: string;
    zipcode: string;
    number: string;
    street: string;
    price: number;
    nb_places: number;
    photos: string[];
}
export async function updateEvent(
    {
        event_id,
        titre,
        description,
        date,
        cloture_billets,
        types,
        country,
        city,
        zipcode,
        number,
        street,
        price,
        nb_places,
        photos
    }: CreateEventProp){
    try {

        const event_to_update = {
            title: titre,
            description: description,
            nb_places: nb_places,
            price: price,
            date: date,
            cloture_billets: cloture_billets,
            types: {
              types: types
            },
            address: {
              city: city,
              zipcode: zipcode,
              number: number,
              street: street,
              country: country
            },
            pictures: photos.map((photo) => ({ photo }))
          };


        const res = await updateEventApi(event_id, JSON.stringify(event_to_update));

        if (!res.ok) {
            console.log(res)
            console.error("Échec du chargement des données");
            return;
        }

        const data = await res.json();
        return data.id;
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}
