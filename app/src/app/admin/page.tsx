"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Loader2, AlertCircle, TrendingUp, Calendar, CheckCircle, Clock, XCircle, Car } from "lucide-react";
import { cn } from "@/lib/utils";

interface AnalyticsOverview {
  total_reservations: number;
  today_reservations: number;
  confirmed_reservations: number;
  active_rentals: number;
  completed_rentals: number;
  cancelled_reservations: number;
  total_revenue: number;
  average_rental_duration: number;
  most_booked_vehicles: Array<{ brand: string; model: string; count: number }>;
  available_vehicles: number;
  returning_vehicles: number;
}

export default function AdminOverview() {
  const [data, setData] = useState<AnalyticsOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const result = await apiRequest<AnalyticsOverview>("/analytics/overview");
        setData(result);
      } catch (err: any) {
        setError(err.message || "Failed to load analytics");
      } finally {
        setLoading(false);
      }
    }
    fetchAnalytics();
  }, []);

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

  if (!data) return null;

  const kpiCards = [
    { label: "Total Revenue", value: `${data.total_revenue.toLocaleString()} MAD`, icon: TrendingUp, color: "text-emerald-600" },
    { label: "Total Bookings", value: data.total_reservations, icon: Calendar, color: "text-blue-600" },
    { label: "Confirmed", value: data.confirmed_reservations, icon: CheckCircle, color: "text-indigo-600" },
    { label: "Active Rentals", value: data.active_rentals, icon: Clock, color: "text-amber-600" },
    { label: "Cancellations", value: data.cancelled_reservations, icon: XCircle, color: "text-red-600" },
    { label: "Fleet Availability", value: `${data.available_vehicles} units`, icon: Car, color: "text-zinc-600" },
  ];

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {kpiCards.map((kpi) => (
          <Card key={kpi.label} className="p-6 flex items-center gap-4">
            <div className={cn("p-3 rounded-xl bg-zinc-100 dark:bg-zinc-800", kpi.color)}>
              <kpi.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">{kpi.label}</p>
              <p className="text-2xl font-bold tracking-tighter">{kpi.value}</p>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-bold mb-6">Most Booked Vehicles</h3>
          <div className="space-y-4">
            {data.most_booked_vehicles.map((v, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-zinc-50 dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800">
                <span className="text-sm font-medium">{v.brand} {v.model}</span>
                <span className="text-sm font-bold bg-zinc-200 dark:bg-zinc-700 px-2 py-1 rounded">{v.count} rentals</span>
              </div>
            ))}
            {data.most_booked_vehicles.length === 0 && <p className="text-sm text-zinc-500 italic">No booking data available.</p>}
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-bold mb-6">Quick Metrics</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-zinc-100 dark:border-zinc-800">
              <span className="text-sm text-zinc-500">Today's Bookings</span>
              <span className="text-sm font-bold">{data.today_reservations}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-zinc-100 dark:border-zinc-800">
              <span className="text-sm text-zinc-500">Avg Rental Duration</span>
              <span className="text-sm font-bold">{data.average_rental_duration.toFixed(1)} days</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-zinc-100 dark:border-zinc-800">
              <span className="text-sm text-zinc-500">Returning Vehicles</span>
              <span className="text-sm font-bold">{data.returning_vehicles}</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
