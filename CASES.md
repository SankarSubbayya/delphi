# Delphi · Showcase Cases

Live runs against Gemini 3.5 Flash, captured on 2026-05-23 during the I/O hackathon.
All cases generated end-to-end through the FastAPI backend: persona-gen → swarm reasoning → aggregation → summary.

---

## Case 1 · forecast mode · consumer pricing

**Question:** *Will most Americans pay $200/month for a personal AI assistant by 2027?*

| | |
| --- | --- |
| Mode | forecast |
| N | 8 |
| Headline | **1.75%** |
| ±1σ band | [0.4%, 3.1%] |
| Failed | 0 |

**Population synthesis**
American consumers overwhelmingly reject the prospect of a $200 monthly AI subscription by 2027, viewing the price as an exorbitant tech-bubble luxury that conflicts with basic household expenses.

**Top reasons for** (minority view)
- Corporate expense account subsidies
- High-end developer productivity gains
- Niche adoption by wealthy urbanites

**Top reasons against**
- Severe competition from free bundled software
- Prioritization of rising grocery and utility costs
- Widespread perception of poor value relative to price

**Demographic split**
While skepticism was universal, Pacific Northwest office workers showed a fractionally higher tolerance for the concept than rural Midwestern and Southern service workers, who rated the likelihood near zero.

> *"Two hundred dollars a month is a utility bill or a week of groceries, and there is no way average working folks are going to hand that over."*
> — 66yo museum security guard, Boston MA

---

## Case 2 · pretest mode · brand tagline

**Tagline tested:** *Walmart — your community's everyday partner.*

| | |
| --- | --- |
| Mode | pretest |
| N | 8 |
| Headline | **negative** |
| Failed | 0 |

**Population synthesis**
The tested tagline faces strong negative consensus, with respondents widely rejecting the community partner framing as cynical corporate marketing that contradicts Walmart's history of displacing local businesses.

**Read as positive** (minority)
- Affordable everyday pricing
- Local philanthropic donations
- Responsive safety policies

**Read as negative**
- Displacement of local businesses
- Substandard worker compensation
- Environmental and ecological degradation

**Demographic split**
While progressive and rural respondents strongly rejected the tagline as corporate greenwashing, an older urban centrist appreciated local community outreach and safety initiatives.

> *"If they want to partner with our neighborhood block associations to keep doing good, I'd welcome them with open arms."*
> — 68yo retired postal worker, Atlanta GA (lone positive vote)

---

## Case 3 · stress-test mode · pricing defence

**Decision tested:** *Spotify is raising prices 5% annually, indexed to AI training costs, starting July 2026.*

| | |
| --- | --- |
| Mode | stress_test |
| N | 8 |
| Headline | **objects** |
| Failed | 0 |

**Population synthesis**
Consumers universally and strongly reject Spotify's proposed price hike, viewing the indexing of subscription fees to corporate AI training costs as an unfair tax on everyday users.

**Steelman the move** (the defenders)
- Funding advanced recommendation algorithms
- Accelerating platform feature development
- Sustaining long-term technological infrastructure

**Objections raised**
- Subsidizing corporate AI research
- Compounding financial subscription fatigue
- Devaluation of human musical craftsmanship

**Demographic split**
Opposition was absolute across all segments, uniting older traditional small business owners in the Midwest with younger progressive service workers in Northeast urban centers.

> *"If I tried to pass off my internal software costs as a mandatory annual rate increase, my clients would rightly take their pets elsewhere."*
> — 65yo veterinary clinic owner, Grand Rapids MI

---

## What these cases collectively show

- **All three modes work end-to-end.** Forecast (numeric), pretest (label), stress-test (label) all produced coherent, structured outputs from the same swarm architecture.
- **Population synthesis adds the missing layer.** Each case turns a one-number summary into a publishable paragraph plus structured reasons and a quote — what a judge would actually take notes on.
- **Demographic divergence is real.** Even in unanimous-position cases (Spotify), the agents stated different reasons for the same conclusion; in split cases (Walmart tagline), the lone outlier vote came from the demographic profile you'd predict.
- **The outlier quote is repeatedly the best line.** Across N=8 runs, Gemini reliably identified one persona with a striking specific phrasing and pulled it cleanly.
