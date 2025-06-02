export async function verifyJwt(token: string){
    try {
        const response = await fetch(`http://localhost:3000/api/auth/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                authorization: `bearer ${token}`
            },
            credentials: "include",
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        console.log("DATA ", response);
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
  }