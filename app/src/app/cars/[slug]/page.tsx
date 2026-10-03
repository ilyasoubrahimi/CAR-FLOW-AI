"use client";

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { apiRequest } from "@/lib/api-client";
import { useBookingStore } from "@/store/useBookingStore";
import {
  Users,
  Briefcase,
  Fuel,
  Settings,
  ArrowLeft,
  Calendar as CalendarIcon,
  CheckCircle2,
  Clock
} from "lucide-react";
import Link from "next/link";

interface Vehicle {
  id: number;
  slug: string;
  brand: string;
  model: string;
  year: number;
  category: string;
  transmission: string;
  fuel: string;
  seats: number;
  luggage: number;
  daily_price: number;
  description: string;
  featured: boolean;
  images: { url: string; is_primary: boolean }[];
}

export default function VehicleDetailPage() {
  const { slug } = useParams();
  const { setVehicle: setBookingVehicle, setDates } = useBookingStore();
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchVehicle() {
      try {
        setLoading(true);
        const data = await apiRequest<Vehicle>(`/vehicles/${slug}`);
        setVehicle(data);
      } catch (err) {
        console.error("Error fetching vehicle details:", err);
        setError("Vehicle not found");
      } finally {
        setLoading(false);
      }
    }

    if (slug) fetchVehicle();
  }, [slug]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-24 max-w-7xl flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-zinc-200 border-t-black rounded-full animate-spin" />
      </div>
    );
  }

  if (error || !vehicle) {
    return (
      <div className="container mx-auto px-4 py-24 max-w-7xl text-center">
        <h2 className="text-2xl font-bold mb-4">{error || "Vehicle not found"}</h2>
        <Link href="/cars">
          <Button variant="outline">Return to Fleet</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-7xl">
      <Link
        href="/cars"
        className="inline-flex items-center gap-2 text-sm font-medium text-zinc-500 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-colors mb-8 group"
      >
        <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />
        Back to Fleet
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Left Column: Gallery and Specs */}
        <div className="lg:col-span-2 space-y-8">
          {/* Gallery */}
          <div className="relative aspect-[16/9] w-full overflow-hidden rounded-3xl shadow-2xl bg-zinc-100 dark:bg-zinc-900">
            <Image
              src={vehicle.images[0]?.url || "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2000"}
              alt={`${vehicle.brand} ${vehicle.model}`}
              fill
              className="object-cover"
              priority
            />
          </div>

          {/* Overview */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h1 className="text-4xl font-bold tracking-tight text-black dark:text-white">
                {vehicle.brand} {vehicle.model}
              </h1>
              <div className="text-right">
                <p className="text-3xl font-bold text-black dark:text-white">{vehicle.daily_price} MAD</p>
                <p className="text-sm text-zinc-500">per day</p>
              </div>
            </div>
            <p className="text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed">
              {vehicle.description || `Experience the unparalleled luxury and performance of the ${vehicle.year} ${vehicle.brand} ${vehicle.model}. A perfect blend of sophistication and power for your journey through Marrakech.`}
            </p>
          </div>

          {/* Specs Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <SpecItem icon={<Users className="w-5 h-5" />} label="Seats" value={vehicle.seats} />
            <SpecItem icon={<Briefcase className="w-5 h-5" />} label="Luggage" value={vehicle.luggage} />
            <SpecItem icon={<Fuel className="w-5 h-5" />} label="Fuel" value={vehicle.fuel} />
            <SpecItem icon={<Settings className="w-5 h-5" />} label="Transmission" value={vehicle.transmission} />
          </div>
        </div>

        {/* Right Column: Booking Card */}
        <div className="lg:col-span-1">
          <Card className="sticky top-24 p-8 border-2 border-black/5 dark:border-white/5 shadow-xl">
            <h3 className="text-xl font-bold mb-6">Reserve this vehicle</h3>

            <div className="space-y-6 mb-8">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Pick-up Date</label>
                <div className="relative">
                  <CalendarIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
                  <input
                    type="date"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 text-sm focus:ring-2 focus:ring-black dark:focus:ring-white outline-none transition-all"
                    onChange={(e) => setDates(e.target.value, "")}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Return Date</label>
                <div className="relative">
                  <CalendarIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
                  <input
                    type="date"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 text-sm focus:ring-2 focus:ring-black dark:focus:ring-white outline-none transition-all"
                    onChange={(e) => setDates("", e.target.value)}
                  />
                </div>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900 mb-8 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-zinc-500">Daily Rate</span>
                <span className="font-medium">{vehicle.daily_price} MAD</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-zinc-500">Taxes & Fees</span>
                <span className="font-medium">Included</span>
              </div>
              <div className="h-px bg-zinc-200 dark:bg-zinc-800 my-2" />
              <div className="flex justify-between font-bold text-lg">
                <span>Estimated Total</span>
                <span>{vehicle.daily_price} MAD</span>
              </div>
            </div>

            <Link href={`/book?vehicle_id=${vehicle.id}`}>
              <Button className="w-full py-6 text-lg rounded-2xl shadow-lg shadow-black/10 dark:shadow-white/10">
                Book Now
              </Button>
            </Link>

            <div className="mt-6 grid grid-cols-1 gap-3">
              <div className="flex items-center gap-3 text-xs text-zinc-500">
                <CheckCircle2 className="w-4 h-4 text-green-500" />
                Instant confirmation
              </div>
              <div className="flex items-center gap-3 text-xs text-zinc-500">
                <Clock className="w-4 h-4 text-blue-500" />
                Flexible cancellation
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function SpecItem({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <div className="p-4 rounded-2xl border border-zinc-100 dark:border-zinc-800 bg-white dark:bg-zinc-950 flex items-center gap-4">
      <div className="p-2 rounded-xl bg-zinc-50 dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400">
        {icon}
      </div>
      <div>
        <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">{label}</p>
        <p className="text-sm font-semibold text-black dark:text-white">{value}</p>
      </div>
    </div>
  );
}
