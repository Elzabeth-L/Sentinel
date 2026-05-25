import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type {
  AzureResourceSummary,
  ClusterSummary,
  NamespaceGovernanceReport,
  OptimizationRecommendation
} from "@/lib/types";

export function useClusters() {
  return useQuery({
    queryKey: ["clusters"],
    queryFn: () => apiGet<ClusterSummary[]>("/clusters")
  });
}

export function useResources() {
  return useQuery({
    queryKey: ["resources"],
    queryFn: () => apiGet<AzureResourceSummary[]>("/resources")
  });
}

export function useGovernance(clusterId: string) {
  return useQuery({
    queryKey: ["governance", clusterId],
    queryFn: () => apiGet<NamespaceGovernanceReport[]>(`/governance/clusters/${encodeURIComponent(clusterId)}/namespaces`),
    enabled: Boolean(clusterId)
  });
}

export function useRecommendations(clusterId: string) {
  return useQuery({
    queryKey: ["recommendations", clusterId],
    queryFn: () => apiGet<OptimizationRecommendation[]>(`/recommendations/clusters/${encodeURIComponent(clusterId)}`),
    enabled: Boolean(clusterId)
  });
}
