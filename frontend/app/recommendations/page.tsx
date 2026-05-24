"use client";

import { Gauge } from "lucide-react";
import { AppShell } from "@/components/shell/app-shell";
import { SectionPanel } from "@/components/dashboard/section-panel";
import { SeverityBadge } from "@/components/dashboard/severity-badge";
import { SkeletonRows } from "@/components/ui/skeleton-rows";
import { useClusters, useRecommendations } from "@/lib/queries";

function explainCategory(category: string) {
  if (category === "Governance") return "A platform safety standard is missing.";
  if (category === "Rightsizing") return "The workload may be reserving more than it uses.";
  if (category === "Cleanup") return "The workload looks idle and may be removable.";
  return "This recommendation needs review.";
}

export default function RecommendationsPage() {
  const clusters = useClusters();
  const recommendations = useRecommendations(clusters.data?.[0]?.id ?? "demo");

  return (
    <AppShell>
      <SectionPanel title="Recommended Actions" icon={Gauge}>
        {recommendations.isLoading ? (
          <SkeletonRows rows={6} />
        ) : (
          <div className="space-y-3">
            {recommendations.data?.map((item) => (
              <div key={item.id} className="rounded-md border border-border bg-background p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <h2 className="font-semibold">{item.title}</h2>
                    <p className="mt-1 text-sm text-muted-foreground">{item.namespace}/{item.workload} - {item.category}</p>
                  </div>
                  <SeverityBadge severity={item.severity} />
                </div>
                <div className="mt-4 grid gap-3 text-sm md:grid-cols-2">
                  <div className="rounded-md bg-muted p-3">
                    <p className="font-medium">Why it matters</p>
                    <p className="mt-1 text-muted-foreground">{explainCategory(item.category)}</p>
                  </div>
                  <div className="rounded-md bg-muted p-3">
                    <p className="font-medium">Recommended next step</p>
                    <p className="mt-1 text-muted-foreground">{item.action}</p>
                  </div>
                </div>
                <div className="mt-3 rounded-md border border-border p-3 text-sm text-muted-foreground">
                  <span className="font-medium text-foreground">Evidence:</span> {item.explanation}
                </div>
                <div className="mt-2 text-xs text-muted-foreground">
                  Rule: {item.deterministic_rule} - Waste signal: ${item.estimated_monthly_waste_usd.toFixed(2)}/month
                </div>
              </div>
            ))}
          </div>
        )}
      </SectionPanel>
    </AppShell>
  );
}

