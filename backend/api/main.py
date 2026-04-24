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

@app.get("/")
async def root():
    return {"status": "online", "message": "Curriculum API is active"}

@app.post("/api/upload-syllabus")
async def upload_syllabus(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    return {"text": text, "filename": file.filename}

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
    
    print("Executing LangGraph workflow...")
    final_state = graph_app.invoke(initial_state)
    print("Workflow complete.")
    
    # Save to storage (Persistence)
    history_file = f"storage/curricula.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    
    result = {
        "domain": final_state["domain"],
        "modules": [m if isinstance(m, dict) else m.dict() for m in final_state["draft_modules"]],
        "prerequisites": final_state["prerequisites"],
        "rationale": final_state["generation_rationale"]
    }
    history.append(result)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
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
