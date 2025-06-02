import { fetchProfileApi } from "@/app/server_components/api";
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
    };
    created_at: string;
    updated_at: string;
  }


export async function fetchProfile(profile_id: number, token: string){
    try {
        const res = await fetchProfileApi(profile_id, token)
        console.log(`RES ${res}`)

        if (!res.ok) {
            console.error("Échec du chargement des données");
            return;
        }

        const data = await res.json();
        return data;
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}