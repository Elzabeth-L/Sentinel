from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
@router.get("/console", include_in_schema=False)
def demo_console() -> HTMLResponse:
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sentinel Console</title>
    <style>
      :root {
        --bg: #f6f8fb;
        --panel: #ffffff;
        --ink: #142033;
        --muted: #64748b;
        --line: #dbe3ee;
        --blue: #1f78d1;
        --green: #1b9366;
        --amber: #c77904;
        --red: #cc3b3b;
        --teal: #0f9c95;
        --violet: #7763d8;
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        min-height: 100vh;
        background: var(--bg);
        color: var(--ink);
        font-size: 16px;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      .shell {
        display: grid;
        grid-template-columns: 232px minmax(0, 1fr);
        min-height: 100vh;
      }

      aside {
        border-right: 1px solid var(--line);
        background: #0f172a;
        color: #f8fafc;
        padding: 22px 18px;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 28px;
      }

      .brand-mark {
        display: grid;
        width: 42px;
        height: 42px;
        place-items: center;
        border-radius: 8px;
        background: #2dd4bf;
        color: #082f49;
        font-weight: 800;
        font-size: 14px;
      }

      .brand-title { font-weight: 750; font-size: 15px; }
      .brand-subtitle { margin-top: 2px; color: #a8b3c7; font-size: 13px; }

      nav {
        display: grid;
        gap: 8px;
      }

      nav a {
        border-radius: 8px;
        color: #cbd5e1;
        padding: 10px 12px;
        text-decoration: none;
        font-size: 15px;
      }

      nav a.active,
      nav a:hover {
        background: rgba(255, 255, 255, 0.08);
        color: #ffffff;
      }

      main {
        width: min(1280px, 100%);
        margin: 0 auto;
        padding: 28px 32px 40px;
      }

      .topbar {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 18px;
        margin-bottom: 22px;
      }

      .eyebrow {
        color: var(--teal);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0;
        margin: 0 0 6px;
      }

      h1 {
        margin: 0;
        max-width: 780px;
        font-size: 34px;
        line-height: 1.15;
      }

      .lead {
        max-width: 780px;
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 16px;
        line-height: 1.6;
      }

      .cluster-pill {
        min-width: 230px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 12px 14px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
      }

      .cluster-pill small {
        display: block;
        color: var(--muted);
        margin-top: 2px;
      }

      .grid {
        display: grid;
        gap: 16px;
      }

      .kpis {
        grid-template-columns: repeat(4, minmax(0, 1fr));
        margin-bottom: 16px;
      }

      .card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 18px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
      }

      .kpi-label {
        color: var(--muted);
        font-size: 14px;
      }

      .kpi-value {
        margin-top: 10px;
        font-size: 28px;
        font-weight: 780;
      }

      .kpi-note {
        margin-top: 6px;
        color: var(--muted);
        font-size: 14px;
      }

      .two-col {
        grid-template-columns: minmax(0, 1fr);
        align-items: start;
      }

      .section-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 14px;
      }

      h2 {
        margin: 0;
        font-size: 20px;
      }

      .hint {
        color: var(--muted);
        font-size: 14px;
      }

      .namespace-list,
      .recommendation-list {
        display: grid;
        gap: 12px;
      }

      .namespace,
      .recommendation {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #fbfdff;
        padding: 14px;
      }

      .row {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 14px;
      }

      .name {
        font-weight: 760;
      }

      .meta {
        margin-top: 4px;
        color: var(--muted);
        font-size: 13px;
      }

      .badge {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        border: 1px solid var(--line);
        padding: 4px 9px;
        font-size: 12px;
        font-weight: 700;
        white-space: nowrap;
      }

      .badge.high, .badge.cleanup { color: var(--red); background: #fff2f2; border-color: #ffd0d0; }
      .badge.medium, .badge.attention { color: var(--amber); background: #fff8e8; border-color: #ffe2a8; }
      .badge.low, .badge.healthy { color: var(--green); background: #eefcf5; border-color: #b9efd3; }
      .badge.info { color: var(--blue); background: #eef6ff; border-color: #c6def8; }

      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
      }

      .chip {
        border-radius: 999px;
        background: #eef2f7;
        color: #475569;
        padding: 5px 9px;
        font-size: 12px;
      }

      .explain {
        display: grid;
        gap: 8px;
        margin-top: 12px;
        color: #334155;
        font-size: 14px;
        line-height: 1.48;
      }

      .explain strong {
        color: var(--ink);
      }

      .progress {
        height: 9px;
        margin-top: 12px;
        overflow: hidden;
        border-radius: 999px;
        background: #e8edf5;
      }

      .progress span {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--teal), var(--blue));
      }

      .empty {
        border: 1px dashed var(--line);
        border-radius: 8px;
        padding: 18px;
        color: var(--muted);
        text-align: center;
      }

      .loading {
        animation: pulse 1.4s ease-in-out infinite;
        background: #e8edf5;
        border-radius: 8px;
        height: 72px;
      }

      @keyframes pulse {
        0%, 100% { opacity: 0.55; }
        50% { opacity: 1; }
      }

      @media (max-width: 960px) {
        .shell { grid-template-columns: 1fr; }
        aside { position: static; }
        .kpis, .two-col { grid-template-columns: 1fr; }
        .topbar { flex-direction: column; }
        .cluster-pill { width: 100%; }
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <aside>
        <div class="brand">
          <div class="brand-mark">AKS</div>
          <div>
            <div class="brand-title">Governance Console</div>
            <div class="brand-subtitle">Demo preview mode</div>
          </div>
        </div>
        <nav>
          <a class="active" href="#overview">Overview</a>
          <a href="#governance">Environment health</a>
          <a href="#recommendations">Recommendations</a>
          <a href="/docs">API docs</a>
        </nav>
      </aside>
      <main>
        <section class="topbar" id="overview">
          <div>
            <p class="eyebrow">AKS environment governance</p>
            <h1>Understand what needs attention, why it matters, and what to do next.</h1>
            <p class="lead">
              This view translates raw Kubernetes and Azure signals into clear cleanup candidates,
              ownership gaps, and resource optimization actions. It uses the same API data you tested in Swagger.
            </p>
          </div>
          <div class="cluster-pill">
            <strong id="clusterName">Loading cluster</strong>
            <small id="clusterMeta">Connecting to demo API</small>
          </div>
        </section>

        <section class="grid kpis">
          <div class="card">
            <div class="kpi-label">Namespaces reviewed</div>
            <div class="kpi-value" id="namespaceCount">-</div>
            <div class="kpi-note">Lifecycle metadata checked</div>
          </div>
          <div class="card">
            <div class="kpi-label">Cleanup candidates</div>
            <div class="kpi-value" id="cleanupCount">-</div>
            <div class="kpi-note">Safe candidates to review</div>
          </div>
          <div class="card">
            <div class="kpi-label">Average health score</div>
            <div class="kpi-value" id="avgScore">-</div>
            <div class="kpi-note">Higher means cleaner ownership</div>
          </div>
          <div class="card">
            <div class="kpi-label">Estimated waste signal</div>
            <div class="kpi-value" id="waste">$-</div>
            <div class="kpi-note">Monthly rule-based estimate</div>
          </div>
        </section>

        <section class="grid two-col">
          <div class="card" id="governance">
            <div class="section-title">
              <h2>Environment health</h2>
              <span class="hint">Sorted by most actionable first</span>
            </div>
            <div class="namespace-list" id="namespaceList">
              <div class="loading"></div>
              <div class="loading"></div>
              <div class="loading"></div>
            </div>
          </div>

          <div class="card" id="recommendations">
            <div class="section-title">
              <h2>Optimization recommendations</h2>
              <span class="hint">Explainable rules only</span>
            </div>
            <div class="recommendation-list" id="recommendationList">
              <div class="loading"></div>
              <div class="loading"></div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <script>
      const headers = { Authorization: "Bearer demo-token" };

      function statusClass(status) {
        if (status === "Cleanup Candidate") return "cleanup";
        if (status === "Needs Attention") return "attention";
        return "healthy";
      }

      function severityClass(severity) {
        return severity.toLowerCase();
      }

      function friendlyViolation(violation) {
        const labels = {
          "missing-owner": "No owner tag",
          "ttl-expired": "TTL expired",
          "missing-activity-signal": "No activity signal",
          "inactive-namespace": "Inactive for too long",
          "scaled-to-zero-or-broken-workloads": "Workloads need review"
        };
        return labels[violation] || violation;
      }

      function explainNamespace(item) {
        if (item.cleanup_candidate) {
          return "This namespace looks stale or past its approved lifetime. Review ownership, confirm it is no longer needed, then schedule cleanup.";
        }
        if (item.violations.length > 0) {
          return "This namespace is still usable, but it is missing governance metadata or activity signals that make lifecycle decisions harder.";
        }
        return "This namespace has healthy ownership and recent activity signals.";
      }

      function nextStepForNamespace(item) {
        if (item.violations.includes("missing-owner")) return "Add an owner annotation before cleanup decisions are made.";
        if (item.cleanup_candidate) return "Ask the owning team to confirm deletion or extend the TTL with a reason.";
        return "No immediate action needed. Keep monitoring TTL and activity.";
      }

      function renderNamespaces(namespaces) {
        const list = document.getElementById("namespaceList");
        if (!namespaces.length) {
          list.innerHTML = '<div class="empty">No namespaces found.</div>';
          return;
        }

        list.innerHTML = namespaces.map((item) => `
          <article class="namespace">
            <div class="row">
              <div>
                <div class="name">${item.namespace}</div>
                <div class="meta">${item.team || "Unassigned team"} - ${item.environment_type || "unknown"} - owner ${item.owner || "missing"}</div>
              </div>
              <span class="badge ${statusClass(item.status)}">${item.status}</span>
            </div>
            <div class="progress" aria-label="Efficiency score">
              <span style="width: ${item.efficiency_score}%"></span>
            </div>
            <div class="chips">
              <span class="chip">Score ${item.efficiency_score}</span>
              <span class="chip">Age ${item.age_hours}h</span>
              <span class="chip">Last activity ${item.last_activity_hours === null ? "unknown" : item.last_activity_hours + "h ago"}</span>
              ${item.violations.map((violation) => `<span class="chip">${friendlyViolation(violation)}</span>`).join("")}
            </div>
            <div class="explain">
              <div><strong>What this means:</strong> ${explainNamespace(item)}</div>
              <div><strong>Next step:</strong> ${nextStepForNamespace(item)}</div>
            </div>
          </article>
        `).join("");
      }

      function renderRecommendations(recommendations) {
        const list = document.getElementById("recommendationList");
        if (!recommendations.length) {
          list.innerHTML = '<div class="empty">No recommendations right now.</div>';
          return;
        }

        list.innerHTML = recommendations.map((item) => `
          <article class="recommendation">
            <div class="row">
              <div>
                <div class="name">${item.title}</div>
                <div class="meta">${item.namespace} / ${item.workload} - ${item.category}</div>
              </div>
              <span class="badge ${severityClass(item.severity)}">${item.severity}</span>
            </div>
            <div class="explain">
              <div><strong>Why it matters:</strong> ${item.explanation}</div>
              <div><strong>Recommended action:</strong> ${item.action}</div>
              <div><strong>Rule used:</strong> ${item.deterministic_rule}</div>
              <div><strong>Waste signal:</strong> $${item.estimated_monthly_waste_usd.toFixed(2)} per month</div>
            </div>
          </article>
        `).join("");
      }

      async function loadConsole() {
        try {
          const clusters = await fetch("/api/v1/clusters", { headers }).then((response) => response.json());
          const cluster = clusters[0] || { id: "demo", name: "demo", location: "local", node_count: 0 };
          document.getElementById("clusterName").textContent = cluster.name;
          document.getElementById("clusterMeta").textContent = `${cluster.location} - ${cluster.node_count} nodes - ${cluster.onboarding_state}`;

          const clusterId = "demo";
          const namespaces = await fetch(`/api/v1/governance/clusters/${clusterId}/namespaces`, { headers }).then((response) => response.json());
          const recommendations = await fetch(`/api/v1/recommendations/clusters/${clusterId}`, { headers }).then((response) => response.json());

          const cleanupCount = namespaces.filter((item) => item.cleanup_candidate).length;
          const avgScore = namespaces.length
            ? Math.round(namespaces.reduce((sum, item) => sum + item.efficiency_score, 0) / namespaces.length)
            : 0;
          const waste = recommendations.reduce((sum, item) => sum + item.estimated_monthly_waste_usd, 0);

          document.getElementById("namespaceCount").textContent = namespaces.length;
          document.getElementById("cleanupCount").textContent = cleanupCount;
          document.getElementById("avgScore").textContent = `${avgScore}%`;
          document.getElementById("waste").textContent = `$${Math.round(waste)}`;

          renderNamespaces(namespaces);
          renderRecommendations(recommendations);
        } catch (error) {
          document.getElementById("namespaceList").innerHTML = '<div class="empty">Could not load governance data. Confirm the backend was restarted after the UI update.</div>';
          document.getElementById("recommendationList").innerHTML = '<div class="empty">Recommendations are unavailable right now.</div>';
        }
      }

      loadConsole();
    </script>
  </body>
</html>
        """
    )
