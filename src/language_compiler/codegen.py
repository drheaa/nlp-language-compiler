from .prompts import PYTHON_CODE_TEMPLATE
from .lm_provider import LMProvider
from .schemas import PseudocodeBlock, CodeBlock

class CodeGenerator:
    def __init__(self, lm: LMProvider):
        self.lm = lm

    def generate_python(self, pseudo: PseudocodeBlock) -> CodeBlock:
        prompt = PYTHON_CODE_TEMPLATE.format(pseudocode=pseudo.code)
        code = self.lm.complete(prompt, max_tokens=700)
        return CodeBlock(language="python", code=code)
