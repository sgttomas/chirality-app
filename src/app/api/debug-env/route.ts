import { NextResponse } from 'next/server';

export async function GET() {
  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.OPENAI_MODEL;
  
  return NextResponse.json({
    hasApiKey: !!apiKey,
    apiKeyEnding: apiKey ? apiKey.slice(-6) : 'none',
    model: model || 'none',
    nodeEnv: process.env.NODE_ENV
  });
}