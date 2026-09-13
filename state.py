from typing import TypedDict, List

class ResearchState(TypedDict):
    topic: str
    subtopics: List[str]
    findings: List[dict]
    critique: str
    needs_more_research: bool
    loop_count: int
    final_report: str
    log: List[str]