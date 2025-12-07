from .schemas import CompilerOutput
from .intent_parser import IntentParser
from .pseudocode import PseudocodeGenerator
from .codegen import CodeGenerator
from .lm_provider import LMProvider

class LanguageCompiler:
    def __init__(self, model: str = "microsoft/Phi-3-mini-4k-instruct"):
        self.lm = LMProvider(model=model)
        self.parser = IntentParser(self.lm)
        self.pseudo = PseudocodeGenerator(self.lm)
        self.codegen = CodeGenerator(self.lm)

    def compile(self, instruction: str, to_code: bool = False) -> CompilerOutput:
        plan = self.parser.parse(instruction)
        pseudo = self.pseudo.generate(plan)
        code = self.codegen.generate_python(pseudo) if to_code else None
        return CompilerOutput(reasoning=plan, pseudocode=pseudo, code=code)

