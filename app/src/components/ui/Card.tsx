import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, title, subtitle, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "group relative overflow-hidden rounded-3xl border border-zinc-200 bg-white p-6 transition-all hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-950",
          className
        )}
        {...props}
      >
        {(title || subtitle) && (
          <div className="mb-4">
            {title && <h3 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">{title}</h3>}
            {subtitle && <p className="text-sm text-zinc-500 dark:text-zinc-400">{subtitle}</p>}
          </div>
        )}
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";
