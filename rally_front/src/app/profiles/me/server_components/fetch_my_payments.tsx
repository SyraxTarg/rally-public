import { fetchMyPaymentsApi } from "@/app/server_components/api";
export async function fetchMyPayments(currentPage: number, limit: number){
    try {
        const offset = (currentPage - 1) * limit;
        const res = await fetchMyPaymentsApi(offset, limit)
        return {
            data: res.data,
            totalPagesRegistrations: Math.ceil(res.total / limit),
          };
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}