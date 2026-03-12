import { NextResponse } from 'next/server';

// Types
interface Metrics {
  smart_cache: {
    hit_rate: string;
    total_requests: number;
    memory_usage_mb: number;
  };
  handoff: {
    total: number;
    acceptance_rate: string;
    avg_time_sec: string;
    pending: number;
  };
  brain_routing: {
    quick: number;
    standard: number;
    complex: number;
    total: number;
  };
  memory_chain: {
    total_entries: number;
    verified: boolean;
    last_hash: string;
  };
  last_updated: string;
}

export async function GET() {
  try {
    // In production, fetch from backend API
    // For now, return mock data (replace with real API calls)
    
    const metrics: Metrics = {
      smart_cache: {
        hit_rate: '95.23%',
        total_requests: 1247,
        memory_usage_mb: 2.34,
      },
      handoff: {
        total: 45,
        acceptance_rate: '100%',
        avg_time_sec: '12.5',
        pending: 3,
      },
      brain_routing: {
        quick: 850,
        standard: 320,
        complex: 77,
        total: 1247,
      },
      memory_chain: {
        total_entries: 1247,
        verified: true,
        last_hash: '2c72a8cfbb82256c...',
      },
      last_updated: new Date().toISOString(),
    };

    return NextResponse.json(metrics);
  } catch (error) {
    console.error('Failed to fetch metrics:', error);
    return NextResponse.json(
      { error: 'Failed to fetch metrics' },
      { status: 500 }
    );
  }
}
