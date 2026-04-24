# Agentic Curriculum Design System

A modern, multi-agent system for universities to design state-of-the-art curricula by analyzing industry trends and academic research.

## Features
- **Industry Trend Scraper**: Connects to job markets and tech blogs to identify in-demand skills.
- **Academic Research Agent**: Fetches the latest papers from ArXiv to ensure cutting-edge theoretical foundations.
- **RAG Pipeline**: Uses LlamaIndex and GPT-4 to synthesize curriculum drafts based on real-world data.
- **LangGraph Orchestration**: Robust multi-agent workflow management.
- **Premium UI**: Futuristic glassmorphism design.

## Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API Key (set in `backend/.env`)

## Getting Started

### Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`.
3. Activate the environment: `.\venv\Scripts\Activate` (Windows) or `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install -r requirements.txt`.
5. Ensure your `.env` file has the `OPENAI_API_KEY`.
6. Run the server: `python -m uvicorn api.main:app --reload`.

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run dev`.

The application will be available at `http://localhost:5173`.
The backend API will run at `http://localhost:8000`.
