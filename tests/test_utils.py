from src.language_compiler.utils import safe_json_loads


def test_safe_json_loads_basic():
    raw = "extra text {\"a\": 1, \"b\": 2} trailing text"
    data = safe_json_loads(raw)
    assert data["a"] == 1
    assert data["b"] == 2


def test_safe_json_loads_nested():
    raw = """
    Some text here
    {
       "steps": [
          {"id": "S1", "role": "condition", "text": "x > 0", "depends_on": []}
       ]
    }
    More garbage
    """
    data = safe_json_loads(raw)
    assert "steps" in data
    assert data["steps"][0]["id"] == "S1"
