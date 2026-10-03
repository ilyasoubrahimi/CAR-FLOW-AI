"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { AdminGuard } from "@/components/auth/AdminGuard";
import {
  LayoutDashboard,
  Calendar,
  Car,
  Users,
  CreditCard,
  MapPin,
  Settings,
  Menu,
  X
} from "lucide-react";
import { Button } from "@/components/ui/Button";

const NAV_ITEMS = [
  { label: "Overview", href: "/admin", icon: LayoutDashboard },
  { label: "Reservations", href: "/admin/reservations", icon: Calendar },
  { label: "Vehicles", href: "/admin/vehicles", icon: Car },
  { label: "Customers", href: "/admin/customers", icon: Users },
  { label: "Pricing", href: "/admin/pricing", icon: CreditCard },
  { label: "Locations", href: "/admin/locations", icon: MapPin },
  { label: "Settings", href: "/admin/settings", icon: Settings },
];

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  return (
    <AdminGuard>
      <div className="flex h-screen overflow-hidden bg-zinc-50 dark:bg-zinc-950">
        {/* Sidebar - Desktop */}
        <aside className="hidden md:flex w-64 flex-col border-r border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
          <div className="flex h-16 items-center px-6 border-b border-zinc-200 dark:border-zinc-800">
            <Link href="/" className="text-lg font-bold tracking-tighter text-black dark:text-white">
              ADMIN<span className="text-zinc-500">PANEL</span>
            </Link>
          </div>

          <nav className="flex-1 overflow-y-auto p-4 space-y-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all",
                    isActive
                      ? "bg-black text-white dark:bg-white dark:text-black"
                      : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
                  )}
                >
                  <item.icon className="w-4 h-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <div className="p-4 border-t border-zinc-200 dark:border-zinc-800">
            <div className="flex items-center gap-3 px-3 py-2">
              <div className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-700 flex items-center justify-center text-xs font-bold">
                AD
              </div>
              <span className="text-xs font-medium text-zinc-500">Administrator</span>
            </div>
          </div>
        </aside>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top Header - Mobile & Desktop */}
          <header className="h-16 border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900 flex items-center justify-between px-4 sm:px-6">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                className="md:hidden p-2"
                onClick={() => setIsMobileMenuOpen(true)}
              >
                <Menu className="w-5 h-5" />
              </Button>
              <h1 className="text-sm font-semibold text-zinc-500 uppercase tracking-wider">
                {NAV_ITEMS.find(i => i.href === pathname)?.label || "Management"}
              </h1>
            </div>

            <div className="flex items-center gap-4">
               <Link
                href="/"
                className="text-xs font-medium text-zinc-500 hover:text-black dark:hover:text-white transition-colors"
               >
                Return to Site
               </Link>
            </div>
          </header>

          <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
            {children}
          </main>
        </div>

        {/* Mobile Sidebar Overlay */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-50 md:hidden">
            <div
              className="absolute inset-0 bg-black/20 backdrop-blur-sm"
              onClick={() => setIsMobileMenuOpen(false)}
            />
            <aside className="absolute inset-y-0 left-0 w-64 bg-white dark:bg-zinc-900 flex flex-col shadow-xl">
              <div className="flex h-16 items-center justify-between px-6 border-b border-zinc-200 dark:border-zinc-800">
                <span className="text-lg font-bold tracking-tighter">ADMIN</span>
                <Button variant="ghost" size="sm" onClick={() => setIsMobileMenuOpen(false)}>
                  <X className="w-5 h-5" />
                </Button>
              </div>
              <nav className="flex-1 p-4 space-y-1">
                {NAV_ITEMS.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all",
                        isActive
                          ? "bg-black text-white dark:bg-white dark:text-black"
                          : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
                      )}
                    >
                      <item.icon className="w-4 h-4" />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>
            </aside>
          </div>
        )}
      </div>
    </AdminGuard>
  );
}
