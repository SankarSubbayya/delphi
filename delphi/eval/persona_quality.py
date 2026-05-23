"""Persona-quality eval · structural metrics on N persona-reasoning traces.

Beyond the LLM-as-judge "in-character" score in adversarial.py, this measures
hard structural signals that don't need a judge call:

  - reasoning-length distribution (mean, median, range)
  - sources-cited rate (% of agents with at least one source)
  - demographic-axis diversity (entropy across each axis)
  - position variance (std deviation of probability estimates)

Usage:
    uv run python -m delphi.eval.persona_quality
"""

import asyncio
import json
import math
import os
import statistics
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from delphi.modes import Mode
from delphi.personas import PersonaGenerator
from delphi.swarm import run_swarm


load_dotenv()


def _shannon_entropy(values: list) -> float:
    counter = Counter(values)
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum(
        (c / total) * math.log2(c / total) for c in counter.values() if c > 0
    )


def _max_entropy(values: list) -> float:
    n = len(set(values))
    return math.log2(n) if n > 1 else 1.0


async def run_persona_quality(
    n_personas: int = 30,
    question: str = "Will US household savings rate exceed 6% by end of 2026?",
) -> dict:
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    print(f"[persona-quality] N={n_personas} on {model}")
    personas = await PersonaGenerator(client, model=model).generate(n_personas)
    forecast = await run_swarm(
        client, personas, question, mode=Mode.FORECAST, model=model
    )
    print(f"  swarm: {forecast.n_personas - forecast.n_failed} / {forecast.n_personas} valid")

    valid = [r for r in forecast.responses if r.position is not None]
    by_id = {p.id: p for p in personas}

    # --- structural metrics ---
    reasoning_lengths = [len(r.reasoning) for r in valid]
    word_counts = [len(r.reasoning.split()) for r in valid]
    sources_per_agent = [len(r.sources) for r in valid]
    sources_cited_rate = sum(1 for c in sources_per_agent if c > 0) / max(len(valid), 1)
    grounded_rate = sum(1 for r in valid if r.grounded) / max(len(valid), 1)

    positions = [
        float(r.position)
        for r in valid
        if isinstance(r.position, (int, float))
    ]
    position_std = statistics.stdev(positions) if len(positions) >= 2 else 0.0
    position_range = (min(positions), max(positions)) if positions else (None, None)

    # --- demographic diversity ---
    axes = ["age", "region", "education", "income", "occupation", "belief_axis"]
    diversity: dict[str, dict] = {}
    for axis in axes:
        values = [by_id[r.persona_id].demographics.get(axis) for r in valid]
        values = [v for v in values if v is not None]
        H = _shannon_entropy(values)
        Hmax = _max_entropy(values)
        diversity[axis] = {
            "unique_values": len(set(values)),
            "shannon_entropy": round(H, 3),
            "max_entropy": round(Hmax, 3),
            "normalised": round(H / Hmax, 3) if Hmax > 0 else 0.0,
        }

    summary = {
        "model": model,
        "question": question,
        "n_personas": forecast.n_personas,
        "n_valid": len(valid),
        "structural": {
            "reasoning_length_chars": {
                "mean": round(statistics.mean(reasoning_lengths), 1) if reasoning_lengths else None,
                "median": int(statistics.median(reasoning_lengths)) if reasoning_lengths else None,
                "stdev": round(statistics.stdev(reasoning_lengths), 1) if len(reasoning_lengths) >= 2 else None,
                "min": min(reasoning_lengths) if reasoning_lengths else None,
                "max": max(reasoning_lengths) if reasoning_lengths else None,
            },
            "reasoning_word_count": {
                "mean": round(statistics.mean(word_counts), 1) if word_counts else None,
                "median": int(statistics.median(word_counts)) if word_counts else None,
            },
            "sources_cited_rate": round(sources_cited_rate, 3),
            "grounded_rate": round(grounded_rate, 3),
            "sources_per_agent": {
                "mean": round(statistics.mean(sources_per_agent), 2) if sources_per_agent else None,
                "max": max(sources_per_agent) if sources_per_agent else None,
            },
        },
        "position_variance": {
            "stdev": round(position_std, 3),
            "min": position_range[0],
            "max": position_range[1],
        },
        "demographic_diversity": diversity,
    }

    out_dir = Path("eval_results")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "persona_quality.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"[persona-quality] saved {out_path}")

    print()
    s = summary["structural"]
    print(f"  reasoning length: mean {s['reasoning_length_chars']['mean']:.0f} chars · "
          f"median {s['reasoning_length_chars']['median']} chars · "
          f"{s['reasoning_word_count']['mean']:.0f} words avg")
    print(f"  sources-cited rate: {s['sources_cited_rate']:.0%}")
    print(f"  grounded rate: {s['grounded_rate']:.0%}")
    print(f"  position stdev: {summary['position_variance']['stdev']:.3f}")
    print()
    print("  axis              | unique | entropy | norm.")
    print("  ------------------+--------+---------+------")
    for axis, d in diversity.items():
        print(f"  {axis:<17} | {d['unique_values']:>5}  | {d['shannon_entropy']:>5.2f}   | {d['normalised']:.2f}")

    return summary


if __name__ == "__main__":
    asyncio.run(run_persona_quality())
