from typing import List, Optional, Literal
from pydantic import BaseModel, Field

Role = Literal["condition", "action", "note"]

class LogicUnit(BaseModel):
    id: str
    role: Role
    text: str

    depends_on: List[str] = Field(default_factory=list)

    operator: Optional[str] = None
    value: Optional[str] = None
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
