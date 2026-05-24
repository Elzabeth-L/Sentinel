from app.services.demo_data import DEMO_METRICS, DEMO_WORKLOADS
from app.services.optimization_engine import OptimizationEngine


def test_optimization_engine_returns_explainable_recommendations() -> None:
    recommendations = OptimizationEngine().evaluate(DEMO_WORKLOADS, DEMO_METRICS)

    assert recommendations
    assert all(item.deterministic_rule for item in recommendations)
    assert any(item.category == "Rightsizing" for item in recommendations)
    assert any(item.category == "Governance" for item in recommendations)

