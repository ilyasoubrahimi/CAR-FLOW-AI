import React from "react";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

export default function Home() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-white dark:bg-zinc-950">
      {/* Hero Section */}
      <section className="relative h-[90vh] flex items-center justify-center px-4">
        <div className="absolute inset-0 z-0 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-white dark:to-zinc-950 z-10" />
          <Image
            src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=2000"
            alt="Luxury car in Marrakech"
            fill
            className="object-cover"
            priority
          />
        </div>

        <div className="relative z-20 text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-6 leading-tight">
            Experience Marrakech <br />
            <span className="text-zinc-400">in Absolute Luxury</span>
          </h1>
          <p className="text-lg md:text-xl text-zinc-200 mb-10 max-w-2xl mx-auto leading-relaxed">
            From sleek city cars to powerful SUVs, discover a curated fleet of premium vehicles
            designed for the most discerning travelers.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/cars">
              <Button size="lg" className="px-10 py-6 text-lg">
                Explore the Fleet
              </Button>
            </Link>
            <Link href="/book">
              <Button variant="outline" size="lg" className="px-10 py-6 text-lg bg-white/10 text-white border-white/20 backdrop-blur-sm hover:bg-white/20">
                Quick Booking
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-24 px-4 bg-white dark:bg-zinc-950">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-black dark:text-white mb-4">
              Beyond Just a Rental
            </h2>
            <p className="text-zinc-500 dark:text-zinc-400 max-w-2xl mx-auto">
              We combine automotive excellence with concierge-level service to ensure your
              stay in Marrakech is nothing short of extraordinary.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Curated Fleet",
                desc: "Only the latest models from world-leading luxury brands.",
                icon: "✨"
              },
              {
                title: "Airport Delivery",
                desc: "Your car awaits you at the terminal. Seamless and swift.",
                icon: "✈️"
              },
              {
                title: "24/7 Concierge",
                desc: "Dedicated support for every moment of your journey.",
                icon: "📞"
              }
            ].map((item, idx) => (
              <div key={idx} className="p-8 rounded-3xl border border-zinc-100 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/50 hover:bg-white dark:hover:bg-zinc-900 transition-colors group">
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">{item.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
