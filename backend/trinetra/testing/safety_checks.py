# backend/trinetra/testing/safety_checks.py
from typing import Dict, Any

class SafetyChecks:
    """
    Minimal safety evaluator: uses testbench+scenarios to produce a risk score.
    """
    def evaluate(self, testbench_report: Dict, scenarios_report: Dict) -> Dict[str, Any]:
        total = testbench_report.get("total", 0)
        passed = testbench_report.get("passed", 0)
        tb_score = (passed / total * 100) if total else 0
        scen_failures = sum(1 for s in scenarios_report.values() if not s.get("ok", False))
        risk = "low" if tb_score > 80 and scen_failures == 0 else ("medium" if tb_score > 50 else "high")
        return {"testbench_score": tb_score, "scenario_failures": scen_failures, "risk": risk}
