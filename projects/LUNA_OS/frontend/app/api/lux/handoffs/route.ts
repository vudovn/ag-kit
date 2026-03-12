import { NextResponse } from 'next/server';

interface Handoff {
  id: string;
  conversation_id: string;
  contact_id: string;
  contact_name?: string;
  reason: string;
  priority: number;
  status: 'pending' | 'accepted' | 'resolved';
  context_summary: string;
  created_at: string;
  accepted_at?: string;
  assigned_to?: string;
}

// GET - List all handoffs
export async function GET() {
  try {
    // In production, fetch from backend API
    // For now, return mock data
    const handoffs: Handoff[] = [
      {
        id: '1',
        conversation_id: 'conv_001',
        contact_id: 'contact_001',
        contact_name: 'João Silva',
        reason: 'customer_requested',
        priority: 7,
        status: 'pending',
        context_summary: 'Cliente quer falar com atendente humano',
        created_at: new Date().toISOString(),
      },
      {
        id: '2',
        conversation_id: 'conv_002',
        contact_id: 'contact_002',
        contact_name: 'Maria Santos',
        reason: 'high_risk',
        priority: 9,
        status: 'accepted',
        context_summary: 'Reclamação sobre serviço',
        created_at: new Date(Date.now() - 3600000).toISOString(),
        accepted_at: new Date(Date.now() - 1800000).toISOString(),
        assigned_to: 'operator_001',
      },
    ];

    return NextResponse.json({ handoffs });
  } catch (error) {
    console.error('Failed to fetch handoffs:', error);
    return NextResponse.json(
      { error: 'Failed to fetch handoffs' },
      { status: 500 }
    );
  }
}
