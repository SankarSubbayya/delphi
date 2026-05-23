"""FastAPI app — REST + WebSocket for the web UI.

Run with: uvicorn delphi.api:app --reload
"""

import asyncio
import os
import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

from delphi.agent import AgentResponse
from delphi.modes import Mode
from delphi.personas import Persona, PersonaGenerator
from delphi.shock import re_run_with_shock
from delphi.summary import SwarmSummary, summarize_swarm
from delphi.swarm import Forecast, run_swarm


load_dotenv()


class RunState:
    def __init__(self, question: str, mode: Mode):
        self.question = question
        self.mode = mode
        self.personas: list[Persona] = []
        self.responses: list[AgentResponse] = []
        self.forecast: Forecast | None = None
        self.summary: SwarmSummary | None = None
        self.done: bool = False
        self.error: str | None = None


RUNS: dict[str, RunState] = {}
CLIENT: genai.Client | None = None
MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global CLIENT
    CLIENT = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    yield


app = FastAPI(title="Delphi", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000", "http://127.0.0.1:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    question: str
    n_personas: int = 100
    mode: Mode = Mode.FORECAST


class ShockRequest(BaseModel):
    shock: str


async def _execute_run(run_id: str, n_personas: int):
    state = RUNS[run_id]
    try:
        assert CLIENT is not None
        generator = PersonaGenerator(CLIENT, model=MODEL)
        state.personas = await generator.generate(n_personas)
        state.forecast = await run_swarm(
            CLIENT,
            state.personas,
            state.question,
            mode=state.mode,
            model=MODEL,
            on_response=state.responses.append,
        )
        state.summary = await summarize_swarm(
            CLIENT, state.forecast, state.personas, MODEL
        )
    except Exception as e:
        state.error = f"{type(e).__name__}: {e}"
    finally:
        state.done = True


@app.post("/swarm/run")
async def create_run(req: RunRequest):
    run_id = str(uuid.uuid4())
    RUNS[run_id] = RunState(req.question, req.mode)
    asyncio.create_task(_execute_run(run_id, req.n_personas))
    return {"run_id": run_id, "status_url": f"/swarm/run/{run_id}"}


@app.get("/swarm/run/{run_id}")
async def get_run(run_id: str):
    state = RUNS.get(run_id)
    if state is None:
        raise HTTPException(404, "run not found")
    return {
        "run_id": run_id,
        "question": state.question,
        "mode": state.mode,
        "done": state.done,
        "error": state.error,
        "n_responses": len(state.responses),
        "n_personas": len(state.personas),
        "forecast": _serialize_forecast(state.forecast) if state.forecast else None,
        "summary": asdict(state.summary) if state.summary else None,
    }


@app.get("/swarm/run/{run_id}/persona/{persona_id}")
async def get_persona(run_id: str, persona_id: str):
    state = RUNS.get(run_id)
    if state is None:
        raise HTTPException(404, "run not found")
    persona = next((p for p in state.personas if p.id == persona_id), None)
    response = next((r for r in state.responses if r.persona_id == persona_id), None)
    if persona is None:
        raise HTTPException(404, "persona not found")
    return {
        "persona": asdict(persona),
        "response": asdict(response) if response else None,
    }


@app.post("/swarm/run/{run_id}/shock")
async def post_shock(run_id: str, req: ShockRequest):
    state = RUNS.get(run_id)
    if state is None:
        raise HTTPException(404, "run not found")
    if not state.done or state.forecast is None:
        raise HTTPException(409, "run not yet complete")
    assert CLIENT is not None
    shocked = await re_run_with_shock(
        CLIENT,
        state.personas,
        state.question,
        req.shock,
        mode=state.mode,
        model=MODEL,
    )
    shocked_summary = await summarize_swarm(
        CLIENT, shocked, state.personas, MODEL
    )
    return {
        "forecast": _serialize_forecast(shocked),
        "summary": asdict(shocked_summary) if shocked_summary else None,
    }


@app.websocket("/swarm/run/{run_id}/stream")
async def stream(ws: WebSocket, run_id: str):
    await ws.accept()
    state = RUNS.get(run_id)
    if state is None:
        await ws.send_json({"error": "run not found"})
        await ws.close()
        return

    personas_sent = False
    responses_sent = 0
    try:
        while True:
            if not personas_sent and state.personas:
                await ws.send_json(
                    {"personas": [asdict(p) for p in state.personas]}
                )
                personas_sent = True
            while len(state.responses) > responses_sent:
                r = state.responses[responses_sent]
                await ws.send_json(
                    {
                        "type": "response",
                        "persona_id": r.persona_id,
                        "position": r.position,
                        "confidence": r.confidence,
                        "reasoning": r.reasoning,
                    }
                )
                responses_sent += 1
            if state.done:
                await ws.send_json(
                    {
                        "done": True,
                        "forecast": _serialize_forecast(state.forecast)
                        if state.forecast
                        else None,
                        "summary": asdict(state.summary) if state.summary else None,
                        "error": state.error,
                    }
                )
                break
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass


def _serialize_forecast(f: Forecast) -> dict:
    return {
        "question": f.question,
        "mode": f.mode,
        "n_personas": f.n_personas,
        "n_failed": f.n_failed,
        "headline": f.headline,
        "confidence_interval": list(f.confidence_interval) if f.confidence_interval else None,
        "distribution": f.distribution,
        "by_demographic": f.by_demographic,
    }
