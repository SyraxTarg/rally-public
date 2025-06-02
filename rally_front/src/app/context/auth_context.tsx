// src/app/context/auth_context.tsx
"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useCookies } from "react-cookie";
import { fetchMeApi } from '../server_components/api';

type Profile = {
  id: number;
  first_name: string;
  last_name: string;
  photo: string;
  nb_like: number;
  user: {
    id: number;
    email: string;
    phone_number: string;
    is_planner: boolean;
    account_id: string | null;
    role: {
      id: number;
      role: string;
    }
  };
  created_at: Date;
  updated_at: Date;
};

type UserContextType = {
  user: Profile | null;
  refetchUser: () => Promise<void>;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Profile | null>(null);
  const [cookies] = useCookies(['user_access_token']);
  console.log("Cookies disponibles:", cookies);
  console.log("Access token trouvé:", cookies.user_access_token);
  

  const fetchUser = async () => {
    try {
      const res = await fetchMeApi();
      if (res && res.ok) {
        const data = await res.json();
        console.log(data)
        setUser(data);
      } else {
        console.warn("fetchMeApi error:", res?.status);
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user:", error);
      setUser(null);
    }
  };
  

  useEffect(() => {
      fetchUser();
  }, []);

  return (
    <UserContext.Provider value={{ user, refetchUser: fetchUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within a UserProvider");
  return context;
}
