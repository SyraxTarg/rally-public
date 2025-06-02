// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET() {
  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/types`,
    {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}
