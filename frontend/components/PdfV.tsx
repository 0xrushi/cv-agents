'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Document, Page, pdfjs } from 'react-pdf'
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`

export default function PdfV() {
  const [pdfContent, setPdfContent] = useState<string | null>(null)
  const [numPages, setNumPages] = useState<number | null>(null)
  const [pageNumber, setPageNumber] = useState(1)
  const [isConnected, setIsConnected] = useState(false)
  const [messages, setMessages] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    wsRef.current = new WebSocket('ws://localhost:8041/ws')

    wsRef.current.onopen = () => {
      console.log('WebSocket connection established')
      setIsConnected(true)
      setMessages(prev => [...prev, 'Connected to server'])
    }

    wsRef.current.onmessage = (event) => {
        if (typeof event.data === 'string') {
          try {
            const data = JSON.parse(event.data);
            if (data.type === "json") {
              setJsonContent(data.content);
              setJsonVersions((prev) => [
                ...prev,
                { timestamp: new Date().toISOString(), content: data.content },
              ]);
            } else if (data.type === "pdf") {
              console.log('Received PDF data');
              // Decode the base64 string
              const pdfData = atob(data.content);
              // Convert the decoded string to a Uint8Array
              const uint8Array = new Uint8Array(pdfData.length);
              for (let i = 0; i < pdfData.length; i++) {
                uint8Array[i] = pdfData.charCodeAt(i);
              }
              // Create a Blob from the Uint8Array
              const pdfBlob = new Blob([uint8Array], { type: 'application/pdf' });
              // Generate a URL for the Blob
              const pdfUrl = URL.createObjectURL(pdfBlob);
              setPdfContent(pdfUrl);
              console.log('PDF blob URL created:', pdfUrl);
              setMessages((prev) => [...prev, "PDF received and ready to display"]);
            }
            setMessages((prev) => [...prev, `Received: ${data.type}`]);
          } catch (error) {
            console.error("Error parsing WebSocket message:", error);
            setMessages((prev) => [...prev, `Error: ${error.message}`]);
          }
        } else {
          console.error("Received unexpected data type:", typeof event.data);
          setMessages((prev) => [...prev, `Error: Unexpected data type received`]);
        }
      };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
      setMessages(prev => [...prev, `WebSocket error: ${error}`])
      setIsConnected(false)
    }

    wsRef.current.onclose = () => {
      console.log('WebSocket connection closed')
      setIsConnected(false)
      setMessages(prev => [...prev, 'Disconnected from server'])
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const requestPDF = (path: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'request_pdf', path: path }))
      setMessages(prev => [...prev, `Sent: PDF request for ${path}`])
    } else {
      setMessages(prev => [...prev, 'Error: WebSocket not connected'])
    }
  }

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages)
    setError(null)
  }

  function onDocumentLoadError(error: Error) {
    console.error('Error loading PDF:', error)
    setError(`Failed to load PDF: ${error.message}`)
  }

  return (
    <div className="flex h-screen">
      <div className="w-1/4 bg-gray-100 p-4 overflow-auto">
        <h2 className="text-lg font-semibold mb-2">Messages</h2>
        <ScrollArea className="h-full">
          {messages.map((msg, index) => (
            <p key={index} className="mb-1">{msg}</p>
          ))}
        </ScrollArea>
      </div>
      <div className="w-3/4 p-4 flex flex-col">
        <div className="mb-4 flex items-center">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} mr-2`}></div>
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
        <div className="flex-grow overflow-auto">
          {pdfContent ? (
            <Document
              file={pdfContent}
              onLoadSuccess={onDocumentLoadSuccess}
              onLoadError={onDocumentLoadError}
              className="flex flex-col items-center"
            >
              {error ? (
                <p className="text-red-500">{error}</p>
              ) : (
                <Page pageNumber={pageNumber} width={600} />
              )}
            </Document>
          ) : (
            <p>No PDF loaded</p>
          )}
        </div>
        {numPages && !error && (
          <div className="flex justify-between items-center mt-4">
            <Button
              onClick={() => setPageNumber(prev => Math.max(prev - 1, 1))}
              disabled={pageNumber <= 1}
            >
              Previous
            </Button>
            <p>
              Page {pageNumber} of {numPages}
            </p>
            <Button
              onClick={() => setPageNumber(prev => Math.min(prev + 1, numPages || 1))}
              disabled={pageNumber >= (numPages || 1)}
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}