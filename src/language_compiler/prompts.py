# ============================================================
# Safe, fully escaped templates for Python .format()
# ============================================================

REASONING_TEMPLATE = """
You extract structured logic from a natural-language instruction.
Return a JSON object following the schema exactly.

Rules:
1. Break the instruction into minimal semantic steps.
2. Assign each step a role: "condition", "action", or "note".
3. Use sequential ids: S1, S2, S3...
4. Use depends_on to indicate causal or logical precedence.
5. If a phrase is ambiguous or missing a numeric threshold 
   (e.g., "too long", "a bit", "after a while", "quickly", "soon"):
       - set clarification_needed = true
       - set clarification_field to the missing value name
         (e.g., "queue_length_threshold", "time_window", "rate_value").
6. Never invent numeric values, conditions, or facts.
7. Never paraphrase meaning.
8. Return ONLY a valid JSON object, no markdown, no explanations.

Instruction:
{instruction}

Return JSON in this exact pattern:
<<<JSON_START>>>
{{"steps":[
  {{"id":"S1","role":"condition","text":"...", "depends_on":[],
    "operator": null, "value": null, "negated": false,
    "clarification_needed": false, "clarification_field": null}}
]}}
"""


# ============================================================

PSEUDOCODE_TEMPLATE = """
Convert this JSON logic plan into clean pseudocode.

Rules:
1. Output ONLY pseudocode.
2. Do NOT include explanations, notes, or meta-commentary.
3. Do NOT mention clarification flags explicitly.
4. Use IF / ELIF / ELSE / LOOP constructs.
5. If clarification_needed = true, insert TODO(<field_name>) inline.
6. Use 4-space indentation.
7. No comments unless strictly required for syntax.

Logic plan JSON:
{logic_json}

Return pseudocode only.
"""


# ============================================================

PYTHON_CODE_TEMPLATE = """
Convert the pseudocode to executable Python 3 code.

Rules:
1. Create stub functions for each action:
       e.g., TURN_ON(x) -> print("TURN_ON", x)
2. Do not use external libraries.
3. Preserve all control flow exactly.
4. Return ONLY Python code — no explanations, no markdown.
5. Do NOT include explanations or natural language.
6. Do NOT describe what the code does.
7. Create stub functions for actions if needed.
8. Preserve control flow exactly.


Pseudocode:
{pseudocode}

Return pseudocode only.
"""
