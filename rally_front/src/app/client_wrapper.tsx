// components/ClientWrapper.tsx
"use client";

import { CookiesProvider } from 'react-cookie';

export default function ClientWrapper({ children }: { children: React.ReactNode }) {
  return (
    <CookiesProvider>
      {children}
    </CookiesProvider>
  );
}
