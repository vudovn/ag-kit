import { NextResponse } from 'next/server';

// GET - Get memory chain entries
export async function GET() {
  try {
    // Mock memory chain data
    const entries = [
      {
        id: '1',
        interaction_id: 'int_001',
        contact_id: 'contact_001',
        timestamp: new Date().toISOString(),
        current_hash: '2c72a8cfbb82256c8f9a3b4e5d6c7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f',
        previous_hash: '1b61a7beaa71145b7e8a2a3d4c5b6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f',
        verified: true,
      },
      {
        id: '2',
        interaction_id: 'int_002',
        contact_id: 'contact_002',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        current_hash: '3d83b9dgcc93367d9g0b4c5f6e7d8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4g5h',
        previous_hash: '2c72a8cfbb82256c8f9a3b4e5d6c7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f',
        verified: true,
      },
    ];

    return NextResponse.json({ 
      entries,
      verified: true,
      total: entries.length,
    });
  } catch (error) {
    console.error('Failed to fetch memory chain:', error);
    return NextResponse.json(
      { error: 'Failed to fetch memory chain' },
      { status: 500 }
    );
  }
}
