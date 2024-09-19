import { NextResponse } from 'next/server'

export async function GET() {
  // In a real application, you would fetch or generate a PDF here
  // For now, we'll return a simple text as a placeholder
  return new NextResponse('Sample PDF content', {
    headers: {
      'Content-Type': 'application/pdf',
    },
  })
}