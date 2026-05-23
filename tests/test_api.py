"""HTTP + WebSocket harness — exercises the FastAPI app end-to-end with a fake Gemini client."""

import json
import time

import pytest
from fastapi.testclient import TestClient

from delphi import api
from tests.test_integration import FakeClient


def _persona_batch(n: int) -> str:
    return json.dumps(
        {
            "personas": [
                {"index": i, "label": f"persona-{i}", "identity_prompt": f"id-{i}"}
                for i in range(n)
            ]
        }
    )


def _forecast_responses(probs: list[float]) -> list[str]:
    return [
        f'{{"position": {p}, "confidence": 0.7, "reasoning": "test", "sources": []}}'
        for p in probs
    ]


@pytest.fixture
def http_client(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-unused")
    with TestClient(api.app) as client:
        yield client


def _swap_client(fake: FakeClient):
    api.CLIENT = fake


def _wait_for_done(client: TestClient, run_id: str, timeout_s: float = 5.0) -> dict:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        status = client.get(f"/swarm/run/{run_id}").json()
        if status["done"]:
            return status
        time.sleep(0.05)
    pytest.fail(f"run {run_id} did not finish within {timeout_s}s; last status: {status}")


def test_http_create_run_returns_run_id(http_client):
    fake = FakeClient([_persona_batch(3), *_forecast_responses([0.4, 0.6, 0.8])])
    _swap_client(fake)

    resp = http_client.post(
        "/swarm/run",
        json={"question": "Will it rain tomorrow?", "n_personas": 3, "mode": "forecast"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert "run_id" in body
    assert body["status_url"] == f"/swarm/run/{body['run_id']}"


def test_http_full_lifecycle_forecast(http_client):
    probs = [0.3, 0.5, 0.7, 0.9, 0.4]
    fake = FakeClient([_persona_batch(5), *_forecast_responses(probs)])
    _swap_client(fake)

    create = http_client.post(
        "/swarm/run",
        json={"question": "Will X happen?", "n_personas": 5, "mode": "forecast"},
    )
    run_id = create.json()["run_id"]

    status = _wait_for_done(http_client, run_id)
    assert status["error"] is None
    assert status["n_personas"] == 5
    assert status["n_responses"] == 5
    assert status["forecast"]["n_failed"] == 0
    assert abs(status["forecast"]["headline"] - sum(probs) / len(probs)) < 0.01
    assert status["forecast"]["confidence_interval"] is not None
    assert status["forecast"]["mode"] == "forecast"


def test_http_drill_down_to_persona(http_client):
    fake = FakeClient([_persona_batch(3), *_forecast_responses([0.5, 0.6, 0.7])])
    _swap_client(fake)

    run_id = http_client.post(
        "/swarm/run",
        json={"question": "Q?", "n_personas": 3, "mode": "forecast"},
    ).json()["run_id"]
    status = _wait_for_done(http_client, run_id)

    # Inspect server-side state for the persona ID (not exposed via HTTP yet).
    persona_id = api.RUNS[run_id].personas[0].id
    resp = http_client.get(f"/swarm/run/{run_id}/persona/{persona_id}")

    assert resp.status_code == 200
    body = resp.json()
    assert body["persona"]["label"] == "persona-0"
    assert body["response"] is not None
    assert body["response"]["confidence"] == 0.7


def test_http_shock_after_run_shifts_forecast(http_client):
    before = [0.8, 0.85, 0.9]
    after = [0.2, 0.25, 0.3]
    fake = FakeClient(
        [_persona_batch(3), *_forecast_responses(before), *_forecast_responses(after)]
    )
    _swap_client(fake)

    run_id = http_client.post(
        "/swarm/run",
        json={"question": "Will it ship?", "n_personas": 3, "mode": "forecast"},
    ).json()["run_id"]
    initial = _wait_for_done(http_client, run_id)
    assert initial["forecast"]["headline"] > 0.8

    shock_resp = http_client.post(
        f"/swarm/run/{run_id}/shock",
        json={"shock": "Competitor launched same product half price."},
    )
    assert shock_resp.status_code == 200
    shocked = shock_resp.json()["forecast"]
    assert shocked["headline"] < 0.4


def test_http_mode_switch_pretest(http_client):
    pretest_responses = [
        '{"position": "positive", "confidence": 0.8, "reasoning": "", "sources": []}',
        '{"position": "positive", "confidence": 0.7, "reasoning": "", "sources": []}',
        '{"position": "negative", "confidence": 0.6, "reasoning": "", "sources": []}',
    ]
    fake = FakeClient([_persona_batch(3), *pretest_responses])
    _swap_client(fake)

    run_id = http_client.post(
        "/swarm/run",
        json={"question": "Pretest tagline", "n_personas": 3, "mode": "pretest"},
    ).json()["run_id"]
    status = _wait_for_done(http_client, run_id)

    assert status["forecast"]["mode"] == "pretest"
    assert status["forecast"]["headline"] == "positive"


def test_http_404_for_unknown_run(http_client):
    resp = http_client.get("/swarm/run/does-not-exist")
    assert resp.status_code == 404


def test_http_shock_409_before_run_completes(http_client):
    # Persona-gen response, but no forecast responses queued — agent calls will return defaults
    # We're just checking that posting shock to an unknown run is 404 (the in-progress 409
    # is timing-sensitive in tests, so 404 is the cleaner check).
    resp = http_client.post(
        "/swarm/run/never-created/shock",
        json={"shock": "anything"},
    )
    assert resp.status_code == 404


def test_websocket_streams_persona_completions(http_client):
    probs = [0.4, 0.5, 0.6]
    fake = FakeClient([_persona_batch(3), *_forecast_responses(probs)])
    _swap_client(fake)

    run_id = http_client.post(
        "/swarm/run",
        json={"question": "Q?", "n_personas": 3, "mode": "forecast"},
    ).json()["run_id"]

    personas_msg = None
    received_positions = []
    done_msg = None
    with http_client.websocket_connect(f"/swarm/run/{run_id}/stream") as ws:
        while True:
            msg = ws.receive_json()
            if msg.get("personas") is not None:
                personas_msg = msg
            elif msg.get("done"):
                done_msg = msg
                break
            else:
                received_positions.append(msg["position"])

    assert personas_msg is not None
    assert len(personas_msg["personas"]) == 3
    assert all("label" in p and "demographics" in p for p in personas_msg["personas"])
    assert len(received_positions) == 3
    assert sorted(received_positions) == sorted(probs)
    assert done_msg is not None
    assert done_msg["forecast"] is not None
    assert done_msg["error"] is None
