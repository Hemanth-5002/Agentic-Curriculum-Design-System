import React from 'react';
import '../index.css';

const ModuleCard = ({ module, index, onFeedback }) => {
  return (
    <div 
      className="glass-panel animate-fade-in" 
      style={{ animationDelay: `${index * 0.1}s`, padding: '1.5rem', marginBottom: '1.5rem', transition: 'all 0.3s ease' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.4rem', color: 'var(--neon-blue)' }}>{module.title}</h3>
        <span style={{ 
          background: 'rgba(157, 0, 255, 0.2)', 
          color: 'var(--neon-purple)', 
          padding: '0.3rem 0.8rem', 
          borderRadius: '50px',
          fontSize: '0.85rem',
          fontWeight: '600'
        }}>
          {module.credit_hours} Credits
        </span>
      </div>
      
      <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '1.5rem' }}>
        {module.description}
      </p>

      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button 
          style={{
            background: 'transparent',
            border: '1px solid var(--neon-pink)',
            color: 'var(--neon-pink)',
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onClick={() => onFeedback(module)}
          onMouseOver={(e) => {
            e.currentTarget.style.background = 'rgba(255, 0, 85, 0.1)';
            e.currentTarget.style.boxShadow = '0 0 10px rgba(255, 0, 85, 0.3)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          Add Feedback
        </button>
      </div>
    </div>
  );
};

export default ModuleCard;
