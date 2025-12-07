from src.language_compiler.schemas import LogicPlan, LogicUnit
from src.language_compiler.pseudocode import PseudocodeGenerator


class DummyLM:
    """Fake LM for pseudocode generation."""
    def complete(self, prompt: str, **kwargs) -> str:
        return (
            "IF NOT raining:\n"
            "    IF temperature > 25:\n"
            "        TURN_ON(AC)"
        )


def test_pseudocode_generation():
    lm = DummyLM()
    gen = PseudocodeGenerator(lm)

    plan = LogicPlan(steps=[
        LogicUnit(id="S1", role="condition", text="NOT raining", depends_on=[]),
        LogicUnit(id="S2", role="condition", text="temperature > 25"),
        LogicUnit(id="S3", role="action", text="TURN_ON AC", depends_on=["S1", "S2"]),
    ])

    pseudo = gen.generate(plan)

    assert "IF NOT raining" in pseudo.code
    assert "TURN_ON(AC)" in pseudo.code
    assert isinstance(pseudo.code, str)

