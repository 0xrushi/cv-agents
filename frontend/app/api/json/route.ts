import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const backendUrl = process.env.WEBSOCKET_SERVER_BACKEND_URL || 'http://127.0.0.1:8041';
    const response = await fetch(`${backendUrl}/getjson`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const jsonData = await response.json()

    return NextResponse.json(jsonData)
  } catch (error) {
    console.error('Error fetching JSON data:', error)
    return NextResponse.json({ error: 'Failed to retrieve JSON data' }, { status: 500 })
  }
}