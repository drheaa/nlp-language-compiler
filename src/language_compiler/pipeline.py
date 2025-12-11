from .schemas import CompilerOutput
from .intent_parser import IntentParser
from .pseudocode import PseudocodeGenerator
from .codegen import CodeGenerator
from .lm_provider import LMProvider


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

    def compile(
        self,
        instruction: str,
        to_code: bool = False,
        interactive: bool = False
    ) -> CompilerOutput:

        # -------------------------
        # Step 1 — Extract logic
        # -------------------------
        plan = self.parser.parse(instruction)

        # -------------------------
        # Step 2 — Generate pseudocode
        # TODO markers inserted for missing clarifications
        # -------------------------
        pseudo = self.pseudo.generate(plan, interactive=interactive)

        # Gather missing clarifications if interactive mode is enabled
        clarifications = (
            pseudo.missing_clarifications if interactive else None
        )

        # -------------------------
        # Step 3 — Generate Python code (optional)
        # -------------------------
        code = None
        if to_code:
            code = self.codegen.generate_python(pseudo)

        # -------------------------
        # Final structured output
        # -------------------------
        return CompilerOutput(
            reasoning=plan,
            pseudocode=pseudo,
            code=code,
            clarifications_needed=clarifications
        )
