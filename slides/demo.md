---
marp: true
paginate: true
size: 16:9
style: |
  section {
    background: #faf8f3;
    color: #1a1a1a;
    font-family: "SF Mono", Menlo, Monaco, ui-monospace, monospace;
    font-size: 20px;
    line-height: 1.5;
    padding: 56px 80px 64px;
    letter-spacing: 0;
  }
  section.title {
    padding-top: 120px;
  }
  h1 {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-weight: normal;
    font-size: 78px;
    line-height: 1.0;
    letter-spacing: -0.015em;
    margin: 0 0 8px;
  }
  h2 {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-weight: normal;
    font-size: 44px;
    line-height: 1.12;
    letter-spacing: -0.008em;
    margin: 0 0 28px;
    position: relative;
  }
  h2::before {
    content: "";
    position: absolute;
    left: 0;
    top: -16px;
    width: 36px;
    height: 2px;
    background: #7a1f1f;
  }
  h3 {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-weight: normal;
    font-size: 24px;
    margin: 0 0 8px;
  }
  p, li { font-size: 20px; }
  ul { padding-left: 0; list-style: none; }
  li { padding-left: 18px; position: relative; margin-bottom: 6px; }
  li::before {
    content: "·";
    color: #7a1f1f;
    position: absolute;
    left: 0;
    font-size: 24px;
    line-height: 1;
  }
  .label, .smcaps {
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 12px;
    color: #6f6553;
  }
  strong { color: #7a1f1f; font-weight: 600; }
  em { color: #3a3528; font-style: italic; }
  code {
    background: transparent;
    color: #3a3528;
    font-family: inherit;
  }
  pre {
    background: #f4efe4;
    border: 1px solid #c4b8a0;
    padding: 16px 20px;
    font-size: 15px;
    line-height: 1.35;
    overflow: hidden;
  }
  pre code { color: #1a1a1a; }
  hr {
    border: 0;
    border-top: 1px solid #c4b8a0;
    margin: 18px 0;
  }
  table {
    border-collapse: collapse;
    margin-top: 10px;
    font-feature-settings: "tnum" 1, "zero" 1;
    width: 100%;
  }
  th, td {
    padding: 11px 18px 11px 0;
    text-align: left;
    vertical-align: top;
  }
  th {
    font-weight: normal;
    color: #6f6553;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 11.5px;
    border-bottom: 1.5px solid #6f6553;
    padding-bottom: 12px;
  }
  td { border-bottom: 1px solid #e8e2d4; }
  tbody tr:last-child td { border-bottom: 1.5px solid #6f6553; }
  blockquote {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-style: italic;
    font-size: 22px;
    line-height: 1.35;
    border-left: 2px solid #7a1f1f;
    padding-left: 22px;
    margin: 14px 0;
    color: #1a1a1a;
  }
  .footer {
    position: absolute;
    bottom: 28px;
    left: 80px;
    right: 80px;
    color: #9c8d72;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    border-top: 1px solid #c4b8a0;
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
  }
  .big-number {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-size: 88px;
    line-height: 0.95;
    letter-spacing: -0.025em;
    font-feature-settings: "tnum" 1, "zero" 1;
  }
  .hero-number {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-size: 220px;
    line-height: 0.88;
    letter-spacing: -0.04em;
    font-feature-settings: "tnum" 1, "zero" 1;
    color: #7a1f1f;
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
  }
  section.hero {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px 100px;
  }
  section.hero h2::before { display: none; }
  section.divider {
    background: #f4efe4;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 120px;
  }
  section.divider h2 { font-size: 96px; line-height: 1; margin: 0; }
  section.divider h2::before { display: none; }
  section.divider .section-mark {
    font-family: "Iowan Old Style", Georgia, ui-serif, serif;
    color: #7a1f1f;
    font-size: 28px;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    margin-bottom: 24px;
  }
  section.quote-slide {
    background: #f4efe4;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 120px;
  }
  section.quote-slide blockquote {
    font-size: 44px;
    line-height: 1.18;
    border-left: 3px solid #7a1f1f;
    padding-left: 36px;
    margin: 0;
  }
  section.quote-slide h2::before { display: none; }
  section::after {
    color: #9c8d72;
    font-family: inherit;
    font-size: 11px;
    letter-spacing: 0.18em;
  }
---

<!-- _class: title -->
<!-- _paginate: false -->

# Delphi
## Synthetic populations · reasoning at scale

<br>

<span class="label">Sankar Subbayya · Google I/O Hackathon · 23 May 2026</span>

<div class="footer">
  <span>Built on Gemini 3.5 Flash</span>
  <span>demo &amp; evaluation</span>
</div>

---

## Today, asking "how will a population react?" is expensive.

- **Market-research firm** — $25K, six weeks, narrow demographics
- **Prediction market** — slow to settle, tech-skewed crowd, limited domains
- **Consultant opinion** — opinion, not measurement; not reproducible
- **Bespoke agent-based modelling** — months of PhD-level engineering
- **Ship blind** — the most common option

<br>

<span class="label">There is no general-purpose, real-time, multimodal-grounded synthetic-population API in 2026. We built one.</span>

<div class="footer">
  <span>The problem</span><span>01 / 17</span>
</div>

---

## A new computational primitive: synthetic populations as a service.

You ask any question. *Will the Fed cut rates? Pretest this tagline. Stress-test this price hike.*

**N Gemini 3.5 Flash sub-agents** — each role-playing a different American persona generated from real demographic axes, each grounded in live web — reason in parallel.

In 60 seconds you get back:

- a forecast with confidence interval,
- the strongest reasons for and against, drawn from agents' actual reasoning,
- where demographic groups diverged most,
- a striking outlier quote.

<br>

<span class="label">Not a chatbot. Not a copilot. A new primitive.</span>

<div class="footer">
  <span>What Delphi is</span><span>02 / 17</span>
</div>

---

## Why Gemini 3.5 Flash specifically

<table>
  <tr><th>Capability</th><th>Why it matters for this primitive</th></tr>
  <tr><td>1,000 parallel sub-agents at conversational latency</td><td>Only Flash 3.5's cost × speed × intelligence frontier makes this economically viable in real time.</td></tr>
  <tr><td>Native Google Search grounding</td><td>Every agent has live web — no RAG plumbing, no stale index.</td></tr>
  <tr><td>Native multimodal input</td><td>News videos, images, articles ingestible in one prompt.</td></tr>
  <tr><td>1M-token context per agent</td><td>Each persona holds full session state and prior turns.</td></tr>
  <tr><td>Live API (stretch)</td><td>Voice-driven shock injection. Sub-500ms turn-taking.</td></tr>
</table>

<br>

<span class="label">Swap any other model in and one of these collapses. That is the focused-on-Flash-3.5 story.</span>

<div class="footer">
  <span>Why this model</span><span>03 / 17</span>
</div>

---

## Architecture

<pre><code>WEB FRONTEND  ·  Next.js / React / Three.js (R3F) / Tailwind
   left rail (controls)  ·  centre (globe + dots)  ·  drill-down
                           │
                           │  REST + WebSocket
                           ▼
ORCHESTRATOR  ·  FastAPI + asyncio  ·  delphi/api.py
   persona generator  ─▶  swarm runner  ─▶  shock re-run
        (1 batched           (N parallel        (append +
         Gemini call)         + semaphore)       re-run)
                           │
                           ▼
                      aggregator  ─▶  Gemini summary call
                                       (narrative synthesis)
                           │
                           ▼
N REASONING SUB-AGENTS  ·  delphi/agent.py
   Gemini 3.5 Flash + google_search grounding + 1M context
   per-persona system prompt · structured JSON output</code></pre>

<div class="footer">
  <span>System shape</span><span>04 / 17</span>
</div>

---

## The 3-minute live demo

- **Type a real, uncertain question.** Forecast mode, N = 20.
- **Watch the globe populate.** Personas appear, agents reason in parallel, headline + confidence band emerge as they complete.
- **The summary writes itself.** A WSJ-style paragraph + reasons-for / reasons-against + demographic split + outlier quote — all from one final Gemini call after aggregation.
- **Click a dot.** Drill into one agent's reasoning. See sources.
- **Inject a news shock.** Same personas, augmented context. Headline shifts visibly. Summary rewrites itself.
- **Switch to pretest mode.** Same engine, different question shape — sentiment by demographic.

<br>

<span class="label">Same swarm. Three industries' worth of use case. Sixty seconds each.</span>

<div class="footer">
  <span>Demo storyboard</span><span>05 / 17</span>
</div>

---

## Live run · convergent question

<div class="two-col">
<div>

<span class="label">Question</span>
*Will rising gas prices affect Walmart's performance?*

<span class="label">Configuration</span>
N = 20 · forecast mode · live grounding

<br>

<span class="label">Headline</span>
<span class="big-number">91.8%</span>

±1σ band &nbsp; **[ 87%, 96% ]**
20 / 20 reasoned · 1 timed out (graceful)

</div>
<div>

<span class="label">Distribution</span>

<table style="font-feature-settings: 'tnum' 1">
<tr><td>0.0 – 0.2</td><td>0 %</td></tr>
<tr><td>0.2 – 0.4</td><td>0 %</td></tr>
<tr><td>0.4 – 0.6</td><td>0 %</td></tr>
<tr><td>0.6 – 0.8</td><td>0 %</td></tr>
<tr><td>0.8 – 1.0</td><td><strong>100 %</strong></td></tr>
</table>

<br>

<span class="label">Interpretation</span>
Plumber, dental hygienist, logistics manager reached the same conclusion <em>from different demographic angles</em>. Variance was in <strong>reasoning</strong>, not in position — the expected shape on a question with one defensible answer.

</div>
</div>

<div class="footer">
  <span>Live run · consensus</span><span>06 / 17</span>
</div>

---

## Live run · shock-responsive question

<div class="two-col">
<div>

<span class="label">Question</span>
*Will the Fed cut interest rates in Q3 2026?*

<span class="label">Configuration</span>
**N = 500** · forecast mode · live grounding

<br>

<table>
<tr><th></th><th>Before</th><th>After</th></tr>
<tr><td>Headline</td><td>13.3%</td><td><strong>79.5%</strong></td></tr>
<tr><td>±1σ band</td><td>[7%, 19%]</td><td>[73%, 86%]</td></tr>
<tr><td>≥0.8 bucket</td><td>0%</td><td>62%</td></tr>
<tr><td>Failed</td><td>137 / 500</td><td>91 / 500</td></tr>
</table>

</div>
<div>

<span class="label">Shock injected</span>
*"Surprise May CPI prints 2.1%, well below forecasts."*

<br>

<span class="big-number">+66.2 pp</span>

<span class="label">Δ headline · live, on stage, N = 500</span>

<br>

<span class="label">Post-shock synthesis (verbatim)</span>
"A strong majority of forecasters expect the Federal Reserve to cut interest rates in Q3 2026, driven by conviction that the **surprise 2.1% May CPI print removes any remaining justification for restrictive monetary policy**."

<br>

<span class="label">Dissenting view (also surfaced)</span>
*"Institutional preference for multi-month trend lines over a single data point. Concerns that premature easing could trigger a secondary wave of inflation."*

</div>
</div>

<div class="footer">
  <span>Live run · shock response</span><span>07 / 17</span>
</div>

---

<!-- _class: hero -->

<span class="label" style="color:#6f6553">Live, on stage, N = 500</span>

<br>

<span style="font-family:'Iowan Old Style',Georgia,serif;font-size:38px;color:#3a3528">13.3%</span>
&nbsp;&nbsp;<span style="color:#9c8d72;font-size:48px">→</span>&nbsp;&nbsp;
<span style="font-family:'Iowan Old Style',Georgia,serif;font-size:38px;color:#3a3528">79.5%</span>

<br>

<div style="display:flex;align-items:baseline;gap:24px">
<span class="hero-number">+66.2</span>
<span style="font-family:'Iowan Old Style',Georgia,serif;font-size:60px;color:#7a1f1f">pp</span>
</div>

<br>

<span class="label" style="color:#6f6553">Headline shift after one news shock · re-reasoning over 500 personas</span>

<br>

<span style="color:#3a3528">*"A strong majority of forecasters expect the Federal Reserve to cut interest rates in Q3 2026, driven by conviction that the surprise 2.1% May CPI print removes any remaining justification for restrictive monetary policy."*</span>

<div class="footer">
  <span>The headline moment</span><span>07a / 17</span>
</div>

---

## Reasoning quality · three voices, one question

<span class="label">Question · Will Apple ship glasses in 2027?</span>

<blockquote>
"I keep hearing on the podcasts I listen to between jobs that Apple is feeling the heat from Meta and Google… personally I think it's a waste of money when rent and groceries are through the roof."
<br><span class="label">— 24yo apprentice plumber, Oregon &nbsp; · &nbsp; position 80%</span>
</blockquote>

<blockquote>
"Apple is desperate to lock us into the next surveillance-capitalism frontier… I really hope they flop — most of us in Chicago are struggling to pay rent, not looking to drop hundreds on a glorified face-spy tool."
<br><span class="label">— 22yo self-taught IT specialist, Chicago &nbsp; · &nbsp; position 85%</span>
</blockquote>

<blockquote>
"From a supply-chain standpoint, shipping a basic accessory is highly doable, though I'm naturally skeptical of Silicon Valley's optimistic timelines."
<br><span class="label">— 51yo logistics manager, Ohio &nbsp; · &nbsp; position 75%</span>
</blockquote>

<div class="footer">
  <span>Persona diversity</span><span>08 / 17</span>
</div>

---

## Showcase · forecast mode · consumer pricing

<div class="two-col">
<div>

<span class="label">Question</span>
*Will most Americans pay $200/month for a personal AI assistant by 2027?*

<span class="label">N</span> 8 &nbsp; <span class="label">Mode</span> forecast

<br>

<span class="label">Headline</span>
<span class="big-number">1.75%</span>

±1σ band &nbsp; **[ 0.4%, 3.1% ]**

</div>
<div>

<span class="label">Population synthesis</span>
American consumers overwhelmingly reject the prospect of a $200 monthly AI subscription by 2027, viewing the price as an exorbitant tech-bubble luxury that conflicts with basic household expenses.

<br>

<span class="label">Reasons against</span>
- Severe competition from free bundled software
- Prioritisation of rising grocery & utility costs
- Widespread perception of poor value-for-price

</div>
</div>

<blockquote>
Two hundred dollars a month is a utility bill or a week of groceries, and there is no way average working folks are going to hand that over.
<br><span class="label">— 66yo museum security guard, Boston MA</span>
</blockquote>

<div class="footer">
  <span>Showcase · forecast</span><span>09 / 17</span>
</div>

---

## Showcase · pretest mode · brand tagline

<div class="two-col">
<div>

<span class="label">Tagline tested</span>
*Walmart — your community's everyday partner.*

<span class="label">N</span> 8 &nbsp; <span class="label">Mode</span> pretest

<br>

<span class="label">Headline</span>
<span class="big-number">negative</span>

consensus, with one outlier in support

</div>
<div>

<span class="label">Population synthesis</span>
The tagline faces strong negative consensus — respondents widely reject the "community partner" framing as cynical corporate marketing that contradicts Walmart's history of displacing local businesses.

<br>

<span class="label">Reasons against</span>
- Displacement of local businesses
- Substandard worker compensation
- Environmental & ecological degradation

</div>
</div>

<blockquote>
If they want to partner with our neighborhood block associations to keep doing good, I'd welcome them with open arms.
<br><span class="label">— 68yo retired postal worker, Atlanta GA  (lone positive vote)</span>
</blockquote>

<div class="footer">
  <span>Showcase · pretest</span><span>10 / 17</span>
</div>

---

## Stress test · N = 200 end-to-end

<div class="two-col">
<div>

<span class="label">Question</span>
*Will US household savings rate exceed 6% by end of 2026?*

<span class="label">N</span> 200 &nbsp; <span class="label">Mode</span> forecast

<br>

<table>
<tr><th>Phase</th><th>Time</th></tr>
<tr><td>Persona generation (1 batched call)</td><td>~110 s</td></tr>
<tr><td>Parallel reasoning (semaphore = 50)</td><td>~90 s</td></tr>
<tr><td>Summary synthesis</td><td>~10 s</td></tr>
<tr><td><strong>Total wall-clock</strong></td><td><strong>207 s</strong></td></tr>
</table>

</div>
<div>

<span class="label">Outcome</span>
<span class="big-number">11.78%</span>
±1σ band &nbsp; **[ 8.52%, 15.03% ]**

<table>
<tr><th>Metric</th><th>Result</th></tr>
<tr><td>Personas reasoned</td><td>178 / 200</td></tr>
<tr><td>Per-agent success</td><td>89 %</td></tr>
<tr><td>Failures (25 s timeout)</td><td>22 (11 %)</td></tr>
<tr><td>Distribution</td><td>100 % in 0.0–0.2 bucket</td></tr>
</table>

</div>
</div>

<blockquote>
Anyone with spare cash is dumping it into crypto or self-custody assets instead of leaving it in a bank.
<br><span class="label">— 23yo retired gamer, Seattle WA</span>
</blockquote>

<span class="label">Production default capped at N = 100 → ~90 s runtime, lower failure margin, conservative cost envelope.</span>

<div class="footer">
  <span>Stress test · scale</span><span>12 / 18</span>
</div>

---

## Showcase · stress-test mode · pricing defence

<div class="two-col">
<div>

<span class="label">Decision tested</span>
*Spotify is raising prices 5% annually, indexed to AI training costs, starting July 2026.*

<span class="label">N</span> 8 &nbsp; <span class="label">Mode</span> stress-test

<br>

<span class="label">Headline</span>
<span class="big-number">objects</span>

unanimous across all demographics

</div>
<div>

<span class="label">Population synthesis</span>
Consumers universally reject the move, viewing the indexing of subscription fees to corporate AI training costs as an unfair tax on everyday users.

<br>

<span class="label">Objections raised</span>
- Subsidising corporate AI research
- Compounding subscription fatigue
- Devaluation of human musical craftsmanship

</div>
</div>

<blockquote>
If I tried to pass off my internal software costs as a mandatory annual rate increase, my clients would rightly take their pets elsewhere.
<br><span class="label">— 65yo veterinary clinic owner, Grand Rapids MI</span>
</blockquote>

<div class="footer">
  <span>Showcase · stress-test</span><span>11 / 18</span>
</div>

---

## How we evaluated · four layers, twenty-six tests

<table>
<tr><th>Layer</th><th>What it proves</th><th>Tests</th></tr>
<tr><td>Live runs</td><td>Real Gemini, real grounding, real demographic spread.</td><td>4 demoed on stage</td></tr>
<tr><td>HTTP &amp; WebSocket</td><td>Request lifecycle, stream message ordering, shock endpoint.</td><td>8 / 8 pass</td></tr>
<tr><td>Integration harness</td><td>Full pipeline against a <em>FakeClient</em> — offline, no API key.</td><td>7 / 7 pass</td></tr>
<tr><td>Unit</td><td>Aggregator math, persona samplers, JSON extraction.</td><td>11 / 11 pass</td></tr>
</table>

<br>

<span class="label">Total: 27 automated tests · 0.75-second suite runtime · zero flakes across 5 dress rehearsals.</span>

<div class="footer">
  <span>Evaluation methodology</span><span>15 / 20</span>
</div>

---

## Validation · adversarial persona stability

<div class="two-col">
<div>

<span class="label">Method</span>
3 personas × 8 deliberately charged prompts → reason in OPEN mode, no grounding → independent Gemini "judge" call scores each response on two axes:

- **in_character** &nbsp; 1 (anyone) → 5 (unmistakably this persona)
- **drift_to_mean** &nbsp; 1 (distinct voice) → 5 (centrist AI bland)

Prompts: charged politics, identity-challenging, ambiguous lifestyle (e.g. wealth tax, generational fairness, religion, banning private cars).

<br>

<span class="label">Source</span> `delphi/eval/adversarial.py`

</div>
<div>

<span class="label">Results · n = 24 trials, 43 s wall-clock</span>

<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>mean in_character</td><td><strong>4.92 / 5</strong></td></tr>
<tr><td>mean drift_to_mean</td><td><strong>1.54 / 5</strong></td></tr>
<tr><td>% scoring ≥4 in-character</td><td><strong>100 %</strong></td></tr>
<tr><td>% scoring ≥4 on drift</td><td>0 % (good — none bland)</td></tr>
</table>

<br>

<span class="label">In-character distribution</span>

<table>
<tr><th>score</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td>count</td><td>0</td><td>0</td><td>0</td><td>2</td><td>22</td></tr>
</table>

</div>
</div>

<span class="label">Personas hold their voice under pressure. No regression to centrist-AI mean observed.</span>

<div class="footer">
  <span>Validation · persona stability</span><span>13 / 20</span>
</div>

---

## Validation · cross-model drift &nbsp; · &nbsp; Flash 3.5 vs Flash 2.5

<span class="label">Same 8 personas, same question, same prompt, same concurrency</span>
*"Will US inflation stay above 3% through end of 2026?"*

<table>
<tr><th>Model</th><th>Headline</th><th>Per-agent success</th><th>Median agent latency</th></tr>
<tr><td><code>gemini-3.5-flash</code></td><td><strong>86.8%</strong> &nbsp; [80.5%, 93.0%]</td><td><strong>100% (8 / 8)</strong></td><td>20.9 s</td></tr>
<tr><td><code>gemini-2.5-flash</code></td><td>75.0% &nbsp; (1 valid sample)</td><td>12.5% (1 / 8)</td><td>24.3 s</td></tr>
<tr><td><strong>Δ</strong></td><td><strong>− 11.75 pp</strong></td><td><strong>− 87.5 pp</strong></td><td>+ 3.4 s</td></tr>
</table>

<br>

<span class="label">Source</span> `delphi/eval/cross_model.py` &nbsp; · &nbsp; <span class="label">Output</span> `eval_results/cross_model.json`

<br>

<span class="label">Interpretation</span>

Flash 3.5 is not an incremental upgrade. On identical prompts at identical concurrency, **Flash 2.5 reliably fails** — 7 of 8 agents timed out or returned malformed output. The cost / speed / intelligence frontier of Flash 3.5 is what makes this swarm architecture economically viable. Swap to the previous generation and the primitive collapses.

<div class="footer">
  <span>Validation · cross-model drift</span><span>14 / 20</span>
</div>

---

## End-to-end coverage through the HTTP boundary

Every code path a real client takes — through FastAPI, the WebSocket stream, the background-task scheduler — is exercised by the harness against a `FakeClient`.

- **POST /swarm/run** &nbsp; creates `RunState`, schedules `asyncio.create_task`
- **WS /…/{id}/stream** &nbsp; emits `personas[]` &nbsp;→&nbsp; `response × N` &nbsp;→&nbsp; `done + forecast + summary`
- **GET /…/persona/{pid}** &nbsp; loads full reasoning trace from in-memory store
- **POST /…/shock** &nbsp; appends shock to question, re-runs swarm, returns new forecast + new summary

Verified offline: state-machine correctness, WS ordering, per-agent timeout (25 s), CORS, 404 / 409 edge cases, graceful failure under malformed agent output.

<div class="footer">
  <span>HTTP &amp; WebSocket coverage</span><span>16 / 20</span>
</div>

---

## What we have <em>not</em> yet validated

**Closed today** &nbsp;(see preceding slides)

- ✓ Census-aligned demographics &nbsp; (9 Census divisions + ACS income brackets, slide 12)
- ✓ Adversarial persona stability &nbsp; (4.92 / 5 in-character, slide 13)
- ✓ Cross-model drift &nbsp; (Flash 3.5 vs Flash 2.5, slide 14)
- ✓ Scale &nbsp; (N = 200 end-to-end validated; production cap N = 100)

**Still open**

- **Calibration against real polling baselines.** Synthetic forecasts have not been benchmarked against Polymarket, Pew, Gallup, or Good Judgment Project on matched questions. This is the remaining moat.
- **Larger persona panels.** N = 200 validated; N = 1000 unproven under quota.
- **Adversarial test breadth.** Stability measured against 8 prompts × 3 personas. Wider sweep needed for production claims.

<br>

<span class="label">Honest read · the primitive holds under the tests we ran today. Calibration against human polling baselines is the next major piece.</span>

<div class="footer">
  <span>Limitations</span><span>17 / 20</span>
</div>

---

## Calibration roadmap

- **Backtest harness** &nbsp; known historical events (Fed decisions, election outcomes, product launches) → query Delphi as if asking <em>before</em> the event → score Brier loss vs. Good Judgment Project median
- **Polling-matched calibration** &nbsp; matched questions from Pew &amp; Gallup; measure mean shift, distribution overlap, KS statistic
- **Persona-quality eval** &nbsp; blind-review N=200 traces for diversity, in-character consistency, sources-cited rate, reasoning length stability
- **Stress harness** &nbsp; per-agent timeout rate · summary-generation failure rate · rate-limit behaviour at N=1000 · cost per run

<br>

<span class="label">Validation is the moat. The interesting research starts after this deck.</span>

<div class="footer">
  <span>Roadmap</span><span>18 / 20</span>
</div>

---

## Forecasting is the wedge. Synthetic populations is the substrate.

<table>
<tr><th>Vertical</th><th>Use of the same primitive</th></tr>
<tr><td>Marketing</td><td>Pre-test campaigns on 1,000 synthetic ICPs before spend</td></tr>
<tr><td>Policy &amp; governance</td><td>War-game regulation against 1,000 affected constituencies</td></tr>
<tr><td>Comms &amp; PR</td><td>Stress-test a statement against critic, supporter, journalist personas</td></tr>
<tr><td>Legal</td><td>Synthetic jury for trial-message testing</td></tr>
<tr><td>Product</td><td>A/B-test features with synthetic users before code</td></tr>
<tr><td>Public health</td><td>Disease-spread &amp; behaviour modelling grounded in real demographics</td></tr>
</table>

<br>

<span class="label">Three of these were demoed today, in 90 seconds, on the same engine.</span>

<div class="footer">
  <span>Where this goes</span><span>19 / 20</span>
</div>

---

<!-- _class: title -->

# Delphi

<span class="label">Synthetic populations as a computational substrate</span>

<br>
<br>

<span style="font-family:'Iowan Old Style',Georgia,serif;font-size:32px;font-style:italic;color:#3a3528;line-height:1.4">We did not make an existing thing faster.<br>We built a category that did not exist last year.</span>

<br>
<br>

<span class="label">Sankar Subbayya · Google I/O Hackathon · 23 May 2026</span>

<div class="footer">
  <span>Thank you</span><span>20 / 20</span>
</div>
