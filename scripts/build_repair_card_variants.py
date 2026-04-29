#!/usr/bin/env python3
"""Build provenance-separated repair-card catalogs for I-layer ablations."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "behavioral-veriloga-eval" / "docs" / "CONTRACT_REPAIR_CARDS.json"
OUT_DIR = ROOT / "behavioral-veriloga-eval" / "docs"

CODEX_SYSTEM_IDS = {
    "pll_system_feedback_graph",
    "dwa_system_rotating_window_graph",
    "pfd_bbpd_system_edge_pulse_graph",
    "adc_dac_system_quantize_reconstruct_graph",
    "serializer_system_load_shift_frame_graph",
}


def _write_variant(name: str, source: dict, cards: list[dict], description: str) -> None:
    payload = {
        "version": source.get("version", 1),
        "description": description,
        "cards": cards,
    }
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{path}: {len(cards)} cards")


def main() -> int:
    source = json.loads(SRC.read_text(encoding="utf-8"))
    cards = source.get("cards", [])
    history_cards = [card for card in cards if card.get("id") not in CODEX_SYSTEM_IDS]
    codex_cards = [card for card in cards if card.get("id") in CODEX_SYSTEM_IDS]

    _write_variant(
        "CONTRACT_REPAIR_CARDS_HISTORY_ONLY.json",
        source,
        history_cards,
        "Repair cards from historical local mechanism work and veriloga-skills. Excludes Codex-distilled system relation graph cards.",
    )
    _write_variant(
        "CONTRACT_REPAIR_CARDS_CODEX_SYSTEM_ONLY.json",
        source,
        codex_cards,
        "Repair cards distilled from Codex/system-relation analysis. Used to isolate system-graph knowledge.",
    )
    _write_variant(
        "CONTRACT_REPAIR_CARDS_FULL_PROVENANCE.json",
        source,
        cards,
        "Full repair-card catalog: historical/veriloga-skills local cards plus Codex/system-relation cards.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
