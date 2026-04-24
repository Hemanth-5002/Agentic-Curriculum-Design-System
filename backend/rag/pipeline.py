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
        if "insufficient_quota" in str(e).lower() or "quota" in str(e).lower():
            print("RAG: Quota exceeded. Returning specialized fallback curriculum.")
            # High-quality fallback
            import json
            fallback = {
                "domain": domain,
                "modules": [
                    {
                        "title": f"Foundation of Advanced {domain}",
                        "description": "Comprehensive introduction reflecting modern industry standards and recent research trends.",
                        "credit_hours": 3
                    },
                    {
                        "title": "Practical Implementation & Case Studies",
                        "description": "Hands-on lab sessions focusing on real-world applications and problem-solving.",
                        "credit_hours": 4
                    },
                    {
                        "title": "Emerging Technologies Nexus",
                        "description": "Deep dive into state-of-the-art frameworks and future-looking academic concepts.",
                        "credit_hours": 4
                    }
                ],
                "prerequisites": ["Domain Basics", "Quantitative Methods", "Advanced Programming"],
                "rationale": "Quota limit reached. This curriculum provides a high-fidelity template based on general best practices for this domain."
            }
            return json.dumps(fallback)
        raise e
