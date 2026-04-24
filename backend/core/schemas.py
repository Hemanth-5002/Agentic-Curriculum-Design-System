from pydantic import BaseModel
from typing import List, Optional

class Module(BaseModel):
    title: str
    description: str
    credit_hours: int

class CurriculumDraft(BaseModel):
    domain: str
    modules: List[Module]
    prerequisites: List[str]
    rationale: str

class Feedback(BaseModel):
    module_title: str
    comment: str
    rating: int

class GenerationRequest(BaseModel):
    domain: str
    university_name: str
    target_degree: str
    current_syllabus: Optional[str] = ""
