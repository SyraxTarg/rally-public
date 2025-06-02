import { fetchMyRgistrationsApi } from "@/app/server_components/api";
export async function fetchMyRegistrations(currentPage: number, limit: number, token: string){
    try {
        const offset = (currentPage - 1) * limit;
        const res = await fetchMyRgistrationsApi(offset, limit, token)
        return {
            data: res.data,
            totalPagesRegistrations: Math.ceil(res.total / limit),
          };
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}