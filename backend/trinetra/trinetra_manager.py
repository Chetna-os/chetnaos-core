# backend/trinetra/trinetra_manager.py
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any

from .perception.text_sensors import TextSensor
from .perception.data_quality import DataQualityChecker
from .perception.signal_detector import SignalDetector
from .testing.agent_testbench import AgentTestbench
from .testing.scenario_runner import ScenarioRunner
from .testing.safety_checks import SafetyChecks
from .robotics.motion_simulator import MotionSimulator

LOG = logging.getLogger("trinetra.manager")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

CONFIG = {
    "simulate_motion": True,
    "max_history": 50
}

class TrinetraManager:
    """
    High-level orchestrator for Trinetra layer.
    Minimal, synchronous & asyncio-friendly interface.
    """
    def _init_(self, config: Dict[str, Any] = None):
        self.config = {**CONFIG, **(config or {})}
        self.text_sensor = TextSensor()
        self.quality = DataQualityChecker()
        self.signal = SignalDetector()
        self.testbench = AgentTestbench()
        self.scenario = ScenarioRunner()
        self.safety = SafetyChecks()
        self.motion = MotionSimulator()
        LOG.info("TrinetraManager initialized")

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Run perception pipeline for text input."""
        LOG.info("Analyze text started")
        cleaned = self.text_sensor.preprocess(text)
        quality_report = self.quality.check(cleaned)
        signals = self.signal.detect(cleaned)
        return {
            "cleaned": cleaned,
            "quality": quality_report,
            "signals": signals
        }

    async def run_tests(self, agent_callable, scenarios: list = None) -> Dict[str, Any]:
        """Run testbench and scenario runner for agent (callable receives text->response)."""
        LOG.info("Running tests")
        tb_report = self.testbench.run_smoke(agent_callable)
        scen_report = self.scenario.run(agent_callable, scenarios or [])
        safety_report = self.safety.evaluate(tb_report, scen_report)
        return {"testbench": tb_report, "scenarios": scen_report, "safety": safety_report}

    async def simulate_actuation(self, commands: list) -> Dict[str, Any]:
        """Simulate motion/actuation commands in the motion simulator."""
        LOG.info("Simulating actuation")
        if not self.config["simulate_motion"]:
            return {"simulated": False, "reason": "simulate_motion disabled"}
        results = []
        for cmd in commands:
            res = self.motion.execute(cmd)
            results.append(res)
        return {"simulated": True, "results": results}

async def demo():
    manager = TrinetraManager()
    text = "User: Interested in farmland price and booking. Please share brochure."
    perception = await manager.analyze_text(text)
    print("Perception:", perception)

    # Dummy agent: echo function
    async def dummy_agent(t):
        return f"AGENT_ECHO: {t}"

    tests = await manager.run_tests(dummy_agent, scenarios=["price_inquiry", "booking_flow"])
    print("Tests:", tests)

    act = await manager.simulate_actuation([{"move": "forward", "steps": 1}, {"pick": "sample"}])
    print("Actuation:", act)

if _name_ == "_main_":
    asyncio.run(demo())
