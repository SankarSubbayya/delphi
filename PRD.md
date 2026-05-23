# Delphi — Product Requirements Document

**Status:** Draft v1
**Owner:** Sankar Subbayya
**Target ship:** Google I/O Hackathon, 2026-05-23 (one-day build)
**Vision horizon:** 12 months
**Companion doc:** [DELPHI.md](DELPHI.md) (pitch / narrative)

---

## 1. Vision

Delphi is **synthetic populations as a computational substrate** — a real-time, multimodal, swarm-reasoning primitive that any team can use to forecast, pretest, or war-game any question whose answer depends on how a population of humans would respond.

Where existing products are vertical (Aaru = political forecasting; Synthetic Users = UX research; Listen Labs = interviews), Delphi is the **general-purpose primitive** beneath all of them — exposed as a UI for the hackathon demo, as an API/SDK for the post-hackathon product.

---

## 2. Problem

Every team that needs to predict, pretest, or simulate population responses today picks one of five bad options:

| Option | Why it's broken |
| --- | --- |
| Market research firms | Weeks-long, $25k+ minimum, narrow demographic reach |
| Human prediction markets (Kalshi / Polymarket) | Slow to settle, tech-skewed crowd, limited question domains |
| Consultant opinions | Slow, opinion-laden, not reproducible |
| Bespoke agent-based modeling | Months of engineering, requires domain PhD |
| Ship blind | The default — expensive failure mode |

Existing AI competitors solve slices: Aaru does politics, Synthetic Users does UX, and a handful of academic systems sit in papers. **No general-purpose, real-time, multimodal, live-grounded synthetic-population API exists in 2026.** That gap is the opportunity.

---

## 3. Target Users

### Primary — demo audience (hackathon)

| Persona | What they want to ask Delphi |
| --- | --- |
| **Founder / PM** | *"Will my launch land with users in segment X?"* |
| **Policy analyst** | *"How will rule change Y affect each constituency?"* |
| **Comms lead** | *"Stress-test this statement against critics, supporters, journalists."* |

### Secondary — post-hackathon expansion

- Marketing teams (campaign pretesting)
- Public-health researchers (behavior simulations)
- Legal teams (synthetic jury for trial messaging)
- Forecasting and intelligence analysts (geopolitical / market)
- Game / sim designers (NPC populations)

---

## 4. Goals & Success Metrics

### Hackathon-day (must-have)

| Metric | Target |
| --- | --- |
| End-to-end run latency (N=200) | <90s |
| News-shock re-run latency | <30s |
| Drill-down agent trace load | <500ms |
| Demo modes available | ≥3 (forecast, marketing pretest, policy stress-test) |
| Demo reliability across 5 dry runs | 100% |
| Judge "holy shit" verbal reaction | ≥1 |

### Post-hackathon (12-month vision)

| Metric | Target |
| --- | --- |
| Teams onboarded to API | 100 |
| Synthetic-population runs executed | 1M |
| Vertical templates productized | 3 (Forecasting, Pretest, Policy) |
| Backtest accuracy vs. real historical events | ≥ Good Judgment Project median |

### Explicit non-goals (hackathon)

- Auth, billing, multi-user collaboration
- Persona persistence across sessions
- Custom persona bank UI editing
- Calibration / backtest harness against real data
- SOC2 / enterprise controls

---

## 5. User Stories

### Hackathon MVP

| ID | Story |
| --- | --- |
| US-1 | As a judge, I type a question and see 200 personas reason about it in real time on a globe. |
| US-2 | As a judge, I click any persona dot and see the agent's full reasoning trace plus cited sources. |
| US-3 | As a judge, I inject a news shock and see the forecast visibly re-compute within 30s. |
| US-4 | As a judge, I switch the same swarm from forecasting to marketing-pretest with one click; same engine, different framing. |
| US-5 | *(Stretch)* As a judge, I speak my query (Live API) and the swarm responds with voice plus a visual forecast. |

