import React, { useState, useEffect, useLayoutEffect, useRef } from 'react';

/**
 * Real-world scenario for useEffect vs useLayoutEffect.
 * Scenario: Implementing a Tooltip that must calculate its position 
 * BEFORE the browser paints to prevent a "jump" or flicker.
 */

const ComplexTooltip = ({ targetRef, text }) => {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const tooltipRef = useRef();

  /*
  useEffect(() => {
    if (targetRef.current && tooltipRef.current) {
      const rect = targetRef.current.getBoundingClientRect();
      setPosition({ top: rect.top - 40, left: rect.left });
    }
  }, [targetRef]);
  */

  useLayoutEffect(() => {
    if (targetRef.current && tooltipRef.current) {
      const rect = targetRef.current.getBoundingClientRect();
      const newTop = Math.max(0, rect.top - tooltipRef.current.offsetHeight - 10);
      setPosition({ top: newTop, left: rect.left });
    }
  }, [targetRef]);

  return (
    <div 
      ref={tooltipRef}
      style={{
        position: 'fixed',
        top: position.top,
        left: position.left,
        backgroundColor: '#333',
        color: '#fff',
        padding: '8px',
        borderRadius: '4px',
        pointerEvents: 'none',
        zIndex: 1000,
        opacity: text ? 1 : 0,
        transition: 'opacity 0.2s'
      }}
    >
      {text}
    </div>
  );
};

export default function AppContainer() {
  const [showTooltip, setShowTooltip] = useState(false);
  const btnRef = useRef();

  return (
    <div style={{ padding: '100px', height: '2000px' }}>
      <h1>Layout Effect Benchmarking</h1>
      <p>Scroll down and hover the button to see the tooltip positioning logic.</p>
      
      <button 
        ref={btnRef}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        style={{ padding: '12px 24px', fontSize: '18px' }}
      >
        Hover over me
      </button>

      {showTooltip && <ComplexTooltip targetRef={btnRef} text="Industry Grade Tooltip Logic" />}
    </div>
  );
}
