import { toast } from "react-toastify";

const NEXT_PUBLIC_RALLY_BACK_HOST = process.env.NEXT_PUBLIC_RALLY_BACK_HOST;


export async function fetchApi(route: string, token: string, method: string){
    try {
        const res = await fetch(`${NEXT_PUBLIC_RALLY_BACK_HOST}${route}`, {
          cache: "no-store",
          credentials: "include",
          method: method,
          headers : {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        }
        });

        if (!res.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await res.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchCommentsEventApi(event_id: number){
  try {
      const res = await fetch(`/api/comments/events?event_id=${event_id}`, {
        cache: "no-store",
        credentials: "include",
        method: "GET",
        headers : {
          "Content-Type": "application/json",
      }
      });

      if (!res.ok) {
        console.error("Échec du chargement des données");
        return;
      }

      const data = await res.json();
      return data;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}

export async function isRegisteredApi(event_id: number){
  try {
      const res = await fetch(`/api/registrations/is_registered?event_id=${event_id}`, {
        cache: "no-store",
        credentials: "include",
        method: "GET",
        headers : {
          "Content-Type": "application/json",
      }
      });

      if (!res.ok) {
        console.error("Échec du chargement des données");
        return;
      }

      const data = await res.json();
      console.log(data)
      return data;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}

export async function loginApi(body_string: string) {
    try {
      const res = await fetch(`/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body_string,
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Identifiant ou mot de passe incorrect");
      }

      return await res.json();
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  }


export async function sendTokenVerificationApi(email: string){
    try {
        const response = await fetch(`/api/auth/send_token?user_email=${email}`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function registerApi(body_string: string){
    try {
        const response = await fetch(`/api/auth/register/user`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: body_string
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function verifyTokenApi(email: string, token: string){
    try {
        const response = await fetch(`/api/auth/verify_token?user_email=${email}&token=${token}`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            }
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          toast.error("Erreur lors de la vérification");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function logoutApi(token: string){
    try {
        const response = await fetch(`/api/auth/logout`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            authorization: `Bearer ${token}`
            },
            credentials: "include"
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function postCommentApi(body_string: string, token: string){
    try {
        const response = await fetch(`/api/comments`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            credentials: "include",
            body: body_string
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function grantRoleApi(user_id: number, role: string){
  try {
      const response = await fetch(`/api/super_admin/user?user_id=${user_id}&role=${role}`, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json',
          },
          credentials: "include",
      });


      if (!response.ok) {
        console.error("Échec du chargement de role");
        return;
      }

      const data = await response.json();
      return data;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}


export async function postLikeApi(event_id: number, token: string){
    try {
        const response = await fetch(`/api/likes?event_id=${event_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        return response;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function postTypeApi(body_string: string){
  try {
      const response = await fetch(`/api/super_admin/types`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          credentials: "include",
          body: body_string
      });


      if (!response.ok) {
        if (response.status == 409){
          toast.error("Le type existe déjà");
        }
        console.error("Échec du post du type");
        return;
      }

      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}


export async function postReasonApi(body_string: string){
  try {
      const response = await fetch(`/api/super_admin/reasons`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          credentials: "include",
          body: body_string
      });


      if (!response.ok) {
        if (response.status == 409){
          toast.error("La raison existe déjà");
        }
        console.error("Échec du post du type");
        return;
      }

      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}


export async function deleteLikeApi(event_id: number, token: string){
    try {
        const response = await fetch(`/api/likes?event_id=${event_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
        });

        console.log("DELETE", response)


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        return response;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function deleteCommentApi(comment_id: number){
  try {
      const response = await fetch(`/api/comments?comment_id=${comment_id}`, {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
          },
          credentials: "include",
      });


      if (!response.ok) {
        console.error("Échec de la suppression du commentaire");
        return;
      }
      toast.success("Commentaire supprimé");
      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
      toast.error(`Erreur lors de la suppression du commentaire : ${err}`);
    }
}


export async function deleteEventApi(event_id: number){
  try {
      const response = await fetch(`/api/events?event_id=${event_id}`, {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
          },
          credentials: "include",
      });

      if (!response.ok) {
        console.error("Échec de la suppression de l'évènement");
        return;
      }
      toast.success("Evènement supprimé");
      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
      toast.error(`Erreur lors de la suppression de l'évènement : ${err}`);
    }
}


export async function fetchTypesApi(){
    try {
        console.log("OF?");
        const res = await fetch(`/api/types`, {
          method: "GET",
          headers : {
            "Content-Type": "application/json",
            }
        });

        if (!res.ok) {
          console.error("Échec du chargement des données");
          return;
        }
        // console.log(await res.json())
        return res;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchProfilesApi(
  limit: number,
  offset: number,
  filters?: {
    nb_like?: string;
    is_planner?: boolean;
    role?: string;
    search?: string;
  }
) {
  try {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    });

    if (filters?.nb_like) params.append("nb_like", filters.nb_like);
    if (filters?.is_planner !== undefined) params.append("is_planner", String(filters.is_planner));
    if (filters?.role) params.append("role", filters.role);
    if (filters?.search) params.append("search", filters.search);

    const res = await fetch(`/api/super_admin/profiles?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials:  "include"
    });

    if (!res.ok) {
      console.error("Échec du chargement des profils");
      return;
    }

    return res;
  } catch (err) {
    console.error("Erreur réseau :", err);
  }
}


export async function fetchPaymentsApi(
  limit: number,
  offset: number,
  filters?: {
    event_title?: string;
    buyer_email?: string;
    organizer_email?: string;
    amount_min?: number;
    amount_max?: number;
    fee_min?: number;
    fee_max?: number;
    brut_amount_min?: number;
    brut_amount_max?: number;
    stripe_session_id?: string;
    stripe_payment_intent_id?: string;
    status?: string;
    date_apres?: string;
    date_avant?: string;
  }
) {
  try {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    });

    console.log("FILTERS", filters)

    if (filters?.event_title) params.append("event_title", filters.event_title);
    if (filters?.buyer_email) params.append("buyer_email", filters.buyer_email);
    if (filters?.organizer_email) params.append("organizer_email", filters.organizer_email);
    if (filters?.amount_min !== undefined) params.append("amount_min", String(filters.amount_min));
    if (filters?.amount_max !== undefined) params.append("amount_max", String(filters.amount_max));
    if (filters?.fee_min !== undefined) params.append("fee_min", String(filters.fee_min));
    if (filters?.fee_max !== undefined) params.append("fee_max", String(filters.fee_max));
    if (filters?.brut_amount_min !== undefined) params.append("brut_amount_min", String(filters.brut_amount_min));
    if (filters?.brut_amount_max !== undefined) params.append("brut_amount_max", String(filters.brut_amount_max));
    if (filters?.stripe_session_id) params.append("stripe_session_id", filters.stripe_session_id);
    if (filters?.stripe_payment_intent_id) params.append("stripe_payment_intent_id", filters.stripe_payment_intent_id);
    if (filters?.status) params.append("status", filters.status);
    if (filters?.date_apres) params.append("date_apres", filters.date_apres);
    if (filters?.date_avant) params.append("date_avant", filters.date_avant);

    const res = await fetch(`/api/super_admin/payments?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    if (!res.ok) {
      console.error("Échec du chargement des paiements");
      return;
    }

    return res;
  } catch (err) {
    console.error("Erreur réseau :", err);
  }
}


export async function fetchLogsApi(
  limit: number,
  offset: number,
  filters?: {
    date?: string;
    action_type?: string;
    log_type?: string;
  }
) {
  try {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    });

    console.log("FILTERS", filters)

    if (filters?.date) params.append("date", filters.date);
    if (filters?.action_type) params.append("action_type", filters.action_type);
    if (filters?.log_type) params.append("log_type", filters.log_type);

    console.log("RORORORRO", params.toString())
    const res = await fetch(`/api/super_admin/action-logs?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    if (!res.ok) {
      console.error("Échec du chargement des paiements");
      return;
    }

    return res;
  } catch (err) {
    console.error("Erreur réseau :", err);
  }
}



export async function fetchReasonsApi(){
    try {
        const res = await fetch(`/api/reasons`, {
          cache: "no-store",
          method: "GET",
          headers : {
            "Content-Type": "application/json",
            },
            credentials: "include",
        });

        if (!res.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        return res;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function postSignaledCommentApi(body_string: string, token: string){
    try {
        const response = await fetch(`/api/signaled_comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
            body: body_string
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function postSignaledEventApi(body_string: string, token: string){
    try {
        const response = await fetch(`/api/signaled_events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
            body: body_string
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function postSignaledUserApi(body_string: string){
  try {
      const response = await fetch(`/api/signaled_users`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          credentials: "include",
          body: body_string
      });


      if (!response.ok) {
        console.error("Échec du chargement des données");
        return;
      }

      const data = await response.json();
      return data;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}


export async function fetchMeApi() {
    try {
      const response = await fetch("/api/profiles/me", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include", // Nécessaire pour que les cookies HttpOnly soient envoyés
      });

      if (!response.ok) {
        console.error("Échec du chargement des données");
        return;
      }

      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  }


export async function fetchSignaledUsers(
  offset: number,
  limit: number,
  filters: {
    signaled_by_user?: string,
    reason_id?: number,
    user_signaled?: string,
    date?: string,
  }
) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });
  if (filters.date) params.append("date", filters.date);
  if (filters.signaled_by_user) params.append("signaled_by_user", filters.signaled_by_user);
  if (filters.reason_id) params.append("reason_id", String(filters.reason_id));
  if (filters.user_signaled) params.append("user_signaled", filters.user_signaled);
    try {
      const response = await fetch(`/api/signaled_users?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include",
      });

      if (!response.ok) {
        console.error("Échec du chargement des données");
        return;
      }

      return response;
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  }


  export async function fetchSignaledEventspi(
    offset: number,
    limit: number,
    filters: {
      date?: string;
      user_id?: number;
      email_user?: string;
      email_event_user?: string;
      reason_id?: number;
      event_id?: number;
      status?: string;
    }
  ) {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    });

    if (filters.date) params.append("date", filters.date);
    if (filters.user_id) params.append("user_id", String(filters.user_id));
    if (filters.email_user) params.append("email_user", filters.email_user);
    if (filters.email_event_user) params.append("email_event_user", filters.email_event_user);
    if (filters.reason_id) params.append("reason_id", String(filters.reason_id));
    if (filters.event_id) params.append("event_id", String(filters.event_id));
    if (filters.status) params.append("status", filters.status);

    try {
      const response = await fetch(`/api/signaled_events?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        console.error('Échec du chargement des données:', response.statusText);
        return null;
      }

      const data = await response.json();
      return data;
    } catch (err) {
      console.error('Erreur réseau :', err);
      return null;
    }
  }



  export async function deleteSignaledUser(
    user_id: number,
    ban: boolean
  ) {
      try {
        const response = await fetch(`/api/signaled_users?user_id=${user_id}&ban=${ban}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: "include",
        });

        if (!response.ok) {
          console.error("Échec du chargement de la suppression du signalement");
          return;
        }

        return response;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
    }


  export async function deleteSignaledEventApi(
      signalement_id: number,
      ban: boolean
    ) {
        try {
          const response = await fetch(`/api/signaled_events?signalement_id=${signalement_id}&ban=${ban}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: "include",
          });

          if (!response.ok) {
            console.error("Échec du chargement de la suppression du signalement");
            return;
          }

          return response;
        } catch (err) {
          console.error("Erreur réseau :", err);
        }
      }



  export async function fetchIsLiked(event_id: number) {
    try {
      const response = await fetch(`/api/likes/is_liked?event_id=${event_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include",
      });

      if (!response.ok) {
        console.error("Échec du chargement des données");
        return;
      }


      return await response.json();
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
  }


export async function fetchEventsApi(route: string){
    try {
        const response = await fetch(`${NEXT_PUBLIC_RALLY_BACK_HOST}${route}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}

export async function registerToEventFreeApi(event_id: number){
    try {
      const res = await fetch(`/api/registrations`, {
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

      return res;
    } catch (error) {
      console.error("Erreur réseau :", error);
      toast.error(error)
    }
}


export async function registerToEventPaymentApi(event_id: number){
  try {
    const res = await fetch(`/api/payments/checkout?event_id=${event_id}`, {
      method: "POST",
      cache: "no-store",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      }
    });
    console.log("PAYMENT ", res);
    return res;
  } catch (error) {
    console.error("Erreur réseau :", error);
    toast.error(error)
  }
}


export async function createStripeAccountApi(){
  try {
    const res = await fetch(`/api/payments/create_account`, {
      method: "POST",
      cache: "no-store",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      }
    });

    return res;
  } catch (error) {
    console.error("Erreur réseau :", error);
    toast.error(error)
  }
}


export async function updateEventApi(event_id: number, body_string: string, token: string){
    try {
      const res = await fetch(`/api/events?event_id=${event_id}`, {
        method: "PATCH",
        cache: "no-store",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: body_string
      });

      return res;
    } catch (error) {
      console.error("Erreur réseau :", error);
    }
}


export async function newEventApi(body_string: string, token: string){
    try {
      const res = await fetch(`/api/events`, {
        method: "POST",
        cache: "no-store",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: body_string
      });

      return res;
    } catch (error) {
      console.error("Erreur réseau :", error);
    }
}

export async function uploadPictureApi(body: FormData, token: string){
    try {
      const res = await fetch(`/api/pictures`, {
        method: "POST",
        cache: "no-store",
        credentials: "include",
        body: body
      });

      const data = await res.json();
      console.log("DTOEN", data)
      return data;
    } catch (error) {
      console.error("Erreur réseau :", error);
    }
}


export async function fetchProfileEventsApi(offset: number, limit: number, profile_id: number, token: string){
    try {
        const response = await fetch(`/api/events/profiles?user_id=${profile_id}&offset=${offset}&limit=${limit}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
            credentials: "include",
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchProfileApi(profile_id: number){
    try {
        const response = await fetch(`/api/profiles/${profile_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
            credentials: "include",
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        // const data = await response.json();
        console.log(`PROFILE ${response}`)
        return response;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchMyEventsApi(user_id: number, offset: number, limit: number, token: string){
    try {
        const response = await fetch(`/api/events/self?user_id=${user_id}&offset=${offset}&limit=${limit}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
            credentials: "include"
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchMyRgistrationsApi(offset: number, limit: number, token: string){
    try {
        const response = await fetch(`/api/registrations/self?offset=${offset}&limit=${limit}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
            credentials: "include"
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }
        console.log(response)
        return response.json();
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}


export async function fetchMyPaymentsApi(offset: number, limit: number){
  try {
      const response = await fetch(`/api/payments?offset=${offset}&limit=${limit}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
          cache: "no-store",
          credentials: "include"
      });


      if (!response.ok) {
        console.error("Échec de la récupération des paiements");
        return;
      }
      return response.json();
    } catch (err) {
      console.error("Erreur réseau :", err);
    }
}


export async function updateProfileApi(body_string: string, token: string){
    try {
        const response = await fetch(`/api/profiles`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: "no-store",
            credentials: "include",
            body: body_string
        });


        if (!response.ok) {
          console.error("Échec du chargement des données");
          return;
        }

        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Erreur réseau :", err);
      }
}



