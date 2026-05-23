"""Delphi CLI — quick local test of a swarm run.

Usage:
    python main.py "Will Apple ship glasses in 2027?"
    DELPHI_N=50 python main.py "Will the Fed cut rates in Q3?"
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.table import Table

from delphi.modes import Mode
from delphi.personas import PersonaGenerator
from delphi.swarm import run_swarm


load_dotenv()
console = Console()


async def main() -> None:
    question = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Will Apple ship glasses in 2027?"
    )
    n = int(os.getenv("DELPHI_N", "20"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print(
            "[bold red]GEMINI_API_KEY not set.[/] "
            "Copy [italic].env.example[/] to [italic].env[/] and add your key."
        )
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    console.rule("[bold cyan]Delphi[/]")
    console.print(f"[bold]Question:[/] {question}")
    console.print(f"[bold]Model:[/] {model}  [bold]N:[/] {n}\n")

    with console.status(f"Generating {n} personas..."):
        personas = await PersonaGenerator(client, model=model).generate(n)

    console.print(f"[green]check[/] Generated {len(personas)} personas")
    for p in personas[:5]:
        console.print(f"  - [dim]{p.label}[/]")
    if n > 5:
        console.print(f"  [dim]... and {n - 5} more[/]\n")

    completed = 0

    def tick(_r):
        nonlocal completed
        completed += 1
        console.print(f"  [dim]{completed}/{n}[/]", end="\r")

    with console.status(f"Reasoning with {n} sub-agents in parallel..."):
        forecast = await run_swarm(
            client,
            personas,
            question,
            mode=Mode.FORECAST,
            model=model,
            on_response=tick,
        )

    console.print()
    console.rule("[bold green]Forecast[/]")
    if isinstance(forecast.headline, float):
        console.print(f"[bold]Headline:[/] {forecast.headline:.1%}")
    else:
        console.print(f"[bold]Headline:[/] {forecast.headline}")
    if forecast.confidence_interval:
        lo, hi = forecast.confidence_interval
        console.print(f"[bold]+/-1 sigma band:[/] [{lo:.1%}, {hi:.1%}]")
    console.print(f"[bold]n:[/] {forecast.n_personas}  [bold]failed:[/] {forecast.n_failed}\n")

    table = Table(title="Probability distribution")
    table.add_column("Bucket")
    table.add_column("Share", justify="right")
    for k, v in forecast.distribution.items():
        table.add_row(k, f"{v:.1%}")
    console.print(table)

    console.print("\n[bold]Sample reasoning traces:[/]")
    for r in forecast.responses[:3]:
        persona = next((p for p in personas if p.id == r.persona_id), None)
        label = persona.label if persona else r.persona_id
        if r.position is None:
            console.print(f"  [red]x[/] {label}: {r.reasoning}")
        else:
            pos = f"{r.position:.0%}" if isinstance(r.position, float) else str(r.position)
            console.print(f"  [cyan]{label}[/] -> [bold]{pos}[/] ({r.confidence:.0%}): {r.reasoning}")


if __name__ == "__main__":
    asyncio.run(main())
