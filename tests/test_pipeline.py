from src.language_compiler.pipeline import LanguageCompiler


class DummyLM:
    """Unified fake LM for reasoning, pseudocode, and Python code."""
    def complete(self, prompt: str, **kwargs):
        text = prompt.lower()

        # --- Reasoning plan ---
        if "steps" in text or "schema" in text:
            return """
            {
              "steps": [
                {"id": "S1", "role": "condition", "text": "NOT raining", "depends_on": []},
                {"id": "S2", "role": "condition", "text": "temperature > 25", "depends_on": []},
                {"id": "S3", "role": "action", "text": "TURN_ON AC", "depends_on": ["S1","S2"]}
              ]
            }
            """

        # --- Pseudocode ---
        if "pseudocode" in text:
            return (
                "IF NOT raining:\n"
                "    IF temperature > 25:\n"
                "        TURN_ON(AC)"
            )

        # --- Python code ---
        return (
            "def TURN_ON(x):\n"
            "    print('TURN_ON', x)\n\n"
            "if not raining:\n"
            "    if temperature > 25:\n"
            "        TURN_ON('AC')"
        )


def fake_init(self, model="phi"):
    """Monkeypatch LMProvider with DummyLM."""
    from src.language_compiler.intent_parser import IntentParser
    from src.language_compiler.pseudocode import PseudocodeGenerator
    from src.language_compiler.codegen import CodeGenerator

    self.lm = DummyLM()
    self.parser = IntentParser(self.lm)
    self.pseudo = PseudocodeGenerator(self.lm)
    self.codegen = CodeGenerator(self.lm)


def test_full_pipeline(monkeypatch):
    monkeypatch.setattr(LanguageCompiler, "__init__", fake_init)

    compiler = LanguageCompiler()
    out = compiler.compile("If temp > 25, turn on AC unless raining.", to_code=True)

    # Check reasoning
    assert len(out.reasoning.steps) == 3
    assert out.reasoning.steps[-1].role == "action"

    # Check pseudocode
    assert "TURN_ON" in out.pseudocode.code

    # Check python code
    assert "def TURN_ON" in out.code.code

