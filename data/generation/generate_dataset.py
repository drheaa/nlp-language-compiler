import json
from instruction_templates import (
    simple_condition, negation, multi_condition, temporal, ambiguous
)

dataset = []

for _ in range(30):
    dataset.append({"type": "simple", "instruction": simple_condition()})

for _ in range(30):
    dataset.append({"type": "threshold", "instruction": simple_condition()})

for _ in range(22):
    dataset.append({"type": "negation", "instruction": negation()})

for _ in range(22):
    dataset.append({"type": "multi_condition", "instruction": multi_condition()})

for _ in range(22):
    dataset.append({"type": "temporal", "instruction": temporal()})

for _ in range(22):
    dataset.append({"type": "ambiguous", "instruction": ambiguous()})

with open("house_instructions.json", "w") as f:
    json.dump(dataset, f, indent=2)
