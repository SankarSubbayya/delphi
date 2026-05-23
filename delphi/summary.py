"""Swarm summary — synthesize N reasoning traces into a population narrative.

A single final Gemini 3.5 Flash call that turns raw agent traces into a tight,
publishable summary: headline narrative, top reasons for/against, demographic
divergence, and a striking outlier quote.
"""

import json
from dataclasses import dataclass

from google import genai
from google.genai import types
from pydantic import BaseModel

from delphi.personas import Persona
from delphi.swarm import Forecast


class _SummarySchema(BaseModel):
    headline_narrative: str
    top_reasons_for: list[str]
    top_reasons_against: list[str]
    demographic_split: str
    outlier_quote: str
    outlier_attribution: str


@dataclass
class SwarmSummary:
    headline_narrative: str
    top_reasons_for: list[str]
    top_reasons_against: list[str]
    demographic_split: str
    outlier_quote: str
    outlier_attribution: str


async def summarize_swarm(
    client: genai.Client,
    forecast: Forecast,
    personas: list[Persona],
    model: str = "gemini-3.5-flash",
    max_traces: int = 80,
) -> SwarmSummary | None:
    by_id = {p.id: p for p in personas}
    traces = []
    for r in forecast.responses[:max_traces]:
        if r.position is None:
            continue
        p = by_id.get(r.persona_id)
        if not p:
            continue
        traces.append(
            {
                "persona": p.label,
                "demographics": p.demographics,
                "position": r.position,
                "reasoning": r.reasoning,
            }
        )

    if not traces:
        return None

    if isinstance(forecast.headline, float):
        headline_str = f"{forecast.headline:.1%}"
    else:
        headline_str = str(forecast.headline)

    prompt = (
        "You are a research analyst summarizing a synthetic-population study.\n\n"
        f"QUESTION: {forecast.question}\n"
        f"MODE: {forecast.mode}\n"
        f"N AGENTS: {forecast.n_personas} (failed: {forecast.n_failed})\n"
        f"AGGREGATE: {headline_str}\n\n"
        f"Individual reasoning traces ({len(traces)} valid):\n"
        f"{json.dumps(traces, indent=2)}\n\n"
        "Produce a tight, publishable summary. Tone: Wall Street Journal lead paragraph, not "
        "marketing copy. Lean into concrete signals from the traces above. Avoid filler.\n\n"
        "Output JSON matching:\n"
        "{\n"
        '  "headline_narrative": "1-2 sentence plain-English conclusion. Lead with direction '
        '(lean yes / lean no / split) and conviction level.",\n'
        '  "top_reasons_for": ["3 short noun-phrase reasons supporting yes/positive/high"],\n'
        '  "top_reasons_against": ["3 short noun-phrase reasons against"],\n'
        '  "demographic_split": "1-2 sentences naming which demographics diverged most, with '
        'specific groups.",\n'
        '  "outlier_quote": "A single striking quote under 30 words distilled from one trace. '
        'No surrounding quotation marks.",\n'
        '  "outlier_attribution": "The persona label of that agent."\n'
        "}\n\n"
        "Respond with JSON only."
    )

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=_SummarySchema,
                temperature=0.4,
            ),
        )
        parsed = _SummarySchema.model_validate_json(response.text)
        return SwarmSummary(**parsed.model_dump())
    except Exception:
        return None
