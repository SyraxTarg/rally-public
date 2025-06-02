
"use server";


import { fetchApi } from "@/app/server_components/api_python";
import { revalidatePath } from "next/cache";
export async function deleteReportComment(report_id: number, ban: boolean){


    await fetchApi(`/signaledComments/${report_id}?ban=${ban}`, "DELETE");
    revalidatePath("/admin/signalements");
}