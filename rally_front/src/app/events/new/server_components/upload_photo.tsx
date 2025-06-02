import { uploadPictureApi } from "@/app/server_components/api";

export async function uploadPhoto(file: File, token: string): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);

    const res = await uploadPictureApi(formData, token)

    return res.url;
  }
