import { useAuthStore } from "@/lib/store";
import { acquireAccessToken } from "@/lib/auth/msal";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

async function getBearerToken() {
  const currentToken = useAuthStore.getState().accessToken;
  if (currentToken) {
    return currentToken;
  }

  const msalToken = await acquireAccessToken();
  if (msalToken) {
    useAuthStore.getState().setAccessToken(msalToken);
  }
  return msalToken;
}

export async function apiGet<T>(path: string): Promise<T> {
  const token = await getBearerToken();
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
