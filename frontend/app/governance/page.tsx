"use client";

import { ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/shell/app-shell";
import { SectionPanel } from "@/components/dashboard/section-panel";
import { SkeletonRows } from "@/components/ui/skeleton-rows";
import { useClusters, useGovernance } from "@/lib/queries";

export default function GovernancePage() {
  const clusters = useClusters();
  const governance = useGovernance(clusters.data?.[0]?.id ?? "demo");

  return (
    <AppShell>
      <SectionPanel title="Namespace Lifecycle Governance" icon={ShieldCheck}>
        {governance.isLoading ? (
          <SkeletonRows rows={7} />
        ) : (
          <div className="space-y-3">
            {governance.data?.map((item) => (
              <div key={item.namespace} className="rounded-md border border-border bg-background p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h2 className="font-semibold">{item.namespace}</h2>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {item.team ?? "Unassigned"} - {item.environment_type ?? "unknown"} - owner {item.owner ?? "missing"}
                    </p>
                  </div>
                  <span className="rounded-sm bg-muted px-2 py-1 text-sm">{item.status}</span>
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {item.violations.length === 0 ? (
                    <span className="rounded-sm border border-success/30 bg-success/10 px-2 py-1 text-xs text-success">no violations</span>
                  ) : (
                    item.violations.map((violation) => (
                      <span key={violation} className="rounded-sm border border-warning/30 bg-warning/10 px-2 py-1 text-xs text-warning">
                        {violation}
                      </span>
                    ))
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </SectionPanel>
    </AppShell>
  );
}
