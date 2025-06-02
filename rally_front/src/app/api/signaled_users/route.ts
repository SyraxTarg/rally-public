import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  let signalement_body;
  try {
    signalement_body = await req.json();
  } catch (error) {
    return NextResponse.json({ message: 'Bad request: invalid JSON' }, { status: 400 });
  }

  const backendRes = await fetch(`${RALLY_BACK_HOST}/signaledUsers`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(signalement_body),
  });

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}


export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get('user_access_token')?.value;

    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const url = new URL(req.url);
    const offset = url.searchParams.get('offset');
    const limit = url.searchParams.get('limit');
    const date = url.searchParams.get('date');
    const signaled_by_user = url.searchParams.get('signaled_by_user');
    const reason_id = url.searchParams.get('reason_id');
    const user_signaled = url.searchParams.get('user_signaled');

    const backendUrl = new URL(`${RALLY_BACK_HOST}/signaledUsers`);
    backendUrl.searchParams.set("limit", limit ?? "10");
    backendUrl.searchParams.set("offset", offset ?? "0");
    if (date) backendUrl.searchParams.set("date", date);
    if (signaled_by_user) backendUrl.searchParams.set("email_user", signaled_by_user);
    if (reason_id) backendUrl.searchParams.set("reason_id", reason_id);
    if (user_signaled) backendUrl.searchParams.set("email_signaled_user", user_signaled);

    const backendRes = await fetch(backendUrl.toString(), {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

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
  const user_id = url.searchParams.get('user_id');
  const ban = url.searchParams.get('ban');


  const backendRes = await fetch(`${RALLY_BACK_HOST}/signaledUsers/${user_id}?ban=${ban}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
    }
  });

  const text = await backendRes.text();

  return NextResponse.json(text, { status: backendRes.status });
}
