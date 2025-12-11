import json
import re


# ------------------------------------------------------
# Safely parse JSON from LLM output
# ------------------------------------------------------
def safe_json_loads(s: str):
    """
    Attempts to extract a valid JSON object from an LLM response.
    Specifically targets and removes common small-model artifacts like preambles.
    """

    # 1. Aggressive cleaning of common noise and markdown
    s = s.strip()
    s = s.replace("```json", "").replace("```JSON", "").replace("```", "")
    
    # NEW: Explicitly remove the model's verbose preamble text
    if "Explanation of the seed:" in s:
        # Find the start of the explanation and discard it and everything before it
        s = s.split("Explanation of the seed:", 1)[-1].strip()
    
    # 2. Aggressive Bounding (Search for the content between the first '{' and the last '}')
    match = re.search(r"(\{.*\})", s, re.DOTALL)
    
    candidate = s
    if match:
        candidate = match.group(1)
    
    # 3. First attempt: Parse the bounded candidate
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass  # Fall through to the final fallback

    # 4. Final fallback: sanitize and try again
    cleaned = re.sub(r"[\x00-\x1F]+", "", s)
    
    try:
        # Retry with the aggressive bounding on the cleaned string
        match_cleaned = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match_cleaned:
            return json.loads(match_cleaned.group(1))
            
    except Exception as e:
        # 5. Final failure
        raise ValueError(f"Failed to parse JSON from model output:\n{s}") from e


# ------------------------------------------------------
# Clean generated Python code
# ------------------------------------------------------
def clean_code(code: str) -> str:
    """
    Removes common artifacts from LLM-generated Python:
    - markdown fences
    - leading 'Here is...' text
    - trailing explanations
    - empty lines
    """

    # Remove markdown code fences
    code = code.replace("```python", "").replace("```", "").strip()

    # Remove narration like "Here is your code:"
    code = re.sub(r"(?i)^here is.*?:", "", code).strip()

    # Remove sentences that are not code (very conservative)
    lines = code.split("\n")
    clean_lines = []
    for line in lines:
        if re.match(r"^\s*(#|def|class|import|from|\w|\s|if|else|elif|for|while|return|try|except)", line):
            clean_lines.append(line)
        # ignore stray natural language lines

    # Rejoin
    cleaned = "\n".join(clean_lines).strip()

    return cleaned


# ------------------------------------------------------
# Optional: normalize whitespace for parsing
# ------------------------------------------------------
def normalize_instruction(text: str) -> str:
    return " ".join(text.strip().split())
