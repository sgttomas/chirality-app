import { NextRequest, NextResponse } from 'next/server';
import { readState, writeState } from '@/chirality-core/state/store';

export const runtime = 'nodejs';

export async function GET(request: NextRequest) {
  try {
    const state = readState();
    return NextResponse.json(state);
  } catch (error) {
    console.error('State GET error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const updated = writeState(body);
    return NextResponse.json(updated);
  } catch (error) {
    console.error('State POST error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    // Reset state to default empty values
    const cleared = writeState({
      problem: { title: '', statement: '', initialVector: [] },
      finals: {}
    });
    return NextResponse.json(cleared);
  } catch (error) {
    console.error('State DELETE error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}