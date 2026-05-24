import { create } from "zustand";
import type { Role } from "@/lib/types";

interface AuthState {
  accessToken: string;
  role: Role;
  setAccessToken: (token: string) => void;
  setRole: (role: Role) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: process.env.NEXT_PUBLIC_DEMO_MODE === "true" ? "demo-token" : "",
  role: "Admin",
  setAccessToken: (accessToken) => set({ accessToken }),
  setRole: (role) => set({ role })
}));

