import json
import pandas as pd

from ..pipeline import LanguageCompiler
from .metrics import SemanticScorer, structural_scores, behavioral_equivalence


def run(gold_path: str, model_name: str = "microsoft/Phi-3-mini-4k-instruct"):
    compiler = LanguageCompiler(model=model_name)
    semantic = SemanticScorer()

    with open(gold_path, "r") as f:
        gold = json.load(f)

    rows = []
    for item in gold:
        instr = item["instruction"]
        out = compiler.compile(instr, to_code=False, interactive=True)

        pred_steps = [s.model_dump() for s in out.reasoning.steps]
        gold_steps = item["gold_steps"]

        pred_pseudo = out.pseudocode.code
        gold_pseudo = item["gold_pseudocode"]

        sem = semantic.score(instr, pred_pseudo)
        struct = structural_scores(pred_steps, gold_steps)
        beh = behavioral_equivalence(pred_pseudo, gold_pseudo)

        rows.append({
            "instruction": instr,
            "semantic_similarity": sem,
            **{f"struct_{k}": v for k, v in struct.items()},
            **{f"beh_{k}": v for k, v in beh.items()},
            "clarifications_needed": out.clarifications_needed
        })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = run("data/gold_house.json")
    print(df.describe(include="all"))
    df.to_csv("eval_results.csv", index=False)
