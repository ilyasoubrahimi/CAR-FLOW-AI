"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Loader2, AlertCircle, Search } from "lucide-react";

interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  country: string;
}

export default function AdminCustomers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCustomers() {
      try {
        const data = await apiRequest<Customer[]>("/customers/");
        setCustomers(data);
      } catch (err: any) {
        setError(err.message || "Failed to load customers");
      } finally {
        setLoading(false);
      }
    }
    fetchCustomers();
  }, []);

  if (loading) return <div className="flex h-64 w-full items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-zinc-400" /></div>;
  if (error) return <div className="p-6 rounded-2xl bg-red-50 text-red-600 flex items-center gap-3 border border-red-100"><AlertCircle className="w-5 h-5" /><p className="text-sm font-medium">{error}</p></div>;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold tracking-tight">Customer Directory</h2>
      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
              <tr className="text-zinc-500 uppercase tracking-wider font-semibold">
                <th className="px-6 py-4">Name</th>
                <th className="px-6 py-4">Email</th>
                <th className="px-6 py-4">Phone</th>
                <th className="px-6 py-4">Country</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {customers.map(c => (
                <tr key={c.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors">
                  <td className="px-6 py-4 font-medium">{c.first_name} {c.last_name}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{c.email}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{c.phone}</td>
                  <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400">{c.country}</td>
                </tr>
              ))}
              {customers.length === 0 && (
                <tr><td colSpan={4} className="px-6 py-12 text-center text-zinc-500 italic">No customers found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
