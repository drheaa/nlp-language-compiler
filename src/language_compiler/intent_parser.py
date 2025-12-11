import re
import uuid
from typing import List
from .schemas import LogicUnit, LogicPlan
from .prompts import REASONING_TEMPLATE
from .lm_provider import LMProvider
from .utils import safe_json_loads

# ---------------------------------------------
# Pattern dictionaries for heuristics
# ---------------------------------------------

VAGUE_PHRASES = {
    "too long": "queue_length_threshold",
    "after a while": "time_window",
    "a bit": "rate_adjustment",
    "quickly": "speed_value",
    "soon": "time_window",
    "busy": "load_threshold",
    "overloaded": "load_threshold"
}

COMPARISON_PATTERNS = [
    (r"greater than (\d+)", ">"),
    (r"more than (\d+)", ">"),
    (r"less than (\d+)", "<"),
    (r"fewer than (\d+)", "<"),
    (r"below (\d+)", "<"),
    (r"above (\d+)", ">"),
    (r"at least (\d+)", ">="),
    (r"at most (\d+)", "<="),
]

ACTION_VERBS = [
    "turn on", "turn off", "print", "send", "notify", "set",
    "activate", "deactivate", "open", "close", "increase", "decrease"
]


# ---------------------------------------------
# IntentParser class
# ---------------------------------------------

class IntentParser:
    """
    Hybrid parser:
    1. Lightweight heuristic pass extracts obvious conditions, actions, and ambiguity.
    2. LM refinement produces a JSON LogicPlan following strict schema.
    """

    def __init__(self, lm: LMProvider):
        self.lm = lm

    # -----------------------------------------
    # Heuristic seed extraction
    # -----------------------------------------
    def _heuristic_seed(self, instruction: str) -> List[LogicUnit]:
        steps = []
        new_id = lambda: f"S{len(steps)+1}"

        inst = instruction.strip().lower()

        # --- (1) detect vague / ambiguous phrases → clarification needed
        for phrase, field in VAGUE_PHRASES.items():
            if phrase in inst:
                steps.append(
                    LogicUnit(
                        id=new_id(),
                        role="note",
                        text=phrase,
                        clarification_needed=True,
                        clarification_field=field
                    )
                )

        # --- (2) detect explicit comparisons
        for pattern, op in COMPARISON_PATTERNS:
            match = re.search(pattern, inst)
            if match:
                value = match.group(1)
                steps.append(
                    LogicUnit(
                        id=new_id(),
                        role="condition",
                        text=f"{op} {value}",
                        operator=op,
                        value=value
                    )
                )

        # --- (3) detect "unless" negation structure
        unless_match = re.search(r"\bunless\b (.+)", inst)
        if unless_match:
            cond = unless_match.group(1).strip()
            steps.append(
                LogicUnit(
                    id=new_id(),
                    role="condition",
                    text=f"NOT ({cond})",
                    negated=True
                )
            )

        # --- (4) detect simple if clause
        if_match = re.search(r"\bif\b (.+?)(,|\bthen\b|$)", inst)
        if if_match:
            cond = if_match.group(1).strip().rstrip(",")
            steps.append(
                LogicUnit(
                    id=new_id(),
                    role="condition",
                    text=cond
                )
            )

        # --- (5) detect multiple action phrases
        for verb in ACTION_VERBS:
            for m in re.finditer(verb + r" (.+?)(?:\.|,|$)", inst):
                rest = m.group(1).strip()
                steps.append(
                    LogicUnit(
                        id=new_id(),
                        role="action",
                        text=f"{verb.upper()} {rest}"
                    )
                )

        # --- (6) detect loops
        loop_match = re.search(r"\bfor each\b (.+?)\b( do|:|$)", inst)
        if loop_match:
            steps.insert(
                0,
                LogicUnit(
                    id=new_id(),
                    role="note",
                    text=f"Loop over {loop_match.group(1).strip()}"
                )
            )

        # --- (7) wire conditions to actions
        cond_ids = [u.id for u in steps if u.role == "condition"]
        for u in steps:
            if u.role == "action":
                u.depends_on = cond_ids.copy()

        return steps

    # -----------------------------------------
    # LLM-assisted refinement into LogicPlan
    # -----------------------------------------
    def parse(self, instruction: str) -> LogicPlan:
        # Step 1: heuristic seed
        seed = self._heuristic_seed(instruction)
        seed_json = {"steps": [u.model_dump() for u in seed]}

        # Step 2: LLM refinement
        prompt = (
            REASONING_TEMPLATE.format(instruction=instruction)
            + "\n\nSeed (rough heuristic; refine strictly to schema):\n"
            + str(seed_json)
        )

        raw = self.lm.complete(prompt)
        data = safe_json_loads(raw)

        # Step 3: build LogicUnits safely
        steps = []
        seen_ids = set()

        for s in data.get("steps", []):
            u = LogicUnit(**s)

            # Ensure unique ids
            if u.id in seen_ids:
                u.id = f"{u.id}_{uuid.uuid4().hex[:4]}"
            seen_ids.add(u.id)

            steps.append(u)

        return LogicPlan(steps=steps)
