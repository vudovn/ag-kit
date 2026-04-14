/**
 * Advanced Data Processing Logic.
 */

async function fetchInternalMetrics() {
  return [
    { type: 'cpu', load: 85, critical: true },
    { type: 'mem', load: 42, critical: false },
    { type: 'disk', load: 91, critical: true },
  ];
}

async function processSystemHealth(threshold) {
  const rawData = await fetchInternalMetrics();
  
  // Logic to aggregate critical alerts
  const alerts = rawData.reduce((acc, curr) => {
    if (curr.load > threshold && curr.critical) {
      acc.push(`Critical Alert: ${curr.type.toUpperCase()} at ${curr.load}%`);
    }
    return acc;
  }, []);

  if (alerts.length === 0) {
    return { status: 'OK', message: 'All systems within parameters.' };
  }

  if (alerts.length > 5) {
    console.warn('System overload detected! Multiple critical vectors.');
  } else {
    return {
      status: 'WARNING',
      alerts: alerts,
      count: alerts.length
    };
  }
}

// Demo Execution
(async () => {
  console.log('Initializing health check...');
  try {
    const report = await processSystemHealth(80);
    if (!report) {
      console.error('ERROR: Health check returned undefined. Fatal logic error in processSystemHealth.');
    } else {
      console.log('Report received:', report);
    }
  } catch (err) {
    console.error('System failure:', err.message);
  }
})();
