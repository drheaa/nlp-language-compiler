import json
from typing import List
from .schemas import LogicPlan, PseudocodeBlock
from .prompts import PSEUDOCODE_TEMPLATE
from .lm_provider import LMProvider


class PseudocodeGenerator:
    """
    Generates pseudocode from a LogicPlan using:
    1. LLM formatting guided by PSEUDOCODE_TEMPLATE
    2. Clarification-aware TODO marker insertion
    """

    def __init__(self, lm: LMProvider):
        self.lm = lm

    # ------------------------------------------------------
    # Extract missing clarifications from the logic plan
    # ------------------------------------------------------
    def _collect_missing_fields(self, plan: LogicPlan) -> List[str]:
        missing = []
        for step in plan.steps:
            if step.clarification_needed and step.clarification_field:
                missing.append(step.clarification_field)
        return missing

    # ------------------------------------------------------
    # Produce pseudocode using the LLM
    # ------------------------------------------------------
    def generate(self, plan: LogicPlan, interactive: bool = False) -> PseudocodeBlock:
        """
        interactive=False  → pseudocode contains TODO(field)
        interactive=True   → same pseudocode, but CompilerOutput will
                             return clarifications_needed list so caller
                             can ask the user for missing values.

        This generator itself NEVER asks the user — that is handled
        by the pipeline.
        """

        logic_json = plan.model_dump()
        logic_str = json.dumps(logic_json, indent=2)

        prompt = PSEUDOCODE_TEMPLATE.format(logic_json=logic_str)

        pseudo = self.lm.complete(prompt, max_tokens=500).strip()

        # Gather missing clarification fields
        missing_fields = self._collect_missing_fields(plan)

        return PseudocodeBlock(
            code=pseudo,
            missing_clarifications=missing_fields if interactive else None
        )
