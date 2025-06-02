import ReportedUsersTable from "@/app/components/admin/signalments/user_signaled";
import ReportedEventsTable from "@/app/components/admin/signalments/event_signaled";
import ReportedCommentsTable from "@/app/components/admin/signalments/comment_signaled";
import { fetchSignaledCommentsApi } from "@/app/server_components/api_python";

export default async function Signalments({ searchParams }) {

    const {
        commentDate,
        comment_signaled_by_user,
        email_comment_signaled,
        comment_reason_id
    } = await searchParams;

    const commentFilters = {
        commentDate,
        comment_signaled_by_user,
        email_comment_signaled,
        comment_reason_id
    }

    const data = await fetchSignaledCommentsApi(commentFilters);
    const comments = data.data;
    console.log(comments)
    return (
        <>
            <ReportedUsersTable />
            <ReportedEventsTable />
            <ReportedCommentsTable comments={comments} filters={commentFilters} />
        </>
    )
}