# src/language_compiler/semantic_preprocessor.py

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .intent_templates import INTENT_TEMPLATES

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None


@dataclass
class SemanticResult:
    normalized_instruction: str
    matched_intent: Optional[str]
    similarity: float
    missing_slots: List[str]


class SemanticPreprocessor:
    """
    Maps raw instructions onto a small template library using embeddings.
    Does NOT invent thresholds. Only normalizes structure and surfaces missing slots.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", min_similarity: float = 0.72):
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is required. Install with: pip install sentence-transformers"
            )
        self.embedder = SentenceTransformer(model_name)
        self.min_similarity = min_similarity

        # Build flattened example index
        self._example_texts: List[str] = []
        self._example_to_template: List[Dict] = []
        for t in INTENT_TEMPLATES:
            for ex in t["examples"]:
                self._example_texts.append(ex)
                self._example_to_template.append(t)

        self._example_embs = self.embedder.encode(self._example_texts, convert_to_tensor=True)

    def normalize(self, instruction: str) -> SemanticResult:
        # Embed and retrieve best matching template example
        q = self.embedder.encode(instruction, convert_to_tensor=True)
        sims = util.cos_sim(q, self._example_embs)[0]
        best_idx = int(sims.argmax())
        best_score = float(sims[best_idx])
        template = self._example_to_template[best_idx]

        # If similarity too low, leave instruction unchanged
        if best_score < self.min_similarity:
            return SemanticResult(
                normalized_instruction=instruction,
                matched_intent=None,
                similarity=best_score,
                missing_slots=[]
            )

        # Light normalization: standardize spacing/casing; do NOT change meaning.
        normalized = self._light_normalize(instruction)

        # Detect missing slots (heuristic: vague phrases & missing numbers where expected)
        missing_slots = self._infer_missing_slots(normalized, template)

        # If missing slots exist, return canonical form to constrain downstream parsing
        if missing_slots:
            normalized = template["canonical_form"]

        return SemanticResult(
            normalized_instruction=normalized,
            matched_intent=template["name"],
            similarity=best_score,
            missing_slots=missing_slots
        )

    def _light_normalize(self, text: str) -> str:
        t = text.strip()
        t = re.sub(r"\s+", " ", t)
        return t

    def _infer_missing_slots(self, text: str, template: Dict) -> List[str]:
        t = text.lower()

        # If canonical expects threshold/operator, try to detect numeric comparison presence
        missing = []

        vague = ["too long", "after a while", "a bit", "quickly", "soon", "busy", "overloaded", "high", "low"]
        if any(v in t for v in vague):
            # vague language usually implies missing threshold/operator
            if "threshold" in template.get("slots", []):
                missing.append("threshold")
            if "operator" in template.get("slots", []):
                missing.append("operator")

        # numeric detection
        has_number = re.search(r"\d+(\.\d+)?", t) is not None
        if "threshold" in template.get("slots", []) and not has_number:
            missing.append("threshold")

        # crude action detection: presence of common verbs
        if "action" in template.get("slots", []):
            if not re.search(r"\b(turn on|turn off|open|close|notify|send|set|activate|deactivate|lock|unlock|start|stop)\b", t):
                missing.append("action")

        return sorted(set(missing))
