from .prompts import PSEUDOCODE_TEMPLATE
from .lm_provider import LMProvider
from .schemas import LogicPlan, PseudocodeBlock

class PseudocodeGenerator:
    def __init__(self, lm: LMProvider):
        self.lm = lm

    def generate(self, plan: LogicPlan) -> PseudocodeBlock:
        logic_json = plan.model_dump_json()
        prompt = PSEUDOCODE_TEMPLATE.format(logic_json=logic_json)
        code = self.lm.complete(prompt, max_tokens=500)
        return PseudocodeBlock(code=code)
