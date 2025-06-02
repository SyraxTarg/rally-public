import Image from "next/image";
import { Chip } from "@heroui/chip";
import Link from "next/link";

interface Profile {
  id: number;
  first_name: string;
  last_name: string;
  photo: string;
  nb_like: number;
  email: string;
  created_at: string;
}

interface Registration {
  id: number;
  profile: Profile;
  event_id: number;
  event_title: string;
  registered_at: string;
  payment_status: "pending" | "paid" | "failed" | "free";
}

interface RegistrationCardProps {
  registration: Registration;
}

export default function RegistrationCard({ registration }: RegistrationCardProps) {
  const { profile, payment_status, registered_at } = registration;

  return (
    <div className="flex items-center gap-4 p-4 shadow-md bg-white overflow-hidden max-w-xs transition-shadow hover:shadow-lg">
      <Image
        src={profile.photo}
        alt={`${profile.first_name} ${profile.last_name}`}
        width={64}
        height={64}
        className="rounded-full object-cover"
      />
      <div className="flex flex-col">
        <Link href={`/events/${registration.event_id}`} className="text-lg font-semibold text-[#123c69] hover:text-blue-600">{registration.event_title}</Link>
        <p className="text-sm text-gray-600">{profile.email}</p>
        <p className="text-sm text-gray-500">
          Inscrit le {new Date(registered_at).toLocaleDateString('fr-FR', {
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            })}
        </p>
        <Chip
            className={
                (payment_status === "paid" || payment_status === "free"
                ? "bg-green-200 text-green-800"
                : payment_status === "pending"
                ? "bg-yellow-200 text-yellow-800"
                : "bg-red-200 text-red-800") +
                " px-3 py-1 rounded-full text-sm font-semibold inline-block"
            }
            >
            {payment_status}
        </Chip>

      </div>
    </div>
  );
}
