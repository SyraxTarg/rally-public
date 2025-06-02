"use client";
import { useState } from "react";
import styles from "./login.module.css"
import AuthButton from "../components/auth_button";
import { useRouter } from 'next/navigation'
import { useUser } from '../../context/auth_context';
import { toast } from "react-toastify";
import { useCookies } from 'react-cookie'
import { loginApi } from "@/app/server_components/api";



const NEXT_PUBLIC_RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST;

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [cookies, setCookie] = useCookies(['user_access_token', 'user_refresh_token', 'user_connected_id']);

    const router = useRouter();
    const { refetchUser } = useUser();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);

        // Prépare les données à envoyer
        const body = {
          "email": email,
          "password": password
        };

        try {
            const data = await loginApi(JSON.stringify(body));

            setCookie('user_access_token', data.access_token)
            setCookie('user_refresh_token', data.refresh_token)
            setCookie('user_connected_id', data.user_id)
            await refetchUser();
            router.push(`/`);
            toast.success("Connexion réussie");

        } catch (error) {
          console.error(error);
          setErrorMessage(error.message); // Affiche l'erreur à l'utilisateur
          toast.error(error.message);
        } finally{
          setIsLoading(false);
        }

      };

    if (!!isLoading) {
      <div className="fixed inset-0 bg-black bg-opacity-30 z-50 flex items-center justify-center">
        <div className="loader">Chargement...</div>
      </div>
    }

    return (
      <>
        <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4 py-12 sm:px-6 lg:px-8">
          <div className="w-full max-w-md bg-white rounded-lg shadow-lg">
              <div className="w-full bg-[#123c69] text-[#edc7b7] text-center py-4 rounded-t-lg">
                <h2 className="text-2xl font-bold">Connexion</h2>
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
                      className={`mt-1 block w-full rounded-md px-3 py-2 text-gray-900 shadow-sm focus:outline-none ${
                        errorMessage
                          ? "border-red-300 focus:ring-red-500 focus:border-red-500 bg-red-200"
                          : "border-gray-300 focus:ring-indigo-500 focus:border-indigo-500"
                      } sm:text-sm`}
                    />
                  </div>

                  <div>
                    <div className="flex items-center justify-between">
                      <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                        Mot de passe
                      </label>
                      <a href="#" className={`text-sm font-medium ${styles.login_links}`}>
                        Mot de passe oublié ?
                      </a>
                    </div>
                    <input
                      id="password"
                      name="password"
                      type="password"
                      autoComplete="current-password"
                      required
                      onChange={(e) => setPassword(e.target.value)}
                      className={`mt-1 block w-full rounded-md px-3 py-2 text-gray-900 shadow-sm focus:outline-none ${
                        errorMessage
                          ? "border-red-300 focus:ring-red-500 focus:border-red-500 bg-red-200"
                          : "border-gray-300 focus:ring-indigo-500 focus:border-indigo-500"
                      } sm:text-sm`}
                    />
                  </div>
                </div>
                {errorMessage && <p className="mt-1 text-sm text-red-600">{errorMessage}</p>}
                <AuthButton text={"Je me connecte"} isLoading={isLoading}/>
              </form>

              <p className="mt-6 text-center text-sm text-gray-500">
                Aucun compte ?{' '}
                <a href="/auth/register" className={`text-sm font-medium ${styles.login_links}`}>
                  Inscrivez-vous
                </a>
              </p>
            </div>
          </div>
        </div>
      </>

    )
  }
