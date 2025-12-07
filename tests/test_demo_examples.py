from src.language_compiler.pipeline import LanguageCompiler


class DummyLM:
    """A unified fake LLM for showcase tests."""
    def complete(self, prompt: str, **kwargs):
        text = prompt.lower()

        # Reasoning plan
        if "steps" in text or "schema" in text:
            return """
            {
              "steps": [
                {"id": "S1", "role": "condition", "text": "value > 10", "depends_on": []},
                {"id": "S2", "role": "action", "text": "PRINT 'OK'", "depends_on": ["S1"]}
              ]
            }
            """

        # Pseudocode
        if "pseudocode" in text:
            return (
                "IF value > 10:\n"
                "    PRINT('OK')"
            )

        # Python code
        return (
            "if value > 10:\n"
            "    print('OK')"
        )


def fake_init(self, model="phi"):
    from src.language_compiler.intent_parser import IntentParser
    from src.language_compiler.pseudocode import PseudocodeGenerator
    from src.language_compiler.codegen import CodeGenerator

    self.lm = DummyLM()
    self.parser = IntentParser(self.lm)
    self.pseudo = PseudocodeGenerator(self.lm)
    self.codegen = CodeGenerator(self.lm)


def test_demo_examples(monkeypatch):
    # Replace real LM with DummyLM
    monkeypatch.setattr(LanguageCompiler, "__init__", fake_init)

    compiler = LanguageCompiler()

    instructions = [
        "If value > 10, print OK.",
        "If value is greater than 10, then print OK.",
        "Print OK only when the value exceeds 10."
    ]

    for instr in instructions:
        out = compiler.compile(instr, to_code=True)

        # reasoning
        assert len(out.reasoning.steps) == 2

        # pseudocode
        assert "PRINT('OK')" in out.pseudocode.code

        # python code
        assert "print('OK')" in out.code.code
