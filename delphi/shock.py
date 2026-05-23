"""News-shock re-run — append shock context, re-run the same personas."""

from collections.abc import Callable

from google import genai

from delphi.agent import AgentResponse
from delphi.modes import Mode
from delphi.personas import Persona
from delphi.swarm import Forecast, run_swarm


async def re_run_with_shock(
    client: genai.Client,
    personas: list[Persona],
    question: str,
    shock: str,
    mode: Mode = Mode.FORECAST,
    model: str = "gemini-3.5-flash",
    concurrency: int = 50,
    use_grounding: bool = True,
    on_response: Callable[[AgentResponse], None] | None = None,
) -> Forecast:
    shocked_question = (
        f"{question}\n\n"
        f"NEW INFORMATION (as of just now): {shock}\n\n"
        "Re-evaluate your answer given this new information."
    )
    return await run_swarm(
        client,
        personas,
        shocked_question,
        mode=mode,
        model=model,
        concurrency=concurrency,
        use_grounding=use_grounding,
        on_response=on_response,
    )
