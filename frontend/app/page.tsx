"use client";

import { Activity, AlertTriangle, Gauge, Layers3, ShieldCheck, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { AppShell } from "@/components/shell/app-shell";
import { MetricCard } from "@/components/dashboard/metric-card";
import { SectionPanel } from "@/components/dashboard/section-panel";
import { SeverityBadge } from "@/components/dashboard/severity-badge";
import { SkeletonRows } from "@/components/ui/skeleton-rows";
import { useClusters, useGovernance, useRecommendations } from "@/lib/queries";

const utilization = [
  { name: "Mon", cpu: 42, memory: 61 },
  { name: "Tue", cpu: 38, memory: 58 },
  { name: "Wed", cpu: 46, memory: 64 },
  { name: "Thu", cpu: 31, memory: 55 },
  { name: "Fri", cpu: 29, memory: 52 },
  { name: "Sat", cpu: 21, memory: 47 },
  { name: "Sun", cpu: 25, memory: 49 }
];

function explainRecommendation(category: string) {
  if (category === "Cleanup") return "This workload may no longer be needed.";
  if (category === "Rightsizing") return "The request is larger than recent usage suggests.";
  if (category === "Governance") return "A safety guardrail is missing.";
  return "This finding needs platform review.";
}

function friendlyViolation(violation: string) {
  const labels: Record<string, string> = {
    "missing-owner": "Owner missing",
    "ttl-expired": "TTL expired",
    "missing-activity-signal": "Activity unknown",
    "inactive-namespace": "Inactive",
    "scaled-to-zero-or-broken-workloads": "Workloads need review"
  };
  return labels[violation] ?? violation;
}

export default function DashboardPage() {
  const clusters = useClusters();
  const selectedClusterId = clusters.data?.[0]?.id ?? "demo";
  const governance = useGovernance(selectedClusterId);
  const recommendations = useRecommendations(selectedClusterId);

  const cleanupCandidates = governance.data?.filter((item) => item.cleanup_candidate).length ?? 0;
  const avgScore =
    governance.data && governance.data.length > 0
      ? Math.round(governance.data.reduce((sum, item) => sum + item.efficiency_score, 0) / governance.data.length)
      : 0;
  const waste =
    recommendations.data?.reduce((sum, item) => sum + item.estimated_monthly_waste_usd, 0) ?? 0;

  return (
    <AppShell>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-2 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">AKS environment governance</p>
            <h1 className="text-3xl font-semibold tracking-normal">What needs attention today?</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-muted-foreground">
              Clear cleanup candidates, ownership gaps, and resource savings signals translated into practical next steps.
            </p>
          </div>
          <div className="rounded-md border border-border bg-card px-3 py-2 text-sm text-muted-foreground">
            {clusters.data?.[0]?.name ?? "Loading cluster"} - {clusters.data?.[0]?.location ?? "Azure"}
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard icon={Layers3} label="Onboarded clusters" value={clusters.data?.length ?? 0} tone="blue" />
          <MetricCard icon={ShieldCheck} label="Average health score" value={`${avgScore}%`} tone="green" />
          <MetricCard icon={AlertTriangle} label="Needs cleanup review" value={cleanupCandidates} tone="amber" />
          <MetricCard icon={Gauge} label="Estimated waste signal" value={`$${waste.toFixed(0)}`} tone="red" />
        </div>

        <div className="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
          <SectionPanel title="Resource Utilization" icon={Activity}>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={utilization}>
                  <defs>
                    <linearGradient id="cpu" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0f7bdc" stopOpacity={0.38} />
                      <stop offset="95%" stopColor="#0f7bdc" stopOpacity={0.02} />
                    </linearGradient>
                    <linearGradient id="memory" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1fa597" stopOpacity={0.34} />
                      <stop offset="95%" stopColor="#1fa597" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" stroke="currentColor" opacity={0.45} />
                  <YAxis stroke="currentColor" opacity={0.45} />
                  <Tooltip />
                  <Area type="monotone" dataKey="cpu" stroke="#0f7bdc" fill="url(#cpu)" strokeWidth={2} />
                  <Area type="monotone" dataKey="memory" stroke="#1fa597" fill="url(#memory)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </SectionPanel>

          <SectionPanel title="Recommended Actions" icon={Sparkles}>
            {recommendations.isLoading ? (
              <SkeletonRows rows={5} />
            ) : (
              <div className="space-y-3">
                {recommendations.data?.slice(0, 5).map((item) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="rounded-md border border-border bg-background p-3"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-medium">{item.title}</p>
                        <p className="mt-1 text-sm text-muted-foreground">{item.namespace}/{item.workload}</p>
                      </div>
                      <SeverityBadge severity={item.severity} />
                    </div>
                    <div className="mt-3 space-y-2 text-sm text-muted-foreground">
                      <p><span className="font-medium text-foreground">Why it matters:</span> {explainRecommendation(item.category)}</p>
                      <p><span className="font-medium text-foreground">Evidence:</span> {item.explanation}</p>
                      <p><span className="font-medium text-foreground">Next step:</span> {item.action}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </SectionPanel>
        </div>

        <SectionPanel title="Environment Health" icon={ShieldCheck}>
          {governance.isLoading ? (
            <SkeletonRows rows={6} />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[860px] text-left text-sm">
                <thead className="text-muted-foreground">
                  <tr className="border-b border-border">
                    <th className="py-3 font-medium">Namespace</th>
                    <th className="py-3 font-medium">Team</th>
                    <th className="py-3 font-medium">Age</th>
                    <th className="py-3 font-medium">Last activity</th>
                    <th className="py-3 font-medium">Status</th>
                    <th className="py-3 font-medium">What to check</th>
                    <th className="py-3 font-medium">Health</th>
                  </tr>
                </thead>
                <tbody>
                  {governance.data?.map((item) => (
                    <tr key={item.namespace} className="border-b border-border/70">
                      <td className="py-3 font-medium">{item.namespace}</td>
                      <td className="py-3 text-muted-foreground">{item.team ?? "Unassigned"}</td>
                      <td className="py-3 text-muted-foreground">{item.age_hours}h</td>
                      <td className="py-3 text-muted-foreground">
                        {item.last_activity_hours === null ? "Unknown" : `${item.last_activity_hours}h ago`}
                      </td>
                      <td className="py-3">{item.status}</td>
                      <td className="py-3 text-muted-foreground">
                        {item.violations.length === 0 ? "No action needed" : item.violations.map(friendlyViolation).join(", ")}
                      </td>
                      <td className="py-3">
                        <span className="rounded-sm bg-muted px-2 py-1 font-medium">{item.efficiency_score}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </SectionPanel>
      </div>
    </AppShell>
  );
}

