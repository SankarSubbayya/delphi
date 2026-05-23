"""Single reasoning sub-agent — one Gemini 3.5 Flash call per persona."""

import asyncio
import json
import re
import time
from dataclasses import dataclass, field

from google import genai
from google.genai import types

from delphi.modes import REASONING_TEMPLATES, Mode
from delphi.personas import Persona


@dataclass
class Source:
    url: str = ""
    title: str = ""
    snippet: str = ""


@dataclass
class AgentResponse:
    persona_id: str
    position: object
    confidence: float
    reasoning: str
    sources: list[Source] = field(default_factory=list)
    grounded: bool = False
    latency_ms: int = 0


_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(text: str) -> dict:
    if not text:
        return {}
    match = _JSON_BLOCK.search(text)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


async def reason_as(
    client: genai.Client,
    persona: Persona,
    question: str,
    mode: Mode = Mode.FORECAST,
    model: str = "gemini-3.5-flash",
    use_grounding: bool = True,
    timeout_s: float = 25.0,
) -> AgentResponse:
    prompt = REASONING_TEMPLATES[mode].format(
        persona_label=persona.label,
        persona_identity=persona.identity_prompt,
        question=question,
    )

    tools = [types.Tool(google_search=types.GoogleSearch())] if use_grounding else []

    started = time.perf_counter()
    try:
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=tools,
                    temperature=0.7,
                ),
            ),
            timeout=timeout_s,
        )
    except (asyncio.TimeoutError, Exception) as e:
        return AgentResponse(
            persona_id=persona.id,
            position=None,
            confidence=0.0,
            reasoning=f"[agent failed: {type(e).__name__}: {e}]",
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    latency_ms = int((time.perf_counter() - started) * 1000)
    data = _extract_json(response.text or "")
    sources = [
        Source(**{k: str(v) for k, v in s.items() if k in {"url", "title", "snippet"}})
        for s in data.get("sources", [])
        if isinstance(s, dict)
    ]
    return AgentResponse(
        persona_id=persona.id,
        position=data.get("position"),
        confidence=float(data.get("confidence", 0.5) or 0.5),
        reasoning=str(data.get("reasoning", "")),
        sources=sources,
        grounded=bool(tools) and bool(sources),
        latency_ms=latency_ms,
    )
