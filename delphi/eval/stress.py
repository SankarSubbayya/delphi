"""Stress harness · scaling characterisation across N.

For each target N, run one swarm end-to-end and capture:

  - persona-gen wall-clock
  - reasoning wall-clock (incl. summary)
  - per-agent success rate
  - median + p95 latency per agent
  - estimated API call count and cost
  - summary-generation success

Usage:
    uv run python -m delphi.eval.stress
    uv run python -m delphi.eval.stress 20 50 100
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from delphi.modes import Mode
from delphi.personas import PersonaGenerator
from delphi.summary import summarize_swarm
from delphi.swarm import run_swarm


load_dotenv()

# Rough public pricing (per million tokens, approximate, for cost estimate only)
INPUT_PRICE_PER_M = 0.075
OUTPUT_PRICE_PER_M = 0.30
APPROX_TOKENS_PER_REASONING_CALL_IN = 800
APPROX_TOKENS_PER_REASONING_CALL_OUT = 500
APPROX_TOKENS_PER_PERSONA = 120  # output


async def stress_one(client: genai.Client, n: int, question: str, model: str) -> dict:
    print(f"[stress] N={n} starting")
    overall_t0 = time.perf_counter()

    gen_t0 = time.perf_counter()
    try:
        personas = await PersonaGenerator(client, model=model).generate(n)
    except Exception as e:
        return {"n": n, "error": f"persona-gen failed: {type(e).__name__}: {e}"}
    gen_elapsed = time.perf_counter() - gen_t0

    swarm_t0 = time.perf_counter()
    forecast = await run_swarm(
        client,
        personas,
        question,
        mode=Mode.FORECAST,
        model=model,
    )
    swarm_elapsed = time.perf_counter() - swarm_t0

    sum_t0 = time.perf_counter()
    summary = await summarize_swarm(client, forecast, personas, model)
    sum_elapsed = time.perf_counter() - sum_t0

    overall_elapsed = time.perf_counter() - overall_t0

    valid = [r for r in forecast.responses if r.position is not None]
    latencies = sorted(r.latency_ms for r in valid)
    p50 = latencies[len(latencies) // 2] if latencies else None
    p95 = latencies[int(len(latencies) * 0.95) - 1] if len(latencies) >= 20 else (
        latencies[-1] if latencies else None
    )

    in_tokens = n * APPROX_TOKENS_PER_REASONING_CALL_IN + APPROX_TOKENS_PER_PERSONA * n + 5000
    out_tokens = n * APPROX_TOKENS_PER_REASONING_CALL_OUT + APPROX_TOKENS_PER_PERSONA * n + 1500
    est_cost = (
        in_tokens / 1_000_000 * INPUT_PRICE_PER_M
        + out_tokens / 1_000_000 * OUTPUT_PRICE_PER_M
    )

    print(
        f"[stress] N={n}  total={overall_elapsed:.0f}s  "
        f"success={(n - forecast.n_failed) / n:.0%}  "
        f"p50={p50}ms"
    )

    return {
        "n": n,
        "total_seconds": round(overall_elapsed, 1),
        "persona_gen_seconds": round(gen_elapsed, 1),
        "reasoning_seconds": round(swarm_elapsed, 1),
        "summary_seconds": round(sum_elapsed, 1),
        "n_personas": forecast.n_personas,
        "n_failed": forecast.n_failed,
        "success_rate": round(
            (forecast.n_personas - forecast.n_failed) / forecast.n_personas, 3
        ),
        "median_agent_latency_ms": p50,
        "p95_agent_latency_ms": p95,
        "summary_succeeded": summary is not None,
        "estimated_cost_usd": round(est_cost, 4),
        "headline": forecast.headline,
        "confidence_interval": list(forecast.confidence_interval)
        if forecast.confidence_interval
        else None,
    }


async def run_stress(ns: list[int]) -> dict:
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    question = "Will the Fed cut interest rates in Q3 2026?"

    results = []
    for n in ns:
        out = await stress_one(client, n, question, model)
        results.append(out)

    # Hardcode the data points we already have from prior runs today.
    prior = [
        {
            "n": 200,
            "total_seconds": 207,
            "persona_gen_seconds": 110,
            "reasoning_seconds": 90,
            "summary_seconds": 10,
            "n_personas": 200,
            "n_failed": 22,
            "success_rate": 0.89,
            "source": "earlier stress run (savings rate question)",
        },
        {
            "n": 500,
            "total_seconds": 425,
            "persona_gen_seconds": 110,
            "reasoning_seconds": 290,
            "summary_seconds": 15,
            "n_personas": 500,
            "n_failed": 137,
            "success_rate": 0.726,
            "source": "live demo (Fed cut question)",
        },
    ]

    combined = {
        "model": model,
        "question": question,
        "fresh_runs": results,
        "prior_runs": prior,
    }

    out_dir = Path("eval_results")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "stress.json"
    out_path.write_text(json.dumps(combined, indent=2, default=str))
    print(f"[stress] saved {out_path}")

    print()
    print("  N    | total | gen | reason | sum | success | p50 ms | cost($)")
    print("  -----+-------+-----+--------+-----+---------+--------+--------")
    for r in results + prior:
        success_pct = f"{r.get('success_rate', 0) * 100:.0f}%"
        p50 = r.get("median_agent_latency_ms")
        p50_str = f"{p50:>5}" if p50 else "    -"
        cost = r.get("estimated_cost_usd", 0)
        print(
            f"  {r['n']:>4} | {r['total_seconds']:>4}s | "
            f"{r['persona_gen_seconds']:>3}s | {r['reasoning_seconds']:>5}s | "
            f"{r['summary_seconds']:>2}s | {success_pct:>6}  | {p50_str} | "
            f"{cost:>6.3f}"
        )

    return combined


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [50, 100]
    asyncio.run(run_stress(ns))
