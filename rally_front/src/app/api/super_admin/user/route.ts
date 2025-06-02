import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const url = new URL(req.url);

    // Reprise des paramètres de pagination
  const user_id = url.searchParams.get("user_id");
  const role = url.searchParams.get("role");
  if (!user_id || !role) {
    return NextResponse.json({ message: 'Missing user id or role' }, { status: 422 });
  }


  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/super-admin/user/${user_id}?role=${role}`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      duplex: 'half',
    } as any
  );
  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}
