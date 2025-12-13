REASONING_TEMPLATE = """
You extract structured logic from a natural-language instruction.

You MUST output a single valid JSON object and nothing else.

Rules:
1. Break the instruction into minimal semantic steps.
2. Assign each step a role: "condition", "action", or "note".
3. Use sequential ids: S1, S2, S3...
4. Use depends_on to indicate causal or logical precedence.
5. If a phrase is ambiguous or missing a numeric threshold
   (e.g., "too long", "a bit", "after a while", "quickly", "soon"):
      - DO NOT guess values
      - Return a clarification-required response
6. Never invent facts or thresholds.
7. Never paraphrase meaning.
8. No markdown, no explanations, no extra text.

If clarification is required, return EXACTLY:
{{"error":"clarification_required","fields":["<field_name>"]}}

Otherwise, return EXACTLY:
{
  "steps": [
    {
      "id": "S1",
      "role": "condition",
      "text": "...",
      "depends_on": [],
      "operator": null,
      "value": null,
      "negated": false,
      "clarification_needed": false,
      "clarification_field": null
    }
  ]
}

Instruction:
{instruction}
"""


# ============================================================

PSEUDOCODE_TEMPLATE = """
Convert this JSON logic plan into clean pseudocode.

Rules:
1. Output ONLY pseudocode.
2. No explanations or commentary.
3. Use IF / ELIF / ELSE / LOOP constructs.
4. Insert TODO(<field_name>) if clarification is needed.
5. Use 4-space indentation.
6. No comments unless required for syntax.

Logic plan JSON:
{logic_json}

Return pseudocode only.
"""


# ============================================================

PYTHON_CODE_TEMPLATE = """
Convert the pseudocode to executable Python 3 code.

Rules:
1. Create stub functions for actions.
2. No external libraries.
3. Preserve control flow exactly.
4. Return ONLY Python code.
5. No explanations or comments.

Pseudocode:
{pseudocode}
"""
