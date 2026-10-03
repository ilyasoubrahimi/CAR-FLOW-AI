"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useBookingStore } from "@/store/useBookingStore";

export const AdminGuard = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const { user, token } = useBookingStore();
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;

    if (!token) {
      router.push("/auth/login");
    } else if (user && user.role !== "ADMIN") {
      // If authenticated but not an admin, redirect to a safe page
      router.push("/");
    }
  }, [token, user, isHydrated, router]);

  if (!isHydrated || !token || (user && user.role !== "ADMIN")) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-zinc-50 dark:bg-zinc-950">
        <div className="text-center">
          <p className="text-zinc-500 animate-pulse">Verifying administrative access...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};
