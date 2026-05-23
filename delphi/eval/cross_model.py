"""Cross-model drift harness.

Run the same swarm against multiple Gemini model variants and compare
forecast convergence, reasoning latency, and per-agent success rate.

Usage:
    uv run python -m delphi.eval.cross_model
"""

import asyncio
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from delphi.modes import Mode
from delphi.personas import Persona, PersonaGenerator
from delphi.summary import summarize_swarm
from delphi.swarm import run_swarm


load_dotenv()


CANDIDATE_MODELS: list[str] = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]


async def _run_one(
    client: genai.Client,
    model: str,
    personas: list[Persona],
    question: str,
) -> dict:
    print(f"[cross-model] running model={model}")
    started = time.perf_counter()
    try:
        forecast = await run_swarm(
            client, personas, question, mode=Mode.FORECAST, model=model, use_grounding=True
        )
    except Exception as e:
        return {"model": model, "error": f"{type(e).__name__}: {e}"}
    elapsed = time.perf_counter() - started

    valid = [r for r in forecast.responses if r.position is not None]
    latencies = [r.latency_ms for r in valid]

    summary_obj = await summarize_swarm(client, forecast, personas, model)
    summary_dict = (
        {
            "headline_narrative": summary_obj.headline_narrative,
            "outlier_quote": summary_obj.outlier_quote,
            "outlier_attribution": summary_obj.outlier_attribution,
        }
        if summary_obj
        else None
    )

    return {
        "model": model,
        "elapsed_seconds": round(elapsed, 1),
        "n_personas": forecast.n_personas,
        "n_failed": forecast.n_failed,
        "success_rate": round(
            (forecast.n_personas - forecast.n_failed) / forecast.n_personas, 3
        ),
        "headline": forecast.headline,
        "confidence_interval": list(forecast.confidence_interval)
        if forecast.confidence_interval
        else None,
        "distribution": forecast.distribution,
        "median_agent_latency_ms": sorted(latencies)[len(latencies) // 2] if latencies else None,
        "mean_agent_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else None,
        "summary": summary_dict,
    }


async def run_cross_model(
    n_personas: int = 8,
    question: str = "Will US inflation stay above 3% through end of 2026?",
    models: list[str] | None = None,
    persona_seed: int = 11,
) -> dict:
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    models = models or CANDIDATE_MODELS

    print(f"[cross-model] generating {n_personas} shared personas (seed={persona_seed})")
    personas = await PersonaGenerator(client, model=models[0]).generate(
        n_personas, seed=persona_seed
    )

    print(f"[cross-model] question: {question}")
    print(f"[cross-model] models: {models}")

    results: list[dict] = []
    for m in models:
        out = await _run_one(client, m, personas, question)
        results.append(out)
        if "error" in out:
            print(f"  ✗ {m}: {out['error']}")
        else:
            h = out.get("headline")
            h_str = f"{h:.1%}" if isinstance(h, float) else str(h)
            print(
                f"  ✓ {m}: headline={h_str}  "
                f"success={out['success_rate']:.0%}  "
                f"elapsed={out['elapsed_seconds']}s"
            )

    successful = [r for r in results if "error" not in r and isinstance(r.get("headline"), float)]
    deltas = None
    if len(successful) >= 2:
        base = successful[0]
        deltas = []
        for r in successful[1:]:
            deltas.append(
                {
                    "base": base["model"],
                    "compare": r["model"],
                    "headline_delta_pp": round(
                        (r["headline"] - base["headline"]) * 100, 2
                    ),
                    "elapsed_delta_seconds": round(
                        r["elapsed_seconds"] - base["elapsed_seconds"], 1
                    ),
                    "success_rate_delta": round(
                        r["success_rate"] - base["success_rate"], 3
                    ),
                    "median_latency_delta_ms": (
                        r["median_agent_latency_ms"] - base["median_agent_latency_ms"]
                        if r["median_agent_latency_ms"] and base["median_agent_latency_ms"]
                        else None
                    ),
                }
            )

    out = {
        "question": question,
        "n_personas": n_personas,
        "models": models,
        "results": results,
        "deltas": deltas,
    }

    out_dir = Path("eval_results")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "cross_model.json"
    out_path.write_text(json.dumps(out, indent=2, default=str))
    print(f"[cross-model] saved {out_path}")

    return out


if __name__ == "__main__":
    asyncio.run(run_cross_model())