### Post-hackathon vision

| ID | Story |
| --- | --- |
| US-6 | As a PM, I save a persona bank for reuse across questions over time. |
| US-7 | As an analyst, I compare two runs to see how a population's opinion shifted. |
| US-8 | As a developer, I POST a question to the Delphi API and get a structured forecast back as JSON. |
| US-9 | As a team lead, I share a run with my team and we annotate findings together. |
| US-10 | As a forecaster, I backtest the swarm against historical events to calibrate trust. |

---

## 6. Functional Requirements

### FR-1 — Persona generation
- Generate N synthetic personas from configurable demographic axes (age, income, region, role, belief proxy, education, occupation).
- Personas grounded in plausible real-world distributions (Census / World Bank proxy data baked in).
- Each persona has: `id`, `label`, `demographics` vector, `role`, `identity_prompt` (1–2 sentences).
- Default N = 200 at demo time; scale to 1,000 only if API rate-limits hold.

### FR-2 — Question ingestion
- Accept text input; optionally accept voice (Live API).
- Auto-classify question type: `forecast | pretest | stress_test | open`.
- If ambiguous, system asks **one** clarifying question (no multi-turn clarifications during demo).

### FR-3 — Swarm reasoning
- N personas reason in parallel. Each has:
  - Google Search grounding (live web)
  - Multimodal input capability (news videos, images, articles)
  - Their persona's identity prompt as system context
- Each agent emits a **structured response**:
  - `position` (probability, choice, or sentiment, depending on mode)
  - `confidence`
  - `reasoning` (free text trace)
  - `sources` (URLs cited)

### FR-4 — Aggregation
- Aggregate N responses into:
  - Headline forecast / position with confidence interval
  - Full distribution across positions
  - Breakdown by each demographic axis
- Aggregation weighted by demographic distribution targeting a reference population (default: US adult population; user-overridable in pretest mode).

### FR-5 — Visualization
- Live globe with N dots, colored by emerging position; dot illuminates as its agent finishes reasoning.
- Headline confidence bar updates in real time as agents converge.
- Click any dot → side panel with persona profile, reasoning trace, sources.
- Distribution chart per demographic axis (toggleable).
- Conceptual demographic-space view (alternate to geographic globe) as toggle for closing-twist demo beat.

### FR-6 — News shock
- Free-text "shock" input box.
- On submit, swarm re-runs with shock injected as context; UI shows visual diff (which dots changed position; new headline forecast vs. prior).

### FR-7 — Mode switching
- Same swarm, three question framings:
  - **Forecast** — probabilistic yes/no/multi-choice
  - **Pretest** — preference / sentiment / "would this work for you?"
  - **Stress-test** — find dissent / objections / failure modes
- Toggle in UI; re-runs the existing personas under the new framing.

### FR-8 *(Stretch)* — Voice interaction
- Live API integration for voice question and spoken forecast summary.
- Sub-1.5s turn-taking.

---

## 7. Non-Functional Requirements

### Performance
- N=200 full run: ≤ 60s p50, ≤ 90s p95
- News-shock re-run: ≤ 30s
- Drill-down trace fetch: ≤ 500ms
- Voice turn (stretch): ≤ 1.5s

### Reliability (demo-critical)
- ≥ 95% successful end-to-end run across 5 consecutive dress rehearsals.
- Graceful degradation: if grounding fails per agent, that agent proceeds with internal knowledge and flags `grounding: false` in its response.
- Hard timeout per agent (e.g., 25s); agents that time out are excluded from aggregation but counted in the failure rate.

### Scale
- Hackathon: 1 concurrent demo user. N=200 default, N=1000 stretch.
- Post-hackathon: 50 concurrent API users at N=200 each.

### Safety & disclaimers
- No real-individual persona-typing (no "what would Tim Cook think").
- No PII in persona generation; demographic vectors are synthetic.
- Output stamp: *"Delphi forecasts are model-generated population simulations; not financial, medical, or legal advice."*
- Banned-domain guardrails: refuse questions framed for medical diagnosis or mental-health analysis (hackathon-banned categories).

