# Language Compiler

Natural Language → Logic → Pseudocode → Executable Code

A modular NLP system that compiles messy human instructions into structured logic, readable pseudocode, and optional executable Python, while explicitly handling ambiguity and preserving reasoning transparency.

---

## Project Overview

This project implements a Natural Language Logic Compiler, inspired by classical compiler design principles and modern LLM-based reasoning.

Instead of directly converting natural language into code, the system introduces an explicit intermediate reasoning layer that represents human intent as a structured logic plan before any code is generated.

This makes the system:

- interpretable
- debuggable
- safer

--- 


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
--- 

## What the System Does

Given a natural-language instruction such as:

- If the temperature is above 30 degrees, turn the AC to 20 degrees.

The compiler performs a three-stage transformation:

1. Natural Language → Logic Plan (Intermediate Representation)

The instruction is parsed into a structured LogicPlan, consisting of atomic steps:

- conditions
- actions
- dependencies between steps
- negations (e.g. unless)
- comparisons (>, <, ≥, ≤)
- loops and notes
- ambiguity flags for missing information

Example (conceptual):

S1: condition → temperature > 30
S2: action → set AC temperature to 20
S2 depends_on S1


This LogicPlan acts as the system’s intermediate representation (IR), similar to the IR used in traditional compilers.

2. Logic Plan → Pseudocode

The structured logic is converted into clean, readable pseudocode:

IF temperature > 30:
    SET_AC_TEMPERATURE(20)


If the instruction is ambiguous (e.g. “too hot”, “after a while”), the system does not hallucinate values.
Instead, it inserts explicit placeholders:

IF temperature > TODO(temperature_threshold):
    TURN_ON_AC()


Missing values are surfaced to the user as clarification fields, enabling safe human-in-the-loop workflows.

3. Pseudocode → Executable Python (Optional)

If enabled, the pseudocode is compiled into executable Python:

- control flow is preserved
- action stubs are created deterministically
- syntax is validated using ast.parse
- invalid code is automatically regenerated

Example:

def SET_AC_TEMPERATURE(value):
    print("SET_AC_TEMPERATURE", value)

if temperature > 30:
    SET_AC_TEMPERATURE(20)

---

## Key Features
1) Explicit Reasoning Layer
Unlike direct NL→code systems, this compiler exposes its reasoning explicitly through a structured LogicPlan.

2) Ambiguity Detection (Not Guessing)
Vague instructions are detected and flagged rather than silently filled with invented values.

3) Hybrid Parsing Strategy
- Lightweight heuristic extraction (regex, patterns)
- LLM-assisted normalization into a strict JSON schema

4) Deterministic, Testable Pipeline
- schema validation via Pydantic
- controlled prompt templates
- syntax-checked code generation
- robust post-processing

5) Fully Local & Free
- runs on lightweight CPU-friendly models (Qwen2.5-0.5B, Phi-3.5-mini)
- no paid APIs
- no GPU required
- reproducible in Google Colab
  
---

## Architecture

```text
Natural Language
        ↓
IntentParser
  (heuristics + LLM)
        ↓
LogicPlan (IR)
        ↓
PseudocodeGenerator
        ↓
Pseudocode
        ↓
CodeGenerator (optional)
        ↓
Executable Python
```

Each stage is modular, testable, and independently inspectable.

---

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI Usage
```bash
python app.py "If the temperature is above 30 degrees, turn the AC to 20 degrees."

python app.py \
  "If the queue gets too long, open another counter after a while." \
  --code \
  --interactive
```

-interactive surfaces missing clarification fields instead of silently guessing values.

## Streamlit UI
```bash
streamlit run ui_app.py
```

The UI allows:
- live instruction input
- model selection
- optional Python generation
- visibility into reasoning and missing clarifications

## Testing
Tests are designed to validate structural correctness, not exact string output, due to the probabilistic nature of LLM-based generation.

High-value tests focus on:
- schema validity
- pipeline execution
- utility robustness

Some legacy tests assuming deterministic text outputs are marked as expected failures (xfail).

```bash
pytest
```
All tests are verified in a clean Google Colab environment for reproducibility.

---

## Why This Project Matters

Most natural-language-to-code systems collapse reasoning into a black box.

This project:
- separates intent, logic, and execution
- makes reasoning inspectable before code runs
- avoids unsafe hallucination
- demonstrates how LLMs can be integrated into classical compiler pipelines

It bridges NLP, program synthesis, and systems design in a way suitable for real-world automation, simulations, and rule-based systems.

--- 

## Team Members
- Devanshi Rhea Aucharaz
- Ridhi Jain
- Makhabat Zhyrgalbekova
- Naima Dzhunushova

---


