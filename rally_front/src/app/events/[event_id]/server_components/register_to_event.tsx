const NEXT_PUBLIC_RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST;


export default async function registerToEvent(event_id: number){
        try {
          const res = await fetch(`${NEXT_PUBLIC_RALLY_BACK_HOST}/registrations`, {
            method: "POST",
            cache: "no-store",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(
                {
                    "event_id": event_id
                }
            )
          });

          if (!res.ok) {
            console.error("Échec de l'envoi de la réservation");
            return;
          }
          console.log("reservation ok");
        } catch (error) {
          console.error("Erreur réseau :", error);
        }
}
