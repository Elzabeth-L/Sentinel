import { useAuthStore } from "@/lib/store";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

export async function apiGet<T>(path: string): Promise<T> {
  const token = useAuthStore.getState().accessToken;
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}
