"""Standalone demo harness — runs the full Delphi pipeline against a FakeClient.

No API key required. Prints a play-by-play of persona gen, swarm reasoning,
aggregation, and a news-shock re-run.

Usage:
    uv run python -m delphi.harness
"""

import asyncio
import json
import random
from dataclasses import asdict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from delphi.modes import Mode
from delphi.personas import Persona, sample_demographics
from delphi.shock import re_run_with_shock
from delphi.swarm import run_swarm


console = Console()


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeAsyncModels:
    def __init__(self):
        self.calls: list[dict] = []

    async def generate_content(self, *, model, contents, config):
        self.calls.append({"contents": contents})
        await asyncio.sleep(random.uniform(0.05, 0.2))

        if "Generate" in contents and "personas from the following" in contents:
            n = contents.count("\n") - contents.count("\n", 0, contents.index("Demographic"))
            # Reasonable upper-bound parse
            n = max(1, min(50, n))
            payload = {
                "personas": [
                    {"index": i, "label": f"persona-{i}", "identity_prompt": _fake_identity(i)}
                    for i in range(n)
                ]
            }
            return _FakeResponse(json.dumps(payload))

        shocked = "NEW INFORMATION" in contents
        base = 0.75 if not shocked else 0.30
        jitter = random.uniform(-0.20, 0.20)
        p = max(0.05, min(0.95, base + jitter))
        return _FakeResponse(
            json.dumps(
                {
                    "position": round(p, 2),
                    "confidence": round(random.uniform(0.5, 0.9), 2),
                    "reasoning": _fake_reasoning(p, shocked),
                    "sources": [],
                }
            )
        )


class _FakeAio:
    def __init__(self, models):
        self.models = models


class FakeClient:
    def __init__(self):
        self.aio = _FakeAio(_FakeAsyncModels())


def _fake_identity(i: int) -> str:
    moods = ["pragmatic", "cautious", "early-adopter", "skeptical", "curious", "loyal"]
    return f"a {moods[i % len(moods)]} person who follows tech news loosely and trusts mainstream coverage"


def _fake_reasoning(p: float, shocked: bool) -> str:
    if shocked:
        return "The new information shifts my view substantially; the competitive landscape changed."
    if p > 0.7:
        return "Recent supply-chain signals and rumored partnerships make this feel likely."
    if p < 0.3:
        return "Apple's pace on new categories is slower than commentators expect."
    return "Hard to call; signals point both ways."


def _print_personas(personas: list[Persona], limit: int = 5) -> None:
    console.print(f"[green]check[/] Generated {len(personas)} personas")
    for p in personas[:limit]:
        demo = ", ".join(f"{k}={v}" for k, v in p.demographics.items())
        console.print(f"  [cyan]{p.label}[/]  [dim]{demo}[/]")
    if len(personas) > limit:
        console.print(f"  [dim]... and {len(personas) - limit} more[/]")


def _print_forecast(label: str, forecast) -> None:
    panel_body = []
    if isinstance(forecast.headline, float):
        panel_body.append(f"[bold]Headline:[/] {forecast.headline:.1%}")
    else:
        panel_body.append(f"[bold]Headline:[/] {forecast.headline}")
    if forecast.confidence_interval:
        lo, hi = forecast.confidence_interval
        panel_body.append(f"[bold]+/-1 sigma:[/] [{lo:.1%}, {hi:.1%}]")
    panel_body.append(f"[bold]n:[/] {forecast.n_personas}  [bold]failed:[/] {forecast.n_failed}")
    console.print(Panel("\n".join(panel_body), title=label, expand=False))

    table = Table(show_header=True)
    table.add_column("Bucket")
    table.add_column("Share", justify="right")
    for k, v in forecast.distribution.items():
        table.add_row(k, f"{v:.1%}")
    console.print(table)


async def main(n: int = 20) -> None:
    random.seed(7)
    client = FakeClient()

    console.rule("[bold cyan]Delphi harness[/] — no real API calls")

    console.print(f"\n[bold]Step 1.[/] Sampling {n} demographic vectors + generating personas")
    from delphi.personas import PersonaGenerator
    gen = PersonaGenerator(client, model="fake-flash")
    personas = await gen.generate(n, seed=7)
    _print_personas(personas)

    question = "Will Apple ship glasses in 2027?"
    console.print(f"\n[bold]Step 2.[/] Running swarm: [italic]{question}[/]")
    initial = await run_swarm(
        client,
        personas,
        question,
        mode=Mode.FORECAST,
        use_grounding=False,
        concurrency=10,
    )
    _print_forecast("Initial forecast", initial)

    shock = "Meta releases sub-$500 glasses in October 2026."
    console.print(f"\n[bold]Step 3.[/] News shock: [italic]{shock}[/]")
    shocked = await re_run_with_shock(
        client,
        personas,
        question,
        shock=shock,
        mode=Mode.FORECAST,
        use_grounding=False,
        concurrency=10,
    )
    _print_forecast("Post-shock forecast", shocked)

    delta = None
    if isinstance(initial.headline, float) and isinstance(shocked.headline, float):
        delta = shocked.headline - initial.headline
        console.print(
            f"\n[bold]Headline shift:[/] "
            f"{initial.headline:.1%} -> {shocked.headline:.1%}  "
            f"[{'red' if delta < 0 else 'green'}]({delta:+.1%})[/]"
        )

    console.print("\n[bold]Step 4.[/] Sample drill-down")
    sample = initial.responses[0]
    p = next(x for x in personas if x.id == sample.persona_id)
    body = (
        f"[bold]Persona:[/] {p.label}\n"
        f"[bold]Identity:[/] {p.identity_prompt}\n"
        f"[bold]Position:[/] {sample.position}  [bold]Confidence:[/] {sample.confidence:.0%}\n"
        f"[bold]Reasoning:[/] {sample.reasoning}"
    )
    console.print(Panel(body, title="One agent's trace", expand=False))

    console.print(f"\n[bold]Total fake API calls:[/] {len(client.aio.models.calls)}")
    console.rule("[bold green]Harness complete[/]")


if __name__ == "__main__":
    asyncio.run(main())
