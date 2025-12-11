import json
import re


# ------------------------------------------------------
# Safely parse JSON from LLM output
# ------------------------------------------------------
def safe_json_loads(s: str):
    """
    Attempts to extract a valid JSON object from an LLM response.

    - Removes markdown fences (e.g., ```json)
    - Uses regex to find and extract the JSON structure (first '{' to last '}')
    - Tries to repair common errors before final parsing
    - Raises clear error if parsing fails
    """

    # 1. Strip and normalize common artifacts
    s = s.strip()
    s = s.replace("```json", "").replace("```JSON", "").replace("```", "")
    s = re.sub(r"^\s*?(\w+\s*?\:\s*?)", "", s, flags=re.MULTILINE).strip() # Removes leading "Response:" or "JSON:"

    # 2. Aggressive Bounding (The key improvement)
    # Search for the content between the first '{' and the last '}'
    match = re.search(r"(\{.*\})", s, re.DOTALL)
    
    candidate = s
    if match:
        candidate = match.group(1)
    
    # 3. First attempt: Parse the bounded candidate
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        # If it fails, try a simpler cleaning/parsing (fallback)
        pass 

    # 4. Fallback: sanitize and try again
    # Replace non-printable characters and try direct loading
    cleaned = re.sub(r"[\x00-\x1F]+", "", s)
    
    # Try the cleaned string
    try:
        # Check if the cleaned string starts with a brace (most reliable signal)
        if cleaned.startswith('{'):
            return json.loads(cleaned)
        # Otherwise, retry the aggressive bounding on the cleaned string
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