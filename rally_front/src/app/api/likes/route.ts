// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
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
    `${RALLY_BACK_HOST}/likes/${event_id}`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}


export async function DELETE(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;
  console.log(`LIKED ${token}`);

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
    `${RALLY_BACK_HOST}/likes/${event_id}`,
    {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}

