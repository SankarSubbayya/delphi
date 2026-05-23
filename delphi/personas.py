"""Demographic-axis persona generator.

Samples N demographic vectors from configured reference distributions, then
asks Gemini for distinguishing identity prompts in a single batched call.
"""

import random
import uuid
from dataclasses import dataclass

from google import genai
from google.genai import types
from pydantic import BaseModel


# Distributions aligned to US Census Bureau / ACS 2022 estimates of the
# adult (18+) population. Weights are population shares, not sample sizes.

AGE_BUCKETS: list[tuple[str, float]] = [
    ("18-29", 0.20),
    ("30-44", 0.26),
    ("45-59", 0.25),
    ("60+", 0.29),
]

# Nine US Census Bureau divisions with 2020 population shares.
REGIONS: list[tuple[str, float]] = [
    ("New England", 0.045),
    ("Mid-Atlantic", 0.126),
    ("East North Central", 0.141),
    ("West North Central", 0.064),
    ("South Atlantic", 0.207),
    ("East South Central", 0.058),
    ("West South Central", 0.127),
    ("Mountain", 0.077),
    ("Pacific", 0.155),
]

# Educational attainment of US adults 25+, ACS 2022.
EDUCATION: list[tuple[str, float]] = [
    ("no high school", 0.10),
    ("high school", 0.27),
    ("some college", 0.27),
    ("bachelors", 0.22),
    ("graduate", 0.14),
]

# Household income brackets, ACS 2022 (rounded shares).
INCOME_BRACKETS: list[tuple[str, float]] = [
    ("under $35k", 0.25),
    ("$35-75k", 0.28),
    ("$75-125k", 0.23),
    ("$125-200k", 0.14),
    ("over $200k", 0.10),
]

OCCUPATION_CLUSTERS: list[str] = [
    "service worker",
    "skilled trades",
    "office / admin",
    "manager / professional",
    "tech / knowledge work",
    "healthcare",
    "education",
    "retired",
    "student",
    "small business owner",
    "agriculture / food production",
    "transportation / logistics",
]

BELIEF_AXIS: list[tuple[str, float]] = [
    ("traditional", 0.30),
    ("centrist", 0.40),
    ("progressive", 0.30),
]


def _weighted_choice(options: list[tuple[str, float]]) -> str:
    labels, weights = zip(*options)
    return random.choices(labels, weights=weights, k=1)[0]


def sample_demographics() -> dict:
    return {
        "age": _weighted_choice(AGE_BUCKETS),
        "region": _weighted_choice(REGIONS),
        "education": _weighted_choice(EDUCATION),
        "income": _weighted_choice(INCOME_BRACKETS),
        "occupation": random.choice(OCCUPATION_CLUSTERS),
        "belief_axis": _weighted_choice(BELIEF_AXIS),
    }


@dataclass
class Persona:
    id: str
    label: str
    demographics: dict
    identity_prompt: str


class _GeneratedIdentity(BaseModel):
    index: int
    label: str
    identity_prompt: str


class _IdentityBatch(BaseModel):
    personas: list[_GeneratedIdentity]


class PersonaGenerator:
    def __init__(self, client: genai.Client, model: str = "gemini-3.5-flash"):
        self.client = client
        self.model = model

    async def generate(self, n: int, seed: int | None = None) -> list[Persona]:
        if seed is not None:
            random.seed(seed)
        demographics_list = [sample_demographics() for _ in range(n)]

        prompt_parts = [
            f"Generate {n} concise, distinguishable personas from the following demographic vectors.",
            "Each persona needs:",
            "- a short human-readable label (e.g., '37yo electrician, rural OH')",
            "- a 1-2 sentence identity_prompt in third person describing this person's worldview, values, daily concerns, and where they get their information from.",
            "Make them feel like real, specific people — not stereotypes. Reflect the demographic vector but add specificity (a hobby, a recent worry, a community they belong to).",
            "",
            "Demographic vectors:",
        ]
        for i, d in enumerate(demographics_list):
            prompt_parts.append(f"{i}: {d}")
        prompt = "\n".join(prompt_parts)

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=_IdentityBatch,
                temperature=0.95,
            ),
        )
        batch = _IdentityBatch.model_validate_json(response.text)
        by_index = {p.index: p for p in batch.personas}

        personas: list[Persona] = []
        for i, d in enumerate(demographics_list):
            ident = by_index.get(i)
            label = ident.label if ident else f"persona-{i}"
            identity_prompt = ident.identity_prompt if ident else ""
            personas.append(
                Persona(
                    id=str(uuid.uuid4()),
                    label=label,
                    demographics=d,
                    identity_prompt=identity_prompt,
                )
            )
        return personas
