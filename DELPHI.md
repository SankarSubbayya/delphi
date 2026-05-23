# Delphi — Synthetic Populations as a Computational Substrate

A hackathon pitch for Google I/O 2026-05-23, built on Gemini 3.5 Flash.

---

## The Concept

You ask any question about the world — *"Will this product land?"* *"How will the EU respond to X?"* *"What does Black Friday look like for indie brands this year?"* — and **1,000 Gemini 3.5 Flash sub-agents**, each modeling a different demographic / role / belief / region, reason in parallel, in real time, each grounded in live web. A forecast emerges in 60 seconds with confidence interval, and you can drill into *any individual agent's* reasoning trace.

It's not a chatbot. It's not a copilot. It's a **new primitive**: synthetic populations as a service.

---

## Why This is the Creative Pick

Most teams will build agent-flavored chatbots, voice apps, video summarizers, code agents — variations on what already exists with a faster LLM. Almost no one will build a **swarm forecaster**, because before Flash 3.5 the cost / latency curve simply did not permit 1,000 reasoning agents in parallel grounded to live data.

You're not making an existing thing faster — you're shipping a category whose execution profile *did not exist last year*.

---

## Long-Lasting Industry Impact

Forecasting alone is a real market (Kalshi, Polymarket, Good Judgment, intelligence agencies, actuarial science). But the *same primitive* underwrites:

| Vertical | Use of synthetic populations |
| --- | --- |
| Marketing | Pre-test campaigns on 1,000 synthetic ICPs before spend |
| Policy / Governance | War-game regulation against 1,000 affected constituencies |
| Comms / PR | Stress-test a statement against critic, supporter, journalist personas |
| Legal | Synthetic jury for trial-message testing |
| Product | A/B-test features with synthetic users before code |
| Public Health | Disease-spread + behavior simulations grounded in real demographics |

A YC / a16z / AI Futures Fund partner sees this and thinks *infrastructure layer*, not toy.

---

## Why Only Gemini 3.5 Flash

- **1,000 parallel sub-agents at conversational latency** — Flash 3.5 is the first model whose cost × speed × intelligence trio makes this affordable in real time. GPT-4o would cost ~$50/query and run for 20 minutes; smaller Flash-class models cannot sustain coherent persona + reasoning.
- **Native Google Search grounding** — every agent has live web without a tool-call plumbing layer.
- **Native multimodality** — agents ingest news *videos*, images, posts, articles in one prompt (no extraction stack).
- **1M context per agent** — each persona carries its full world-state and history.
- **Live API** — the demo lets the judge *talk* to the swarm and re-run with a voice shock.

Swap any other model in and one of these collapses. That is the focused-on-Flash-3.5 story.

---

## The 3-Minute Demo

1. Judge picks any question. (*"Will Apple ship glasses in 2027?"* works.)
2. 1,000 dots scatter on a world map, each labeled with its demographic.
3. Dots light up as agents reason — colored by emerging position. Live confidence bar at the top.
4. Drill into one dot → see that agent's persona + reasoning trace + cited sources.
5. Judge throws a *shock*: *"What if Meta launches first next month?"* Swarm re-runs in 15s, forecast visibly shifts.
6. **Closing twist** — same swarm, different question type — flip to *"Pre-test this marketing tagline"* live. The audience sees the primitive is universal.

That last beat is the killer: same architecture, three completely different industries, in 30 seconds. They get that they're watching infrastructure, not a feature.

---

## Banned-List Check

- Not job-screening, medical, mental health, nutrition, education chatbot, image analyzer, basic RAG, Streamlit.
- **Personality Analyzer risk: LOW** — frame as *demographic / population modeling*, not personality typing. The "consumer personality quiz" category is what's banned; agentic forecasting at population scale is its own thing. Use census / market-research framing in the deck.

---

## One-Day Build Order

| Hour | Deliverable |
| --- | --- |
| 0–2 | One agent: persona + grounding + structured forecast output |
| 2–4 | N=20 parallel agents + aggregator with confidence band |
| 4–6 | Persona generation from demographic axes (income / region / age / belief proxies) |
| 6–9 | Live globe UI + drill-down to single agent reasoning |
| 9–11 | News-shock re-run + multi-question (forecast / marketing / policy) flexibility |
| 11–13 | Live API voice query |
| 13+ | Polish, scale N from 20 → 1,000, prep demo |

