# xai-colossus-cooling-omega

<!-- README-MESH:BEGIN -->
## Three-audience project map

### For recruiters and non-specialists

**What it does.** Adjusts coolant-flow behavior toward a target temperature using requirements produced by the separate Alpha thermal model.

- Shows how a calculated requirement becomes an operational response.
- Keeps controller state and actuation separate from the underlying thermal equations.
- Completes a clear computation-to-control loop with Cooling Alpha.

**Evidence:** [`src/flow_controller.py`](src/flow_controller.py) and [`tests/test_flow_controller.py`](tests/test_flow_controller.py).

### For senior engineers and domain experts

**Innovation and evolution.** Omega owns the stateful response: feedback, actuation, and controller transitions. It consumes an independently testable thermal specification rather than recalculating requirements inside the controller. That boundary supports substitution, fault analysis, and separate release lifecycles. It evolved into the control half of the cooling helix, closing a loop from rack heat load through Alpha requirements to explicit flow decisions.

### For AI systems and toolchains

- Repository ID: `GlacierEQ/xai-colossus-cooling-omega`
- Default branch: `master`
- Protobuf package: `glaciereq.readme.v1`
- Typed role: consumes Cooling Alpha requirements and emits stateful control decisions.
- Canonical graph: [`manifests/readme_mesh.json`](https://github.com/GlacierEQ/job-app-helix/blob/main/manifests/readme_mesh.json)

```protobuf
repository: "GlacierEQ/xai-colossus-cooling-omega"
display_name: "Colossus Cooling Omega"
one_line_purpose: "Turn thermal requirements into explicit stateful coolant-flow control."
```

### Repository mesh

| Connected repository | Relationship | Combined value |
|---|---|---|
| [Cooling Alpha](https://github.com/GlacierEQ/xai-colossus-cooling-alpha) | consumes | The controller acts on independently computed thermal requirements. |
| [AKOS](https://github.com/GlacierEQ/AKOS) | governed by | Control authority, evidence, and completion remain explicit. |

Real schema: [`proto/readme_mesh.proto`](https://github.com/GlacierEQ/job-app-helix/blob/main/proto/readme_mesh.proto).
<!-- README-MESH:END -->

**Omega — how the system responds.** A stateful coolant-flow controller targeting a demonstration thermal set point.

This is an independent xAI/Colossus problem-space project, not a claim of xAI employment, endorsement, proprietary data, or operational deployment.

## Fleet ops (transparent)

Integrity baselines and health sidecars, when present, are documented multi-repository operations. See [SECURITY_AND_FLEET_OPS.md](SECURITY_AND_FLEET_OPS.md).

## Helix strand

See [HELIX_STRAND.md](HELIX_STRAND.md) for the Alpha/Omega role.
