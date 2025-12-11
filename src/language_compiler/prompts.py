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
{"steps":[
  {"id":"S1","role":"condition","text":"...", "depends_on":[], 
   "operator": null, "value": null, "negated": false,
   "clarification_needed": false, "clarification_field": null}
]}
"""

PSEUDOCODE_TEMPLATE = """
Convert this JSON logic plan into clean pseudocode.

Rules:
1. Preserve step order based on depends_on relationships.
2. Use IF / ELIF / ELSE / LOOP for logic.
3. Convert negated conditions into NOT(...).
4. For any step where clarification_needed = true,
       insert TODO(clarification_field) in place of missing values.
5. Use 4-space indentation.
6. Output ONLY pseudocode, no markdown, no comments.

Logic plan JSON:
{logic_json}
"""

PYTHON_CODE_TEMPLATE = """
Convert the pseudocode to executable Python 3 code.

Rules:
1. Create stub functions for each action:
       e.g., TURN_ON(x) -> print("TURN_ON", x)
2. Do not use external libraries.
3. Preserve all control flow exactly.
4. Return ONLY Python code — no explanations, no markdown.

Pseudocode:
{pseudocode}
"""
