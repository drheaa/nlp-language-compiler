# Language Compiler

Human intent → transparent logic → pseudocode → (optional) Python.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate 
pip install -r requirements.txt
cp .env.example .env  
```

## CLI

```bash
python app.py "If the temperature is above 25, turn on the AC unless it's raining."
python app.py "For each item in the list, if price > 100, apply 10% discount." --code
```

## Streamlit UI

```bash
streamlit run ui_app.py
```

## Design

- **IntentParser**: NL → structured logic plan (JSON). Hybrid: heuristic seeding + LM normalization.
- **PseudocodeGenerator**: logic plan → clean pseudocode.
- **CodeGenerator** (optional): pseudocode → Python stubs.

## Why This Matters

Unlike a pseudocoder, this surfaces the reasoning layer before any code runs. That's interpretability and safety in one shot.

## Tests

```bash
pytest -q
```

## Team Members
- Devanshi Rhea Aucharaz
- Ridhi Jain
- Makhabat Zhyrgalbekova
- Naima Dzhunushova


