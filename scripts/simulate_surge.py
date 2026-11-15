#!/usr/bin/env python3
"""Toy model: how surge-mode design choices change the human queue during a
live event.

Compares two strategies over the event timeline:
  standard     - normal troubleshooting flows all night
  surge_modes  - fast paths, known-issue-first during the incident,
                 minimal troubleshooting, callback offers

All inputs come from config/sim-assumptions.yaml and are ILLUSTRATIVE, not
real data. The point is the shape of the difference, not the numbers.

    python scripts/simulate_surge.py                 # summary table
    python scripts/simulate_surge.py --chart docs/surge-sim.png
    python scripts/simulate_surge.py --csv out.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def window_at(minute: int, cfg: dict) -> dict | None:
    """The spike window covering this minute; the biggest multiplier wins."""
    active = [s for s in cfg["spikes"] if s["from"] <= minute < s["to"]]
    return max(active, key=lambda s: s["multiplier"]) if active else None


def simulate(cfg: dict, strategy: str) -> list[dict]:
    step = cfg["bucket_minutes"]
    cap = cfg["human_capacity_per_bucket"]
    contain = cfg["containment"][strategy]
    repeat_rate = cfg["repeat_rate"][strategy]
    callback_rate = cfg["callback_acceptance"] if strategy == "surge_modes" else 0.0

    backlog = 0.0
    repeats = 0.0
    rows = []
    for minute in range(cfg["start_minute"], cfg["end_minute"], step):
        win = window_at(minute, cfg)
        mult = win["multiplier"] if win else 1
        mix = win["mix"] if win else cfg["default_mix"]
        incident = bool(win and win["name"] == "incident")

        arrivals = cfg["baseline_contacts_per_bucket"] * mult + repeats
        escalated = callbacks = 0.0
        for intent, share in mix.items():
            n = arrivals * share
            key = "playback_during_incident" if intent == "playback" and incident else intent
            not_contained = n * (1 - contain[key])
            # Payment failures always keep a live human lane.
            deferred = 0.0 if intent == "payment" else not_contained * callback_rate
            callbacks += deferred
            escalated += not_contained - deferred

        repeats = (escalated + callbacks) * repeat_rate
        backlog += escalated
        served = min(backlog, cap)
        backlog -= served
        wait = backlog / cap * step  # minutes a new arrival waits, roughly

        rows.append({"minute": minute, "phase": win["name"] if win else "baseline",
                     "arrivals": round(arrivals), "to_humans": round(escalated),
                     "callbacks": round(callbacks), "backlog": round(backlog),
                     "est_wait_min": round(wait, 1)})
    return rows


def summarize(rows: list[dict]) -> dict:
    return {
        "contacts": sum(r["arrivals"] for r in rows),
        "to_humans": sum(r["to_humans"] for r in rows),
        "callbacks": sum(r["callbacks"] for r in rows),
        "peak_backlog": max(r["backlog"] for r in rows),
        "peak_wait": max(r["est_wait_min"] for r in rows),
        "mins_over_10": sum(5 for r in rows if r["est_wait_min"] > 10),
    }


def chart(results: dict, cfg: dict, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, muted, grid = "#fcfcfb", "#1f1f1e", "#6b6a64", "#e6e5df"
    colors = {"standard": "#2a78d6", "surge_modes": "#eb6834"}
    labels = {"standard": "Standard flows", "surge_modes": "Surge modes"}

    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=160)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)

    inc = next(s for s in cfg["spikes"] if s["name"] == "incident")
    ax.axvspan(inc["from"], inc["to"], color="#f1efe8", zorder=0, lw=0)
    ax.text((inc["from"] + inc["to"]) / 2, 0.97, "incident", transform=ax.get_xaxis_transform(),
            ha="center", va="top", color=muted, fontsize=9)
    ax.axvline(0, color=grid, lw=1, zorder=1)
    ax.text(1, 0.97, "event starts", transform=ax.get_xaxis_transform(),
            ha="left", va="top", color=muted, fontsize=9)
    ax.axhline(10, color=muted, lw=1, ls=(0, (3, 3)), zorder=1)
    ax.text(cfg["start_minute"] + 2, 10.8, "10-min wait target", ha="left", color=muted, fontsize=8.5)

    for strat, rows in results.items():
        xs = [r["minute"] for r in rows]
        ys = [r["est_wait_min"] for r in rows]
        ax.plot(xs, ys, color=colors[strat], lw=2, label=labels[strat], zorder=3,
                solid_capstyle="round")
        peak = max(rows, key=lambda r: r["est_wait_min"])
        ax.annotate(f"{labels[strat]}: peak {peak['est_wait_min']:.0f} min",
                    (peak["minute"], peak["est_wait_min"]), xytext=(8, 4),
                    textcoords="offset points", color=ink, fontsize=9)

    ax.set_xlabel("Minutes from event start", color=muted, fontsize=9)
    ax.set_ylabel("Estimated wait for a human (min)", color=muted, fontsize=9)
    ax.set_title("Human queue wait during a live event (illustrative model)",
                 loc="left", color=ink, fontsize=11.5, pad=12)
    ax.grid(axis="y", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.tick_params(colors=muted, labelsize=8.5, length=0)
    ax.set_ylim(bottom=0)
    ax.set_xlim(cfg["start_minute"], cfg["end_minute"])
    leg = ax.legend(frameon=False, loc="upper left", fontsize=9)
    for t in leg.get_texts():
        t.set_color(ink)
    fig.tight_layout()
    fig.savefig(path, facecolor=surface)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    cfg = yaml.safe_load((ROOT / "config" / "sim-assumptions.yaml").read_text())
    results = {s: simulate(cfg, s) for s in ("standard", "surge_modes")}
    sums = {s: summarize(r) for s, r in results.items()}

    print("ILLUSTRATIVE MODEL - assumptions in config/sim-assumptions.yaml\n")
    print(f"{'':<28}{'standard':>12}{'surge modes':>14}")
    rows = [("Total contacts", "contacts"), ("Sent to live human queue", "to_humans"),
            ("Deferred to callback", "callbacks"), ("Peak queue backlog", "peak_backlog"),
            ("Peak est. wait (min)", "peak_wait"), ("Minutes with wait > 10", "mins_over_10")]
    for label, key in rows:
        print(f"{label:<28}{sums['standard'][key]:>12,}{sums['surge_modes'][key]:>14,}")

    if args.csv:
        with args.csv.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["strategy"] + list(results["standard"][0].keys()))
            for strat, rs in results.items():
                for r in rs:
                    w.writerow([strat] + list(r.values()))
        print(f"\nPer-bucket results written to {args.csv}")
    if args.chart:
        chart(results, cfg, args.chart)
        print(f"Chart written to {args.chart}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
