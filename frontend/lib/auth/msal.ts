import { PublicClientApplication, type Configuration } from "@azure/msal-browser";

const tenantId = process.env.NEXT_PUBLIC_AZURE_TENANT_ID ?? "common";
const clientId = process.env.NEXT_PUBLIC_AZURE_CLIENT_ID ?? "";
const redirectUri = process.env.NEXT_PUBLIC_AZURE_REDIRECT_URI ?? "https://sentinel.vaultrix.in/auth/callback";
const apiScope = process.env.NEXT_PUBLIC_AZURE_API_SCOPE ?? `${clientId}/.default`;

export const msalConfig: Configuration = {
  auth: {
    clientId,
    authority: `https://login.microsoftonline.com/${tenantId}`,
    redirectUri
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false
  }
};

export const loginRequest = {
  scopes: [apiScope]
};

let msalClient: PublicClientApplication | null = null;
let initializePromise: Promise<void> | null = null;

export function hasValidEntraConfig() {
  return Boolean(clientId && tenantId && !clientId.startsWith("00000000") && !tenantId.startsWith("00000000"));
}

export async function getMsalClient() {
  if (!msalClient) {
    msalClient = new PublicClientApplication(msalConfig);
  }

  initializePromise ??= msalClient.initialize();
  await initializePromise;
  return msalClient;
}

export function clearMsalBrowserState() {
  for (const storage of [window.sessionStorage, window.localStorage]) {
    Object.keys(storage)
      .filter((key) => key.toLowerCase().includes("msal"))
      .forEach((key) => storage.removeItem(key));
  }
}
