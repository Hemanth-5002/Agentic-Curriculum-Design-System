import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print("Testing /health...")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_generate():
    print("\nTesting /api/generate (Autonomous Mode)...")
    print("This involves AI research and synthesis. Please wait...")
    payload = {
        "domain": "Software Engineering",
        "university_name": "Antigravity University",
        "target_degree": "B.S."
    }
    try:
        # Increased timeout for LangGraph + ArXiv + OpenAI
        start = time.time()
        r = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=120)
        end = time.time()
        print(f"Status: {r.status_code} (took {end-start:.1f}s)")
        data = r.json()
        if r.status_code == 200:
            print(f"✅ Domain: {data.get('domain')}")
            print(f"✅ Rationale: {data.get('rationale')[:100]}...")
            print(f"✅ Modules Count: {len(data.get('modules', []))}")
        return r.status_code == 200 and len(data.get('modules', [])) > 0
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

def test_export():
    print("\nTesting /api/export-pdf...")
    payload = {
        "domain": "AI Test",
        "modules": [{"title": "Test Module", "description": "Desc", "credit_hours": 3}]
    }
    try:
        r = requests.post(f"{BASE_URL}/api/export-pdf", json=payload, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        return r.status_code == 200 and "application/pdf" in r.headers.get('Content-Type', '')
    except Exception as e:
        print(f"Export failed: {e}")
        return False

if __name__ == "__main__":
    h = test_health()
    if h:
        e = test_export() # Test export first as it's faster
        g = test_generate() # Test generate last as it's slow
        
        print("\n" + "="*20)
        print("FINAL CHECK SUMMARY")
        print(f"Health: {'PASS' if h else 'FAIL'}")
        print(f"Export: {'PASS' if e else 'FAIL'}")
        print(f"Generation: {'PASS' if g else 'FAIL'}")
        print("="*20)
    else:
        print("Backend seems offline. Ensure uvicorn is running.")
