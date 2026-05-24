import { test, expect } from "@playwright/test";

test("dashboard renders governance shell", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("What needs attention today?")).toBeVisible();
  await expect(page.getByText("Environment Governance")).toBeVisible();
});
