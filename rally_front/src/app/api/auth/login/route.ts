// src/app/api/auth/login/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { email, password } = body;

  const backendRes = await fetch(`${RALLY_BACK_HOST}/authent/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  const data = await backendRes.json();
  console.log(data)

  const res = NextResponse.json(data, { status: backendRes.status });

  if (!backendRes.ok) {
    return res;
  }

  console.log(backendRes)


  res.cookies.set('user_access_token', data.access_token, {
    httpOnly: true,
    secure: false,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60, // 1 heure
  });

  res.cookies.set('user_refresh_token', data.refresh_token, {
    httpOnly: true,
    secure: false,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60, // 1 heure
  });


  res.cookies.set('user_connected_id', data.user_id, {
    httpOnly: true,
    secure: false,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60, // 1 heure
  });

  return res;
}
