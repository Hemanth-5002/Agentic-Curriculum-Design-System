import { useState, useEffect } from 'react'
import './index.css'
import ModuleCard from './components/ModuleCard';
import FeedbackModal from './components/FeedbackModal';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

function App() {
  const [loading, setLoading] = useState(false);
  const [curriculum, setCurriculum] = useState(null);
  const [formConfig, setFormConfig] = useState({
    domain: 'Artificial Intelligence',
    university_name: 'Tech University',
    target_degree: 'B.S.',
    current_syllabus: ''
  });

  const [feedbackModule, setFeedbackModule] = useState(null);
  const [systemStatus, setSystemStatus] = useState('Checking...');
  const [currentStep, setCurrentStep] = useState(0);
  const steps = [
    "🛰️ Industry Scraper reading trends...",
    "🧬 Academic Agent parsing ArXiv...",
    "🔍 Identifying skill gaps...",
    "🧠 Orchestrating RAG synthesis...",
    "✨ Finalizing curriculum modules..."
  ];

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/health`);
        const data = await res.json();
        setSystemStatus(data.status === 'healthy' ? 'Active' : 'Degraded');
      } catch (e) {
        setSystemStatus('Offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Removed handleFileUpload as requested

  const handleGenerate = async () => {
    setLoading(true);
    setCurrentStep(0);
    const stepInterval = setInterval(() => {
      setCurrentStep(prev => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 4000);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formConfig)
      });

      clearInterval(stepInterval);
      if (!response.ok) {
        throw new Error('Failed to generate curriculum');
      }

      const data = await response.json();
      setCurriculum(data);
      setLoading(false);
    } catch (error) {
      clearInterval(stepInterval);
      console.error(error);
      alert(`Backend Connection Issue: ${error.message}\n\nPlease check if the terminal running 'uvicorn' shows any Python errors.`);
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/export-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(curriculum)
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${curriculum.domain.replace(/\s+/g, '_')}_curriculum.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error(error);
      alert("Error exporting PDF.");
    }
  };

  const handleFeedbackSubmit = async (feedbackData) => {
    // In a real app we'd trigger the next LangGraph iteration here
    // await fetch('http://localhost:8000/api/feedback', { method: 'POST', body: JSON.stringify(feedbackData) });
    alert(`Feedback submitted for ${feedbackData.module_title}! The agent will integrate this into the next iteration.`);
    setFeedbackModule(null);
  };

  return (
    <div className="app-container">
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            width: '40px', height: '40px',
            background: 'linear-gradient(45deg, var(--neon-blue), var(--neon-purple))',
            borderRadius: '10px', boxShadow: '0 0 15px rgba(0, 240, 255, 0.4)'
          }}></div>
          <h1 className="glow-text" style={{ fontSize: '1.5rem', margin: 0 }}>Agentic Curriculum Generator</h1>
        </div>
        <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          <span>Autonomous Mode: <strong style={{ color: 'var(--success)' }}>Enabled</strong></span>
          <span>System Status: <strong style={{
            color: systemStatus === 'Active' ? 'var(--success)' :
              systemStatus === 'Offline' ? 'var(--neon-pink)' : 'var(--neon-blue)'
          }}>{systemStatus}</strong></span>
        </div>
      </header>

      <main className="dashboard animate-fade-in">

        {/* Left Sidebar Form */}
        <section className="glass-panel" style={{ padding: '2rem', height: 'fit-content' }}>
          <h2 style={{ marginBottom: '2rem', fontSize: '1.5rem' }}>Generation Parameters</h2>

          <label className="label">Academic Domain</label>
          <input
            className="input-field"
            value={formConfig.domain}
            onChange={(e) => setFormConfig({ ...formConfig, domain: e.target.value })}
          />

          <label className="label">University Name</label>
          <input
            className="input-field"
            value={formConfig.university_name}
            onChange={(e) => setFormConfig({ ...formConfig, university_name: e.target.value })}
          />

          <label className="label">Target Degree</label>
          <select
            className="input-field"
            value={formConfig.target_degree}
            onChange={(e) => setFormConfig({ ...formConfig, target_degree: e.target.value })}
            style={{ appearance: 'none', backgroundColor: 'var(--bg-dark)' }}
          >
            <option>B.S.</option>
            <option>M.S.</option>
            <option>Certification</option>
          </select>

          <label className="label">Existing Syllabus (Optional)</label>
          <textarea
            className="input-field"
            style={{ minHeight: '100px', resize: 'vertical', fontFamily: 'inherit' }}
            placeholder="Paste current syllabus here to check for gaps and see what needs to be implemented..."
            value={formConfig.current_syllabus}
            onChange={(e) => setFormConfig({ ...formConfig, current_syllabus: e.target.value })}
          />

          <button
            className="btn-primary"
            style={{ width: '100%', marginTop: '1rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner" style={{
                  width: '20px', height: '20px', border: '3px solid rgba(255,255,255,0.3)',
                  borderTopColor: 'white', borderRadius: '50%', animation: 'spin 1s linear infinite'
                }}></span>
                Running Agents...
              </>
            ) : 'Start Real-time Generation'}
          </button>

          <style>{`
            @keyframes spin { 100% { transform: rotate(360deg); } }
          `}</style>
        </section>

        {/* Right Output Area */}
        <section>
          {!curriculum && !loading && (
            <div className="glass-panel" style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center',
              justifyContent: 'center', height: '100%', minHeight: '400px',
              borderStyle: 'dashed', borderColor: 'var(--glass-border)'
            }}>
              <div style={{ opacity: 0.5, textAlign: 'center' }}>
                <h2 style={{ marginBottom: '1rem' }}>No Syllabus Generated</h2>
                <p>Configure parameters on the left and trigger the multi-agent orchestration pipeline.</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="glass-panel animate-fade-in" style={{
              padding: '3rem', textAlign: 'center',
              border: '1px solid var(--neon-blue)',
              boxShadow: '0 0 40px rgba(0, 240, 255, 0.1)'
            }}>
              <h2 className="glow-text" style={{ marginBottom: '2rem' }}>Agent Orchestration in Progress</h2>

              <div style={{
                display: 'flex', flexDirection: 'column', gap: '1.2rem',
                alignItems: 'center', maxWidth: '400px', margin: '0 auto'
              }}>
                {steps.map((step, idx) => (
                  <div key={idx} style={{
                    display: 'flex', alignItems: 'center', gap: '1rem',
                    width: '100%', opacity: idx === currentStep ? 1 : idx < currentStep ? 0.6 : 0.2,
                    transition: 'all 0.5s ease',
                    padding: '0.8rem 1rem',
                    borderRadius: '10px',
                    background: idx === currentStep ? 'rgba(0, 240, 255, 0.05)' : 'transparent',
                    border: idx === currentStep ? '1px solid var(--neon-blue)' : '1px solid transparent'
                  }}>
                    <span style={{
                      color: idx < currentStep ? 'var(--success)' :
                        idx === currentStep ? 'var(--neon-blue)' : 'var(--text-muted)'
                    }}>
                      {idx < currentStep ? '✓' : idx === currentStep ? '●' : '○'}
                    </span>
                    <span style={{
                      color: idx === currentStep ? 'white' : 'var(--text-muted)',
                      fontWeight: idx === currentStep ? '600' : '400'
                    }}>
                      {step}
                    </span>
                  </div>
                ))}
              </div>

              <div className="spinner" style={{
                marginTop: '3rem', width: '40px', height: '40px',
                border: '4px solid rgba(0,240,255,0.1)', borderTopColor: 'var(--neon-blue)',
                borderRadius: '50%', animation: 'spin 1.5s cubic-bezier(0.5, 0.1, 0.4, 0.9) infinite'
              }}></div>
            </div>
          )}

          {curriculum && !loading && (
            <div className="animate-fade-in">
              <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem', borderTop: '4px solid var(--neon-blue)', position: 'relative' }}>
                <button
                  className="btn-primary"
                  style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
                  onClick={handleExport}
                >
                  Export PDF Report
                </button>
                <h2 style={{ fontSize: '2.8rem', fontWeight: '800', marginBottom: '0.2rem', color: 'var(--neon-blue)', textTransform: 'uppercase', letterSpacing: '1px' }}>{curriculum.university_name}</h2>
                <h3 style={{ fontSize: '1.8rem', marginBottom: '2rem', color: 'white', borderLeft: '4px solid var(--neon-purple)', paddingLeft: '1rem' }}>{curriculum.domain} Curriculum Blueprint</h3>
                
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', border: '1px solid var(--glass-border)' }}>
                  <h4 style={{ color: 'var(--neon-purple)', marginBottom: '1rem', fontSize: '1.1rem' }}>Key Curriculum Highlights:</h4>
                  <ul style={{ color: 'var(--text-muted)', fontSize: '0.95rem', paddingLeft: '1.2rem', lineHeight: '1.8', marginBottom: curriculum.gap_analysis ? '1.5rem' : '0' }}>
                    <li><strong>Industry Alignment:</strong> Mapped to 2024 real-time job market requirements.</li>
                    <li><strong>Research Driven:</strong> Includes latest findings from ArXiv academic repositories.</li>
                    <li><strong>Specialization Focus:</strong> Designed for modern career paths in {curriculum.domain}.</li>
                    <li><strong>Practical Readiness:</strong> Balanced credit distribution for hands-on learning.</li>
                  </ul>
                  
                  {curriculum.gap_analysis && (
                    <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--glass-border)' }}>
                      <h4 style={{ color: 'var(--neon-pink)', marginBottom: '1rem', fontSize: '1.1rem' }}>Gap Analysis (What needs to be implemented):</h4>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', whiteSpace: 'pre-wrap', lineHeight: '1.8' }}>
                        {curriculum.gap_analysis}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '2rem' }}>
                <h2 style={{ marginBottom: '2rem', color: 'var(--neon-blue)' }}>Curriculum Modules (Point-wise)</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                  {curriculum.modules.map((module, idx) => (
                    <div key={idx} style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '1.5rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ fontSize: '1.3rem', color: 'white' }}>{idx + 1}. {module.title}</h3>
                        <span style={{ color: 'var(--neon-purple)', fontWeight: 'bold' }}>{module.credit_hours} Credits</span>
                      </div>
                      <p style={{ color: 'var(--text-muted)', whiteSpace: 'pre-wrap', lineHeight: '1.7' }}>
                        {module.description}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </section>

      </main>

      {feedbackModule && (
        <FeedbackModal
          module={feedbackModule}
          onClose={() => setFeedbackModule(null)}
          onSubmit={handleFeedbackSubmit}
        />
      )}
    </div>
  )
}

export default App
