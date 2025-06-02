import { fetchTypesApi } from "@/app/server_components/api";

export async function fetchTypes(){
    try {
        const res = fetchTypesApi();
        if (!res.ok) {
            console.error("Échec du chargement des données");
            return;
        }
        return res
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}