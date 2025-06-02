import { NextRequest, NextResponse } from 'next/server';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const new_user = req.body;

  if (!new_user) {
    return NextResponse.json({ message: 'Bad request' }, { status: 422 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/authent/register/user`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: new_user,
      duplex: 'half',
  } as any
  );
  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}
