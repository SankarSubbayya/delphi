"""End-to-end harness using a fake Gemini client.

Exercises persona generation -> swarm -> aggregator -> forecast without an API key.
"""

import json

import pytest

from delphi.modes import Mode
from delphi.personas import Persona, PersonaGenerator
from delphi.shock import re_run_with_shock
from delphi.swarm import run_swarm


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeAsyncModels:
    def __init__(self, responses: list[str]):
        self.responses = list(responses)
        self.calls: list[dict] = []

    async def generate_content(self, *, model, contents, config):
        self.calls.append({"model": model, "contents": contents})
        idx = len(self.calls) - 1
        if idx >= len(self.responses):
            return _FakeResponse(
                '{"position": 0.5, "confidence": 0.5, "reasoning": "default", "sources": []}'
            )
        return _FakeResponse(self.responses[idx])


class _FakeAio:
    def __init__(self, models: _FakeAsyncModels):
        self.models = models


class FakeClient:
    def __init__(self, responses: list[str]):
        self.aio = _FakeAio(_FakeAsyncModels(responses))


def _persona(i: int) -> Persona:
    return Persona(
        id=f"p{i}",
        label=f"Persona {i}",
        demographics={
            "age": "30-44",
            "region": "East North Central",
            "education": "bachelors",
            "income": "$75-125k",
            "occupation": "tech / knowledge work",
            "belief_axis": "centrist",
        },
        identity_prompt=f"Test persona {i}",
    )


async def test_swarm_runs_end_to_end():
    personas = [_persona(i) for i in range(5)]
    forecasts = [0.3, 0.5, 0.7, 0.9, 0.4]
    responses = [
        f'{{"position": {p}, "confidence": 0.7, "reasoning": "test", "sources": []}}'
        for p in forecasts
    ]
    client = FakeClient(responses)

    forecast = await run_swarm(
        client,
        personas,
        "Will X happen?",
        mode=Mode.FORECAST,
        use_grounding=False,
    )

    assert forecast.n_personas == 5
    assert forecast.n_failed == 0
    assert isinstance(forecast.headline, float)
    assert abs(forecast.headline - sum(forecasts) / len(forecasts)) < 0.01
    assert len(forecast.responses) == 5
    assert forecast.confidence_interval is not None


async def test_persona_generator_with_fake_client():
    payload = json.dumps(
        {
            "personas": [
                {
                    "index": i,
                    "label": f"persona-{i}",
                    "identity_prompt": f"identity for {i}",
                }
                for i in range(5)
            ]
        }
    )
    client = FakeClient([payload])
    generator = PersonaGenerator(client, model="test-model")

    personas = await generator.generate(5, seed=42)

    assert len(personas) == 5
    for i, p in enumerate(personas):
        assert p.label == f"persona-{i}"
        assert p.identity_prompt == f"identity for {i}"
        assert set(p.demographics.keys()) == {
            "age",
            "region",
            "education",
            "income",
            "occupation",
            "belief_axis",
        }


async def test_swarm_handles_malformed_agent_output():
    personas = [_persona(i) for i in range(3)]
    responses = [
        '{"position": 0.7, "confidence": 0.8, "reasoning": "ok", "sources": []}',
        "this is not json at all",
        '{"position": 0.3, "confidence": 0.5, "reasoning": "ok", "sources": []}',
    ]
    client = FakeClient(responses)

    forecast = await run_swarm(
        client,
        personas,
        "Q?",
        mode=Mode.FORECAST,
        use_grounding=False,
    )

    assert forecast.n_personas == 3
    assert forecast.n_failed == 1
    assert isinstance(forecast.headline, float)


async def test_pretest_mode_aggregates_labels():
    personas = [_persona(i) for i in range(4)]
    responses = [
        '{"position": "positive", "confidence": 0.8, "reasoning": "", "sources": []}',
        '{"position": "positive", "confidence": 0.7, "reasoning": "", "sources": []}',
        '{"position": "negative", "confidence": 0.6, "reasoning": "", "sources": []}',
        '{"position": "neutral", "confidence": 0.5, "reasoning": "", "sources": []}',
    ]
    client = FakeClient(responses)

    forecast = await run_swarm(
        client,
        personas,
        "Pretest this idea",
        mode=Mode.PRETEST,
        use_grounding=False,
    )

    assert forecast.headline == "positive"
    assert forecast.distribution["positive"] == 0.5


async def test_shock_re_runs_with_appended_context():
    personas = [_persona(i) for i in range(3)]
    before = [
        '{"position": 0.8, "confidence": 0.7, "reasoning": "", "sources": []}',
        '{"position": 0.9, "confidence": 0.8, "reasoning": "", "sources": []}',
        '{"position": 0.7, "confidence": 0.6, "reasoning": "", "sources": []}',
    ]
    after = [
        '{"position": 0.3, "confidence": 0.7, "reasoning": "", "sources": []}',
        '{"position": 0.2, "confidence": 0.8, "reasoning": "", "sources": []}',
        '{"position": 0.4, "confidence": 0.6, "reasoning": "", "sources": []}',
    ]
    client = FakeClient(before + after)

    initial = await run_swarm(
        client, personas, "Will X happen?", mode=Mode.FORECAST, use_grounding=False
    )
    shocked = await re_run_with_shock(
        client,
        personas,
        "Will X happen?",
        shock="A competitor just released the same product cheaper.",
        mode=Mode.FORECAST,
        use_grounding=False,
    )

    assert initial.headline > 0.7
    assert shocked.headline < 0.5
    later_calls = client.aio.models.calls[3:]
    assert all("NEW INFORMATION" in c["contents"] for c in later_calls)


async def test_concurrency_respects_semaphore():
    n = 20
    personas = [_persona(i) for i in range(n)]
    responses = [
        f'{{"position": {0.5 + i * 0.01}, "confidence": 0.7, "reasoning": "", "sources": []}}'
        for i in range(n)
    ]
    client = FakeClient(responses)

    forecast = await run_swarm(
        client,
        personas,
        "Q?",
        mode=Mode.FORECAST,
        concurrency=4,
        use_grounding=False,
    )

    assert forecast.n_personas == n
    assert forecast.n_failed == 0
    assert len(client.aio.models.calls) == n


def test_public_api_imports():
    from delphi import (
        AgentResponse,
        Forecast,
        Mode,
        Persona,
        PersonaGenerator,
        Source,
        aggregate,
        re_run_with_shock,
        reason_as,
        run_swarm,
    )

    assert Mode.FORECAST == "forecast"
    assert Mode.PRETEST == "pretest"
