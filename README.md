# Delphi

**Synthetic populations as a computational substrate.**
Built on Gemini 3.5 Flash for the Google I/O Hackathon, 2026-05-23.

You ask any question — *Will the Fed cut rates in Q3? Pretest this tagline. Stress-test this decision* — and a swarm of Gemini 3.5 Flash sub-agents, each role-playing a different American persona generated from US Census–aligned demographic axes and each grounded in live web, reasons in parallel. In ~60 seconds you get back: a probabilistic forecast with confidence interval, the strongest reasons for and against drawn from agents' own reasoning, the demographic axes where groups diverged most, a striking outlier quote, and a Wall Street Journal–style synthesis paragraph — all produced by one final Gemini call after aggregation.

It is not a chatbot. It is not a copilot. It is a new primitive.

---

## Headline result

Live, on stage, **N = 500** synthetic Americans, the question *"Will the Fed cut interest rates in Q3 2026?"*:

|                          | Before shock | After shock |       Δ       |
| ------------------------ | -----------: | ----------: | ------------: |
| Headline                 |        13.3% |   **79.5%** | **+66.2 pp**  |
| ±1σ band                 |    [7%, 19%] |  [73%, 86%] | tighter       |
| Bullish bucket (≥ 0.8)   |           0% |         62% | full flip     |
| Per-agent success        |   363 / 500  |   409 / 500 | improved      |

Shock injected: *"Surprise May CPI prints 2.1%, well below forecasts."*

The post-shock synthesis, verbatim from a Gemini call after aggregation:

> *A strong majority of forecasters expect the Federal Reserve to cut interest rates in Q3 2026, driven by conviction that the surprise 2.1% May CPI print removes any remaining justification for restrictive monetary policy.*

The dissenting view, surfaced by the same call:

> *Institutional preference for multi-month trend lines over a single data point. Concerns that premature easing could trigger a secondary wave of inflation.*

The agents genuinely re-reasoned given the new context. Not keyword substitution.

---

## Why this only works on Gemini 3.5 Flash

We ran the same swarm — same personas, same question, same prompt, same concurrency — on Gemini 3.5 Flash vs Gemini 2.5 Flash. Results from our cross-model harness:

| Model               |              Headline | Per-agent success | Median latency |
| ------------------- | --------------------: | ----------------: | -------------: |
| `gemini-3.5-flash`  | 86.8% [80.5%, 93.0%]  |    **100% (8/8)** |        20.9 s  |
| `gemini-2.5-flash`  |  75.0% (1 valid call) |        12.5% (1/8)|        24.3 s  |
| **Δ**               |         **−11.75 pp** |     **−87.5 pp**  |        +3.4 s  |

Flash 3.5 is not an incremental upgrade — Flash 2.5 reliably *fails* on identical prompts at identical concurrency. The cost × speed × intelligence frontier of Flash 3.5 is what makes hundreds of parallel grounded reasoning agents economically viable. Swap to the previous generation and the primitive collapses.

Source: [`delphi/eval/cross_model.py`](delphi/eval/cross_model.py) · raw output in [`eval_results/cross_model.json`](eval_results/cross_model.json).

---

## Run it

```bash
# 1 · Backend
cp .env.example .env          # fill in your GEMINI_API_KEY
uv sync --all-extras
uv run uvicorn delphi.api:app --port 8000

# 2 · Frontend  (in another terminal)
cd web
npm install
npm run dev                   # serves at http://localhost:4000

# 3 · CLI alternative
uv run python main.py "Will Apple ship smart glasses in 2027?"

# 4 · Offline demo with no API key  (FakeClient harness)
uv run python -m delphi.harness
```

Then open **http://localhost:4000** and convene the swarm.

---

## Architecture

```
WEB FRONTEND · Next.js / React / Three.js (R3F) / Tailwind
   left rail (controls)  ·  centre (globe + dots)  ·  drill-down + synthesis
                              │
                              │ REST  +  WebSocket
                              ▼
ORCHESTRATOR · FastAPI + asyncio · delphi/api.py
   persona generator  ──▶  swarm runner  ──▶  shock re-run
        (1 batched           (N parallel        (append +
         Gemini call)         + semaphore K)     re-run)
                              │
                              ▼
                       aggregator  ──▶  Gemini summary call
                                         (narrative + quote)
                              │
                              ▼
N REASONING SUB-AGENTS · delphi/agent.py
   Gemini 3.5 Flash + google_search grounding + 1M context per agent
   structured JSON output · 25s per-agent timeout
```

