"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { apiRequest } from "@/lib/api-client";
import { Search, Package, Calendar, User, Clock, CheckCircle2, MessageCircle, Car } from "lucide-react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

interface Reservation {
  id: string;
  code: string;
  status: string;
  vehicle: {
    brand: string;
    model: string;
  };
  pickup_date: string;
  return_date: string;
  total_price: number;
}

export default function MyRentalPage() {
  const [code, setCode] = useState("");
  const [reservation, setReservation] = useState<Reservation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await apiRequest<Reservation>(`/reservations/lookup/${code}`);
      setReservation(data);
    } catch (err: any) {
      setError("Reservation not found. Please check your code and try again.");
      setReservation(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      {!reservation ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-20"
        >
          <div className="w-16 h-16 bg-zinc-100 dark:bg-zinc-900 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <Search className="w-8 h-8 text-zinc-400" />
          </div>
          <h1 className="text-3xl font-bold mb-4">Track Your Journey</h1>
          <p className="text-zinc-500 mb-10 max-w-md mx-auto">
            Enter your reservation code to view your booking status, vehicle details, and pickup instructions.
          </p>

          <form onSubmit={handleLookup} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <Input
              placeholder="Enter Reservation Code (e.g. MD-XXXX)"
              className="text-center uppercase tracking-widest"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
            <Button type="submit" disabled={loading} className="px-8">
              {loading ? "Searching..." : "Track"}
            </Button>
          </form>
          {error && (
            <p className="text-red-500 text-sm mt-4">{error}</p>
          )}
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="space-y-8"
        >
          <div className="flex items-center justify-between mb-4">
            <Link href="/my-rental" className="text-sm font-medium text-zinc-500 hover:text-black transition-colors flex items-center gap-2">
              ← New Search
            </Link>
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-bold uppercase tracking-wider">
              <CheckCircle2 className="w-3 h-3" /> {reservation.status}
            </div>
          </div>

          <Card className="p-8 border-2 border-black/5 dark:border-white/5 shadow-xl">
            <div className="flex justify-between items-start mb-8">
              <div>
                <p className="text-xs font-bold uppercase tracking-widest text-zinc-400 mb-1">Reservation Code</p>
                <h2 className="text-3xl font-mono font-bold tracking-tighter">{reservation.code}</h2>
              </div>
              <div className="text-right">
                <p className="text-xs font-bold uppercase tracking-widest text-zinc-400 mb-1">Total Price</p>
                <p className="text-2xl font-bold">{reservation.total_price} MAD</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div className="space-y-4">
                <div className="flex items-center gap-4 p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900">
                  <div className="p-2 rounded-lg bg-white dark:bg-zinc-800 shadow-sm">
                    <Car className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-[10px] font-bold uppercase text-zinc-400">Vehicle</p>
                    <p className="font-semibold">{reservation.vehicle.brand} {reservation.vehicle.model}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4 p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900">
                  <div className="p-2 rounded-lg bg-white dark:bg-zinc-800 shadow-sm">
                    <Calendar className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-[10px] font-bold uppercase text-zinc-400">Dates</p>
                    <p className="font-semibold">{reservation.pickup_date} → {reservation.return_date}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-4 p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900">
                  <div className="p-2 rounded-lg bg-white dark:bg-zinc-800 shadow-sm">
                    <User className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-[10px] font-bold uppercase text-zinc-400">Driver</p>
                    <p className="font-semibold">Confirmed</p>
                  </div>
                </div>
                <div className="flex items-center gap-4 p-4 rounded-2xl bg-zinc-50 dark:bg-zinc-900">
                  <div className="p-2 rounded-lg bg-white dark:bg-zinc-800 shadow-sm">
                    <Clock className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-[10px] font-bold uppercase text-zinc-400">Pickup Status</p>
                    <p className="font-semibold">Awaiting Arrival</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-8 border-t border-zinc-100 dark:border-zinc-800">
              <div className="flex flex-col sm:flex-row gap-4">
                <Button className="flex-1 py-6 text-lg rounded-2xl" onClick={() => window.open(`https://wa.me/your-number?text=Hi, I'm inquiring about reservation ${reservation.code}`)}>
                  <MessageCircle className="mr-2 w-5 h-5" /> Chat on WhatsApp
                </Button>
                <Button variant="outline" className="flex-1 py-6 text-lg rounded-2xl">
                  Download Invoice
                </Button>
              </div>
            </div>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
