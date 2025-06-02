import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function POST(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const new_comment = req.body;

  if (!new_comment) {
    return NextResponse.json({ message: 'Bad request' }, { status: 422 });
  }

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/comments/`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: new_comment,
      duplex: 'half',
    } as any
  );


  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}


export async function DELETE(req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const url = new URL(req.url);
  const comment_id = url.searchParams.get('comment_id');

  const backendRes = await fetch(
    `${RALLY_BACK_HOST}/comments/${comment_id}`,
    {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );


  const data = await backendRes.json();
  return NextResponse.json(data, { status: backendRes.status });
}

