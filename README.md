# Cooling Omega — Modeled Flow-Control Policy

A small stateful control-policy component that converts modeled temperature observations into bounded normalized flow decisions.

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It does not claim proprietary Colossus data, facility access, live telemetry, or physical actuator authority.

## Recruiter view

The canonical public implementation is [`src/flow_controller.py`](src/flow_controller.py). It maintains a PID-like local state and produces normalized `0..1` flow outputs from caller-supplied temperature values.

Current verified behavior:

- computes proportional/integral/derivative-style response terms;
- clamps integral state and output bounds;
- returns deterministic modeled flow decisions for a supplied temperature sequence;
- performs no network queries, telemetry reads, pump/valve commands, or external actions.

The output is a **modeled controller decision**, not hardware actuation.

## Engineering boundary

```text
caller-supplied temperature sequence
              │
              ▼
       src/flow_controller.py
              │
              ▼
 normalized local flow decisions (0..1)
```

Canonical proof paths:

| Path | Role |
|---|---|
| `src/flow_controller.py` | stateful bounded local control policy |
| `tests/test_flow_controller.py` | deterministic response check |
| `scripts/verify_public_core.py` | receipt-producing public verifier |
| `.github/workflows/ci.yml` | exact-branch Python truth gate |

Older root-level experiments, integrity artifacts, and integration-oriented files remain preserved but are not automatically promoted by this contract.

## Alpha / Omega relationship

Omega is architecturally paired with [`xai-colossus-cooling-alpha`](https://github.com/GlacierEQ/xai-colossus-cooling-alpha). Alpha evaluates a thermal envelope; Omega models a stateful response. There is no claimed live cross-repository runtime, shared facility telemetry stream, or physical actuator connection.

## Verify

```bash
python tests/test_flow_controller.py
python scripts/verify_public_core.py
```

## Machine contract

```yaml
schema: glaciereq.component-surface.v1
repository: GlacierEQ/xai-colossus-cooling-omega
canonical_branch: master
role: SPECIALIST_COMPONENT
capability: modeled_flow_control_policy
evidence_level: TEST
external_queries: 0
external_actions: 0
live_telemetry: false
hardware_actuation: false
runtime_pairing_with_alpha: false
company_affiliation_claim: false
```

## Nonclaims

This repository does not establish xAI affiliation, proprietary access, production deployment, live Colossus telemetry, pump/valve/chiller actuation, physical-system safety, measured cooling efficiency, or validation at a specific GPU/MW/rack scale.
