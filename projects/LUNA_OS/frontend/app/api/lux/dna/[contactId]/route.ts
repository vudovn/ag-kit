import { NextResponse } from 'next/server';

// GET - Get DNA for specific contact
export async function GET(
  request: Request,
  { params }: { params: { contactId: string } }
) {
  try {
    // Mock DNA data
    const dna = {
      contact_id: params.contactId,
      tone: 'professional',
      vocabulary: 'standard',
      emoji_usage: 'moderate',
      response_length: 'medium',
      formality_level: 6,
      communication_style: 'balanced',
      decision_speed: 'medium',
    };

    return NextResponse.json({ dna });
  } catch (error) {
    console.error('Failed to fetch DNA:', error);
    return NextResponse.json(
      { error: 'Failed to fetch DNA' },
      { status: 500 }
    );
  }
}

// POST - Save DNA for contact
export async function POST(
  request: Request,
  { params }: { params: { contactId: string } }
) {
  try {
    const body = await request.json();
    const { dna } = body;

    // In production, save to database
    console.log('Saving DNA for contact:', params.contactId, dna);

    return NextResponse.json({ success: true, dna });
  } catch (error) {
    console.error('Failed to save DNA:', error);
    return NextResponse.json(
      { error: 'Failed to save DNA' },
      { status: 500 }
    );
  }
}
