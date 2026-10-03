"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { apiRequest } from "@/lib/api-client";
import Link from "next/link";
import Image from "next/image";
import { Search, Filter, Car, Calendar, MapPin } from "lucide-react";

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
  featured: boolean;
  images: { url: string; is_primary: boolean }[];
}

export default function CarsPage() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: "",
    transmission: "",
    fuel: "",
    max_price: "",
    location_id: "",
  });

  const fetchVehicles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.category) params.append("category", filters.category);
      if (filters.transmission) params.append("transmission", filters.transmission);
      if (filters.fuel) params.append("fuel", filters.fuel);
      if (filters.max_price) params.append("max_price", filters.max_price);
      if (filters.location_id) params.append("location_id", filters.location_id);

      const data = await apiRequest<{ vehicles: Vehicle[] }>(`/vehicles/?${params.toString()}`);
      setVehicles(data.vehicles);
    } catch (error) {
      console.error("Failed to fetch vehicles:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, [filters]);

  return (
    <div className="container mx-auto px-4 py-12 max-w-7xl">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Filters Sidebar */}
        <aside className="w-full md:w-64 shrink-0">
          <Card className="sticky top-24 p-6">
            <div className="flex items-center gap-2 mb-6 text-black dark:text-white">
              <Filter className="w-4 h-4" />
              <h3 className="font-semibold">Filters</h3>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-medium text-zinc-500">Category</label>
                <select
                  className="w-full rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-950 dark:text-white"
                  value={filters.category}
                  onChange={(e) => setFilters(f => ({ ...f, category: e.target.value }))}
                >
                  <option value="">All Categories</option>
                  <option value="Economy">Economy</option>
                  <option value="Premium">Premium</option>
                  <option value="Luxury">Luxury</option>
                  <option value="SUV">SUV</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-medium text-zinc-500">Transmission</label>
                <select
                  className="w-full rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-950 dark:text-white"
                  value={filters.transmission}
                  onChange={(e) => setFilters(f => ({ ...f, transmission: e.target.value }))}
                >
                  <option value="">All</option>
                  <option value="Automatic">Automatic</option>
                  <option value="Manual">Manual</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-medium text-zinc-500">Max Daily Price (MAD)</label>
                <Input
                  type="number"
                  placeholder="e.g. 1000"
                  value={filters.max_price}
                  onChange={(e) => setFilters(f => ({ ...f, max_price: e.target.value }))}
                />
              </div>

              <Button
                variant="outline"
                className="w-full"
                onClick={() => setFilters({ category: "", transmission: "", fuel: "", max_price: "", location_id: "" })}
              >
                Reset Filters
              </Button>
            </div>
          </Card>
        </aside>

        {/* Vehicle Grid */}
        <div className="flex-1">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold tracking-tight text-black dark:text-white">Our Fleet</h1>
            <div className="text-sm text-zinc-500">
              Showing {vehicles.length} vehicles
            </div>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-80 rounded-3xl bg-zinc-100 dark:bg-zinc-900 animate-pulse" />
              ))}
            </div>
          ) : vehicles.length === 0 ? (
            <div className="text-center py-24 rounded-3xl border-2 border-dashed border-zinc-200 dark:border-zinc-800">
              <Car className="w-12 h-12 mx-auto text-zinc-300 mb-4" />
              <h3 className="text-lg font-medium mb-2">No vehicles found</h3>
              <p className="text-zinc-500 mb-6">Try adjusting your filters to find a car.</p>
              <Button onClick={() => setFilters({ category: "", transmission: "", fuel: "", max_price: "", location_id: "" })}>
                Clear all filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {vehicles.map((vehicle) => (
                <Link href={`/cars/${vehicle.slug}`} key={vehicle.id}>
                  <Card className="h-full cursor-pointer group">
                    <div className="relative h-48 w-full mb-4 overflow-hidden rounded-2xl">
                      <Image
                        src={vehicle.images[0]?.url || "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=800"}
                        alt={vehicle.model}
                        fill
                        className="object-cover transition-transform group-hover:scale-105"
                      />
                      {vehicle.featured && (
                        <div className="absolute top-3 left-3 bg-black text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider">
                          Featured
                        </div>
                      )}
                    </div>
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold text-lg">{vehicle.brand} {vehicle.model}</h3>
                        <p className="text-sm text-zinc-500">{vehicle.year} • {vehicle.category}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-black dark:text-white">{vehicle.daily_price} MAD</p>
                        <p className="text-xs text-zinc-400">per day</p>
                      </div>
                    </div>
                    <div className="flex gap-3 mt-4">
                      <div className="flex items-center gap-1 text-xs text-zinc-500">
                        <span className="w-1 h-1 rounded-full bg-zinc-400" />
                        {vehicle.transmission}
                      </div>
                      <div className="flex items-center gap-1 text-xs text-zinc-500">
                        <span className="w-1 h-1 rounded-full bg-zinc-400" />
                        {vehicle.fuel}
                      </div>
                      <div className="flex items-center gap-1 text-xs text-zinc-500">
                        <span className="w-1 h-1 rounded-full bg-zinc-400" />
                        {vehicle.seats} Seats
                      </div>
                    </div>
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
