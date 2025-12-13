import re
import uuid
import json
from typing import List
from .schemas import LogicUnit, LogicPlan
from .prompts import REASONING_TEMPLATE
from .lm_provider import LMProvider
from .utils import safe_json_loads


VAGUE_PHRASES = {
    "too long": "queue_length_threshold",
    "after a while": "time_window",
    "a bit": "rate_adjustment",
    "quickly": "speed_value",
    "soon": "time_window",
    "busy": "load_threshold",
    "overloaded": "load_threshold"
}


class IntentParser:
    def __init__(self, lm: LMProvider):
        self.lm = lm

    def parse(self, instruction: str) -> LogicPlan:
        # ------------------------------------------------
        # STEP 0 — HARD ambiguity short-circuit
        # ------------------------------------------------
        inst_lower = instruction.lower()
        missing = [
            field for phrase, field in VAGUE_PHRASES.items()
            if phrase in inst_lower
        ]

        if missing:
            return LogicPlan(
                steps=[
                    LogicUnit(
                        id="S1",
                        role="note",
                        text="Ambiguous instruction",
                        clarification_needed=True,
                        clarification_field=missing[0]
                    )
                ]
            )

        # ------------------------------------------------
        # STEP 1 — LLM reasoning
        # ------------------------------------------------
        prompt = REASONING_TEMPLATE.format(instruction=instruction)
        raw = self.lm.complete(prompt)
        data = safe_json_loads(raw)

        # ------------------------------------------------
        # STEP 2 — Controlled error response
        # ------------------------------------------------
        if "error" in data:
            return LogicPlan(
                steps=[
                    LogicUnit(
                        id="S1",
                        role="note",
                        text="Clarification required",
                        clarification_needed=True,
                        clarification_field=(
                            data.get("fields") or [None]
                        )[0]
                    )
                ]
            )

        # ------------------------------------------------
        # STEP 3 — Build LogicPlan safely
        # ------------------------------------------------
        steps = []
        seen_ids = set()

        for s in data.get("steps", []):
            u = LogicUnit(**s)

            if u.id in seen_ids:
                u.id = f"{u.id}_{uuid.uuid4().hex[:4]}"
            seen_ids.add(u.id)

            steps.append(u)

        return LogicPlan(steps=steps)
