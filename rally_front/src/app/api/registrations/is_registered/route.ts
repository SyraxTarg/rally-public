// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  // Récupérer le slug dans les query params
  const url = new URL(req.url);
  const event_id = url.searchParams.get('event_id');

  if (!event_id) {
    return NextResponse.json({ message: 'Missing slug parameter' }, { status: 400 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/registrations/is-registered?event_id=${event_id}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    }
  );

  const data = await backendRes.json();
  console.log("is registered", data);
  
  return NextResponse.json(data, { status: backendRes.status });
  
}
