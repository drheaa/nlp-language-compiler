REASONING_TEMPLATE = """You are a careful logic planner.
Given a human instruction, produce a strictly structured logic plan as JSON.
Rules:
- Break into minimal atomic steps.
- Label each step: "condition" or "action" or "note".
- Use ids "S1", "S2", ...
- Use depends_on to encode precedence.
- Do NOT invent facts.

Instruction:
{instruction}

Return JSON with schema:
{{"steps":[{{"id":"S1","role":"condition|action|note","text":"...","depends_on":["Sx"]}}]}}
"""

PSEUDOCODE_TEMPLATE = """You convert a logic plan into clean, minimal pseudocode.
Follow these rules:
- Use IF/ELSE/ELIF/LOOP constructs.
- Use clear function-like actions (e.g., TURN_ON(AC)).
- Keep indentation consistent with 4 spaces.
- No comments unless essential.

Logic plan JSON:
{logic_json}

Return only the pseudocode, nothing else.
"""

PYTHON_CODE_TEMPLATE = """Convert the pseudocode to idiomatic Python 3.
- Create stub functions for actions (e.g., TURN_ON(x) -> print("TURN_ON", x)).
- Keep control flow intact.
- No external libraries.

Pseudocode:
{pseudocode}
"""

