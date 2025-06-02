import { newEventApi } from "@/app/server_components/api";

const NEXT_PUBLIC_RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST;

interface CreateEventProp{
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
    token: string
}
export async function createEvent(
    {
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
        photos,
        token
    }: CreateEventProp){
    try {

        const new_event = {
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

          console.log(new_event);

        const res = await newEventApi(JSON.stringify(new_event), token);

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
