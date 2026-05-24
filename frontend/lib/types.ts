export type Role = "Admin" | "Platform Engineer" | "Viewer";

export interface ClusterSummary {
  id: string;
  name: string;
  subscription_id: string;
  resource_group: string;
  location: string;
  kubernetes_version: string;
  node_count: number;
  onboarding_state: string;
}

export interface NamespaceGovernanceReport {
  namespace: string;
  owner: string | null;
  team: string | null;
  environment_type: string | null;
  age_hours: number;
  ttl_hours: number | null;
  last_activity_hours: number | null;
  status: string;
  violations: string[];
  cleanup_candidate: boolean;
  efficiency_score: number;
}

export interface OptimizationRecommendation {
  id: string;
  namespace: string;
  workload: string;
  category: string;
  severity: string;
  title: string;
  explanation: string;
  deterministic_rule: string;
  estimated_monthly_waste_usd: number;
  action: string;
}

