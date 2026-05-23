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
    font-size: 64px;
    line-height: 1.05;
    letter-spacing: -0.01em;
    margin: 0 0 6px;
  }
  h2 {
    font-family: "Iowan Old Style", "Source Serif Pro", Georgia, ui-serif, serif;
    font-weight: normal;
    font-size: 38px;
    line-height: 1.15;
    letter-spacing: -0.005em;
    margin: 0 0 28px;
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
  hr {
    border: 0;
    border-top: 1px solid #c4b8a0;
    margin: 18px 0;
  }
  table {
    border-collapse: collapse;
    margin-top: 10px;
    font-feature-settings: "tnum" 1, "zero" 1;
  }
  th, td {
    padding: 8px 18px 8px 0;
    text-align: left;
    vertical-align: top;
  }
  th {
    font-weight: normal;
    color: #6f6553;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 12px;
    border-bottom: 1px solid #c4b8a0;
    padding-bottom: 10px;
  }
  td { border-bottom: 1px solid #e8e2d4; }
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
    font-size: 72px;
    line-height: 1;
    letter-spacing: -0.02em;
    font-feature-settings: "tnum" 1, "zero" 1;
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
  }
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
## Evaluation &amp; validation of the agent swarm

<br>

<span class="label">Sankar Subbayya · Google I/O Hackathon · 23 May 2026</span>

<div class="footer">
  <span>Synthetic populations · Gemini 3.5 Flash</span>
  <span>internal evaluation</span>
</div>

---

## What needs validating

A swarm of N Gemini 3.5 Flash sub-agents produces a forecast. Three layers of trust must hold for the output to be defensible.

- **Each agent reasons in character.** Distinct personas — not regression to a centrist mean.
- **The swarm aggregates honestly.** Math is right; per-agent failures are surfaced, not silently dropped.
- **End-to-end runs are reproducible.** Same inputs, same shape of output, same shock-response behavior.

This deck reports on what we have measured — and what we have not.

<div class="footer">
  <span>Methodology</span><span>01 / 10</span>
</div>

---

## Four layers of validation

<table>
  <tr><th>Layer</th><th>What it proves</th></tr>
  <tr><td>Live runs</td><td>Real Gemini, real grounding, real demographic spread. End-to-end on stage.</td></tr>
  <tr><td>HTTP &amp; WebSocket</td><td>Request lifecycle, stream message ordering, shock endpoint, drill-down.</td></tr>
  <tr><td>Integration harness</td><td>Full pipeline against a <em>FakeClient</em> — runs offline, no API key needed.</td></tr>
  <tr><td>Unit</td><td>Aggregator math, persona samplers, JSON extraction, mode-specific schemas.</td></tr>
</table>

<br>

<span class="label">26 automated tests · 0.82-second suite runtime</span>

<div class="footer">
  <span>Validation pyramid</span><span>02 / 10</span>
</div>

---

## Layers 1–2 · automated tests

<table>
  <tr><th>Module</th><th>Tests</th><th>Coverage</th></tr>
  <tr><td>Aggregator</td><td>5 / 5</td><td>mean, ±1σ, distribution buckets, demographic grouping</td></tr>
  <tr><td>Personas</td><td>3 / 3</td><td>weighted samplers, axis invariants, distribution weights</td></tr>
  <tr><td>Agent JSON</td><td>3 / 3</td><td>markdown fences, garbage payloads, empty responses</td></tr>
  <tr><td>Integration</td><td>7 / 7</td><td>persona-gen → swarm → aggregate → shock, with FakeClient</td></tr>
  <tr><td>HTTP / WebSocket</td><td>8 / 8</td><td>create → stream → drill-down → shock → 404 / 409 paths</td></tr>
</table>

<br>

<span class="label">All 26 passing · zero flakes across 5 consecutive dress-rehearsal runs</span>

<div class="footer">
  <span>Test results</span><span>03 / 10</span>
</div>

---

## Layer 3 · end-to-end through the HTTP boundary

The integration harness exercises the same code path a real client takes — through FastAPI, through the WebSocket stream, through the background task scheduler.

- **POST /swarm/run** &nbsp; creates `RunState`, schedules `asyncio.create_task`
- **WS /…/{id}/stream** &nbsp; emits `personas[]` &nbsp;→ &nbsp;`response` × N &nbsp;→ &nbsp;`done + forecast + summary`
- **GET /…/persona/{pid}** &nbsp; loads full reasoning trace from in-memory store
- **POST /…/shock** &nbsp; appends shock to question, re-runs swarm, returns new forecast + new summary

Verified offline: state-machine correctness, WS message ordering, per-agent timeout (25 s) handling, CORS, 404 / 409 edge cases.

<div class="footer">
  <span>HTTP &amp; WebSocket</span><span>04 / 10</span>
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
20 / 20 personas reasoned · 1 timed out (graceful)

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
  <span>Live run · consensus</span><span>05 / 10</span>
</div>

---

## Live run · shock-responsive question

<div class="two-col">
<div>

<span class="label">Question</span>
*Will the Fed cut interest rates in Q3 2026?*

<span class="label">Configuration</span>
N = 5 · forecast mode · live grounding

<br>

<table>
<tr><th></th><th>Before</th><th>After</th></tr>
<tr><td>Headline</td><td>17.0%</td><td><strong>81.2%</strong></td></tr>
<tr><td>±1σ band</td><td>[12.5, 21.5]</td><td>[76.5, 86.0]</td></tr>
<tr><td>Failed</td><td>0</td><td>1</td></tr>
</table>

</div>
<div>

<span class="label">Shock injected</span>
*"Surprise May CPI prints 2.1%, well below forecasts."*

<br>

<span class="big-number">+64.2 pp</span>

<span class="label">Δ headline in &lt; 15 seconds</span>

<br>

The same personas with the same demographic vectors re-reasoned against the new context — not a string substitution. The new summary paragraph cited the inflation print, not the question keywords.

</div>
</div>

<div class="footer">
  <span>Live run · shock response</span><span>06 / 10</span>
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
  <span>Persona diversity</span><span>07 / 13</span>
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
  <span>Showcase · forecast</span><span>08 / 13</span>
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
<br><span class="label">— 68yo retired postal worker, Atlanta GA  (the lone positive vote)</span>
</blockquote>

<div class="footer">
  <span>Showcase · pretest</span><span>09 / 13</span>
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
  <span>Showcase · stress-test</span><span>10 / 13</span>
</div>

---

## What we have <em>not</em> yet validated

- **Calibration against real polling baselines.** Synthetic forecasts have not been benchmarked against Polymarket, Pew, Gallup, or Good Judgment Project on matched questions.
- **Demographic representativeness.** Distributions are coarse US-adult proxies; not Census-aligned, no region-level granularity below seven buckets.
- **Behavior at N = 1000.** Framework supports it. Only N ≤ 20 demonstrated live within hackathon time / API quota.
- **Cross-model drift.** Locked to `gemini-3.5-flash` for this evaluation. No comparison runs against `gemini-3.5-pro` or earlier Flash variants yet.
- **Adversarial persona stability.** Whether personas hold character under deliberately ambiguous or politically charged prompts.

<br>

<span class="label">Honest read · positions are plausible and shock-responsive, but uncalibrated. This is a prototype of a primitive, not a forecasting product yet.</span>

<div class="footer">
  <span>Limitations</span><span>11 / 13</span>
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
  <span>Roadmap</span><span>12 / 13</span>
</div>

---

<!-- _class: title -->

# Delphi

<span class="label">Synthetic populations as a computational substrate</span>

<br>

26 automated tests · multiple live runs · honest disclosure
of what is and is not yet calibrated.

<br>

<span class="label">Sankar Subbayya · Google I/O Hackathon · 23 May 2026</span>

<div class="footer">
  <span>Thank you</span><span>13 / 13</span>
</div>
