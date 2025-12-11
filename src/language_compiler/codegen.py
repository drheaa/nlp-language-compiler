import ast
from .prompts import PYTHON_CODE_TEMPLATE
from .lm_provider import LMProvider
from .schemas import PseudocodeBlock, CodeBlock
from .utils import clean_code

class CodeGenerator:
    """
    Converts pseudocode → executable Python.
    - Ensures deterministic output
    - Repairs invalid Python via second-pass prompt
    """

    def __init__(self, lm: LMProvider):
        self.lm = lm

    # ------------------------------------------------------
    # Helper: check if code is valid Python syntax
    # ------------------------------------------------------
    def _is_valid_python(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    # ------------------------------------------------------
    # Helper: second-pass correction if syntax fails
    # ------------------------------------------------------
    def _repair_code(self, pseudo: str) -> str:
        fix_prompt = (
            "The previous Python output contained syntax errors.\n"
            "Regenerate correct, executable Python 3 code.\n\n"
            "Pseudocode:\n"
            f"{pseudo}"
        )
        fixed = self.lm.complete(fix_prompt, max_tokens=700)
        return clean_code(fixed)

    # ------------------------------------------------------
    # Main generator
    # ------------------------------------------------------
    def generate_python(self, pseudo_block: PseudocodeBlock) -> CodeBlock:
        pseudo = pseudo_block.code

        # First attempt
        prompt = PYTHON_CODE_TEMPLATE.format(pseudocode=pseudo)
        code = self.lm.complete(prompt, max_tokens=700)
        code = clean_code(code)

        # Validate syntax
        if not self._is_valid_python(code):
            code = self._repair_code(pseudo)

        return CodeBlock(language="python", code=code)
