"use client";
import { useState } from "react";
import styles from "./register.module.css"
import AuthButton from "../components/auth_button";
import { useRouter } from 'next/navigation';
import { registerApi } from "@/app/server_components/api";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [phone, setPhone] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        // Prépare les données à envoyer
        const data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone,
            "photo": "/pfps/default.jpg"
        };

        try {
            const result = await registerApi(JSON.stringify(data));


            if (result?.email) {
              // Petit délai pour s'assurer que tout est bien traité
              setTimeout(() => {
                sessionStorage.setItem("registeredEmail", result.email);
                router.push(`/auth/verification`);
              }, 100);
            } else {
              throw new Error("Email non retourné par l'API");
            }

        } catch (error) {
          console.error(error);
          setErrorMessage(error.message); // Affiche l'erreur à l'utilisateur
        }
      };

    return (
      <>
        <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4 py-12 sm:px-6 lg:px-8">
          <div className="w-full max-w-md bg-white rounded-lg shadow-lg">
              <div className="w-full bg-[#123c69] text-[#edc7b7] text-center py-4 rounded-t-lg">
                <h2 className="text-2xl font-bold">Inscription</h2>
              </div>
            <div className="pb-8 pl-8 pr-8">

              <form action="#" method="POST" className="mt-8 space-y-6" onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      Email
                    </label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      autoComplete="email"
                      required
                      onChange={(e) => setEmail(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <div className="flex items-center justify-between">
                      <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                        Mot de passe
                      </label>
                    </div>
                    <input
                      id="password"
                      name="password"
                      type="password"
                      autoComplete="current-password"
                      required
                      onChange={(e) => setPassword(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                      Prénom
                    </label>
                    <input
                      id="first_name"
                      name="first_name"
                      type="text"
                      autoComplete="first_name"
                      required
                      onChange={(e) => setFirstName(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                      Nom
                    </label>
                    <input
                      id="last_name"
                      name="last_name"
                      type="text"
                      autoComplete="last_name"
                      required
                      onChange={(e) => setLastName(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                      N° de téléphone
                    </label>
                    <input
                      id="phone"
                      name="phone"
                      type="tel"
                      autoComplete="phone"
                      required
                      onChange={(e) => setPhone(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm px-3 py-2 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>

                <AuthButton text={"Je m'inscris"}/>
              </form>

              <p className="mt-6 text-center text-sm text-gray-500">
                Déjà inscrit(e) ?{' '}
                <a href="/auth/login" className={`text-sm font-medium ${styles.login_links}`}>
                  Connectez-vous
                </a>
              </p>
            </div>
          </div>
        </div>
      </>

    )
  }
