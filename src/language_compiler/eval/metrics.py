import re
from typing import Dict, List, Tuple, Optional

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None


# -------------------------
# Semantic similarity
# -------------------------

class SemanticScorer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if SentenceTransformer is None:
            raise ImportError("pip install sentence-transformers")
        self.model = SentenceTransformer(model_name)

    def score(self, instruction: str, rendered: str) -> float:
        e1 = self.model.encode(instruction, convert_to_tensor=True)
        e2 = self.model.encode(rendered, convert_to_tensor=True)
        return float(util.cos_sim(e1, e2))


# -------------------------
# Structural scoring
# -------------------------

def structural_scores(pred_steps: List[Dict], gold_steps: List[Dict]) -> Dict[str, float]:
    """
    pred_steps and gold_steps are lists of dicts (LogicUnit.model_dump()).
    Order-insensitive matching by (role, operator, value, negated, text coarse).
    """
    def key(s):
        txt = (s.get("text") or "").lower()
        txt = re.sub(r"\s+", " ", txt).strip()
        return (
            s.get("role"),
            s.get("operator"),
            str(s.get("value")) if s.get("value") is not None else None,
            bool(s.get("negated")),
            txt
        )

    pred_keys = [key(s) for s in pred_steps]
    gold_keys = [key(s) for s in gold_steps]

    # multiset match counts
    matched = 0
    pred_pool = pred_keys.copy()

    for g in gold_keys:
        if g in pred_pool:
            matched += 1
            pred_pool.remove(g)

    precision = matched / max(len(pred_keys), 1)
    recall = matched / max(len(gold_keys), 1)
    f1 = (2 * precision * recall / max(precision + recall, 1e-9)) if (precision + recall) else 0.0

    # dependency correctness (simple): percent of action steps whose depends_on set matches gold (by id mapping is hard)
    # We compute a coarse dependency score: actions should depend on at least one condition if gold action does.
    def dep_signature(steps):
        sig = []
        for s in steps:
            if s.get("role") == "action":
                sig.append(len(s.get("depends_on") or []))
        return sig

    pred_dep = dep_signature(pred_steps)
    gold_dep = dep_signature(gold_steps)

    dep_correct = 0
    for p, g in zip(pred_dep, gold_dep):
        dep_correct += int((p > 0) == (g > 0))
    dep_acc = dep_correct / max(len(gold_dep), 1)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "dependency_acc": dep_acc
    }


# -------------------------
# Behavioral scoring
# -------------------------

def behavioral_equivalence(pred_pseudocode: str, gold_pseudocode: str) -> Dict[str, float]:
    """
    Lightweight behavioral proxy:
    - compares extracted condition/operator/value/action tokens.
    Not a full interpreter, but consistent and reportable.
    """
    def tokens(p):
        t = p.lower()
        t = re.sub(r"[^a-z0-9_><= ]+", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return set(t.split())

    tp = tokens(pred_pseudocode)
    tg = tokens(gold_pseudocode)

    jacc = len(tp & tg) / max(len(tp | tg), 1)
    return {"token_jaccard": jacc}
