import { fetchProfileApi, fetchEventsProfileApi, fetchMeApi } from "@/app/server_components/api_python";
import ProfilePage from "./profile_page";

export default async function Profile({
  params,
  searchParams,
}: {
  params: { profile_id: string };
  searchParams: { eventCurrentPage?: string; registrationsCurrentPage?: string; paymentsCurrentPage?: string };
}) {
  const user = fetchMeApi();
  const limit = 1;
  const {
    eventCurrentPage = "1",
  } = await searchParams;

  const profile = await fetchProfileApi(Number(params.profile_id));
  const currentPageEvents = Number(eventCurrentPage);
  const eventOffset = (currentPageEvents - 1) * limit;
  const eventsData = await fetchEventsProfileApi(profile.id, eventOffset, limit);
  const events = eventsData.data;
  const totalPagesEvents = eventsData.total;

  return (
    <ProfilePage
      profile={profile}
      profileEvents={events}
      totalPages={totalPagesEvents}
      currentPage={currentPageEvents}
      user={user}
    />
  );
}
