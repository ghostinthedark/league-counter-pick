"""Deprecated: premium guides now live in data/counters/matchups.json.

Kept as a thin stub so older scripts importing generate_guide fail clearly.
"""

from __future__ import annotations

from typing import Any


def generate_guide(_detail: dict[str, Any]) -> dict[str, Any]:
    raise RuntimeError(
        "Auto-generated guides are disabled. Regenerate data/counters/matchups.json "
        "with scripts/merge_and_generate.py instead."
    )
