import json

def safe_json_loads(s: str):
    # try to find first/last braces to reduce stray text
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end >= start:
        s = s[start:end+1]
    return json.loads(s)
