'use client';

import { useEffect, useState } from 'react';
import { fetchSignaledUsers, deleteSignaledUser } from '@/app/server_components/api';
import SignalementFiltersModal from './filter_signaled_user_modal';

interface Report {
  id: number;
  user_signaled_id: number;
  user_signaled_email: string;
  reason: {
    id: number;
    reason: string;
  };
  signaled_by_id: number;
  signaled_by_email: string;
  created_at: string;
  status: string;
}

interface FilterValues {
  date?: string;
  signaled_by_user?: string;
  user_signaled?: string;
  reason_id?: number;
}

const PAGE_SIZE = 10;

export default function ReportedUsersTable() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [filters, setFilters] = useState<FilterValues>({});
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchReports = async (page: number, activeFilters: FilterValues) => {
    try {
      const offset = (page - 1) * PAGE_SIZE;
      const res = await fetchSignaledUsers(offset, PAGE_SIZE, activeFilters);
      const users = await res?.json();
      setReports(users.data);
      setTotal(users.total);
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


  const handleDeleteSignalment = async (user_id: number, ban: boolean) => {
    setIsSubmitting(true);
    try {
      await deleteSignaledUser(user_id, ban);
      await fetchReports(currentPage, filters);
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
      {/* Bouton filtres */}
      <div className="mb-6 text-right">
        <button
          onClick={() => setIsFiltersOpen(true)}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition shadow"
        >
          Filtres
        </button>
      </div>

      {/* Table en desktop */}
      <div className="hidden sm:block rounded-xl shadow overflow-hidden bg-white">
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs tracking-wider">
              <tr>
                <th className="px-6 py-3">#</th>
                <th className="px-6 py-3">Utilisateur signalé</th>
                <th className="px-6 py-3">Signalé par</th>
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
                  <td className="px-6 py-4">{report.user_signaled_email}</td>
                  <td className="px-6 py-4">{report.signaled_by_email}</td>
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
                        const confirmBan = confirm('Es-tu sûr de vouloir bannir cet utilisateur ?');
                        if (confirmBan) {
                          handleDeleteSignalment(report.id, true);
                          console.log(report.user_signaled_id)
                        }
                      }}
                    >
                      Bannir user
                    </button>
                    <button
                      disabled={isSubmitting}
                      className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded-md text-sm font-semibold shadow-sm transition"
                      onClick={() => {
                        const confirmReject = confirm('Rejeter ce signalement ?');
                        if (confirmReject) {
                          handleDeleteSignalment(report.id, false);
                          console.log(report.user_signaled_id)
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

      {/* Format mobile */}
      <div className="sm:hidden space-y-4">
        {reports.map((report) => (
          <div key={report.id} className="bg-white rounded-lg shadow p-4">
            <div className="text-sm font-semibold text-gray-700 mb-2">Signalement #{report.id}</div>
            <div className="text-sm text-gray-600">
              <strong>Utilisateur signalé :</strong> {report.user_signaled_email}
            </div>
            <div className="text-sm text-gray-600">
              <strong>Signalé par :</strong> {report.signaled_by_email}
            </div>
            <div className="text-sm text-gray-600">
              <strong>Raison :</strong> {report.reason.reason}
            </div>
            <div className="text-sm text-gray-600">
              <strong>Date :</strong> {new Date(report.created_at).toLocaleString('fr-FR')}
            </div>
            <div className="mt-2">
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
            </div>
          </div>
        ))}
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

      <SignalementFiltersModal
        isOpen={isFiltersOpen}
        initialFilters={filters}
        onApply={handleApplyFilters}
        onClose={() => setIsFiltersOpen(false)}
      />
    </div>
  );
}
