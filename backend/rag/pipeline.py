import os
from typing import List
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from dotenv import load_dotenv

load_dotenv()

def generate_curriculum_rag(domain: str, industry_data: List[str], academic_papers: List[dict], current_syllabus: str) -> str:
    """
    Use RAG to synthesize a curriculum draft.
    """
    llm = OpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # Combine all research data into documents
    documents = []
    
    # Industry data
    industry_text = "Industry Trends: " + ", ".join(industry_data)
    documents.append(Document(text=industry_text, metadata={"source": "industry_search"}))
    
    # Academic data
    for paper in academic_papers:
        text = f"Title: {paper['title']}\nSummary: {paper['summary']}"
        documents.append(Document(text=text, metadata={"source": "arxiv", "link": paper['link']}))
        
    # Current Syllabus data
    documents.append(Document(text=f"Existing Syllabus: {current_syllabus}", metadata={"source": "university_input"}))
    
    try:
        # Create index
        print("RAG: Creating VectorStoreIndex...")
        index = VectorStoreIndex.from_documents(documents)
        
        # Query engine
        print("RAG: Querying LLM (gpt-4o-mini)...")
        query_engine = index.as_query_engine(llm=llm)
        
        prompt = f"""
        Based on the provided industry trends, academic papers, and current syllabus for {domain}, 
        propose a modern curriculum. 
        Focus on closing the gap between academia and industry.
        
        Return the response in JSON format matching this schema:
        {{
            "domain": "{domain}",
            "modules": [
                {{
                    "title": "Module Title",
                    "description": "Module Description",
                    "credit_hours": 3
                }}
            ],
            "prerequisites": ["Prereq 1", "Prereq 2"],
            "rationale": "Detailed explanation of why this was chosen."
        }}
        """
        
        response = query_engine.query(prompt)
        print("RAG: LLM response received.")
        return str(response)
    except Exception as e:
        print(f"RAG Error: {e}")
        # Always return fallback instead of raising to keep the UI alive
        import json
        fallback = {
            "domain": domain,
            "modules": [
                {
                    "title": f"Core Principles of {domain}",
                    "description": "Foundational module covering high-demand industry skills and modern research applications.",
                    "credit_hours": 4
                },
                {
                    "title": "Agentic Implementation Lab",
                    "description": "Practical session focusing on autonomous systems and real-world deployment.",
                    "credit_hours": 3
                }
            ],
            "prerequisites": ["Foundational Mathematics", "Programming Proficiency"],
            "rationale": f"Generated via Autonomous Mode Fallback. Reason: {str(e)[:50]}..."
        }
        return json.dumps(fallback)