### Cost
- Hackathon budget cap: $100 in Gemini API spend across all dry runs + live demo.
- Per-run cost target (N=200): ≤ $0.50.

---

## 8. Technical Architecture

### High-level (hackathon MVP)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ WEB FRONTEND  ·  Next.js 15 / React 19 / Tailwind 3 / Three.js (R3F)     │
│                                                                          │
│  ┌──────────────┐   ┌──────────────────┐   ┌─────────────────────────┐   │
│  │ left rail    │   │  centre · GLOBE  │   │ right rail · drill-down │   │
│  │ question     │   │  (dark ink)      │   │ persona dossier         │   │
│  │ mode toggle  │   │  N dots placed   │   │ (opens on dot click)    │   │
│  │ N            │   │  by region; live │   │                         │   │
│  │ convene btn  │   │  recolour as     │   │                         │   │
│  │ shock input  │   │  agents finish   │   │                         │   │
│  └──────────────┘   └──────────────────┘   └─────────────────────────┘   │
│                     ┌─────────────────────────────────────────────────┐  │
│                     │ forecast bar · headline · ±1σ · n/failed · shift│  │
│                     │             · 5-bucket distribution             │  │
│                     └─────────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────────────┬─────────────────┘
                  │ REST (fetch)                         │ WebSocket
                  │   POST /swarm/run                    │   /swarm/run/{id}/stream
                  │   GET  /swarm/run/{id}               │     ← personas[]
                  │   GET  /swarm/run/{id}/persona/{pid} │     ← response (×N)
                  │   POST /swarm/run/{id}/shock         │     ← done + forecast
                  ▼                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR  ·  FastAPI + asyncio  ·  delphi/api.py                     │
│                                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │ RunState    │◀─▶│ persona      │──▶│ swarm       │──▶│ shock       │  │
│  │ in-memory   │   │ generator    │   │ runner      │   │ re-run      │  │
│  │ dict by     │   │ personas.py  │   │ swarm.py    │   │ shock.py    │  │
│  │ run_id      │   │ (1 batched   │   │ (N parallel │   │ (append +   │  │
│  │             │   │  Gemini call)│   │  + sem K)   │   │  re-run)    │  │
│  └─────────────┘   └──────────────┘   └──────┬──────┘   └─────────────┘  │
│                                              │                            │
│                                              ▼                            │
│                                      ┌──────────────┐                     │
│                                      │ aggregator   │                     │
│                                      │ mean · ±1σ · │                     │
│                                      │ distrib. ·   │                     │
│                                      │ by-demographic│                    │
│                                      └──────────────┘                     │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │  asyncio.gather over N
                               │  · Semaphore(K) concurrency cap
                               │  · 25s per-agent timeout
                               │  · structured JSON response
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ REASONING SUB-AGENTS  ·  delphi/agent.py  ·  N instances per run         │
│                                                                          │
│    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐                     │
│    │agent#1│ │agent#2│ │agent#3│ │agent#4│ │agent#N│   …                 │
│    └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘                     │
│        └─────────┴─────────┼─────────┴─────────┘                         │
│                            ▼                                             │
│            ┌────────────────────────────────────────┐                    │
│            │ Gemini 3.5 Flash (per-agent call)      │                    │
│            │   · google_search grounding tool       │                    │
│            │   · native multimodal input            │                    │
│            │   · 1M context window per agent        │                    │
│            │   · persona system prompt + question   │                    │
│            │   · returns structured JSON            │                    │
│            └────────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Run lifecycle (sequence)

