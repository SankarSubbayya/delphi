"""Delphi — synthetic populations as a computational substrate."""

from delphi.agent import AgentResponse, Source, reason_as
from delphi.modes import Mode
from delphi.personas import Persona, PersonaGenerator
from delphi.shock import re_run_with_shock
from delphi.swarm import Forecast, aggregate, run_swarm

__all__ = [
    "AgentResponse",
    "Forecast",
    "Mode",
    "Persona",
    "PersonaGenerator",
    "Source",
    "aggregate",
    "reason_as",
    "re_run_with_shock",
    "run_swarm",
]
