"""Parallel swarm runner + aggregator."""

import asyncio
from collections import Counter, defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from statistics import mean, stdev

from google import genai

from delphi.agent import AgentResponse, reason_as
from delphi.modes import Mode
from delphi.personas import Persona


@dataclass
class Forecast:
    question: str
    mode: Mode
    n_personas: int
    n_failed: int
    headline: object
    confidence_interval: tuple[float, float] | None
    distribution: dict
    by_demographic: dict[str, dict]
    responses: list[AgentResponse] = field(default_factory=list)


async def run_swarm(
    client: genai.Client,
    personas: list[Persona],
    question: str,
    mode: Mode = Mode.FORECAST,
    model: str = "gemini-3.5-flash",
    concurrency: int = 50,
    use_grounding: bool = True,
    on_response: Callable[[AgentResponse], None] | None = None,
) -> Forecast:
    sem = asyncio.Semaphore(concurrency)

    async def one(p: Persona) -> AgentResponse:
        async with sem:
            r = await reason_as(client, p, question, mode, model, use_grounding)
            if on_response is not None:
                on_response(r)
            return r

    responses = await asyncio.gather(*(one(p) for p in personas))
    return aggregate(responses, personas, question, mode)


def aggregate(
    responses: list[AgentResponse],
    personas: list[Persona],
    question: str,
    mode: Mode,
) -> Forecast:
    by_id = {p.id: p for p in personas}
    valid = [r for r in responses if r.position is not None]
    n_failed = len(responses) - len(valid)

    if mode == Mode.FORECAST:
        probs = [
            float(r.position)
            for r in valid
            if isinstance(r.position, (int, float))
        ]
        if probs:
            headline = mean(probs)
            spread = stdev(probs) if len(probs) >= 2 else 0.0
            ci = (max(0.0, headline - spread), min(1.0, headline + spread))
        else:
            headline = None
            ci = None
        distribution = _bucket_probs(probs)
    else:
        positions = [str(r.position) for r in valid]
        counter = Counter(positions)
        total = sum(counter.values()) or 1
        distribution = {k: v / total for k, v in counter.items()}
        headline = counter.most_common(1)[0][0] if counter else None
        ci = None

    by_demo = _group_by_demographics(valid, by_id, mode)

    return Forecast(
        question=question,
        mode=mode,
        n_personas=len(personas),
        n_failed=n_failed,
        headline=headline,
        confidence_interval=ci,
        distribution=distribution,
        by_demographic=by_demo,
        responses=responses,
    )


def _bucket_probs(probs: list[float]) -> dict:
    buckets = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
    for p in probs:
        if p < 0.2:
            buckets["0.0-0.2"] += 1
        elif p < 0.4:
            buckets["0.2-0.4"] += 1
        elif p < 0.6:
            buckets["0.4-0.6"] += 1
        elif p < 0.8:
            buckets["0.6-0.8"] += 1
        else:
            buckets["0.8-1.0"] += 1
    total = sum(buckets.values()) or 1
    return {k: v / total for k, v in buckets.items()}


def _group_by_demographics(
    valid: list[AgentResponse],
    by_id: dict[str, Persona],
    mode: Mode,
) -> dict[str, dict]:
    axes = ["age", "region", "education", "income", "occupation", "belief_axis"]
    grouped: dict[str, dict[str, list]] = {axis: defaultdict(list) for axis in axes}
    for r in valid:
        p = by_id.get(r.persona_id)
        if not p:
            continue
        for axis in axes:
            grouped[axis][p.demographics[axis]].append(r.position)

    summary: dict[str, dict] = {}
    for axis, buckets in grouped.items():
        summary[axis] = {}
        for bucket_label, positions in buckets.items():
            if mode == Mode.FORECAST:
                nums = [float(x) for x in positions if isinstance(x, (int, float))]
                summary[axis][bucket_label] = {
                    "n": len(nums),
                    "mean": mean(nums) if nums else None,
                }
            else:
                counter = Counter(str(x) for x in positions)
                summary[axis][bucket_label] = {
                    "n": len(positions),
                    "top": counter.most_common(1)[0][0] if counter else None,
                }
    return summary
