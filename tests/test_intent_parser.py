from src.language_compiler.intent_parser import IntentParser
from src.language_compiler.schemas import LogicUnit, LogicPlan


class DummyLM:
    """Fake LM for reasoning → returns structured JSON no matter the prompt."""
    def complete(self, prompt: str, **kwargs) -> str:
        return """
        {
            "steps": [
                {"id": "S1", "role": "condition", "text": "NOT raining", "depends_on": []},
                {"id": "S2", "role": "condition", "text": "temperature > 25", "depends_on": []},
                {"id": "S3", "role": "action", "text": "TURN_ON AC", "depends_on": ["S1", "S2"]}
            ]
        }
        """


def test_intent_parser_basic():
    parser = IntentParser(DummyLM())
    plan = parser.parse("If temperature > 25, turn on AC unless raining.")

    assert isinstance(plan, LogicPlan)
    assert len(plan.steps) == 3

    assert plan.steps[0].role == "condition"
    assert plan.steps[-1].role == "action"
    assert "TURN_ON" in plan.steps[-1].text

