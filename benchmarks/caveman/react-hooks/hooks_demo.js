import React, { useState, useEffect, useCallback, useMemo, createContext, useContext } from 'react';

/**
 * Industry-Grade Dashboard Showcase for React Hooks.
 * Demonstrates: useState, useEffect, useCallback, useMemo, and Context API.
 */

const DashboardContext = createContext();

const AnalyticsModule = ({ data }) => {
  // useMemo for heavy calculations
  const processedData = useMemo(() => {
    console.log('Performing expensive calculations on data...');
    return data.map(item => ({
      ...item,
      normalizedValue: item.value * Math.random(),
      timestamp: new Date().toISOString()
    })).filter(item => item.value > 10);
  }, [data]);

  return (
    <div className="analytics-module">
      <h3>Live Metrics</h3>
      <ul>
        {processedData.map(item => (
          <li key={item.id}>{item.name}: {item.normalizedValue.toFixed(2)}</li>
        ))}
      </ul>
    </div>
  );
};

export default function ProfessionalDashboard() {
  const [session, setSession] = useState({ user: 'Admin', active: true });
  const [metrics, setMetrics] = useState([
    { id: 1, name: 'Throughput', value: 45 },
    { id: 2, name: 'Latency', value: 12 },
    { id: 3, name: 'Error Rate', value: 2 },
  ]);

  // useCallback for stable event handlers
  const handleToggleSession = useCallback(() => {
    setSession(prev => ({ ...prev, active: !prev.active }));
  }, []);

  // useEffect for lifecycle/API synchronization
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => prev.map(m => ({
        ...m,
        value: Math.max(0, m.value + (Math.random() - 0.5) * 10)
      })));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardContext.Provider value={{ session, handleToggleSession }}>
      <main className="dashboard-container">
        <header>
          <h1>Antigravity Enterprise Dashboard</h1>
          <p>User: {session.user} | Status: {session.active ? '🟢 Active' : '🔴 Idle'}</p>
          <button onClick={handleToggleSession}>Toggle Status</button>
        </header>

        <section className="dashboard-grid">
          <AnalyticsModule data={metrics} />
          
          <div className="system-status">
            <h3>Infrastructure Health</h3>
            <p>Uptime: 99.98%</p>
            <p>Region: us-east-1</p>
          </div>
        </section>
      </main>
    </DashboardContext.Provider>
  );
}
