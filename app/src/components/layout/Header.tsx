import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { AuthButton } from "@/components/auth/AuthButton";

export const Header = ({ className }: { className?: string }) => {
  return (
    <header className={cn("sticky top-0 z-50 w-full border-b border-zinc-200 bg-white/80 backdrop-blur-md dark:border-zinc-800 dark:bg-zinc-950/80", className)}>
      <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6">
        <Link href="/" className="text-xl font-bold tracking-tighter text-black dark:text-white">
          MARRAKECH<span className="text-zinc-500">DRIVE</span>
        </Link>
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
          <Link href="/cars" className="text-zinc-600 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-colors">Fleet</Link>
          <Link href="/book" className="text-zinc-600 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-colors">Booking</Link>
          <Link href="/my-rental" className="text-zinc-600 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-colors">My Rental</Link>
        </nav>
        <div className="flex items-center gap-4">
          <AuthButton />
          <Link
            href="/book"
            className="hidden sm:block rounded-full bg-black px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-white dark:text-black dark:hover:bg-zinc-200"
          >
            Reserve Now
          </Link>
        </div>
      </div>
    </header>
  );
};
