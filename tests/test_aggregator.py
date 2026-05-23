from delphi.agent import AgentResponse
from delphi.modes import Mode
from delphi.personas import Persona
from delphi.swarm import _bucket_probs, aggregate


def _persona(id_: str, **demo) -> Persona:
    base = {
        "age": "30-44",
        "region": "East North Central",
        "education": "bachelors",
        "income": "$75-125k",
        "occupation": "tech / knowledge work",
        "belief_axis": "centrist",
    }
    base.update(demo)
    return Persona(id=id_, label=f"p{id_}", demographics=base, identity_prompt="")


def _resp(persona_id: str, position, confidence: float = 0.7) -> AgentResponse:
    return AgentResponse(
        persona_id=persona_id,
        position=position,
        confidence=confidence,
        reasoning="",
    )


def test_bucket_probs_partitions_into_5():
    out = _bucket_probs([0.1, 0.3, 0.5, 0.7, 0.9])
    assert set(out.keys()) == {"0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"}
    assert sum(out.values()) == 1.0


def test_forecast_aggregate_computes_mean_and_ci():
    personas = [_persona(str(i)) for i in range(5)]
    responses = [
        _resp("0", 0.2),
        _resp("1", 0.4),
        _resp("2", 0.6),
        _resp("3", 0.8),
        _resp("4", 1.0),
    ]
    forecast = aggregate(responses, personas, "Q?", Mode.FORECAST)
    assert forecast.n_personas == 5
    assert forecast.n_failed == 0
    assert isinstance(forecast.headline, float)
    assert abs(forecast.headline - 0.6) < 0.01
    assert forecast.confidence_interval is not None
    lo, hi = forecast.confidence_interval
    assert 0.0 <= lo < forecast.headline < hi <= 1.0


def test_forecast_skips_failed_responses():
    personas = [_persona(str(i)) for i in range(3)]
    responses = [
        _resp("0", 0.5),
        _resp("1", None),
        _resp("2", 0.7),
    ]
    forecast = aggregate(responses, personas, "Q?", Mode.FORECAST)
    assert forecast.n_personas == 3
    assert forecast.n_failed == 1
    assert abs(forecast.headline - 0.6) < 0.01


def test_pretest_aggregate_returns_majority_label():
    personas = [_persona(str(i)) for i in range(5)]
    responses = [
        _resp("0", "positive"),
        _resp("1", "positive"),
        _resp("2", "negative"),
        _resp("3", "positive"),
        _resp("4", "neutral"),
    ]
    forecast = aggregate(responses, personas, "Tagline?", Mode.PRETEST)
    assert forecast.headline == "positive"
    assert forecast.distribution["positive"] == 0.6
    assert forecast.distribution["negative"] == 0.2
    assert forecast.distribution["neutral"] == 0.2


def test_by_demographic_groups_correctly():
    personas = [
        _persona("0", age="18-29"),
        _persona("1", age="18-29"),
        _persona("2", age="60+"),
    ]
    responses = [_resp("0", 0.9), _resp("1", 0.8), _resp("2", 0.2)]
    forecast = aggregate(responses, personas, "Q?", Mode.FORECAST)
    age_breakdown = forecast.by_demographic["age"]
    assert age_breakdown["18-29"]["n"] == 2
    assert abs(age_breakdown["18-29"]["mean"] - 0.85) < 0.01
    assert age_breakdown["60+"]["n"] == 1
    assert abs(age_breakdown["60+"]["mean"] - 0.2) < 0.01
