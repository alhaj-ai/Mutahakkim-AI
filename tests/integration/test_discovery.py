from __future__ import annotations

from computer_use.discovery import DiscoveryEngine
from computer_use.evidence import EvidenceLog
from computer_use.planner import FakePlanner
from computer_use.policy import PolicyEngine
from computer_use.redaction import Redactor
from computer_use.sessions import ControlSession
from computer_use.settings import load_settings
from computer_use.surfaces import attach_surface, launch_browser


def test_offline_discovery_with_fake_planner(app_server, tmp_path):
    settings = load_settings()
    control = ControlSession("disc")
    runtime = launch_browser(headed=False, persistent=False)
    surface = attach_surface(runtime, control)
    evidence = EvidenceLog(tmp_path / "discovery", Redactor())
    engine = DiscoveryEngine(
        surface, FakePlanner(), PolicyEngine(), control, evidence, max_steps=12
    )
    try:
        result, trace = engine.run(
            "Look up member 10001 and return their current savings balance.",
            f"{settings.bank_base_url}/pine/",
            "disc",
        )
        assert result.kind in {"success", "business_outcome", "human_required"}
        assert trace.steps
        assert result.model_calls >= 0
    finally:
        runtime.close()
