"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Loader2, AlertCircle, Filter, Search } from "lucide-react";
import { cn } from "@/lib/utils";

interface Reservation {
  id: number;
  reservation_code: string;
  customer_id: number;
  vehicle_id: number;
  pickup_datetime: string;
  return_datetime: string;
  status: string;
  total: string;
  currency: string;
}

export default function AdminReservations() {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filters, setFilters] = useState({
    status: "",
    vehicle_id: "",
  });

  useEffect(() => {
    async function fetchReservations() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (filters.status) params.append("status", filters.status);
        if (filters.vehicle_id) params.append("vehicle_id", filters.vehicle_id);

        const data = await apiRequest<Reservation[]>(`/reservations/?${params.toString()}`);
        setReservations(data);
      } catch (err: any) {
        setError(err.message || "Failed to load reservations");
      } finally {
        setLoading(false);
      }
    }
    fetchReservations();
  }, [filters]);

  const handleFilterChange = (field: string, value: string) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  if (loading) {
    return (
      <div className="flex h-64 w-full items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-zinc-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 rounded-2xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 flex items-center gap-3 border border-red-100 dark:border-red-800">
        <AlertCircle className="w-5 h-5" />
        <p className="text-sm font-medium">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold tracking-tight">All Reservations</h2>

        <div className="flex flex-wrap gap-3">
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
            <Input
              placeholder="Filter by Status"
              className="pl-9 w-40"
              value={filters.status}
              onChange={(e) => handleFilterChange("status", e.target.value)}
            />
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
            <Input
              placeholder="Vehicle ID"
              className="pl-9 w-32"
              value={filters.vehicle_id}
              onChange={(e) => handleFilterChange("vehicle_id", e.target.value)}
            />
          </div>
        </div>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
              <tr className="text-zinc-500 uppercase tracking-wider font-semibold">
                <th className="px-6 py-4">Code</th>
                <th className="px-6 py-4">Customer ID</th>
                <th className="px-6 py-4">Vehicle ID</th>
                <th className="px-6 py-4">Dates</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Total</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {reservations.map((res) => (
                <tr key={res.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors">
                  <td className="px-6 py-4 font-mono font-medium">{res.reservation_code}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{res.customer_id}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{res.vehicle_id}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">
                    {new Date(res.pickup_datetime).toLocaleDateString()} &rarr; {new Date(res.return_datetime).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide",
                      res.status === "CONFIRMED" ? "bg-emerald-100 text-emerald-700" :
                      res.status === "DRAFT" ? "bg-zinc-100 text-zinc-700" :
                      res.status === "CANCELLED" ? "bg-red-100 text-red-700" : "bg-zinc-100 text-zinc-700"
                    )}>
                      {res.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right font-bold">{res.total} {res.currency}</td>
                </tr>
              ))}
              {reservations.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-zinc-500 italic">
                    No reservations found matching the current filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
