from langgraph.graph import StateGraph, END
from agents.state import AgentState
from scrapers.industry import search_industry_trends
from scrapers.academic import search_arxiv
from rag.pipeline import generate_curriculum_rag
import json

# Real nodes for the agents
def industry_trends_agent(state: AgentState):
    domain = state.get("domain", "Artificial Intelligence")
    trends = search_industry_trends(domain)
    return {"industry_trends": trends}

def skill_gap_agent(state: AgentState):
    # logic to identify gaps could be complex, for now we pass through
    # in real setup, this might be another LLM call comparing trends with current_syllabus
    return {"skill_gap": ["Practical implementation", "Latest research integration"]}

# Node removed for autonomous tracking mode

def academic_agent(state: AgentState):
    domain = state.get("domain", "Artificial Intelligence")
    print(f"Academic Agent: Searching ArXiv for {domain}...")
    papers = search_arxiv(domain)
    print(f"Academic Agent: Found {len(papers)} papers.")
    # Store title and link for the RAG
    research_summaries = [f"{p['title']} ({p['link']})" for p in papers]
    return {
        "academic_research": research_summaries,
        "academic_papers_raw": papers # We might need to handle extra keys in TypedDict
    }

def orchestrator(state: AgentState):
    domain = state["domain"]
    industry = state["industry_trends"]
    academic = state.get("academic_papers_raw", [])
    if not academic:
        academic = [] 
        
    current_syllabus = "AUTONOMOUS_TRACKING_MODE: No legacy syllabus provided. Agent must generate based on 100% real-time industry and academic needs."
    
    # Trigger RAG to generate the curriculum
    print("Orchestrator: Triggering RAG synthesis...")
    content = generate_curriculum_rag(domain, industry, academic, current_syllabus)
    print("Orchestrator: RAG synthesis complete.")
    
    try:
        # Check if LLM returned JSON block
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        return {
            "draft_modules": data.get("modules", []),
            "generation_rationale": data.get("rationale", ""),
            "prerequisites": data.get("prerequisites", [])
        }
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return {
            "generation_rationale": f"Error occurred: {str(e)}",
            "draft_modules": []
        }

# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("industry_trends", industry_trends_agent)
workflow.add_node("skill_gap", skill_gap_agent)
workflow.add_node("academic", academic_agent)
workflow.add_node("orchestrator", orchestrator)

# Define edges
workflow.set_entry_point("industry_trends")

# Start both research paths immediately
workflow.add_edge("industry_trends", "academic")
workflow.add_edge("industry_trends", "skill_gap")

# Finally, all flow into orchestrator
workflow.add_edge("skill_gap", "orchestrator")
workflow.add_edge("academic", "orchestrator")

workflow.add_edge("orchestrator", END)

app = workflow.compile()
