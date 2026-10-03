"use client";

import React, { useState, useEffect } from "react";
import { useBookingStore } from "@/store/useBookingStore";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { apiRequest } from "@/lib/api-client";
import {
  ChevronRight,
  ChevronLeft,
  CheckCircle2,
  Car,
  Calendar,
  User,
  CreditCard,
  Info
} from "lucide-react";
import { useSearchParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

function BookingContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const {
    vehicleId, setVehicle,
    pickupDate, returnDate, setDates,
    locationId, setLocation,
    extras, toggleExtra,
    customerDetails, setCustomerDetails,
    step, setStep,
    reset
  } = useBookingStore();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [totalPrice, setTotalPrice] = useState<number | null>(null);

  useEffect(() => {
    async function calculateTotal() {
      if (step === 4 && vehicleId && pickupDate && returnDate) {
        try {
          const params = new URLSearchParams({
            vehicle_id: vehicleId,
            pickup_date: pickupDate,
            return_date: returnDate,
            ...extras.reduce((acc, ex) => ({ ...acc, [ex]: "true" }), {})
          });
          const data = await apiRequest<{ total: number }>(`/availability/quote?${params.toString()}`);
          setTotalPrice(data.total);
        } catch (err) {
          console.error("Price calculation failed:", err);
        }
      }
    }
    calculateTotal();
  }, [step, vehicleId, pickupDate, returnDate, extras]);

  useEffect(() => {
    const vId = searchParams.get("vehicle_id");
    if (vId) setVehicle(vId);
  }, [searchParams, setVehicle]);

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleConfirmBooking = async () => {
    setLoading(true);
    setError(null);

    // Validation
    if (!pickupDate || !returnDate) {
      setError("Please select both pickup and return dates.");
      setLoading(false);
      return;
    }
    if (new Date(pickupDate) >= new Date(returnDate)) {
      setError("Return date must be after the pickup date.");
      setLoading(false);
      return;
    }
    if (!customerDetails.firstName || !customerDetails.lastName || !customerDetails.email || !customerDetails.phone || !customerDetails.passportNumber) {
      setError("Please fill in all customer details.");
      setLoading(false);
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(customerDetails.email)) {
      setError("Please enter a valid email address.");
      setLoading(false);
      return;
    }
    if (customerDetails.passportNumber.length < 6) {
      setError("Passport number is too short.");
      setLoading(false);
      return;
    }

    try {
      // 1. Create Draft
      const draft = await apiRequest<{ id: string, code: string }>(`/reservations/`, {
        method: "POST",
        body: JSON.stringify({
          vehicle_id: parseInt(vehicleId!),
          pickup_date: pickupDate,
          return_date: returnDate,
          customer: {
            first_name: customerDetails.firstName,
            last_name: customerDetails.lastName,
            email: customerDetails.email,
            phone: customerDetails.phone,
            passport_number: customerDetails.passportNumber,
          },
          extras: extras
        })
      });

      // 2. Confirm Reservation
      await apiRequest(`/reservations/${draft.id}/confirm`, { method: "POST" });

      setSuccess(draft.code);
      reset();
    } catch (err: any) {
      setError(err.message || "Booking failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="container mx-auto px-4 py-24 max-w-2xl text-center">
        <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h1 className="text-4xl font-bold mb-4">Reservation Confirmed!</h1>
        <p className="text-zinc-500 mb-8">Your luxury vehicle is secured. We've sent the confirmation details to your email.</p>
        <Card className="p-6 bg-zinc-50 dark:bg-zinc-900 border-2 border-dashed border-zinc-200 dark:border-zinc-800 mb-8">
          <p className="text-sm text-zinc-500 uppercase tracking-widest mb-2">Reservation Code</p>
          <p className="text-3xl font-mono font-bold tracking-tighter">{success}</p>
        </Card>
        <div className="flex gap-4 justify-center">
          <Button onClick={() => router.push("/my-rental")}>Track My Rental</Button>
          <Button variant="outline" onClick={() => router.push("/")}>Return Home</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      {/* Stepper */}
      <div className="flex justify-between mb-12 relative">
        <div className="absolute top-1/2 left-0 w-full h-0.5 bg-zinc-200 dark:bg-zinc-800 -z-10" />
        {[
          { label: "Details", icon: <Car className="w-4 h-4" /> },
          { label: "Extras", icon: <Info className="w-4 h-4" /> },
          { label: "Customer", icon: <User className="w-4 h-4" /> },
          { label: "Review", icon: <CreditCard className="w-4 h-4" /> },
        ].map((s, i) => (
          <div key={i} className="flex flex-col items-center gap-2">
            <div className={cn(
              "w-10 h-10 rounded-full flex items-center justify-center transition-all border-2",
              step > i ? "bg-black text-white border-black dark:bg-white dark:text-black dark:border-white"
              : step === i + 1 ? "bg-white text-black border-black ring-4 ring-zinc-100 dark:bg-zinc-950 dark:text-white dark:border-white dark:ring-zinc-800"
              : "bg-white text-zinc-400 border-zinc-200 dark:bg-zinc-950 dark:text-zinc-600 dark:border-zinc-800"
            )}>
              {step > i ? <CheckCircle2 className="w-5 h-5" /> : s.icon}
            </div>
            <span className={cn(
              "text-xs font-medium",
              step === i + 1 ? "text-black dark:text-white" : "text-zinc-400"
            )}>{s.label}</span>
          </div>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
        >
          {step === 1 && (
            <Card className="p-8">
              <h2 className="text-2xl font-bold mb-6">Rental Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-zinc-500 uppercase">Pickup Date</label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
                    <Input
                      type="date"
                      className="pl-10"
                      value={pickupDate}
                      onChange={(e) => setDates(e.target.value, returnDate)}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-zinc-500 uppercase">Return Date</label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
                    <Input
                      type="date"
                      className="pl-10"
                      value={returnDate}
                      onChange={(e) => setDates(pickupDate, e.target.value)}
                    />
                  </div>
                </div>
              </div>
              <div className="mt-8 flex justify-end">
                <Button onClick={nextStep} className="px-8">Continue <ChevronRight className="ml-2 w-4 h-4" /></Button>
              </div>
            </Card>
          )}

          {step === 2 && (
            <Card className="p-8">
              <h2 className="text-2xl font-bold mb-6">Enhance Your Experience</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                {[
                  { id: "gps", name: "Premium GPS", price: 15 },
                  { id: "child_seat", name: "Child Seat", price: 10 },
                  { id: "insurance_full", name: "Full Insurance", price: 25 },
                  { id: "wifi", name: "Mobile Wi-Fi", price: 5 },
                ].map((extra) => (
                  <div
                    key={extra.id}
                    onClick={() => toggleExtra(extra.id)}
                    className={cn(
                      "p-4 rounded-2xl border-2 cursor-pointer transition-all flex justify-between items-center",
                      extras.includes(extra.id)
                        ? "border-black bg-zinc-50 dark:border-white dark:bg-zinc-900"
                        : "border-zinc-100 dark:border-zinc-800 hover:border-zinc-300"
                    )}
                  >
                    <span className="font-medium">{extra.name}</span>
                    <span className="text-sm text-zinc-500">+{extra.price} MAD/day</span>
                  </div>
                ))}
              </div>
              <div className="mt-8 flex justify-between">
                <Button variant="ghost" onClick={prevStep} className="px-8"><ChevronLeft className="mr-2 w-4 h-4" /> Back</Button>
                <Button onClick={nextStep} className="px-8">Continue <ChevronRight className="ml-2 w-4 h-4" /></Button>
              </div>
            </Card>
          )}

          {step === 3 && (
            <Card className="p-8">
              <h2 className="text-2xl font-bold mb-6">Customer Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                <Input
                  placeholder="First Name"
                  value={customerDetails.firstName}
                  onChange={(e) => setCustomerDetails({ firstName: e.target.value })}
                />
                <Input
                  placeholder="Last Name"
                  value={customerDetails.lastName}
                  onChange={(e) => setCustomerDetails({ lastName: e.target.value })}
                />
                <Input
                  placeholder="Email Address"
                  type="email"
                  value={customerDetails.email}
                  onChange={(e) => setCustomerDetails({ email: e.target.value })}
                />
                <Input
                  placeholder="Phone Number"
                  value={customerDetails.phone}
                  onChange={(e) => setCustomerDetails({ phone: e.target.value })}
                />
                <div className="md:col-span-2">
                  <Input
                    placeholder="Passport Number"
                    value={customerDetails.passportNumber}
                    onChange={(e) => setCustomerDetails({ passportNumber: e.target.value })}
                  />
                </div>
              </div>
              <div className="mt-8 flex justify-between">
                <Button variant="ghost" onClick={prevStep} className="px-8"><ChevronLeft className="mr-2 w-4 h-4" /> Back</Button>
                <Button onClick={nextStep} className="px-8">Review Booking <ChevronRight className="ml-2 w-4 h-4" /></Button>
              </div>
            </Card>
          )}

          {step === 4 && (
            <Card className="p-8">
              <h2 className="text-2xl font-bold mb-6">Final Review</h2>
              <div className="space-y-6 mb-8">
                <div className="p-6 rounded-2xl bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800">
                  <div className="flex justify-between mb-2">
                    <span className="text-zinc-500">Vehicle</span>
                    <span className="font-bold">Premium Selection</span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span className="text-zinc-500">Dates</span>
                    <span className="font-medium">{pickupDate} to {returnDate}</span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span className="text-zinc-500">Customer</span>
                    <span className="font-medium">{customerDetails.firstName} {customerDetails.lastName}</span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span className="text-zinc-500">Payment Method</span>
                    <span className="font-bold text-black dark:text-white">Pay at pickup</span>
                  </div>
                  <div className="h-px bg-zinc-200 dark:bg-zinc-800 my-4" />
                  <div className="flex justify-between text-xl font-bold">
                    <span>Total Estimated</span>
                    <span>{totalPrice ? `${totalPrice} MAD` : "Calculating..."}</span>
                  </div>
                  <p className="text-[10px] text-zinc-400 mt-4 text-center italic">
                    No online payment is required. You will pay upon vehicle pickup.
                  </p>
                </div>

                {error && (
                  <div className="p-4 rounded-xl bg-red-50 text-red-600 text-sm flex items-center gap-3">
                    <Info className="w-4 h-4" /> {error}
                  </div>
                )}
              </div>
              <div className="mt-8 flex justify-between">
                <Button variant="ghost" onClick={prevStep} className="px-8"><ChevronLeft className="mr-2 w-4 h-4" /> Back</Button>
                <Button
                  onClick={handleConfirmBooking}
                  disabled={loading}
                  className="px-10 py-6 text-lg rounded-2xl shadow-xl"
                >
                  {loading ? "Processing..." : "Confirm & Reserve Now"}
                </Button>
              </div>
            </Card>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

export default function BookingPage() {
  return (
    <React.Suspense fallback={<div className="container mx-auto px-4 py-12 text-center">Loading booking...</div>}>
      <BookingContent />
    </React.Suspense>
  );
}
