"use client";

import Link from "next/link";
import MyProfile from "./my_profile";
import { useUser } from "../context/auth_context";

import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { useState } from "react";

export default function Navbar() {
  const { user } = useUser();
  const [currentPage, setCurrentPage] = useState(1);

  const navLinks = [
    { name: "Accueil", href: "/", page: 1 },
    { name: "Évènements", href: "/events", page: 2 },
  ];

  return (
    <Disclosure
      as="nav"
      className="bg-white shadow top-0 left-0 right-0 z-50 fixed h-16"
    >
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="relative flex h-16 items-center sm:justify-between">

              {/* Mobile: Menu button on the left */}
              <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                <DisclosureButton className="inline-flex items-center justify-center rounded-md p-2 text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </DisclosureButton>
              </div>

              {/* Logo: centered on mobile, left on desktop */}
              <div className="flex-1 flex justify-center sm:justify-start">
                <Link
                  href="/"
                  className="text-blue-600 font-bold text-xl"
                  onClick={() => setCurrentPage(1)}
                >
                  Rally
                </Link>
              </div>

              {/* Desktop navigation links */}
              <div className="hidden sm:flex sm:space-x-4 ml-6">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setCurrentPage(link.page)}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentPage === link.page
                      ? "text-blue-600 font-semibold"
                      : "text-gray-700 hover:text-blue-600"
                  }`}
                >
                  {link.name}
                </Link>
              ))}

              {user && (
                <Link
                  href="/events/new"
                  onClick={() => setCurrentPage(3)}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentPage === 3
                      ? "text-blue-600 font-semibold"
                      : "text-gray-700 hover:text-blue-600"
                  }`}
                >
                  Ajouter un évènement
                </Link>
              )}

                {!user && (
                  <Link
                    href="/auth/login"
                    onClick={() => setCurrentPage(4)}
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      currentPage === 4
                        ? "text-blue-600 font-semibold"
                        : "text-gray-700 hover:text-blue-600"
                    }`}
                  >
                    Connexion
                  </Link>
                )}
              </div>

              {/* Profile: right side on all screen sizes */}
              <div className="absolute inset-y-0 right-0 flex items-center sm:static sm:ml-auto">
                {user && <MyProfile photo={user.photo} email={user.user.email} />}
              </div>
            </div>
          </div>

          {/* Mobile menu panel */}
          <DisclosurePanel className="sm:hidden bg-white border-t border-gray-200 shadow-md">
            <div className="space-y-1 px-2 pt-2 pb-3">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setCurrentPage(link.page)}
                  className={`block px-3 py-2 rounded-md text-base font-medium ${
                    currentPage === link.page
                      ? "text-blue-600 font-semibold"
                      : "text-gray-700 hover:text-blue-600"
                  }`}
                >
                  {link.name}
                </Link>
              ))}
              {user && (
                <Link
                  href="/events/new"
                  onClick={() => setCurrentPage(3)}
                  className={`block px-3 py-2 rounded-md text-base font-medium ${
                    currentPage === 3
                      ? "text-blue-600 font-semibold"
                      : "text-gray-700 hover:text-blue-600"
                  }`}
                >
                  Ajouter un évènement
                </Link>
              )}
              {!user && (
                <Link
                  href="/auth/login"
                  onClick={() => setCurrentPage(4)}
                  className={`block px-3 py-2 rounded-md text-base font-medium ${
                    currentPage === 4
                      ? "text-blue-600 font-semibold"
                      : "text-gray-700 hover:text-blue-600"
                  }`}
                >
                  Connexion
                </Link>
              )}
            </div>
          </DisclosurePanel>
        </>
      )}
    </Disclosure>
  );
}
