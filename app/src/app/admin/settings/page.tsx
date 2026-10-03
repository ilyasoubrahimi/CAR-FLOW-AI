"use client";

import React, { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Card } from "@/components/ui/Card";
import { Loader2, AlertCircle } from "lucide-react";

interface CompanySettings {
  name: string;
  logo_url: string;
  primary_color: string;
  secondary_color: string;
  phone: string;
  whatsapp_number: string;
  email: string;
  address: string;
  default_currency: string;
}

export default function AdminSettings() {
  const [settings, setSettings] = useState<CompanySettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchSettings() {
      try {
        const data = await apiRequest<CompanySettings>("/company/");
        setSettings(data);
      } catch (err: any) {
        setError(err.message || "Failed to load settings");
      } finally {
        setLoading(false);
      }
    }
    fetchSettings();
  }, []);

  if (loading) return <div className="flex h-64 w-full items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-zinc-400" /></div>;
  if (error) return <div className="p-6 rounded-2xl bg-red-50 text-red-600 flex items-center gap-3 border border-red-100"><AlertCircle className="w-5 h-5" /><p className="text-sm font-medium">{error}</p></div>;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold tracking-tight">Company Settings</h2>
      <Card className="p-6 max-w-2xl">
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <span className="text-xs font-medium text-zinc-500">Company Name</span>
              <p className="font-medium">{settings?.name}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs font-medium text-zinc-500">Email</span>
              <p className="font-medium">{settings?.email}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs font-medium text-zinc-500">Phone</span>
              <p className="font-medium">{settings?.phone}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs font-medium text-zinc-500">WhatsApp</span>
              <p className="font-medium">{settings?.whatsapp_number}</p>
            </div>
          </div>
          <div className="space-y-1">
            <span className="text-xs font-medium text-zinc-500">Address</span>
            <p className="font-medium">{settings?.address}</p>
          </div>
          <div className="space-y-1">
            <span className="text-xs font-medium text-zinc-500">Default Currency</span>
            <p className="font-medium">{settings?.default_currency}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
