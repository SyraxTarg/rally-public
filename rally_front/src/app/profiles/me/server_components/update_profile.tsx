import { updateProfileApi } from "@/app/server_components/api";
export async function updateProfile(first_name: string, last_name: string, phone_number: string, photo: string, token: string){
    const data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "photo": photo
    };

    try {
        const response = await updateProfileApi(JSON.stringify(data), token);
        return response;


    } catch (error) {
      console.error(error);
    }
}
