import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;
  console.log(token)

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const url = new URL(req.url);
  const pathname = url.pathname; // e.g. "/api/profiles/abc123"
  const match = pathname.match(/\/api\/profiles\/([^/]+)/);
  const profile_id = match?.[1];

  if (!profile_id) {
    return NextResponse.json({ message: 'Missing slug parameter' }, { status: 400 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/profiles/${profile_id}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}
