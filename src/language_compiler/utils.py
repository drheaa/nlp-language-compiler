import json
import re


# ------------------------------------------------------
# Safely parse JSON from LLM output
# ------------------------------------------------------
def safe_json_loads(s: str):
    """
    Attempts to extract a valid JSON object from an LLM response.

    - Removes markdown fences
    - Finds first '{' and last '}'
    - Falls back to a simple eval-safe approach
    - Raises clear error if parsing fails

    This is MUCH more robust than the naive version.
    """

    # Remove backticks or code fences
    s = s.strip().replace("```", "")

    # Try basic bounding by braces
    start = s.find("{")
    end = s.rfind("}")

    if start != -1 and end != -1 and end >= start:
        candidate = s[start:end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass  # fall through to next attempt

    # Fallback: try to locate something that looks like JSON
    try:
        return json.loads(s)
    except Exception:
        pass

    # Final fallback: attempt to sanitize commonly broken patterns
    cleaned = re.sub(r"[\x00-\x1F]+", "", s)
    try:
        return json.loads(cleaned)
    except Exception as e:
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
