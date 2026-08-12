"""Installed CLI for the local Cooling Omega response policy."""
from __future__ import annotations

import argparse
import json

from flow_controller import PolicyConfig, feedforward_from_requirement, simulate


def _temperatures(value: str) -> list[float]:
    try:
        rows = [float(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("temperatures must be comma-separated numbers") from exc
    if not rows:
        raise argparse.ArgumentTypeError("at least one temperature is required")
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulate a bounded local thermal response policy")
    parser.add_argument("--temperatures", type=_temperatures, default=_temperatures("40,43,46,44,41"))
    parser.add_argument("--target-c", type=float, default=42.0)
    parser.add_argument("--kp", type=float, default=0.08)
    parser.add_argument("--ki", type=float, default=0.02)
    parser.add_argument("--kd", type=float, default=0.01)
    parser.add_argument("--dt", type=float, default=1.0)
    parser.add_argument("--feedforward", type=float, default=None)
    parser.add_argument("--required-flow-lpm", type=float, default=None)
    parser.add_argument("--design-flow-lpm", type=float, default=None)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(argv)

    direct_ff = args.feedforward
    flow_pair = args.required_flow_lpm is not None or args.design_flow_lpm is not None
    if direct_ff is not None and flow_pair:
        parser.error("use either --feedforward or the required/design flow pair, not both")
    if flow_pair and (args.required_flow_lpm is None or args.design_flow_lpm is None):
        parser.error("--required-flow-lpm and --design-flow-lpm must be supplied together")

    bridge = None
    if flow_pair:
        bridge = feedforward_from_requirement(args.required_flow_lpm, args.design_flow_lpm)
        feedforward = bridge["feedforward_fraction"]
    else:
        feedforward = 0.0 if direct_ff is None else direct_ff

    result = simulate(
        args.temperatures,
        config=PolicyConfig(target_c=args.target_c, kp=args.kp, ki=args.ki, kd=args.kd),
        dt=args.dt,
        feedforward_fraction=feedforward,
    )
    if bridge is not None:
        result["feedforward_bridge"] = bridge
    print(json.dumps(result, sort_keys=True, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
