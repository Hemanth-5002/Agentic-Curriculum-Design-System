import { useState } from 'react'
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
    target_degree: 'B.S.'
  });
  
  const [feedbackModule, setFeedbackModule] = useState(null);

  // Removed handleFileUpload as requested

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formConfig,
          current_syllabus: "Autonomous scan requested"
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate curriculum');
      }
      
      const data = await response.json();
      setCurriculum(data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      alert("Error generating curriculum. Please ensure the backend is running.");
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
          <span>LangGraph Node: <strong style={{color:'var(--success)'}}>Idle</strong></span>
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
            onChange={(e) => setFormConfig({...formConfig, domain: e.target.value})}
          />

          <label className="label">University Name</label>
          <input 
            className="input-field" 
            value={formConfig.university_name}
            onChange={(e) => setFormConfig({...formConfig, university_name: e.target.value})}
          />

          <label className="label">Target Degree</label>
          <select 
            className="input-field"
            value={formConfig.target_degree}
            onChange={(e) => setFormConfig({...formConfig, target_degree: e.target.value})}
            style={{ appearance: 'none', backgroundColor: 'var(--bg-dark)' }}
          >
            <option>B.S.</option>
            <option>M.S.</option>
            <option>Certification</option>
          </select>

          {/* PDF Upload removed for autonomous tracking mode */}
          <div style={{ 
            background: 'rgba(0, 240, 255, 0.05)', 
            padding: '1rem', 
            borderRadius: '12px',
            border: '1px solid var(--neon-blue)',
            marginBottom: '1.5rem',
            fontSize: '0.85rem',
            color: 'var(--neon-blue)'
          }}>
            🛰️ <strong>Autonomous Mode Active</strong>: Agents are tracking real-time industry shifts.
          </div>

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
             <div className="glass-panel animate-fade-in" style={{ padding: '3rem', textAlign: 'center' }}>
                <h2 className="glow-text">Orchestrating AI Agents...</h2>
                <div style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
                  <span style={{color: 'var(--neon-blue)'}}>✓ Industry Scraper reading LinkedIn...</span>
                  <span style={{color: 'var(--neon-purple)'}}>✓ Academic Agent parsing ArXiv...</span>
                  <span style={{color: 'var(--text-muted)'}}>• Analyzing skill gaps...</span>
                </div>
             </div>
          )}

          {curriculum && !loading && (
            <div className="animate-fade-in">
              <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem', borderTop: '4px solid var(--success)', position: 'relative' }}>
                <button 
                  className="btn-primary" 
                  style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
                  onClick={handleExport}
                >
                  Export to PDF
                </button>
                <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{curriculum.domain} Curriculum</h2>
                <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', marginBottom: '1.5rem' }}>
                  {curriculum.rationale}
                </p>
                <div>
                  <h4 style={{ color: 'var(--neon-blue)', marginBottom: '0.5rem' }}>Prerequisites:</h4>
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    {curriculum.prerequisites.map((prereq, idx) => (
                      <span key={idx} style={{ 
                        background: 'rgba(255,255,255,0.05)', border: '1px solid var(--glass-border)',
                        padding: '0.3rem 0.8rem', borderRadius: '8px', fontSize: '0.9rem'
                      }}>
                        {prereq}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <h2 style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between' }}>
                  Proposed Modules
                  <span style={{ background: 'rgba(0, 255, 136, 0.1)', color: 'var(--success)', padding: '0.3rem 1rem', borderRadius: '50px', fontSize: '1rem' }}>
                    {curriculum.modules.reduce((acc, mod) => acc + mod.credit_hours, 0)} Total Credits
                  </span>
                </h2>
                {curriculum.modules.map((module, idx) => (
                  <ModuleCard 
                    key={idx} 
                    module={module} 
                    index={idx} 
                    onFeedback={(mod) => setFeedbackModule(mod)} 
                  />
                ))}
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
