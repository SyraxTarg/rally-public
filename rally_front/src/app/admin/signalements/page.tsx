import ReportedUsersTable from "@/app/components/admin/signalments/user_signaled";
import ReportedEventsTable from "@/app/components/admin/signalments/event_signaled";

export default function Signalments(){
    return (
        <>
            <ReportedUsersTable />
            <ReportedEventsTable />
        </>
    )
}