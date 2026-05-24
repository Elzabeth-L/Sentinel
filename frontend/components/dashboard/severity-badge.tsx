import { cn } from "@/lib/utils";

export function SeverityBadge({ severity }: { severity: string }) {
  const tone =
    severity === "High"
      ? "border-destructive/30 bg-destructive/10 text-destructive"
      : severity === "Medium"
        ? "border-warning/30 bg-warning/10 text-warning"
        : "border-success/30 bg-success/10 text-success";

  return <span className={cn("rounded-sm border px-2 py-1 text-xs font-medium", tone)}>{severity}</span>;
}

