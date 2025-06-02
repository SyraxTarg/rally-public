// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
    // Récupérer le slug dans les query params
   const url = new URL(req.url);
   const event_id = url.searchParams.get('event_id');

   if (!event_id) {
    return NextResponse.json({ message: 'Missing slug event_id' }, { status: 422 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/comments/events/${event_id}`,
    {
      method: 'GET',
      headers: {
        "Content-Type": "application/json"
      },
    }
  );


  const data = await backendRes.json();
  console.log("comments", data)
  return NextResponse.json(data, { status: backendRes.status });
}
