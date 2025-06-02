'use client';

import Link from "next/link";
import { useSelectedLayoutSegments } from "next/navigation";
import { useUser } from "@/app/context/auth_context";

export default function SideMenu() {
  const segments = useSelectedLayoutSegments();
  const user = useUser().user;
  const currentSegment = segments[segments.length - 1] || "";

  const navLinks = [
    { name: "Signalements", href: "/admin/signalements", segment: "signalements" },
  ];

  if (user?.user.role.role == "ROLE_SUPER_ADMIN"){
    navLinks.push(
      { name: "Profiles", href: "/admin/super-admin/profiles", segment: "profiles" },
    { name: "Logs", href: "/admin/super-admin/action-logs", segment: "action-logs" },
    { name: "Paiements", href: "/admin/super-admin/payments", segment: "payments" },
    { name: "Tables", href: "/admin/super-admin/tables", segment: "tables" },
    )
  }


  return (
    <aside
      id="default-sidebar"
      className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0 bg-gray-50 dark:bg-gray-800 pt-16"
      aria-label="Sidebar"
    >
      <nav className="h-full px-3 py-4 overflow-y-auto">
        <ul className="space-y-2 font-medium">
          {navLinks.map((link) => {
            const isActive = currentSegment === link.segment;
            return (
              <li key={link.name}>
                <Link
                  href={link.href}
                  className={`block px-4 py-2 rounded-md text-sm transition-colors duration-200 ${
                    isActive
                      ? "bg-blue-100 text-blue-700 font-semibold dark:bg-blue-900 dark:text-blue-300"
                      : "text-gray-700 hover:bg-gray-200 hover:text-blue-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-blue-400"
                  }`}
                >
                  {link.name}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
