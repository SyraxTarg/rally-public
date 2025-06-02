// src/app/api/profiles/me/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST!;

export async function GET(req: NextRequest) {
    const cookieStore = await cookies();
    const token = cookieStore.get("user_access_token")?.value;

    if (!token) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
    }

    const url = new URL(req.url);
    const searchParams = url.searchParams;

    // Reprise des paramètres de pagination
    const offset = searchParams.get("offset");
    const limit = searchParams.get("limit");

    // Reconstruction de l’URL avec tous les filtres autorisés
    const backendUrl = new URL(`${RALLY_BACK_HOST}/super-admin/payments`);
    backendUrl.searchParams.set("offset", offset ?? "0");
    backendUrl.searchParams.set("limit", limit ?? "10");

    // Liste des filtres autorisés à propager
    const filterKeys = [
      "event_title",
      "buyer_email",
      "organizer_email",
      "amount_min",
      "amount_max",
      "fee_min",
      "fee_max",
      "brut_amount_min",
      "brut_amount_max",
      "stripe_session_id",
      "stripe_payment_intent_id",
      "status",
      "date_apres",
      "date_avant",
    ];

    for (const key of filterKeys) {
      const value = searchParams.get(key);
      if (value !== null) {
        backendUrl.searchParams.set(key, value);
      }
    }

    const backendRes = await fetch(backendUrl.toString(), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(backendUrl.toString());

    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  }
