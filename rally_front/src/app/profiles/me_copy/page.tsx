
import { fetchMyEventsApi, fetchMeApi, fetchMyPaymentsApi, fetchMyRegistrationsApi } from "@/app/server_components/api_python";
import MePage from "./me_page";


export default async function MyProfile({searchParams}) {
  const user = await fetchMeApi();
  const limit = 1;

  const {eventCurrentPage = '1', registrationsCurrentPage = '1', paymentsCurrentPage = '1'} = await searchParams;

  if (!user) {
    return (
      <p className="text-center text-lg text-gray-600 mt-10">
        Vous n'êtes pas connecté.
      </p>
    );
  }


  {/*FETCH MY EVENTS*/}
  const currentPageEvents = Number(eventCurrentPage);
   const eventOffset = (currentPageEvents - 1) * limit;
    const events = await fetchMyEventsApi(user?.id, eventOffset, limit);
    const myEvents = events.data;
    const totalPagesEvents = events.total;

  const currentPageRegistrations = Number(registrationsCurrentPage);
   const registrationsOffset = (currentPageRegistrations - 1) * limit;
    const registrations = await fetchMyRegistrationsApi(registrationsOffset, limit);
    const myRegistrations = registrations.data;
    const totalPagesRegistrations = registrations.total;

    const currentPagePayments = Number(paymentsCurrentPage);
    const paymentsOffset = (currentPagePayments - 1) * limit;
     const payments = await fetchMyPaymentsApi(paymentsOffset, limit);
     const myPayments = payments.data;
     const totalPagesPayments = payments.total;



  return (
    <>
    <MePage
      myEvents={myEvents}
      totalPagesEvents={totalPagesEvents}
      user={user}
      currentPageEvents={currentPageEvents}
      myRegistrations={myRegistrations}
      totalPagesRegistrations={totalPagesRegistrations}
      currentPageRegistrations={currentPageRegistrations}
      myPayments={myPayments}
      totalPagesPayments={totalPagesPayments}
      currentPagePayments={currentPagePayments}
    />
    </>
  );
}
