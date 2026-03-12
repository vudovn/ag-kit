import { NextResponse } from 'next/server';

interface BehavioralDNA {
  contact_id: string;
  contact_name?: string;
  tone: string;
  vocabulary: string;
  emoji_usage: string;
  response_length: string;
  formality_level: number;
  communication_style: string;
  decision_speed: string;
}

// GET - List all contacts with DNA
export async function GET() {
  try {
    // Mock data for now
    const contacts = [
      { id: 'contact_001', name: 'João Silva', email: 'joao@example.com', phone: '+5511999999999' },
      { id: 'contact_002', name: 'Maria Santos', email: 'maria@example.com', phone: '+5511999999998' },
      { id: 'contact_003', name: 'Pedro Oliveira', email: 'pedro@example.com', phone: '+5511999999997' },
    ];

    return NextResponse.json({ contacts });
  } catch (error) {
    console.error('Failed to fetch contacts:', error);
    return NextResponse.json(
      { error: 'Failed to fetch contacts' },
      { status: 500 }
    );
  }
}
