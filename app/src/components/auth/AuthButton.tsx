"use client";

import React from "react";
import { useBookingStore } from "@/store/useBookingStore";
import { Button } from "@/components/ui/Button";
import { User, LogOut } from "lucide-react";
import Link from "next/link";

export function AuthButton() {
  const { user, token, setAuth } = useBookingStore();

  if (!user) {
    return (
      <Link href="/auth/login">
        <Button variant="ghost" className="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium">
          <User className="w-4 h-4" /> Sign In
        </Button>
      </Link>
    );
  }

  return (
    <div className="flex items-center gap-4">
      <div className="hidden sm:flex flex-col text-right mr-2">
        <p className="text-xs font-bold text-black dark:text-white leading-none">{user.username}</p>
        <p className="text-[10px] text-zinc-500 uppercase tracking-tighter">{user.role}</p>
      </div>
      <Button
        variant="ghost"
        onClick={() => setAuth(null, null)}
        className="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium"
      >
        <LogOut className="w-4 h-4" /> Sign Out
      </Button>
    </div>
  );
}
