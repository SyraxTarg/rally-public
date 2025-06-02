"use client";

import React, { useEffect, useState } from "react";
import { fetchLogsApi } from "@/app/server_components/api";
import LogsFiltersModal from "@/app/components/admin/super-admin/action-logs/filters_modal";

const PAGE_SIZE = 10;

export default function Logs() {
  const [logs, setLogs] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [isModalOpen, setModalOpen] = useState(false);
  const [filters, setFilters] = useState({});

  const fetchPayments = async (page: number) => {
    setLoading(true);
    setError(null);
    try {
      const offset = (page - 1) * PAGE_SIZE;
      const response = await fetchLogsApi(PAGE_SIZE, offset, filters);
      const data = await response?.json();
      setLogs(data.data);
      setTotal(data.total);
    } catch (err) {
      setError("Échec du chargement des logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments(currentPage);
  }, [currentPage, filters]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (loading) return <div className="p-4">Chargement...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <>
      <div className="p-4 sm:p-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Journal des actions</h1>
          <button
            onClick={() => setModalOpen(true)}
            className="bg-[#123c69] text-[#edc7b7] px-5 py-2 rounded-lg shadow hover:bg-[#0f2a4a] transition"
          >
            Filtres
          </button>
        </div>

        {/* Table (desktop) */}
        <div className="hidden md:block overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
          <table className="min-w-full text-sm text-left text-gray-700">
            <thead className="text-xs uppercase bg-gray-100 text-gray-600">
              <tr>
                <th className="px-4 py-3">ID</th>
                <th className="px-4 py-3">Email utilisateur</th>
                <th className="px-4 py-3">Téléphone</th>
                <th className="px-4 py-3">Rôle</th>
                <th className="px-4 py-3">Action</th>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50 transition">
                  <td className="px-4 py-3">{log.id}</td>
                  <td className="px-4 py-3">{log.user?.email || "—"}</td>
                  <td className="px-4 py-3">{log.user?.phone_number || "—"}</td>
                  <td className="px-4 py-3">{log.user?.role?.role || "—"}</td>
                  <td className="px-4 py-3 capitalize">{log.actionType}</td>
                  <td className="px-4 py-3">{log.description}</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    {new Date(log.date).toLocaleString("fr-FR", {
                      dateStyle: "short",
                      timeStyle: "short",
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Cards (mobile) */}
        <div className="md:hidden space-y-4">
          {logs.map((log) => (
            <div
              key={log.id}
              className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 text-sm text-gray-700"
            >
              <div><strong>ID:</strong> {log.id}</div>
              <div><strong>Email:</strong> {log.user?.email || "—"}</div>
              <div><strong>Téléphone:</strong> {log.user?.phone_number || "—"}</div>
              <div><strong>Rôle:</strong> {log.user?.role?.role || "—"}</div>
              <div><strong>Action:</strong> {log.actionType}</div>
              <div><strong>Description:</strong> {log.description}</div>
              <div><strong>Date:</strong> {new Date(log.date).toLocaleString("fr-FR", {
                dateStyle: "short",
                timeStyle: "short",
              })}</div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        <nav className="flex flex-col sm:flex-row sm:items-center justify-between pt-6 gap-4">
          <span className="text-sm text-gray-600">
            Affiche {Math.min((currentPage - 1) * PAGE_SIZE + 1, total)}–{Math.min(currentPage * PAGE_SIZE, total)} sur {total}
          </span>
          <ul className="inline-flex flex-wrap gap-2 text-sm">
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
                      ? "bg-blue-100 text-blue-600 font-medium"
                      : "hover:bg-gray-100"
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
        </nav>
      </div>

      {/* Modal */}
      <LogsFiltersModal
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        onApply={(newFilters) => {
          setFilters(newFilters);
          setCurrentPage(1);
        }}
        initialFilters={filters}
      />
    </>
  );
}
