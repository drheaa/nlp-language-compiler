import json
import re

# ------------------------------------------------------
# Safely parse JSON from LLM output (FINAL REVISION)
# ------------------------------------------------------
def safe_json_loads(s: str):
    """
    Attempts to extract a valid JSON object from an LLM response.
    Aggressively strips all leading and trailing non-JSON artifacts.
    """

    # 1. Strip markdown fences and general whitespace
    s = s.strip()
    s = s.replace("```json", "").replace("```JSON", "").replace("```", "")
    
    # 2. CRITICAL FIX: Aggressively strip everything BEFORE the first opening brace.
    # This is necessary to remove the "Explanation of the seed:" preamble.
    start = s.find('{')
    if start == -1:
        # If no opening brace is found, the model failed completely.
        raise ValueError(f"Failed to find starting JSON brace in model output:\n{s}")

    # Candidate starts at the first '{' and ends at the last '}'
    # rfind('}') + 1 ensures we include the closing brace.
    candidate = s[start:s.rfind('}') + 1]
    
    # 3. First attempt: Parse the clean candidate string
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass  # Fall through to the final fallback

    # 4. Final fallback: sanitize (remove non-printable chars) and retry
    cleaned = re.sub(r"[\x00-\x1F\u2022\u2023]+", "", candidate)
    
    try:
        return json.loads(cleaned)
            
    except Exception as e:
        # 5. Final failure - use the original output for context in the error
        raise ValueError(f"Failed to parse JSON from model output (Check LLM output):\n{s}") from e


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