Scale to N=1,000 only if rate limits hold; the visual works at N=200 too.

---

## Competitive Landscape

Honest read: the **concept** of LLM-driven synthetic populations is not novel in 2026. Direct competitors exist.

### Direct competitors

| Player | What they do | Status |
| --- | --- | --- |
| **Aaru.ai** | AI agents replicating voter / consumer behavior at population scale for forecasting and market research | Funded, ~2024 launch — closest to Delphi as pitched |
| **Synthetic Users** (syntheticusers.com) | AI personas for product research / interviews | Multi-million funded, real customers |
| **Listen Labs, Outset.ai, Strella, Verb AI** | Synthetic user interviews for UX research | Well-funded startup cluster |
| **Stanford "Generative Agents"** (Park et al., 2023) | "Smallville" — 25 LLM agents in a simulated town | Foundational paper everyone cites |
| **MIT / Stanford ABM-with-LLM groups** | Agent-based modeling with LLMs for policy / economics | Academic, several published systems |

### Adjacent competitors

- **Polymarket, Kalshi, Manifold** — human prediction markets
- **Good Judgment Project** — human superforecasters; the standard to beat
- **Anthropic, OpenAI, Google DeepMind** — internal research on persona simulation + synthetic data

### What is still genuinely open

1. **Real-time, live-grounded swarm** — most competitors run batch surveys, not streaming forecasts that update on news shocks. Aaru is closest but not real-time.
2. **General-purpose substrate** vs. vertical-specific. Synthetic Users = UX only. Aaru = political / market only. A *primitive* exposed as an API hasn't been won.
3. **Scale to N=1,000+** with multimodal grounding at conversational latency — this is where Flash 3.5 unlocks the genuine moat.

---

## Positioning — Two Paths Forward

### Path A: Keep Delphi, reframe to dodge the comparison

Don't pitch it as "synthetic populations." Pitch it as **a new live-grounded substrate for swarm reasoning** with forecasting as *one* use case demoed live. Sell the API / SDK angle. Show three different verticals in 90 seconds (forecasting → marketing test → policy stress-test) to make clear you're shipping infrastructure, not an app. This minimizes the "you're Aaru" reaction.

### Path B: Pivot to something less crowded

Alternatives that score better on novelty in 2026:

| Pitch | One-liner |
| --- | --- |
| **Probe** | Adversarial agent swarm that reverse-engineers any black-box system (API, competitor product, regulator's algo, opaque website) and outputs the inferred spec |
| **Hindsight** | Point at any completed project's artifacts (git, Slack, calendar, call recordings) → agents reconstruct what *really* happened and write the post-mortem nobody had time to write |
| **Wake** | A long-running ambient agent — runs for *weeks*, watches a project's comms / code / customer signal, surfaces only the things the team should worry about |
| **Negotiate** | Agent-to-agent negotiation protocol — your agent negotiates your bills, lease, contracts with the other party's agent. The plumbing for agentic commerce |

---

## Risks + Mitigations

- **API rate limits at N=1,000** → fallback to N=100 with the same visual impact, or simulate at N=1,000 with a fast first pass
- **Predictions being "obvious"** → curate the demo question to be interesting (one where the forecast actually shifts meaningfully)
- **"You're just Aaru"** comparison → lean into Path A reframing; show three verticals in the demo to position as infra, not an app
- **Persona quality** → ground each persona in real demographic axes (Census-style proxies) so they have grounded distinguishing context, not just labels

---

## Open Questions to Resolve Before Build

- N at demo time — 200, 500, or 1,000?
- How are personas generated? (Pre-built bank vs. on-demand from demographic axes vs. clustered from a real dataset)
- What's the aggregation function? (Weighted majority, distribution, or persona-grouped sub-forecasts?)
- How is the globe-UI laid out? (Real geography, conceptual demographic space, or both views toggle-able?)
- Live API voice — required for the demo or stretch goal?
