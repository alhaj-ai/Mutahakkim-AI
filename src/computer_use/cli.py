from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from computer_use.runtime import ConfigError, ensure_app, run_discover, run_replay
from computer_use.settings import load_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cu")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_disc = sub.add_parser("discover")
    p_disc.add_argument("--member-id", default="10001")
    p_disc.add_argument("--tenant", default="pine")
    p_disc.add_argument(
        "--fake",
        action="store_true",
        help="Use FakePlanner offline (explicit). Live discovery requires NVIDIA_API_KEY.",
    )
    p_rep = sub.add_parser("replay")
    p_rep.add_argument("--member-id", default="10002")
    p_rep.add_argument("--tenant", default="pine")
    p_rep.add_argument("--artifact", default="evidence/capabilities/lookup_savings_balance.v1.yaml")
    p_rep.add_argument(
        "--capability",
        default=None,
        help="Capability identifier (resolves to evidence/capabilities/<capability>.v1.yaml)",
    )
    p_rep.add_argument("--headless", action="store_true")
    sub.add_parser("handoff")
    sub.add_parser("evals")
    sub.add_parser("qualify")
    sub.add_parser("app")
    sub.add_parser("console")
    args = parser.parse_args(argv)
    settings = load_settings()

    if args.cmd in {"app", "console"}:
        print("Meridian MemberServ + operator console on", settings.bank_base_url)
        print("Console:", settings.bank_base_url.rstrip("/") + "/console/live")
        ensure_app(settings)
        try:
            while True:
                import time

                time.sleep(1)
        except KeyboardInterrupt:
            return 0

    if args.cmd == "replay":
        artifact_path = Path(args.artifact)
        if args.capability:
            cand = Path(f"evidence/capabilities/{args.capability}.v1.yaml")
            artifact_path = cand if cand.exists() else Path(args.capability)
        result = run_replay(
            member_id=args.member_id,
            tenant=args.tenant,
            artifact_path=artifact_path,
            headed=not args.headless,
            evidence_name="replay-business-outcome"
            if args.member_id == "99999"
            else "replay-permission"
            if args.member_id == "20001"
            else "replay-success",
            settings=settings,
        )
        print(result.model_dump_json(indent=2))
        return 0 if result.kind in {"success", "business_outcome"} else 1

    if args.cmd == "discover":
        try:
            result, path = run_discover(
                member_id=args.member_id,
                tenant=args.tenant,
                use_fake=args.fake,
                settings=settings,
            )
        except ConfigError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(result.model_dump_json(indent=2))
        if path:
            print("wrote", path)
        return 0 if result.kind in {"success", "business_outcome", "human_required"} else 1

    if args.cmd == "handoff":
        from computer_use.handoff_demo import run_handoff

        result = run_handoff(settings)
        print(result.model_dump_json(indent=2))
        return 0

    if args.cmd == "evals":
        from computer_use.evals import run_evals

        report = run_evals(settings)
        print(json.dumps(report, indent=2))
        return 0

    if args.cmd == "qualify":
        from computer_use.qualify import run_qualification

        report = run_qualification(settings)
        print(json.dumps(report, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
