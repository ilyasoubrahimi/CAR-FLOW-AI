"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Loader2, AlertCircle, Trash2, Edit3, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

interface Vehicle {
  id: number;
  slug: string;
  brand: string;
  model: string;
  year: number;
  category: string;
  daily_price: string;
  status: string;
  featured: boolean;
  location_id: number;
}

export default function AdminVehicles() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    async function fetchVehicles() {
      try {
        // Use the discovery endpoint but without filters to get the fleet
        const data = await apiRequest<{ vehicles: Vehicle[] }>("/vehicles/");
        setVehicles(data.vehicles);
      } catch (err: any) {
        setError(err.message || "Failed to load fleet");
      } finally {
        setLoading(false);
      }
    }
    fetchVehicles();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this vehicle?")) return;
    try {
      await apiRequest(`/vehicles/${id}`, { method: "DELETE" });
      setVehicles(prev => prev.filter(v => v.id !== id));
    } catch (err: any) {
      alert(err.message || "Delete failed");
    }
  };

  if (loading) return <div className="flex h-64 w-full items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-zinc-400" /></div>;
  if (error) return <div className="p-6 rounded-2xl bg-red-50 text-red-600 flex items-center gap-3 border border-red-100"><AlertCircle className="w-5 h-5" /><p className="text-sm font-medium">{error}</p></div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Fleet Management</h2>
        <Button onClick={() => setIsAdding(true)} className="gap-2">
          <Plus className="w-4 h-4" /> Add Vehicle
        </Button>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
              <tr className="text-zinc-500 uppercase tracking-wider font-semibold">
                <th className="px-6 py-4">Vehicle</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4">Price/Day</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {vehicles.map(v => (
                <tr key={v.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="font-medium">{v.brand} {v.model}</div>
                    <div className="text-xs text-zinc-500">{v.year} • {v.slug}</div>
                  </td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{v.category}</td>
                  <td className="px-6 py-4 font-bold">{v.daily_price} MAD</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 rounded-full text-[10px] font-bold uppercase",
                      v.status === "AVAILABLE" ? "bg-emerald-100 text-emerald-700" :
                      v.status === "RENTED" ? "bg-blue-100 text-blue-700" : "bg-zinc-100 text-zinc-700"
                    )}>{v.status}</span>
                  </td>
                  <td className="px-6 py-4 text-right space-x-2">
                    <Button variant="ghost" size="sm" className="p-2"><Edit3 className="w-4 h-4" /></Button>
                    <Button variant="ghost" size="sm" className="p-2 text-red-500 hover:text-red-700" onClick={() => handleDelete(v.id)}><Trash2 className="w-4 h-4" /></Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
