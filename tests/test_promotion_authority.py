from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repository_known_local_hmac_promotion_is_retired() -> None:
    promotion = json.loads((ROOT / "machine" / "promotion_authority.json").read_text())
    excellence = json.loads((ROOT / "machine" / "excellence-state.json").read_text())
    assert promotion["status"] == "RETIRED"
    assert promotion["authoritative"] is False
    assert excellence["state"] == "FUNCTIONAL_CRYSTALLIZATION_CANDIDATE"
