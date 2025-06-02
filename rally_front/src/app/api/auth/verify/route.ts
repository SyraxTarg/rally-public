// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { headers } from 'next/headers'

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
    const headersList = await headers()
    const token = headersList.get('authorization')

    console.log("TOKENTO ", token);

    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const backendRes = await fetch(
      `${RALLY_BACK_HOST}/authent/verify`,
      {
        method: 'POST',
        headers: {
          Authorization: token,
        }
        }
    );
    const data = await backendRes.json();
    console.log("USER ", backendRes);
    return NextResponse.json(data, { status: backendRes.status });
  }
