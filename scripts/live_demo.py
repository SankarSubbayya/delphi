"""Live end-to-end demo against real Gemini 3.5 Flash.

Exercises: persona-gen -> swarm forecast -> news shock -> mode switch to pretest.

Usage:
    uv run python scripts/live_demo.py
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delphi.modes import Mode
from delphi.personas import PersonaGenerator
from delphi.shock import re_run_with_shock
from delphi.swarm import run_swarm


load_dotenv()
console = Console()


def _summary(label: str, f) -> None:
    body = []
    if isinstance(f.headline, float):
        body.append(f"[bold]Headline:[/] {f.headline:.1%}")
    else:
        body.append(f"[bold]Headline:[/] {f.headline}")
    if f.confidence_interval:
        lo, hi = f.confidence_interval
        body.append(f"[bold]+/-1 sigma:[/] [{lo:.1%}, {hi:.1%}]")
    body.append(f"[bold]n:[/] {f.n_personas}  [bold]failed:[/] {f.n_failed}")
    body.append(f"[bold]distribution:[/] {f.distribution}")
    console.print(Panel("\n".join(body), title=label, expand=False))


async def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]GEMINI_API_KEY not set[/]")
        sys.exit(1)
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    n = int(os.getenv("DELPHI_N", "8"))
    client = genai.Client(api_key=api_key)

    console.rule(f"[bold cyan]Delphi live demo[/]  N={n}  model={model}")

    console.print(f"\n[bold]Step 1.[/] Generating {n} personas")
    personas = await PersonaGenerator(client, model=model).generate(n)
    for p in personas:
        console.print(f"  - {p.label}")

    question = "Will Apple ship smart glasses in 2027?"
    console.print(f"\n[bold]Step 2.[/] Forecast swarm: [italic]{question}[/]")
    initial = await run_swarm(client, personas, question, mode=Mode.FORECAST, model=model)
    _summary("Initial forecast", initial)

    shock = "Meta releases polished sub-$500 smart glasses in October 2026 with strong reviews."
    console.print(f"\n[bold]Step 3.[/] News shock re-run: [italic]{shock}[/]")
    shocked = await re_run_with_shock(
        client, personas, question, shock=shock, mode=Mode.FORECAST, model=model
    )
    _summary("Post-shock forecast", shocked)

    if isinstance(initial.headline, float) and isinstance(shocked.headline, float):
        delta = shocked.headline - initial.headline
        color = "red" if delta < 0 else "green"
        console.print(
            f"\n[bold]Headline shift:[/] {initial.headline:.1%} -> {shocked.headline:.1%}  "
            f"[{color}]({delta:+.1%})[/]"
        )

    pretest_q = "Tagline: 'Vision Pro 2 — wear the future.' How does this land?"
    console.print(f"\n[bold]Step 4.[/] Same personas, switch to PRETEST mode: [italic]{pretest_q}[/]")
    pretest = await run_swarm(client, personas, pretest_q, mode=Mode.PRETEST, model=model)
    _summary("Pretest result", pretest)

    console.print("\n[bold]Sample pretest reactions:[/]")
    for r in pretest.responses[:3]:
        p = next((x for x in personas if x.id == r.persona_id), None)
        label = p.label if p else r.persona_id
        if r.position is not None:
            console.print(f"  [cyan]{label}[/] -> [bold]{r.position}[/]: {r.reasoning}")

    console.rule("[bold green]Live demo complete[/]")


if __name__ == "__main__":
    asyncio.run(main())
