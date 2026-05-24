"use client";

import { LogIn, ShieldCheck } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { clearMsalBrowserState, getMsalClient, hasValidEntraConfig, loginRequest } from "@/lib/auth/msal";
import { useAuthStore } from "@/lib/store";

export default function LoginPage() {
  const router = useRouter();
  const setAccessToken = useAuthStore((state) => state.setAccessToken);
  const [isSigningIn, setIsSigningIn] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function signIn() {
    if (isSigningIn) return;
    setError(null);
    setIsSigningIn(true);

    if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
      setAccessToken("demo-token");
      router.push("/");
      return;
    }

    if (!hasValidEntraConfig()) {
      setError("Microsoft Entra is not configured yet. Add frontend/.env.local with your tenant ID and client ID, then rebuild and restart Sentinel.");
      setIsSigningIn(false);
      return;
    }

    try {
      const msal = await getMsalClient();
      const redirectResult = await msal.handleRedirectPromise();

      if (redirectResult?.account) {
        const token = await msal.acquireTokenSilent({ ...loginRequest, account: redirectResult.account });
        setAccessToken(token.accessToken);
        router.push("/");
        return;
      }

      await msal.loginRedirect(loginRequest);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Sign-in failed.";
      if (message.includes("interaction_in_progress")) {
        setError("A sign-in attempt is already in progress. Click Reset sign-in state, then try again.");
      } else {
        setError(message);
      }
      setIsSigningIn(false);
    }
  }

  function resetSignInState() {
    clearMsalBrowserState();
    setError(null);
    setIsSigningIn(false);
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4">
      <section className="w-full max-w-md rounded-lg border border-border bg-card p-6 shadow-panel">
        <div className="flex h-12 w-12 items-center justify-center rounded-md bg-primary text-primary-foreground">
          <ShieldCheck className="h-6 w-6" />
        </div>
        <h1 className="mt-5 text-2xl font-semibold">Sentinel</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Sign in with Microsoft Entra ID to access cluster governance and optimization workflows.
        </p>
        {error && (
          <div className="mt-4 rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
            {error}
          </div>
        )}
        <button
          onClick={signIn}
          disabled={isSigningIn}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground"
        >
          <LogIn className="h-4 w-4" />
          {isSigningIn ? "Signing in..." : "Sign in"}
        </button>
        <button
          onClick={resetSignInState}
          className="mt-3 w-full rounded-md border border-border px-4 py-2.5 text-sm font-medium text-muted-foreground"
        >
          Reset sign-in state
        </button>
      </section>
    </main>
  );
}
