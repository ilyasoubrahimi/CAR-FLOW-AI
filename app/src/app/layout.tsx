import React from "react";
import { cn } from "@/lib/utils";
import { Header } from "@/components/layout/Header";
import { AIAssistant } from "@/components/ai/AIAssistant";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" className="h-full antialiased">
      <body className="min-h-full bg-zinc-50 text-zinc-900 font-sans selection:bg-zinc-200 dark:bg-zinc-950 dark:text-zinc-50 selection:bg-zinc-800">
        <Header />
        <main className="flex-1">{children}</main>
        <AIAssistant />
        <footer className="border-t border-zinc-200 py-12 text-center text-sm text-zinc-500 dark:border-zinc-800 dark:text-zinc-400">
          © {new Date().getFullYear()} Marrakech Drive. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
