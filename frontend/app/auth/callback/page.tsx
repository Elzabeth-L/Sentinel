"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getMsalClient, loginRequest } from "@/lib/auth/msal";
import { useAuthStore } from "@/lib/store";

export default function AuthCallbackPage() {
  const router = useRouter();
  const setAccessToken = useAuthStore((state) => state.setAccessToken);

  useEffect(() => {
    async function completeLogin() {
      const msal = await getMsalClient();
      const result = await msal.handleRedirectPromise();
      const account = result?.account ?? msal.getAllAccounts()[0];

      if (!account) {
        router.replace("/login");
        return;
      }

      const token = await msal.acquireTokenSilent({ ...loginRequest, account });
      setAccessToken(token.accessToken);
      router.replace("/");
    }

    completeLogin().catch(() => router.replace("/login"));
  }, [router, setAccessToken]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-background">
      <div className="rounded-md border border-border bg-card px-4 py-3 text-sm text-muted-foreground">
        Completing secure sign-in
      </div>
    </main>
  );
}
