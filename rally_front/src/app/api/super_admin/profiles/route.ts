import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';


const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get("user_access_token")?.value;


    if (!token) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
    }

    const url = new URL(req.url);
    const limit = url.searchParams.get("limit");
    const offset = url.searchParams.get("offset");
    const nb_like = url.searchParams.get("nb_like");
    const is_planner = url.searchParams.get("is_planner");
    const role = url.searchParams.get("role");
    const search = url.searchParams.get("search");

    const backendUrl = new URL(`${RALLY_BACK_HOST}/super-admin/profiles`);
    backendUrl.searchParams.set("limit", limit ?? "10");
    backendUrl.searchParams.set("offset", offset ?? "0");
    if (nb_like) backendUrl.searchParams.set("nb_like", nb_like);
    if (is_planner) backendUrl.searchParams.set("is_planner", is_planner);
    if (role) backendUrl.searchParams.set("role", role);
    if (search) backendUrl.searchParams.set("search", search);

    const backendRes = await fetch(backendUrl.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        authorization: `bearer ${token}`,
      },
    });

    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  }
