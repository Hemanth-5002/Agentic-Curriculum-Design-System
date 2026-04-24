import React, { useState } from 'react';

const FeedbackModal = ({ module, onClose, onSubmit }) => {
  const [comment, setComment] = useState('');

  if (!module) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.7)',
      backdropFilter: 'blur(10px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="glass-panel animate-fade-in" style={{ padding: '2.5rem', width: '100%', maxWidth: '500px' }}>
        <h2 style={{ color: 'var(--neon-pink)', marginBottom: '0.5rem' }}>Provide Feedback</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
          For module: <strong>{module.title}</strong>
        </p>

        <label className="label">Your Comments / Proposed Changes</label>
        <textarea 
          className="input-field"
          style={{ minHeight: '120px', resize: 'vertical' }}
          placeholder="e.g. Please include more focus on Vector Databases..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
          <button 
            style={{
              background: 'transparent',
              border: '1px solid var(--text-muted)',
              color: 'var(--text-main)',
              padding: '0.8rem 1.5rem',
              borderRadius: '12px',
              cursor: 'pointer'
            }}
            onClick={onClose}
          >
            Cancel
          </button>
          <button 
            className="btn-primary"
            style={{ background: 'linear-gradient(45deg, var(--neon-pink), var(--neon-purple))' }}
            onClick={() => onSubmit({ module_title: module.title, comment, rating: 5 })}
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  );
};

export default FeedbackModal;
