import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get('user_access_token')?.value;

    if (!token) {
      return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const url = new URL(req.url);
    const offset = url.searchParams.get('offset');
    const limit = url.searchParams.get('limit');

    const backendRes = await fetch(
      `${RALLY_BACK_HOST}/payments?offset=${offset}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        }
        }
    );

    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  }