Full architecture, request-lifecycle sequence diagram, data models, and decision log live in [`PRD.md`](PRD.md) §8.

---

## What's in this repo

| Path                     | Contents                                                                  |
| ------------------------ | ------------------------------------------------------------------------- |
| [`delphi/`](delphi/)     | Python backend — orchestrator, agent, swarm, summary, shock               |
| [`delphi/eval/`](delphi/eval/) | Validation harnesses — adversarial, cross-model, stress, persona-quality |
| [`web/`](web/)           | Next.js frontend — globe, drill-down, synthesis panel, shock injector     |
| [`tests/`](tests/)       | 27 pytest tests · `FakeClient` integration harness · 0.75 s suite         |
| [`slides/`](slides/)     | Demo + evaluation deck (Marp markdown + exported PDF)                     |
| [`eval_results/`](eval_results/) | JSON outputs from each validation harness                          |
| [`PRD.md`](PRD.md)       | Product requirements document                                             |
| [`DELPHI.md`](DELPHI.md) | Project pitch, positioning, competitive landscape                         |
| [`CASES.md`](CASES.md)   | Three live-run case studies — one per mode                                |

---

## Validation

| Layer                | What we measured                                                         | Result                                  |
| -------------------- | ------------------------------------------------------------------------ | --------------------------------------- |
| Architecture         | Aggregator math · schema parsing · HTTP / WS lifecycle · failure paths   | **27 / 27** tests pass, 0.75 s suite    |
| Persona stability    | LLM-as-judge in-character score across 24 charged-prompt trials          | **4.92 / 5** mean, 0% drift to centrist |
| Model dependence     | Flash 3.5 vs Flash 2.5 on identical swarm + identical concurrency        | **87.5 pp** per-agent success-rate gap  |
| Scale                | End-to-end at N = 200 and N = 500                                        | 207 s / 89% success at N = 200          |

Sources: [`delphi/eval/adversarial.py`](delphi/eval/adversarial.py) · [`delphi/eval/cross_model.py`](delphi/eval/cross_model.py) · [`delphi/eval/stress.py`](delphi/eval/stress.py) · [`delphi/eval/persona_quality.py`](delphi/eval/persona_quality.py). Raw outputs in [`eval_results/`](eval_results/).

---

## What is *not* yet validated

- **Calibration against real polling baselines.** Synthetic forecasts have not been benchmarked against Polymarket, Pew, Gallup, or Good Judgment Project on matched questions.
- **Larger persona panels.** N = 200 validated end-to-end; N = 500 demonstrated live with 27% per-agent failure; N = 1000 untested under quota.
- **Adversarial test breadth.** Stability measured against 8 charged prompts × 3 personas. Wider sweep needed for production claims.
- **Cross-model breadth.** Compared `gemini-3.5-flash` vs `gemini-2.5-flash`. Other Flash-class models (Claude Haiku, GPT-4o-mini) not yet tested.

Delphi today is a prototype of a primitive, not a calibrated forecasting product. The next major piece is a backtest harness against historical events (past Fed decisions, elections, product launches), scored by Brier loss against the Good Judgment Project median.

---

## Forecasting is the wedge

The same primitive underwrites:

| Vertical            | Use                                                                       |
| ------------------- | ------------------------------------------------------------------------- |
| Marketing           | Pre-test campaigns on 1,000 synthetic ICPs before spend                   |
| Policy / governance | War-game regulation against 1,000 affected constituencies                 |
| Comms / PR          | Stress-test a statement against critic, supporter, journalist personas    |
| Legal               | Synthetic jury for trial-message testing                                  |
| Product             | A/B-test features with synthetic users before code                        |
| Public health       | Disease-spread and behaviour modelling grounded in real demographics      |

We didn't make an existing thing faster. We built a category that did not exist last year.

---

## Built solo, on 2026-05-23

One person, one day, one model. Built at Shack15, San Francisco, for the Google I/O Hackathon hosted with the Google DeepMind team.
