"use client";

import React, { useEffect, useState } from "react";
import {
  fetchTypesApi,
  fetchReasonsApi,
  postReasonApi,
  postTypeApi,
} from "@/app/server_components/api";

export default function TypesAndReasonsList() {
  const [types, setTypes] = useState<any[]>([]);
  const [typesCount, setTypesCount] = useState<number>(0);
  const [reasons, setReasons] = useState<any[]>([]);
  const [reasonsCount, setReasonsCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newType, setNewType] = useState("");
  const [newReason, setNewReason] = useState("");

  const fetchData = async () => {
    try {
      const typesRes = await fetchTypesApi();
      const reasonsRes = await fetchReasonsApi();
      const typesData = await typesRes.json();
      const reasonsData = await reasonsRes.json();

      setTypes(typesData.data);
      setTypesCount(typesData.count);
      setReasons(reasonsData.data);
      setReasonsCount(reasonsData.count);
    } catch {
      setError("Échec du chargement des types ou des raisons");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [typesCount, reasonsCount]);

  const handleAddType = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newType.trim()) return;

    await postTypeApi(JSON.stringify({ type: newType }));
    setTypesCount(typesCount + 1);
    setNewType("");
  };

  const handleAddReason = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReason.trim()) return;

    await postReasonApi(JSON.stringify({ reason: newReason }));
    setReasonsCount(reasonsCount + 1);
    setNewReason("");
  };

  if (loading) return <div className="p-6 text-lg font-medium">Chargement...</div>;
  if (error) return <div className="p-6 text-red-600 font-semibold">{error}</div>;

  return (
    <div className="p-8 space-y-16 bg-gray-50 min-h-screen">
      {/* Types */}
      <div className="bg-white p-6 rounded-2xl shadow-md">
        <h2 className="text-3xl font-bold mb-6 text-blue-700">Types</h2>

        <form onSubmit={handleAddType} className="mb-6 flex flex-wrap items-center gap-4">
        <input
          type="text"
          placeholder="Nouveau type"
          value={newType}
          onChange={(e) => setNewType(e.target.value)}
          className="border border-gray-300 px-4 py-2 rounded-lg w-full sm:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Ajouter
          </button>
        </form>

        <div className="overflow-x-auto">
        <table className="min-w-full border text-left text-sm rounded-xl overflow-hidden">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs">
              <tr>
                <th className="px-6 py-3 border-b">ID</th>
                <th className="px-6 py-3 border-b">Type</th>
              </tr>
            </thead>
            <tbody>
              {types.map((type: { id: string; type: string }) => (
                <tr
                  key={type.id}
                  className="border-b bg-white hover:bg-gray-50 transition"
                >
                  <td className="px-6 py-4">{type.id}</td>
                  <td className="px-6 py-4">{type.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Raisons */}
      <div className="bg-white p-6 rounded-2xl shadow-md">
        <h2 className="text-3xl font-bold mb-6 text-green-700">Raisons</h2>

        <form onSubmit={handleAddReason} className="mb-6 flex flex-wrap items-center gap-4">
        <input
          type="text"
          placeholder="Nouvelle raison"
          value={newReason}
          onChange={(e) => setNewReason(e.target.value)}
          className="border border-gray-300 px-4 py-2 rounded-lg w-full sm:w-64 focus:outline-none focus:ring-2 focus:ring-green-500"
        />
          <button
            type="submit"
            className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition"
          >
            Ajouter
          </button>
        </form>

        <div className="overflow-x-auto">
        <table className="min-w-full border text-left text-sm rounded-xl overflow-hidden">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs">
              <tr>
                <th className="px-6 py-3 border-b">ID</th>
                <th className="px-6 py-3 border-b">Raison</th>
              </tr>
            </thead>
            <tbody>
              {reasons.map((reason: { id: string; reason: string }) => (
                <tr
                  key={reason.id}
                  className="border-b bg-white hover:bg-gray-50 transition"
                >
                  <td className="px-6 py-4">{reason.id}</td>
                  <td className="px-6 py-4">{reason.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
