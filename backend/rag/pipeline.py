import os
from typing import List
from llama_index.core import Document, VectorStoreIndex, StorageContext
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def call_gemini_api(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API Error: {response.text}")

def generate_curriculum_rag(domain: str, industry_data: List[str], academic_papers: List[dict], current_syllabus: str) -> str:
    """
    Use custom API call to synthesize a curriculum draft.
    """
    
    # Combine all research data into documents
    documents = []
    
    try:
        # Build the full context for the prompt
        industry_text = "Industry Trends: " + ", ".join(industry_data)
        context = f"Industry Data: {industry_text}\n\nAcademic Papers:\n"
        for paper in academic_papers:
            context += f"- {paper['title']}: {paper['summary']}\n"
        
        context += f"\nExisting Syllabus: {current_syllabus}"

        prompt = f"""
        Act as a Senior Educational Consultant. Based on the provided data for {domain}, 
        propose a modern curriculum. 
        
        DATA CONTEXT:
        {context}
        
        CRITICAL INSTRUCTIONS FOR CLARITY:
        1. Use SIMPLE, PLAIN LANGUAGE. Avoid unnecessary academic jargon.
        2. In "description", use clear bullet points for key topics.
        3. Make the "rationale" read like a friendly executive summary that explains the "Why" in 3 simple sentences.
        4. Ensure the titles are catchy and professional.
        5. Provide a "gap_analysis" section. If an "Existing Syllabus" is provided, explicitly state what is missing compared to modern industry trends and what HAS TO BE IMPLEMENTED. If none is provided, just say "Full modern implementation required."
        6. YOU MUST GENERATE EXACTLY 5 DIFFERENT MODULES. DO NOT GENERATE LESS THAN 5 MODULES. THIS IS A HARD REQUIREMENT.
        
        Return the response in JSON format matching this schema:
        {{
            "domain": "{domain}",
            "modules": [
                {{
                    "title": "Module 1 Title",
                    "description": "A short 1-sentence intro followed by 3 bullet points of simple learning outcomes.",
                    "credit_hours": 3
                }},
                {{
                    "title": "Module 2 Title",
                    "description": "Description for the next module...",
                    "credit_hours": 4
                }}
                // ... YOU MUST create exactly 5 modules total. Do not deviate from this.
            ],
            "prerequisites": ["List of simple skills needed before starting"],
            "rationale": "A 3-sentence simple explanation: 1. Current state, 2. The Gap found, 3. How this curriculum fixes it.",
            "gap_analysis": "Point-wise explanation of what needs to be implemented and what was missing in the old syllabus."
        }}
        """
        
        print("RAG: Calling Gemini API directly...")
        response = call_gemini_api(prompt)
        print("RAG: Gemini response received.")
        return str(response)
    except Exception as e:
        print(f"Generation Error: {e}")
        # Return fallback with the ACTUAL error so we can debug
        import json
        fallback = {
            "domain": domain,
            "modules": [
                {
                    "title": f"Core Principles of {domain}",
                    "description": "Foundational module covering high-demand industry skills and modern research applications.",
                    "credit_hours": 4
                }
            ],
            "prerequisites": ["Foundational Mathematics"],
            "rationale": f"System Error: {str(e)}"
        }
        return json.dumps(fallback)
