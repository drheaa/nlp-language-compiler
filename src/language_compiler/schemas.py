from typing import List, Optional, Literal
from pydantic import BaseModel

Role = Literal["condition", "action", "note"]

class LogicUnit(BaseModel):
    id: str
    role: Role
    text: str
    depends_on: List[str] = []

    # NEW optional fields for upgraded reasoning
    operator: Optional[str] = None          # AND, OR, >, <, ==, >=, <=
    value: Optional[str] = None             # "25", "5 minutes", etc.
    negated: Optional[bool] = False

    clarification_needed: Optional[bool] = False
    clarification_field: Optional[str] = None


class LogicPlan(BaseModel):
    steps: List[LogicUnit]


class PseudocodeBlock(BaseModel):
    language: str = "pseudocode"
    code: str
    missing_clarifications: Optional[List[str]] = None


class CodeBlock(BaseModel):
    language: str = "python"
    code: str


class CompilerOutput(BaseModel):
    reasoning: LogicPlan
    pseudocode: PseudocodeBlock
    code: Optional[CodeBlock] = None
    clarifications_needed: Optional[List[str]] = None
