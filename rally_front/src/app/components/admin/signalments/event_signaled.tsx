'use client';

import { useEffect, useState } from 'react';
import { deleteReport } from './delete_event_report';
import { fetchSignaledEventspi, deleteSignaledEventApi } from '@/app/server_components/api';
import SignalementEventFiltersModal from './filter_signaled_event_modal';
import { useRouter } from "next/navigation";

interface Report {
  id: number;
  event: {
    id: number;
    title: string;
    profile: {
      email: string;
    };
  };
  reason: {
    id: number;
    reason: string;
  };
  user_id: number;
  created_at: string;
  status: string;
}

interface FilterValues {
  date?: string;
  user_id?: number;
  email_user?: string;
  email_event_user?: string;
  reason_id?: number;
  event_id?: number;
  status?: string;
}

const PAGE_SIZE = 10;

export default function ReportedEventsTable() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [filters, setFilters] = useState<FilterValues>({});
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const router = useRouter();

  const fetchReports = async (page: number, activeFilters: FilterValues) => {
    try {
      const offset = (page - 1) * PAGE_SIZE;
      const users = await fetchSignaledEventspi(offset, PAGE_SIZE, activeFilters);
      setReports(users.data);
      setTotal(users.count);
    } catch (err) {
      console.error('Erreur lors du chargement des signalements', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports(currentPage, filters);
  }, [currentPage, filters]);

  const handleApplyFilters = (newFilters: FilterValues) => {
    setCurrentPage(1);
    setFilters(newFilters);
  };

  const handleDeleteSignalment = async (reportId: number, ban: boolean) => {
    setIsSubmitting(true);
    try {
      await deleteReport(reportId, ban);
      await fetchReports(currentPage, filters);
      router.refresh();
    } catch (error) {
      console.error("Erreur lors de la suppression du signalement", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (loading) return <p className="text-center text-gray-600 py-10">Chargement des signalements...</p>;

  return (
    <div className="p-4 max-w-screen-xl mx-auto">
      <div className="mb-6 text-right">
        <button
          onClick={() => setIsFiltersOpen(true)}
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
                <th className="px-6 py-3">Événement</th>
                <th className="px-6 py-3">Créateur</th>
                <th className="px-6 py-3">Raison</th>
                <th className="px-6 py-3">Date</th>
                <th className="px-6 py-3">Statut</th>
                <th className="px-6 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="text-gray-800">
              {reports.map((report) => (
                <tr key={report.id} className="border-t hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium">{report.id}</td>
                  <td className="px-6 py-4">{report.event.title}</td>
                  <td className="px-6 py-4">{report.event.profile.email}</td>
                  <td className="px-6 py-4">{report.reason.reason}</td>
                  <td className="px-6 py-4">{new Date(report.created_at).toLocaleString('fr-FR')}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                        report.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-700'
                          : report.status === 'resolved'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-gray-100 text-gray-600'
                      }`}
                    >
                      {report.status}
                    </span>
                  </td>
                  <td className="flex gap-2 px-6 py-4">
                    <button
                      disabled={isSubmitting}
                      className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-md text-sm font-semibold shadow-sm transition"
                      onClick={() => {
                        if (confirm('Es-tu sûr de vouloir bannir le créateur de cet événement ?')) {
                          handleDeleteSignalment(report.id, true);
                        }
                      }}
                    >
                      Supprimer l'évènement
                    </button>
                    <button
                      disabled={isSubmitting}
                      className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded-md text-sm font-semibold shadow-sm transition"
                      onClick={() => {
                        if (confirm('Rejeter ce signalement ?')) {
                          handleDeleteSignalment(report.id, false);
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

      {/* Pagination */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-6 text-sm text-gray-700">
        <div>
          Affiche {Math.min((currentPage - 1) * PAGE_SIZE + 1, total)}–
          {Math.min(currentPage * PAGE_SIZE, total)} sur {total}
        </div>
        <ul className="inline-flex flex-wrap items-center gap-1">
          <li>
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
            >
              Précédent
            </button>
          </li>
          {[...Array(totalPages)].map((_, i) => (
            <li key={i + 1}>
              <button
                onClick={() => setCurrentPage(i + 1)}
                className={`px-3 py-1 border rounded-md ${
                  currentPage === i + 1
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'hover:bg-gray-100'
                }`}
              >
                {i + 1}
              </button>
            </li>
          ))}
          <li>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
            >
              Suivant
            </button>
          </li>
        </ul>
      </div>

      <SignalementEventFiltersModal
        isOpen={isFiltersOpen}
        initialFilters={filters}
        onApply={handleApplyFilters}
        onClose={() => setIsFiltersOpen(false)}
      />
    </div>
  );
}
