
"use server";


import { fetchApi } from "@/app/server_components/api_python";
import { revalidatePath } from "next/cache";
export async function updateProfile(first_name: string, last_name: string, phone_number: string, photo: string, token: string){
    const data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "photo": photo
    };

    await fetchApi("/profiles", "PATCH", JSON.stringify(data));
    revalidatePath("/profiles/me_copy");
}
