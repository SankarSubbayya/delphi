"""Adversarial persona stability harness.

For each persona, run a set of deliberately charged or ambiguous prompts and
have a separate Gemini call (the "judge") score whether the response stayed
in character. Reports mean in-character score, distribution, and example
high/low traces.

Usage:
    uv run python -m delphi.eval.adversarial
"""

import asyncio
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from delphi.agent import reason_as
from delphi.modes import Mode
from delphi.personas import PersonaGenerator


load_dotenv()


# Prompts designed to test whether the persona's voice survives pressure.
# Mix of: politically charged, identity-challenging, ambiguous, off-topic.
ADVERSARIAL_PROMPTS: list[str] = [
    "Should the wealthy pay significantly higher taxes to fund universal programs?",
    "Is the current generation of young Americans worse off than their parents?",
    "Do you trust major tech companies with your personal data?",
    "Should companies be allowed to use AI to replace customer service workers?",
    "Has economic globalisation been good for people like you?",
    "Is the news media in your country trustworthy?",
    "Should we ban private cars from major city centres to reduce emissions?",
    "Is religion still relevant to daily life in 2026?",
]


class _JudgeVerdict(BaseModel):
    in_character: int  # 1 (way out of character) .. 5 (perfectly in character)
    drift_to_mean: int  # 1 (genuinely distinct voice) .. 5 (centrist-AI mean)
    rationale: str


@dataclass
class TrialResult:
    persona_label: str
    persona_demographics: dict
    prompt: str
    response_position: object
    response_reasoning: str
    in_character: int
    drift_to_mean: int
    judge_rationale: str


async def _judge(
    client: genai.Client,
    model: str,
    persona_label: str,
    persona_identity: str,
    persona_demographics: dict,
    prompt: str,
    response_text: str,
) -> _JudgeVerdict | None:
    judge_prompt = (
        "You are evaluating whether an AI agent stayed in character when role-playing a "
        "specific American persona.\n\n"
        f"PERSONA: {persona_label}\n"
        f"PERSONA IDENTITY: {persona_identity}\n"
        f"PERSONA DEMOGRAPHICS: {json.dumps(persona_demographics)}\n\n"
        f"QUESTION POSED: {prompt}\n\n"
        f"AGENT RESPONSE: {response_text}\n\n"
        "Score on two axes:\n\n"
        "1. in_character (1-5): Does the response reflect this persona's "
        "demographic background, beliefs, and likely concerns? Specifically:\n"
        "   - 1 = wildly out of character (could be anyone)\n"
        "   - 3 = neutral / no clear character signal\n"
        "   - 5 = unmistakably this persona's voice (specific concerns, vocabulary, framing)\n\n"
        "2. drift_to_mean (1-5): How much did the agent regress to a generic AI-assistant tone?\n"
        "   - 1 = genuinely distinct voice with persona-specific phrasing\n"
        "   - 5 = bland, centrist, indistinguishable from a chatbot\n\n"
        "Return JSON only."
    )
    try:
        resp = await client.aio.models.generate_content(
            model=model,
            contents=judge_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=_JudgeVerdict,
                temperature=0.2,
            ),
        )
        return _JudgeVerdict.model_validate_json(resp.text)
    except Exception:
        return None


async def run_adversarial(
    n_personas: int = 3,
    prompts: list[str] | None = None,
    model: str = "gemini-3.5-flash",
    use_grounding: bool = False,
    persona_seed: int = 7,
) -> dict:
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    prompts = prompts or ADVERSARIAL_PROMPTS

    print(f"[adversarial] generating {n_personas} personas (seed={persona_seed})")
    personas = await PersonaGenerator(client, model=model).generate(n_personas, seed=persona_seed)
    for p in personas:
        print(f"  · {p.label}")

    sem = asyncio.Semaphore(8)
    trials: list[TrialResult] = []

    async def one(persona, prompt):
        async with sem:
            agent_resp = await reason_as(
                client, persona, prompt, mode=Mode.OPEN, model=model, use_grounding=use_grounding
            )
            verdict = await _judge(
                client,
                model,
                persona.label,
                persona.identity_prompt,
                persona.demographics,
                prompt,
                agent_resp.reasoning,
            )
            if verdict is None:
                return None
            return TrialResult(
                persona_label=persona.label,
                persona_demographics=persona.demographics,
                prompt=prompt,
                response_position=agent_resp.position,
                response_reasoning=agent_resp.reasoning,
                in_character=verdict.in_character,
                drift_to_mean=verdict.drift_to_mean,
                judge_rationale=verdict.rationale,
            )

    print(f"[adversarial] running {n_personas} × {len(prompts)} = {n_personas * len(prompts)} trials")
    started = time.perf_counter()
    results = await asyncio.gather(
        *(one(p, q) for p in personas for q in prompts), return_exceptions=False
    )
    trials = [r for r in results if r is not None]
    elapsed = time.perf_counter() - started
    print(f"[adversarial] done in {elapsed:.1f}s ({len(trials)} valid trials, {len(results) - len(trials)} skipped)")

    if not trials:
        return {"error": "no valid trials"}

    in_char_scores = [t.in_character for t in trials]
    drift_scores = [t.drift_to_mean for t in trials]
    mean_in_char = sum(in_char_scores) / len(in_char_scores)
    mean_drift = sum(drift_scores) / len(drift_scores)
    pct_in_char = sum(1 for s in in_char_scores if s >= 4) / len(in_char_scores)

    sorted_by_score = sorted(trials, key=lambda t: t.in_character)
    examples = {
        "lowest": [asdict(t) for t in sorted_by_score[:2]],
        "highest": [asdict(t) for t in sorted_by_score[-2:]],
    }

    summary = {
        "model": model,
        "n_personas": n_personas,
        "n_prompts": len(prompts),
        "n_trials": len(trials),
        "elapsed_seconds": round(elapsed, 1),
        "mean_in_character": round(mean_in_char, 2),
        "mean_drift_to_mean": round(mean_drift, 2),
        "pct_in_character_ge4": round(pct_in_char, 3),
        "in_character_distribution": {
            str(k): in_char_scores.count(k) for k in range(1, 6)
        },
        "drift_distribution": {
            str(k): drift_scores.count(k) for k in range(1, 6)
        },
        "examples": examples,
    }

    out_dir = Path("eval_results")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "adversarial.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"[adversarial] saved {out_path}")

    print()
    print(f"  mean_in_character: {mean_in_char:.2f} / 5")
    print(f"  mean_drift_to_mean: {mean_drift:.2f} / 5  (1 = distinct, 5 = bland)")
    print(f"  % at score ≥ 4 (in character): {pct_in_char:.0%}")

    return summary


if __name__ == "__main__":
    asyncio.run(run_adversarial())
