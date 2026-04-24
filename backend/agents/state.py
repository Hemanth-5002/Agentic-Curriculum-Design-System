from typing import TypedDict, List
from core.schemas import Module

class AgentState(TypedDict):
    domain: str
    target_degree: str
    industry_trends: List[str]
    skill_gap: List[str]
    current_syllabus: str
    academic_research: List[str]
    academic_papers_raw: List[dict]
    draft_modules: List[Module]
    prerequisites: List[str]
    generation_rationale: str
    feedback: List[str]
