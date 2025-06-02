// src/app/api/auth/login/route.ts
import { NextRequest, NextResponse } from 'next/server';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {

      // Récupérer le slug dans les query params
  const url = new URL(req.url);
  const email = url.searchParams.get('user_email');

  const backendRes = await fetch(`${RALLY_BACK_HOST}/authent/send-token?user_email=${email}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
  });

  const data = await backendRes.json();
  console.log(data)

  const res = NextResponse.json(data, { status: backendRes.status });

  if (!backendRes.ok) {
    return res;
  }

  console.log(backendRes)

  return res;
}
