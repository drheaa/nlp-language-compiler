from .schemas import CompilerOutput
from .intent_parser import IntentParser
from .pseudocode import PseudocodeGenerator
from .codegen import CodeGenerator
from .lm_provider import LMProvider
from .semantic_preprocessor import SemanticPreprocessor 


class LanguageCompiler:
    """
    Main orchestrator:
    - Parse natural language → LogicPlan
    - Convert LogicPlan → pseudocode (with TODOs if ambiguous)
    - Optionally generate Python code

    Supports hybrid clarification mode:
        compile(instruction, interactive=True)
    returns missing clarifications in CompilerOutput.clarifications_needed.
    """

    def __init__(self, model: str = "microsoft/Phi-3-mini-4k-instruct"):
        self.lm = LMProvider(model=model)
        self.parser = IntentParser(self.lm)
        self.pseudo = PseudocodeGenerator(self.lm)
        self.codegen = CodeGenerator(self.lm)
        self.semantic = SemanticPreprocessor()

    def compile(self, instruction: str, to_code: bool = False, interactive: bool = False) -> CompilerOutput:
        sem = self.semantic.normalize(instruction)
        instruction_norm = sem.normalized_instruction

        plan = self.parser.parse(instruction_norm)
        pseudo = self.pseudo.generate(plan, interactive=interactive)

        clarifications = (pseudo.missing_clarifications if interactive else None)

        return CompilerOutput(
            reasoning=plan,
            pseudocode=pseudo,
            code=None if not to_code else self.codegen.generate_python(pseudo),
            clarifications_needed=clarifications
        )
