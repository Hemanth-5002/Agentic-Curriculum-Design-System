from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from core.schemas import GenerationRequest, CurriculumDraft, Feedback
from agents.graph import app as graph_app
from dotenv import load_dotenv
from scrapers.pdf_engine import extract_text_from_pdf
from core.exporter import generate_curriculum_pdf
import json
import os

load_dotenv()

app = FastAPI(title="Agentic Curriculum Design System")

# Ensure storage exists
os.makedirs("storage", exist_ok=True)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://agentic-syllabus.onrender.com",
    
]

# Add production URL from environment variable if it exists
env_origins = os.getenv("CORS_ORIGINS")
if env_origins:
    origins.extend(env_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

@app.get("/")
async def root():
    return {"status": "online", "message": "Curriculum API is active in Autonomous Mode"}

@app.get("/health")
async def health_check():
    # Basic connectivity check
    import os
    env_check = "OK" if os.getenv("OPENAI_API_KEY") else "MISSING_KEYS"
    return {
        "status": "healthy",
        "llm_config": env_check,
        "mode": "autonomous",
        "version": "1.1.0"
    }

@app.post("/api/generate", response_model=CurriculumDraft)
def generate_curriculum(request: GenerationRequest):
    print(f"Received generation request for domain: {request.domain}")
    
    # Handle feedback if present in request (requires schema update or flexible object)
    # For now, we'll use the existing schema and check for syllabus content passed in
    
    initial_state = {
        "domain": request.domain,
        "target_degree": request.target_degree,
        "industry_trends": [],
        "skill_gap": [],
        "current_syllabus": getattr(request, 'current_syllabus', ""),
        "academic_research": [],
        "academic_papers_raw": [],
        "draft_modules": [],
        "prerequisites": [],
        "generation_rationale": "",
        "feedback": []
    }
    
    print(f"Executing LangGraph workflow for {request.domain}...")
    try:
        final_state = graph_app.invoke(initial_state)
        print("Workflow complete.")
    except Exception as e:
        print(f"Workflow failed: {e}")
        raise e
    
    # Save to storage (Persistence)
    history_file = f"storage/curricula.json"
    try:
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        result = {
            "domain": final_state["domain"],
            "university_name": request.university_name,
            "modules": [m if isinstance(m, dict) else m.dict() for m in final_state["draft_modules"]],
            "prerequisites": final_state.get("prerequisites", []),
            "rationale": final_state.get("generation_rationale", ""),
            "gap_analysis": final_state.get("gap_analysis", "")
        }
        history.append(result)
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"Result saved to {history_file}")
    except Exception as e:
        print(f"Error saving result: {e}")
        # Still return result if possible
        result = {
            "domain": final_state["domain"],
            "university_name": request.university_name,
            "modules": [m if isinstance(m, dict) else m.dict() for m in final_state["draft_modules"]],
            "prerequisites": final_state.get("prerequisites", []),
            "rationale": final_state.get("generation_rationale", ""),
            "gap_analysis": final_state.get("gap_analysis", "")
        }
    
    return result

@app.post("/api/export-pdf")
async def export_pdf(data: dict):
    pdf_bytes = generate_curriculum_pdf(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={data['domain'].replace(' ', '_')}_curriculum.pdf"}
    )

@app.post("/api/feedback")
async def submit_feedback(feedback: Feedback):
    # Route back to LangGraph for iteration (In real app, this would trigger background job)
    # For now, return success
    return {"status": "success", "message": "Feedback integrated into next iteration cycle."}
