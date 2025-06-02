"use client";

import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@heroui/dropdown";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useDisclosure } from "@heroui/modal";
import LogoutModal from "./logout_modal";
import { useUser } from '../context/auth_context';
import { toast } from "react-toastify";
import { logoutApi } from "../server_components/api";
import { useCookies } from "react-cookie";
import Avatar from "./avatar";


export default function MyProfile({ photo, email }: { photo: string, email: string }) {
  const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const router = useRouter();
  const { refetchUser } = useUser();

  const logout = async () => {
    try {
      await logoutApi(cookies.user_access_token);
      await refetchUser();
      router.push(`/`);
      onClose();
      toast.success("Déconnexion réussie");
    } catch (error) {
      console.error("Erreur lors du logout:", error);
    }
  };

  return (
    <>
      <Dropdown>
      <DropdownTrigger>
        <button type="button">
          <Avatar src={photo} alt={`Avatar de ${email}`} />
        </button>
      </DropdownTrigger>

        <DropdownMenu
          aria-label="Menu du profil"
          className="bg-white shadow-lg rounded-lg px-2 py-2 w-48"
        >
          <DropdownItem
            key="my_profile"
            className="hover:bg-gray-100 rounded-md px-2 py-1"
          >
            <Link
              href="/profiles/me"
              className="block text-gray-800 hover:text-blue-600"
            >
              Mon profil
            </Link>
          </DropdownItem>
          <DropdownItem
            key="logout"
            className="hover:bg-red-50 rounded-md px-2 py-1"
          >
            <button
              className="block text-red-600 hover:text-red-700"
              onClick={onOpen}
            >
              Déconnexion
            </button>
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
      <LogoutModal isOpen={isOpen} onClose={onClose} onLogout={logout} />
    </>
  );
}
