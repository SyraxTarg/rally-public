import { fetchProfileEventsApi } from "@/app/server_components/api";
export async function fetchProfileEvents(profile_id: number, currentPage: number, limit: number, token: string){
    try {
        const offset = (currentPage - 1) * limit;
        const res = await fetchProfileEventsApi(offset, limit, profile_id, token)

        // const data = await res.json();
        return res;
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}
