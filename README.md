# Cooling Omega — Stateful Thermal Response Policy

**Installable, deterministic local response-policy simulation for converting modeled temperature error into a bounded normalized cooling-demand fraction.**

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It has no facility telemetry, pump/valve/chiller access, emergency authority, or physical-system safety role.

Evidence state: `LOCAL_STATEFUL_COOLING_RESPONSE_POLICY_NOT_XAI_HARDWARE_CONTROL`

## What the product does

The canonical product is `src/flow_controller.py`. It implements a transparent stateful response policy:

- explicit target temperature and P/I/D gains;
- finite-input validation and strict `dt > 0` refusal;
- first-sample derivative suppression so the initial observation does not manufacture derivative kick;
- bounded integral state with anti-windup clamp;
- explicit proportional, integral, derivative, feedforward, raw, and clamped output terms;
- deterministic saturation/review reasons and SHA-256 decision receipts;
- reset and state-inspection semantics;
- normalized output bounded to `[0, 1]`, representing **modeled cooling-demand fraction**, not a hardware command;
- optional caller-supplied Alpha-style requirement feedforward, computed only from `required_flow_lpm / design_flow_lpm` supplied as numbers. No cross-repository import, network call, or live runtime pairing occurs.

The historical `PID` class and `control_loop()` function remain compatibility surfaces. Their values are still local modeled outputs, never actuator commands.

## Alpha / Omega boundary

Cooling Alpha answers: **what steady-state flow requirement follows from a modeled heat load and temperature-rise envelope?**

Cooling Omega answers: **how could a bounded stateful response policy adjust normalized demand around a caller-provided baseline as modeled temperature changes?**

A caller may transform an Alpha-style requirement into Omega feedforward with:

```python
from flow_controller import feedforward_from_requirement
fraction = feedforward_from_requirement(required_flow_lpm=48000, design_flow_lpm=60000)
```

That arithmetic bridge is intentionally data-only. `runtime_pairing_with_alpha: false` remains part of every product receipt.

## Install and run

```bash
python -m pip install .
cooling-omega-simulate --temperatures 40,43,46,44,41 --feedforward 0.50
python scripts/operate.py
```

## Python API

```python
from flow_controller import PolicyConfig, ResponsePolicy

policy = ResponsePolicy(PolicyConfig(target_c=42.0))
receipt = policy.step(46.0, dt=1.0, feedforward_fraction=0.5)
print(receipt["output_fraction"])
print(policy.state())
policy.reset()
```

## Historical material

Root-level legacy failover/emergency/controller documents and old promotion receipts remain for lineage. They are not imported by the installed product and do not establish automatic failover, backup pumps, emergency shutdown, GPU throttling, dry-cooler/chilled-water control, live health monitoring, neural prediction, Mastermind/APEX alerts, or MCP tools.

The previous local HMAC `PROMOTED` mechanism used a repository-known reference secret and is retired. A repository signing its own status with a published secret proves only that hashes are very obedient creatures.

## Verify

```bash
python -m pytest -q
python scripts/verify_public_core.py
```

CI builds and installs the exact wheel, executes the installed CLI and direct operator on Python 3.11 and 3.13, rejects merge-conflict markers and unsupported public claims, and enforces an empty material gap matrix.

## Evidence boundary

This repository does **not** establish:

- xAI affiliation, proprietary facility access, deployment, or production data;
- backup/emergency cooling equipment or automatic failover;
- pump, valve, fan, cooling-tower, chiller, dry-cooler, GPU-throttle, or shutdown actuation;
- physical PID tuning, plant identification, transient calibration, or control-loop stability for real equipment;
- measured PUE, production efficiency, reliability, availability, or safety performance;
- live Alpha runtime pairing, telemetry, MCP, APEX, AKOS, Mastermind, or agent-mesh connectivity.

The complete product is a local **stateful normalized response-policy simulator**, not an emergency cooling controller.
