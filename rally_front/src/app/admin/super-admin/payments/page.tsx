"use client";

import React, { useEffect, useState } from "react";
import { fetchPaymentsApi } from "@/app/server_components/api";
import PaymentFiltersModal from "@/app/components/admin/super-admin/payments/filters_modal";

const PAGE_SIZE = 10;

const PaymentsBackOffice: React.FC = () => {
  const [payments, setPayments] = useState<any[]>([]);
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
      const response = await fetchPaymentsApi(PAGE_SIZE, offset, filters);
      const data = await response?.json();
      setPayments(data.data);
      setTotal(data.total);
    } catch (err) {
      setError("Échec du chargement des paiements");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments(currentPage);
  }, [currentPage, filters]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (loading)
    return (
      <div className="flex justify-center items-center p-10 text-gray-600 text-lg font-semibold">
        Chargement...
      </div>
    );

  if (error)
    return (
      <div className="p-6 bg-red-100 text-red-700 rounded-md font-medium">
        {error}
      </div>
    );

  return (
    <>
      <div className="px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
            Liste des Paiements
          </h1>
          <button
            onClick={() => setModalOpen(true)}
            className="self-start sm:self-auto bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md shadow transition"
          >
            Filtres
          </button>
        </div>

        {/* Table on Desktop / Cards on Mobile */}
        <div className="overflow-x-auto hidden md:block">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-sm">
            <thead className="bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300">
              <tr>
                <th className="px-4 py-2 text-left">ID</th>
                <th className="px-4 py-2 text-left">Événement</th>
                <th className="px-4 py-2 text-left">Acheteur</th>
                <th className="px-4 py-2 text-left">Organisateur</th>
                <th className="px-4 py-2 text-left">Montant</th>
                <th className="px-4 py-2 text-left">Frais</th>
                <th className="px-4 py-2 text-left">Brut</th>
                <th className="px-4 py-2 text-left">Statut</th>
                <th className="px-4 py-2 text-left">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700 bg-white dark:bg-gray-900">
              {payments.map((payment) => (
                <tr key={payment.id}>
                  <td className="px-4 py-3">{payment.id}</td>
                  <td className="px-4 py-3">{payment.event_title}</td>
                  <td className="px-4 py-3">{payment.buyer_email}</td>
                  <td className="px-4 py-3">{payment.organizer_email}</td>
                  <td className="px-4 py-3">{payment.amount.toFixed(2)} €</td>
                  <td className="px-4 py-3">{payment.fee.toFixed(2)} €</td>
                  <td className="px-4 py-3">{payment.brut_amount.toFixed(2)} €</td>
                  <td className="px-4 py-3">{payment.status}</td>
                  <td className="px-4 py-3">{new Date(payment.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Cards on Mobile */}
        <div className="space-y-4 md:hidden">
          {payments.map((payment) => (
            <div
              key={payment.id}
              className="bg-white dark:bg-gray-900 shadow rounded-md p-4 space-y-1 text-sm text-gray-700 dark:text-gray-300"
            >
              <div><span className="font-semibold">ID:</span> {payment.id}</div>
              <div><span className="font-semibold">Événement:</span> {payment.event_title}</div>
              <div><span className="font-semibold">Acheteur:</span> {payment.buyer_email}</div>
              <div><span className="font-semibold">Organisateur:</span> {payment.organizer_email}</div>
              <div><span className="font-semibold">Montant:</span> {payment.amount.toFixed(2)} €</div>
              <div><span className="font-semibold">Frais:</span> {payment.fee.toFixed(2)} €</div>
              <div><span className="font-semibold">Brut:</span> {payment.brut_amount.toFixed(2)} €</div>
              <div><span className="font-semibold">Statut:</span> {payment.status}</div>
              <div><span className="font-semibold">Date:</span> {new Date(payment.created_at).toLocaleDateString()}</div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        <nav className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mt-6">
          <span className="text-sm text-gray-600 dark:text-gray-400">
            Affiche{" "}
            <span className="font-semibold">
              {(currentPage - 1) * PAGE_SIZE + 1}–
              {Math.min(currentPage * PAGE_SIZE, total)}
            </span>{" "}
            sur <span className="font-semibold">{total}</span> paiements
          </span>
          <div className="flex flex-wrap gap-2">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-3 py-1 border rounded-md text-sm disabled:opacity-50"
            >
              Précédent
            </button>
            {Array.from({ length: totalPages }, (_, i) => (
              <button
                key={i + 1}
                onClick={() => setCurrentPage(i + 1)}
                className={`px-3 py-1 border rounded-md text-sm ${
                  currentPage === i + 1
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-100"
                }`}
              >
                {i + 1}
              </button>
            ))}
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-3 py-1 border rounded-md text-sm disabled:opacity-50"
            >
              Suivant
            </button>
          </div>
        </nav>
      </div>

      {/* Filtres modale */}
      <PaymentFiltersModal
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
};

export default PaymentsBackOffice;