```
 User        Frontend             Backend (FastAPI)           Gemini 3.5 Flash
  │             │                       │                            │
  │ Convene     │                       │                            │
  ├────────────▶│ POST /swarm/run       │                            │
  │             ├──────────────────────▶│ create RunState            │
  │             │       { run_id }      │ asyncio.create_task(…)     │
  │             │◀──────────────────────│                            │
  │             │                       │                            │
  │             │ WS /…/{id}/stream     │                            │
  │             ├──────────────────────▶│                            │
  │             │                       │ persona-gen (1 call) ─────▶│
  │             │                       │◀── batched personas        │
  │             │    personas[]         │                            │
  │             │◀──────────────────────│                            │
  │             │                       │ reason × N (parallel) ────▶│
  │             │                       │                  …         │
  │             │    response           │◀── response #1             │
  │             │◀──────────────────────│                            │
  │             │    response           │◀── response #2             │
  │             │◀──────────────────────│                  …         │
  │             │                       │ aggregate                  │
  │             │    done + forecast    │                            │
  │             │◀──────────────────────│                            │
  │             │                       │                            │
  │ Click dot   │                       │                            │
  ├────────────▶│ GET /…/persona/{pid}  │                            │
  │             ├──────────────────────▶│ lookup persona + response  │
  │             │  persona + response   │                            │
  │             │◀──────────────────────│                            │
  │             │                       │                            │
  │ Inject shock│                       │                            │
  ├────────────▶│ POST /…/{id}/shock    │                            │
  │             ├──────────────────────▶│ append shock to question   │
  │             │                       │ reason × N (parallel) ────▶│
  │             │                       │ aggregate                  │
  │             │       forecast        │                            │
  │             │◀──────────────────────│                            │
```

### Components

| Component | Responsibility | Tech |
| --- | --- | --- |
| Frontend | Globe view, drill-down, mode toggle, shock input, forecast bar | Next.js 15, React 19, Three.js + @react-three/fiber (globe), Tailwind 3 (charts via CSS) |
| Realtime channel | Stream agent completions as they finish | WebSocket (native) |
| Orchestrator | Generate personas, fan out, collect, aggregate | FastAPI + asyncio |
| Persona-gen agent | Demographic axes → N identity prompts | Gemini 3.5 Flash (single call, structured output) |
| Reasoning sub-agent (×N) | Persona reasons about question with grounding | Gemini 3.5 Flash with Google Search tool |
| Aggregator | Combine N responses into headline + distribution + by-axis breakdown | Deterministic Python (no LLM in critical path) |
| Voice gateway *(stretch)* | Live API for voice in / spoken summary out | Gemini Live API |
| State store | In-memory dict keyed by `run_id` | Python dict (hackathon); Postgres + Redis (vision) |

### Data models

```python
@dataclass
class Persona:
    id: str
    label: str               # human-readable e.g. "42yo electrician, rural OH"
    demographics: dict       # {age, region, income, education, role, belief_axis}
    identity_prompt: str     # 1–2 sentence persona for the LLM system prompt

@dataclass
class Question:
    id: str
    text: str
    type: Literal["forecast", "pretest", "stress_test", "open"]
    context: dict            # optional news shock, prior shocks chain

@dataclass
class Source:
    url: str
    title: str
    snippet: str

@dataclass
class AgentResponse:
    persona_id: str
    position: Any            # probability | choice | sentiment
    confidence: float        # 0..1
    reasoning: str
    sources: list[Source]
    grounded: bool
    latency_ms: int

@dataclass
class Forecast:
    question_id: str
    headline: Any
    confidence_interval: tuple[float, float]
    distribution: dict[str, float]
    by_demographic: dict[str, dict]
    n_personas: int
    n_failed: int
```

### Public API (post-hackathon shape — wired but unauthenticated in MVP)

```
POST /swarm/run
  body: { question, n_personas?, mode?, persona_bank?, reference_population? }
  → { run_id, status_url, forecast?, distribution? }

GET /swarm/run/{run_id}
  → { run_id, forecast, distribution, by_demographic, status }

GET /swarm/run/{run_id}/persona/{persona_id}
  → { persona, response }

POST /swarm/run/{run_id}/shock
  body: { shock_text }
  → { new_forecast, diff, shock_id }

WS /swarm/run/{run_id}/stream
  ← incremental {persona_id, response} events
```

