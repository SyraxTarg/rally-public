import { NextRequest, NextResponse } from 'next/server'
import { verifyJwt } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  console.log("⛳ Middleware called for:", request.nextUrl.pathname);
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('user_access_token')?.value;

  if (!token) {
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  const user = await verifyJwt(token);

  if (!user) {
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  // 🔐 Protéger certaines pages
  if (
    pathname.startsWith("/events/new") ||
    pathname.startsWith("/profiles/me")
  ) {
    // Si on arrive ici, on est déjà authentifié donc pas besoin de revérifier
    return NextResponse.next();
  }

  // 🔐 Vérifie rôle pour les routes super admin
  if (pathname.startsWith("/admin/super-admin")) {
    const hasAccess = user?.role?.role === "ROLE_SUPER_ADMIN";
    if (!hasAccess) {
      return NextResponse.redirect(new URL('/', request.url));
    }
  }

  if (pathname.startsWith("/admin")) {
    const hasAccess = user?.role?.role === "ROLE_ADMIN" || user?.role?.role === "ROLE_SUPER_ADMIN";
    if (!hasAccess) {
      return NextResponse.redirect(new URL('/', request.url));
    }
  }

  // ✅ Si tout est ok
  return NextResponse.next();
}

// Important : ajouter les routes que tu veux surveiller
export const config = {
  matcher: [
    '/admin/:path*',
    '/admin/super-admin/:path*',
    '/events/new',
    '/profiles/me',
  ],
}

