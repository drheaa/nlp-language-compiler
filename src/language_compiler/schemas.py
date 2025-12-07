from typing import List, Optional, Literal
from pydantic import BaseModel

Role = Literal["condition", "action", "note"]

class LogicUnit(BaseModel):
    id: str
    role: Role
    text: str
    depends_on: List[str] = []

class LogicPlan(BaseModel):
    steps: List[LogicUnit]

class PseudocodeBlock(BaseModel):
    language: str = "pseudocode"
    code: str

class CodeBlock(BaseModel):
    language: str = "python"
    code: str

class CompilerOutput(BaseModel):
    reasoning: LogicPlan
    pseudocode: PseudocodeBlock
    code: Optional[CodeBlock] = None