### LLM contract — reasoning sub-agent (per persona)

System prompt template (sketch):

```
You are {persona.label}. {persona.identity_prompt}
Your job is to give your honest opinion on the following question,
grounded in publicly available evidence you can find via search.

Question: {question.text}
Mode: {question.type}    # forecast | pretest | stress_test

Respond in JSON matching this schema:
{
  "position": <see mode-specific schema>,
  "confidence": 0.0–1.0,
  "reasoning": "<1–3 sentences reflecting YOUR persona's view>",
  "sources": [ { "url", "title", "snippet" } ]
}

Use Google Search when you need current information.
Stay in character; reason as this persona would, including their blind spots.
```

### Concurrency & rate-limiting

- `asyncio.Semaphore(K)` where `K` is the per-minute Gemini quota / 60s, with safety buffer.
- Exponential backoff on 429.
- Per-agent timeout: 25s. Timeouts excluded from aggregation, surfaced as `n_failed`.
- If demo network is hostile, fall back to a pre-recorded run replay (canned `Forecast` object) — this is the **demo safety net**, not the headline.

---

## 9. Phasing (hour-by-hour, hackathon)

| Hour | Deliverable | Owner |
| --- | --- | --- |
| 0–1 | Repo scaffold, Gemini SDK key, single agent reasoning loop end-to-end | — |
| 1–2 | Structured-output schema, single agent with grounding | — |
| 2–4 | Parallel runner (N=20), naive aggregator, basic UI showing positions | — |
| 4–6 | Persona generator from demographic axes; N=50 with diverse personas | — |
| 6–9 | Globe UI (Three.js), live agent illumination, drill-down panel | — |
| 9–10 | News-shock input + re-run + visual diff | — |
| 10–11 | Mode switcher (forecast / pretest / stress-test) | — |
| 11–12 | Demographic-space alt-view (for closing twist) | — |
| 12–13 | *(Stretch)* Live API voice query | — |
| 13–14 | Scale N from 50 → 200 → 1000 (rate-limit-permitting); rehearse | — |
| 14+ | Polish, dress rehearsal × 3, prep canned-replay safety net | — |

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Gemini API rate limits at N=1000 | High | Medium | Default to N=200; pre-warm quota; canned-replay safety net |
| Forecast looks "obvious" / unimpressive | Medium | High | Curate demo questions in advance to ones where forecast genuinely shifts on shock |
| Grounding tool returns garbage on niche questions | Medium | Medium | Per-agent `grounded: false` flag; agents proceed without; surface in UI |
| "You're just Aaru" comparison | High | Medium | Lean into 3-vertical demo beat; position as primitive, not app |
| Network failure on demo Wi-Fi | Medium | Critical | Canned-replay fallback pre-recorded; can demo offline if needed |
| Globe UI flaky on judges' projector | Low | High | Test in 1080p and 4K modes; degrade to 2D distribution chart if WebGL fails |
| LLM persona drift (agents collapse to centrist averages) | Medium | High | Strong persona prompts with concrete identity anchors + role + belief axis; few-shot bias examples |
| Banned-list misreading by a judge | Low | Critical | Use forecasting + marketing + policy verticals in demo; medical / mental-health entirely off-table |

---

## 11. Decisions Locked (defaults; override before build)

| Question | Locked default |
| --- | --- |
| **N at demo time** | 200 (with 1000 as stretch if quota holds) |
| **Persona generation** | On-demand from demographic axes at run start (fresh per demo) |
| **Aggregation** | Weighted by reference population (US adult default; user-overridable) |
| **Globe UI** | Real-geography default; conceptual demographic-space toggle for closing twist |
| **Voice (Live API)** | Stretch goal; text-first build |
| **Backend language** | Python (FastAPI + asyncio) |
| **Frontend stack** | Next.js + Three.js + Tailwind |
| **Hosting (demo day)** | Local laptop (no cloud risk on demo Wi-Fi); deploy post-hackathon |
| **State persistence** | None (in-memory); per-session only |

