import re
import uuid
from typing import List
from .schemas import LogicUnit, LogicPlan
from .prompts import REASONING_TEMPLATE
from .lm_provider import LMProvider
from .utils import safe_json_loads

class IntentParser:
    """
    Hybrid: quick heuristic pass for common patterns (if/unless/else, loops),
    then LM normalization to a consistent JSON logic plan.
    """

    def __init__(self, lm: LMProvider):
        self.lm = lm

    def _heuristic_seed(self, instruction: str) -> List[LogicUnit]:
        steps = []
        sid = lambda: f"S{len(steps)+1}"

        inst = instruction.strip().lower()

        # find "unless" -> precedence condition that blocks others
        unless_match = re.search(r"\bunless\b (.+)", inst)
        if unless_match:
            cond_text = f"NOT ({unless_match.group(1).strip()})"
            steps.append(LogicUnit(id=sid(), role="condition", text=cond_text))

        # find "if ... then" or "if ...," simple condition
        if_match = re.search(r"\bif\b (.+?)(,|\bthen\b|$)", inst)
        if if_match:
            cond_text = if_match.group(1).strip().rstrip(",")
            steps.append(LogicUnit(id=sid(), role="condition", text=cond_text))

        # actions: simple verbs like "turn on", "print", "send", "notify"
        action_match = re.findall(r"\b(turn on|turn off|print|send|notify|set|activate|deactivate)\b(.+)", inst)
        if action_match:
            # take first action phrase
            verb, rest = action_match[0]
            steps.append(LogicUnit(id=sid(), role="action", text=f"{verb.upper()} {rest.strip()}"))

        loop_match = re.search(r"\bfor each\b (.+?)\b( do|:|$)", inst)
        if loop_match:
            steps.insert(0, LogicUnit(id=sid(), role="note", text=f"Loop over {loop_match.group(1).strip()}"))

        if steps:
            cond_ids = [u.id for u in steps if u.role == "condition"]
            for u in steps:
                if u.role == "action":
                    u.depends_on = cond_ids

        return steps

    def parse(self, instruction: str) -> LogicPlan:
        seed = self._heuristic_seed(instruction)
        seed_json = {
            "steps": [u.model_dump() for u in seed] if seed else []
        }
        prompt = REASONING_TEMPLATE.format(instruction=instruction) + \
                 f"\n\nHere is a rough seed; refine and correct it strictly to schema:\n{seed_json}"
        raw = self.lm.complete(prompt)
        data = safe_json_loads(raw)
        steps = [LogicUnit(**s) for s in data["steps"]]
        seen = set()
        for s in steps:
            if s.id in seen:
                s.id = f"{s.id}_{uuid.uuid4().hex[:4]}"
            seen.add(s.id)
        return LogicPlan(steps=steps)
