// app/lib/getUserFromCookies.ts (server-side)
import { cookies } from "next/headers";

export default async function getCookies() {
  const cookieStore = await cookies();
  const token = cookieStore.get("user_access_token")?.value;
  return token;
}
