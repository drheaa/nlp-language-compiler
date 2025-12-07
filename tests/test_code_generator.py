from src.language_compiler.schemas import PseudocodeBlock
from src.language_compiler.codegen import CodeGenerator


class DummyLM:
    """Fake LM for Python code generation."""
    def complete(self, prompt: str, **kwargs) -> str:
        return (
            "def TURN_ON(x):\n"
            "    print('TURN_ON', x)\n\n"
            "if not raining:\n"
            "    if temperature > 25:\n"
            "        TURN_ON('AC')"
        )


def test_code_generator_python():
    cg = CodeGenerator(DummyLM())

    pseudo = PseudocodeBlock(
        code="IF NOT raining:\n    IF temperature > 25:\n        TURN_ON(AC)"
    )

    code = cg.generate_python(pseudo)

    assert "def TURN_ON" in code.code
    assert "if" in code.code.lower()
    assert isinstance(code.code, str)

