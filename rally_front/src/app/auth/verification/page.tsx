"use client";
import { useState, useEffect } from "react";
import CodeInput from "./components/code_input";
import AuthButton from "../components/auth_button";
import style from './verification.module.css'
import { useRouter } from 'next/navigation'
import { sendTokenVerificationApi, verifyTokenApi } from "@/app/server_components/api";
import { toast } from "react-toastify";

const NEXT_PUBLIC_RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST;

export default function VerificationPage() {
    const [code, setCode] = useState(["", "", "", "", "", ""]);
    const [timeLeft, setTimeLeft] = useState(0);
    const [tokenSent, setTokenSent] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const router = useRouter();

    const [email, setEmail] = useState("");

    useEffect(() => {
      const storedEmail = sessionStorage.getItem("registeredEmail");
      console.log("MAIL ", storedEmail);
      if (storedEmail) {
        setEmail(storedEmail);
      } else {
        setErrorMessage("Adresse email introuvable. Veuillez vous réinscrire.");
        // Optionnel : router.push('/auth/register')
      }
    }, []);


    const sendTokenEmail = async () => {

       try {
            await sendTokenVerificationApi(email);

            // //   Vérifie si la réponse est correcte
            // if (!response.ok) {
            //     console.log(response)
            //     throw new Error('Erreur lors de la connexion');
            // }
            setTimeLeft(1200); // 20 minutes = 1200 sec
            setTokenSent(true);

        } catch (error) {
          console.error(error);
          setErrorMessage(error.message); // Affiche l'erreur à l'utilisateur
        }

      };

    useEffect(() => {
        if (timeLeft <= 0) return;

        const interval = setInterval(() => {
          setTimeLeft((prev) => {
            if (prev <= 1) {
              clearInterval(interval);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);

        return () => clearInterval(interval);
      }, [timeLeft]);

      const formatTime = (seconds) => {
        const m = String(Math.floor(seconds / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${m}:${s}`;
      };

    const handleSubmit = async (e) => {
      e.preventDefault();
      const token = code.join("");
      try {
            await verifyTokenApi(email, token);
            toast.success("Compte vérifié");
            router.push(`/auth/login`);

        } catch (error) {
          console.error(error);
          setErrorMessage(error.message);
          toast.error(`Erreur pendant la vérification: ${errorMessage}`);
        }
    };


    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
        <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full text-center">
          <h1 className={`text-2xl font-bold text-gray-800 mb-4 ${style.verif_title}`}>Vérifiez votre compte !</h1>
          <p className="text-gray-600 mb-6">Veuillez entrer le code à 6 chiffres envoyé à votre email</p>

          <form onSubmit={handleSubmit}>
            <CodeInput code={code} setCode={setCode}/>
            <AuthButton text ={"Vérifier le code"}/>
            <p className="mt-6 text-center text-sm text-[#ac3b61] cursor-pointer">
                <a className={`text-sm font-medium`} onClick={sendTokenEmail}>
                  Renvoyer un code
                </a>
              </p>
                {tokenSent && (
                <div className="mt-6 text-lg text-gray-700 font-medium">
                    Le token est encore valide pendant :{" "}
                    <span className="font-mono text-[#ac3b61]">{formatTime(timeLeft)}</span>
                </div>
                )}
          </form>
        </div>
      </div>
    );
  }
