"use client";

import { Bell, Boxes, Gauge, LayoutDashboard, Moon, Search, Server, ShieldCheck, Sun, UserCircle } from "lucide-react";
import { useTheme } from "next-themes";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/lib/store";

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard, roles: ["Admin", "Platform Engineer", "Viewer"] },
  { href: "/resources", label: "Resources", icon: Server, roles: ["Admin", "Platform Engineer", "Viewer"] },
  { href: "/clusters", label: "Clusters", icon: Boxes, roles: ["Admin", "Platform Engineer", "Viewer"] },
  { href: "/governance", label: "Governance", icon: ShieldCheck, roles: ["Admin", "Platform Engineer", "Viewer"] },
  { href: "/recommendations", label: "Optimization", icon: Gauge, roles: ["Admin", "Platform Engineer"] }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const role = useAuthStore((state) => state.role);
  const accessToken = useAuthStore((state) => state.accessToken);

  useEffect(() => {
    if (!accessToken) {
      router.replace("/login");
    }
  }, [accessToken, router]);

  if (!accessToken) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background">
        <div className="rounded-md border border-border bg-card px-4 py-3 text-sm text-muted-foreground">
          Checking secure session
        </div>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-border bg-card lg:block">
        <div className="flex h-16 items-center gap-3 border-b border-border px-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <div>
            <p className="text-sm font-semibold">Sentinel</p>
            <p className="text-xs text-muted-foreground">Azure-native operations</p>
          </div>
        </div>
        <nav className="space-y-1 p-3">
          {nav
            .filter((item) => item.roles.includes(role))
            .map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground",
                  pathname === item.href && "bg-muted text-foreground"
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            ))}
        </nav>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-border bg-background/92 px-4 backdrop-blur lg:px-6">
          <div className="flex w-full max-w-xl items-center gap-2 rounded-md border border-border bg-card px-3 py-2 text-sm text-muted-foreground">
            <Search className="h-4 w-4" />
            <span>Search clusters, namespaces, owners</span>
          </div>
          <div className="ml-3 flex items-center gap-2">
            <button className="rounded-md border border-border p-2" aria-label="Notifications">
              <Bell className="h-4 w-4" />
            </button>
            <button
              className="rounded-md border border-border p-2"
              aria-label="Toggle theme"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
            <div className="hidden items-center gap-2 rounded-md border border-border px-3 py-2 text-sm md:flex">
              <UserCircle className="h-4 w-4" />
              {role}
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 lg:px-6">{children}</main>
      </div>
    </div>
  );
}
