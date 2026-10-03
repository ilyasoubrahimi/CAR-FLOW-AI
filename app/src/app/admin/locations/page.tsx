"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Loader2, AlertCircle, Trash2, Edit3, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

interface Location {
  id: number;
  name: string;
  slug: string;
  type: string;
  city: string;
  active: boolean;
}

export default function AdminLocations() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchLocations() {
      try {
        const data = await apiRequest<Location[]>("/locations/");
        setLocations(data);
      } catch (err: any) {
        setError(err.message || "Failed to load locations");
      } finally {
        setLoading(false);
      }
    }
    fetchLocations();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this location?")) return;
    try {
      await apiRequest(`/locations/${id}`, { method: "DELETE" });
      setLocations(prev => prev.filter(l => l.id !== id));
    } catch (err: any) {
      alert(err.message || "Delete failed");
    }
  };

  if (loading) return <div className="flex h-64 w-full items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-zinc-400" /></div>;
  if (error) return <div className="p-6 rounded-2xl bg-red-50 text-red-600 flex items-center gap-3 border border-red-100"><AlertCircle className="w-5 h-5" /><p className="text-sm font-medium">{error}</p></div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Location Management</h2>
        <Button className="gap-2"><Plus className="w-4 h-4" /> Add Location</Button>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
              <tr className="text-zinc-500 uppercase tracking-wider font-semibold">
                <th className="px-6 py-4">Name</th>
                <th className="px-6 py-4">City</th>
                <th className="px-6 py-4">Type</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {locations.map(l => (
                <tr key={l.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors">
                  <td className="px-6 py-4 font-medium">{l.name}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{l.city}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{l.type}</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 rounded-full text-[10px] font-bold uppercase",
                      l.active ? "bg-emerald-100 text-emerald-700" : "bg-zinc-100 text-zinc-700"
                    )}>{l.active ? "Active" : "Inactive"}</span>
                  </td>
                  <td className="px-6 py-4 text-right space-x-2">
                    <Button variant="ghost" size="sm" className="p-2"><Edit3 className="w-4 h-4" /></Button>
                    <Button variant="ghost" size="sm" className="p-2 text-red-500 hover:text-red-700" onClick={() => handleDelete(l.id)}><Trash2 className="w-4 h-4" /></Button>
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

function Button({ children, className, variant = "default", size = "default", ...props }: any) {
  const variants = {
    default: "bg-black text-white dark:bg-white dark:text-black",
    ghost: "bg-transparent hover:bg-zinc-100 dark:hover:bg-zinc-800",
  };
  const sizes = {
    default: "px-4 py-2",
    sm: "px-2 py-1",
  };
  return (
    <button className={cn(variants[variant as keyof typeof variants], sizes[size as keyof typeof sizes], className)} {...props}>
      {children}
    </button>
  );
}
