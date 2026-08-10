<<<<<<< HEAD
# Cooling Omega — Modeled Flow-Control Policy
=======
# xAI Colossus Cooling Omega — Secondary/Emergency Cooling Systems 🌊

> **Backup and emergency thermal management with dry cooler failover and ambient cooling activation.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![Domain](https://img.shields.io/badge/Domain-Emergency%20Cooling-cyan)]()
>>>>>>> 19af744 (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)

A small stateful control-policy component that converts modeled temperature observations into bounded normalized flow decisions.

<<<<<<< HEAD
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
=======
## 🎯 For Recruiters & Hiring Managers

This is the **secondary and emergency cooling system** — the failover layer that activates when primary cooling degrades or fails. It demonstrates:

- **Redundant system design** with automatic failover detection and activation
- **Emergency shutdown sequences** for controlled GPU thermal throttling under cooling loss
- **Dry cooler management** for ambient air cooling when chilled water is unavailable
- **Health monitoring** of backup pumps, fans, and cooling tower capacity

**Why this matters**: Emergency systems engineering requires the **highest reliability standards** — the same design discipline used in aviation backup systems, hospital power, and nuclear safety systems.

---

## 🔬 For Engineers & Technical Reviewers

### Core Components

| Component | Language | Purpose |
|---|---|---|
| `src/cooling_omega.py` | Python | Emergency controller, dry cooler management, failover FSM |
| `tests/` | Python | Primary cooling failure scenarios with thermal cascade simulation |

---

## 🤖 ML/AI & Programmatic Mesh Integration

- **MCP Tool**: `emergency_status()` — backup system readiness queryable by agents
- **Mastermind Sidecar**: Publishes emergency alerts to APEX Highway mesh
- **AI Extension**: Predictive failure model estimating time-to-thermal-emergency from degradation trends

```python
status = await mcp_client.call_tool("colossus-cooling-omega", "emergency_readiness")
```

---

## ⚡ Quick Start

```bash
python3 src/cooling_omega.py
python3 tests/test_cooling_omega.py
```
>>>>>>> 19af744 (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)
