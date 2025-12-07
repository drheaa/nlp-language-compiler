from src.language_compiler.schemas import (
    LogicUnit,
    LogicPlan,
    PseudocodeBlock,
    CodeBlock,
    CompilerOutput
)


def test_logic_unit_model():
    u = LogicUnit(id="S1", role="condition", text="x > 0", depends_on=["S0"])
    assert u.id == "S1"
    assert u.role == "condition"
    assert u.text == "x > 0"
    assert u.depends_on == ["S0"]


def test_logic_plan_model():
    steps = [
        LogicUnit(id="S1", role="condition", text="x > 0", depends_on=[])
    ]
    plan = LogicPlan(steps=steps)
    assert len(plan.steps) == 1
    assert plan.steps[0].text == "x > 0"


def test_pseudocode_block_model():
    p = PseudocodeBlock(code="IF x > 0: PRINT('hi')")
    assert "PRINT" in p.code


def test_codeblock_model():
    c = CodeBlock(code="print('hello')", language="python")
    assert "print" in c.code


def test_compiler_output_model():
    reasoning = LogicPlan(steps=[])
    pseudo = PseudocodeBlock(code="pass")
    out = CompilerOutput(reasoning=reasoning, pseudocode=pseudo, code=None)
    assert out.reasoning.steps == []
    assert out.pseudocode.code == "pass"

