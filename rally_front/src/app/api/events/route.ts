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

  const new_event = req.body;

  if (!new_event) {
    return NextResponse.json({ message: 'Bad request' }, { status: 422 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/events/`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: new_event,
      duplex: 'half',
    } as any
  );

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}

export async function PATCH(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get('user_access_token')?.value;

    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const event_body = req.body;

    if (!event_body) {
      return NextResponse.json({ message: 'Bad request' }, { status: 422 });
    }

    // Récupérer le slug dans les query params
    const url = new URL(req.url);
    const event_id = url.searchParams.get('event_id');

    const backendRes = await fetch(
      `${RALLY_BACK_HOST}/events/${event_id}`,
      {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: event_body,
        duplex: 'half',
    } as any
  );
    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  }


  export async function DELETE(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get('user_access_token')?.value;

    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const url = new URL(req.url);
    const event_id = url.searchParams.get('event_id');

    const backendRes = await fetch(
      `${RALLY_BACK_HOST}/events/${event_id}`,
      {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const text = await backendRes.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch (err) {
      console.error('Failed to parse JSON from backend:', text);
      return NextResponse.json(
        { error: 'Invalid JSON from backend', backendMessage: text },
        { status: 500 }
      );
    }

    return NextResponse.json(data, { status: backendRes.status });
  }

