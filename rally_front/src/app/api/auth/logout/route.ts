// src/app/api/auth/login/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  const backendRes = await fetch(`${RALLY_BACK_HOST}/authent/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      authorization: `bearer ${token}`
     },
  });

  const data = await backendRes.json();

  const res = NextResponse.json(data, { status: backendRes.status });

  if (!backendRes.ok) {
    return res;
  }

  console.log(backendRes)


  res.cookies.delete('user_access_token');

  res.cookies.delete('user_refresh_token');

  res.cookies.delete('user_connected_id');

  return res;
}
