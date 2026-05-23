"""Question framings: forecast / pretest / stress-test / open."""

from enum import Enum


class Mode(str, Enum):
    FORECAST = "forecast"
    PRETEST = "pretest"
    STRESS_TEST = "stress_test"
    OPEN = "open"


REASONING_TEMPLATES: dict[Mode, str] = {
    Mode.FORECAST: """You are {persona_label}. {persona_identity}

Question: {question}

Give your honest forecast from YOUR persona's perspective — including this persona's blind spots and biases. Use search when current information would help.

Respond with JSON only, matching:
{{
  "position": <float 0..1, your probability that the answer is yes>,
  "confidence": <float 0..1, how confident YOU are in your estimate>,
  "reasoning": "<1-3 sentences in your persona's voice>",
  "sources": [{{"url": "<string>", "title": "<string>", "snippet": "<string>"}}]
}}""",
    Mode.PRETEST: """You are {persona_label}. {persona_identity}

You are reacting to the following message / product / idea:
{question}

React honestly from YOUR persona's perspective.

Respond with JSON only, matching:
{{
  "position": "positive" | "neutral" | "negative",
  "confidence": <float 0..1>,
  "reasoning": "<1-3 sentences in your persona's voice>",
  "sources": [{{"url": "<string>", "title": "<string>", "snippet": "<string>"}}]
}}""",
    Mode.STRESS_TEST: """You are {persona_label}. {persona_identity}

The following statement / decision / launch is being proposed:
{question}

Surface the most likely objections, failure modes, or concerns from YOUR persona's perspective. Be specific.

Respond with JSON only, matching:
{{
  "position": "supports" | "neutral" | "objects",
  "confidence": <float 0..1>,
  "reasoning": "<1-3 sentences naming the specific concern in your voice>",
  "sources": [{{"url": "<string>", "title": "<string>", "snippet": "<string>"}}]
}}""",
    Mode.OPEN: """You are {persona_label}. {persona_identity}

Question: {question}

Respond as this persona would.

Respond with JSON only, matching:
{{
  "position": "<short free-text answer>",
  "confidence": <float 0..1>,
  "reasoning": "<1-3 sentences>",
  "sources": [{{"url": "<string>", "title": "<string>", "snippet": "<string>"}}]
}}""",
}