---

## 12. Post-Hackathon Roadmap (12 months)

| Quarter | Theme | Key deliverables |
| --- | --- | --- |
| Q1 | Productize the primitive | Hosted API, auth, billing, persona-bank persistence, three vertical templates |
| Q2 | Trust + calibration | Backtest harness vs. historical events; published accuracy scorecards; comparison to Good Judgment Project median |
| Q3 | Enterprise wedge | SOC2 prep, custom persona banks from real survey/Census data, team collab, export to PDF / Looker |
| Q4 | Multimodal + agentic | Voice / video pretest mode; agent-to-agent debate within swarm; integrations (Slack, Notion, Salesforce) |

---

## 13. Open Questions (post-launch)

- How do we **calibrate** personas to real human poll data without overfitting?
- What's the right **pricing primitive** — per-run, per-persona-second, per-question?
- Do we let customers **bring their own persona banks** (from CRM / survey data) or only use Delphi-generated ones?
- How do we handle **questions with no ground truth** (forecasts of distant futures)?
- What's the **ethics framework** for synthetic-population research that could displace real human surveys?

---

## Appendix A — Demo script (3 minutes)

```
[0:00] Judge: "Will Apple ship glasses in 2027?"
[0:05] On-screen: 200 dots scatter on globe, demographic labels visible.
[0:15] Dots begin to illuminate — green = yes, red = no — as each agent
       finishes reasoning. Confidence bar starts climbing.
[0:45] Bar settles: 64% Yes ± 11%. Distribution chart shows
       skew by age and tech-adoption axis.
[1:00] Judge clicks a dot. Side panel shows:
       "37yo software engineer, Bangalore — voted Yes (0.71).
        Reasoning: Apple's Vision Pro pricing trajectory, supply-chain
        signals from Hon Hai. Sources: 3 cited URLs."
[1:30] Judge types news shock:
       "Meta releases sub-$500 glasses in October 2026."
[1:35] Swarm re-runs. ~30s.
[2:05] New bar: 41% Yes ± 14%. ~80 dots visibly flipped — globe ripple.
[2:15] Judge clicks mode toggle → "Pretest" mode.
       Same swarm, new framing:
       "Pretest this tagline: 'Vision Pro 2 — wear the future.'"
[2:35] New distribution: sentiment by demographic.
       Headline: "67% positive, but skews older / urban."
[2:45] Closing line: "Same 200 agents. Three industries. One primitive."
[3:00] End.
```

---

## Appendix B — Repository layout (proposed)

```
google_io_may23_2026/
├── PRD.md                   (this doc)
├── DELPHI.md                (pitch / narrative)
├── HACKATHON.md             (event guide)
├── pyproject.toml
├── main.py                  (CLI entry for local runs)
├── delphi/
│   ├── __init__.py
│   ├── personas.py          (generator from demographic axes)
│   ├── agent.py             (single reasoning sub-agent)
│   ├── swarm.py             (parallel runner + aggregator)
│   ├── shock.py             (news-shock re-run)
│   ├── modes.py             (forecast / pretest / stress-test prompts)
│   ├── voice.py             (Live API integration — stretch)
│   └── api.py               (FastAPI app)
├── web/
│   ├── package.json
│   ├── app/
│   │   ├── page.tsx         (main globe view)
│   │   ├── components/
│   │   │   ├── Globe.tsx
│   │   │   ├── DrillDown.tsx
│   │   │   ├── ShockInput.tsx
│   │   │   └── ModeToggle.tsx
│   └── lib/
│       └── ws.ts            (WebSocket client)
└── tests/
    ├── test_personas.py
    ├── test_swarm.py
    └── test_aggregator.py
```
