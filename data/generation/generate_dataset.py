import json
from data.generation.instruction_templates import (
    simple_condition,
    negation,
    multi_condition,
    temporal,
    ambiguous
)

dataset = []

def add(n, fn, label):
    for _ in range(n):
        dataset.append({
            "type": label,
            "instruction": fn()
        })

add(30, simple_condition, "simple")
add(30, simple_condition, "threshold")
add(22, negation, "negation")
add(22, multi_condition, "multi_condition")
add(22, temporal, "temporal")
add(22, ambiguous, "ambiguous")

with open("data/instructions/house_instructions.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Generated", len(dataset), "instructions")
