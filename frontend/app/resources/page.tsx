"use client";

import { Server } from "lucide-react";
import { AppShell } from "@/components/shell/app-shell";
import { SectionPanel } from "@/components/dashboard/section-panel";
import { SkeletonRows } from "@/components/ui/skeleton-rows";
import { useResources } from "@/lib/queries";

export default function ResourcesPage() {
  const resources = useResources();

  return (
    <AppShell>
      <SectionPanel title="Azure Resource Inventory" icon={Server} eyebrow="Live Azure inventory">
        {resources.isLoading ? (
          <SkeletonRows rows={8} />
        ) : resources.isError ? (
          <div className="rounded-md border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
            Could not load Azure resources. Confirm the VM managed identity has Reader access on the subscription.
          </div>
        ) : (
          <div className="overflow-hidden rounded-md border border-border">
            <table className="w-full text-left text-sm">
              <thead className="bg-muted text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3">Resource group</th>
                  <th className="px-4 py-3">Location</th>
                </tr>
              </thead>
              <tbody>
                {resources.data?.map((resource) => (
                  <tr key={resource.id} className="border-t border-border">
                    <td className="px-4 py-3 font-medium">{resource.name}</td>
                    <td className="px-4 py-3 text-muted-foreground">{resource.type}</td>
                    <td className="px-4 py-3">{resource.resource_group}</td>
                    <td className="px-4 py-3">{resource.location || "global"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </SectionPanel>
    </AppShell>
  );
}
