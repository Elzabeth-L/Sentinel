"use client";

import { Boxes } from "lucide-react";
import { AppShell } from "@/components/shell/app-shell";
import { SectionPanel } from "@/components/dashboard/section-panel";
import { SkeletonRows } from "@/components/ui/skeleton-rows";
import { useClusters } from "@/lib/queries";

export default function ClustersPage() {
  const clusters = useClusters();

  return (
    <AppShell>
      <SectionPanel title="Cluster Overview" icon={Boxes}>
        {clusters.isLoading ? (
          <SkeletonRows rows={4} />
        ) : (
          <div className="grid gap-3 md:grid-cols-2">
            {clusters.data?.map((cluster) => (
              <div key={cluster.id} className="rounded-md border border-border bg-background p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="font-semibold">{cluster.name}</h2>
                    <p className="mt-1 text-sm text-muted-foreground">{cluster.resource_group} - {cluster.location}</p>
                  </div>
                  <span className="rounded-sm bg-muted px-2 py-1 text-xs">{cluster.onboarding_state}</span>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                  <span className="text-muted-foreground">Version</span>
                  <span>{cluster.kubernetes_version}</span>
                  <span className="text-muted-foreground">Nodes</span>
                  <span>{cluster.node_count}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </SectionPanel>
    </AppShell>
  );
}
