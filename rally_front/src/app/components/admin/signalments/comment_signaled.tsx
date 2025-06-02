"use client";
import { deleteReportComment } from "./delete_comment_report";
import { useDisclosure } from "@heroui/modal";
import { useRouter } from "next/navigation";
import SignalementCommentFiltersModal from "./filter_signaled_comment_modal";

export default function ReportedCommentsTable({ comments, filters }) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const router = useRouter();

    const handleApplyFilters = (filters) => {
        console.log(filters)
        const params = new URLSearchParams();

        if (filters.commentDate) params.set("commentDate", filters.commentDate);
        if (filters.comment_signaled_by_user) params.set("comment_signaled_by_user", filters.comment_signaled_by_user);
        if (filters.email_comment_signaled) params.set("email_comment_signaled", filters.email_comment_signaled);
        if (filters.comment_reason_id) params.set("comment_reason_id", filters.comment_reason_id);
        console.log(params.toString())
        router.push(`/admin/signalements?${params.toString()}`);
    };

    return (
        <div className="p-4 max-w-screen-xl mx-auto">
            <div className="mb-6 text-right">
                <button
                    onClick={onOpen}
                    className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition shadow"
                >
                    Filtres
                </button>
            </div>

            <div className="hidden sm:block rounded-xl shadow overflow-hidden bg-white">
                <div className="overflow-x-auto">
                    <table className="min-w-full text-sm text-left">
                        <thead className="bg-gray-100 text-gray-700 uppercase text-xs tracking-wider">
                            <tr>
                                <th className="px-6 py-3">#</th>
                                <th className="px-6 py-3">Commentaire</th>
                                <th className="px-6 py-3">Auteur</th>
                                <th className="px-6 py-3">Raison</th>
                                <th className="px-6 py-3">Date</th>
                                <th className="px-6 py-3">Statut</th>
                                <th className="px-6 py-3">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="text-gray-800">
                            {comments.map((comment) => (
                                <tr key={comment.id} className="border-t hover:bg-gray-50">
                                    <td className="px-6 py-4 font-medium">{comment.id}</td>
                                    <td className="px-6 py-4">{comment.comment.content}</td>
                                    <td className="px-6 py-4">{comment.comment.profile.email}</td>
                                    <td className="px-6 py-4">{comment.reason.reason}</td>
                                    <td className="px-6 py-4">
                                        {new Date(comment.created_at).toLocaleString('fr-FR')}
                                    </td>
                                    <td className="px-6 py-4">
                                        <span
                                            className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${comment.status === 'pending'
                                                    ? 'bg-yellow-100 text-yellow-700'
                                                    : comment.status === 'resolved'
                                                        ? 'bg-green-100 text-green-700'
                                                        : 'bg-gray-100 text-gray-600'
                                                }`}
                                        >
                                            {comment.status}
                                        </span>
                                    </td>
                                    <td className="flex gap-2 px-6 py-4">
                                        <button
                                            //   disabled={isSubmitting}
                                            className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-md text-sm font-semibold shadow-sm transition"
                                            onClick={() => {
                                                if (confirm("Supprimer ce commentaire ?")) {
                                                    deleteReportComment(comment.id, true);
                                                }
                                            }}
                                        >
                                            Supprimer le commentaire
                                        </button>
                                        <button
                                            //   disabled={isSubmitting}
                                            className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded-md text-sm font-semibold shadow-sm transition"
                                            onClick={() => {
                                                if (confirm("Supprimer ce signalement ?")) {
                                                    deleteReportComment(comment.id, false);
                                                }
                                            }}
                                        >
                                            Rejeter signalement
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <SignalementCommentFiltersModal
                isOpen={isOpen}
                initialFilters={filters}
                onApply={handleApplyFilters}
                onClose={onClose}
            />
        </div>
    );
}