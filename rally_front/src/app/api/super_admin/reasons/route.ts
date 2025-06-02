import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const new_reason = req.body;

  if (!new_reason) {
    return NextResponse.json({ message: 'Bad request' }, { status: 422 });
  }


  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/super-admin/reasons`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: new_reason,
      duplex: 'half',
    } as any
  );
  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}
