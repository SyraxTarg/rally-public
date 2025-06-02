import { fetchMyEventsApi } from "@/app/server_components/api";
export async function fetchMyEvents(user_id: number, currentPage: number, limit: number, token: string){
    try {
        const offset = (currentPage - 1) * limit;
        const data = await fetchMyEventsApi(user_id, offset, limit, token);

        return {
            data: data.data,
            totalPagesEvents: Math.ceil(data.total / limit),
          };
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}