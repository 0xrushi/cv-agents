"use client"

import { useState, useEffect, useRef } from 'react'
import { Terminal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { toast } from "@/components/ui/use-toast"
import { Document, Page } from 'react-pdf'
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

import { pdfjs } from "react-pdf";

const PDFViewer = ({ content }) => {
  const [numPages, setNumPages] = useState(null)
  const [pageNumber, setPageNumber] = useState(1)
  const [error, setError] = useState(null)

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages)
    setError(null)
  }

  function onDocumentLoadError(error) {
    console.error('Error loading PDF:', error)
    setError('Failed to load PDF. Please try again.')
  }

  return (
    <div className="h-full overflow-auto p-4">
      {content ? (
        <Document
          file={content}
          onLoadSuccess={onDocumentLoadSuccess}
          onLoadError={onDocumentLoadError}
          className="flex flex-col items-center"
        >
          {error ? (
            <div className="text-red-500">{error}</div>
          ) : (
            <>
              <Page pageNumber={pageNumber} />
              <div className="flex justify-center mt-4">
                <Button
                  onClick={() => setPageNumber(page => Math.max(page - 1, 1))}
                  disabled={pageNumber <= 1}
                >
                  Previous
                </Button>
                <p className="mx-4">
                  Page {pageNumber} of {numPages}
                </p>
                <Button
                  onClick={() => setPageNumber(page => Math.min(page + 1, numPages))}
                  disabled={pageNumber >= numPages}
                >
                  Next
                </Button>
              </div>
            </>
          )}
        </Document>
      ) : (
        <div className="flex items-center justify-center h-full">
          <p className="text-lg text-gray-500">No PDF file specified.</p>
        </div>
      )}
    </div>
  )
}

const JSONEditor = ({ content, onChange }) => {
  const [jsonContent, setJsonContent] = useState(JSON.stringify(content || {}, null, 2))

  useEffect(() => {
    setJsonContent(JSON.stringify(content || {}, null, 2))
  }, [content])

  const handleChange = (event) => {
    const newContent = event.target.value
    setJsonContent(newContent)
    try {
      const parsedContent = JSON.parse(newContent)
      onChange(parsedContent)
    } catch (error) {
      console.error('Invalid JSON:', error)
    }
  }

  return (
    <div className="h-full p-4">
      <textarea
        className="w-full h-full p-4 font-mono text-sm bg-gray-900 text-white rounded-md resize-none"
        value={jsonContent}
        onChange={handleChange}
        aria-label="JSON Editor"
      />
    </div>
  )
}

const WebTerminal = ({ isOpen, onClose }) => {
  return (
    <div className={`fixed inset-y-0 left-0 z-50 w-80 transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
      <div className="bg-black bg-opacity-80 text-green-400 h-full p-4 shadow-lg">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-semibold">Terminal</h2>
          <Button variant="ghost" size="sm" onClick={onClose} aria-label="Close Terminal">
            Close
          </Button>
        </div>
        <ScrollArea className="h-[calc(100%-2rem)]">
          <p>$ Welcome to the Web Terminal</p>
          <p>$ Type your commands here</p>
        </ScrollArea>
      </div>
    </div>
  )
}

export default function SplitPaneLayout() {
  const [isTerminalOpen, setIsTerminalOpen] = useState(false)
  const [pdfContent, setPdfContent] = useState(null)
  const [jsonContent, setJsonContent] = useState(null)
  const [isMobile, setIsMobile] = useState(false)
  const wsRef = useRef(null)


useEffect(() => {
    const loadWorker = async () => {
    //   const workerSrc = await import("pdfjs-dist/build/pdf.worker.mjs");
      pdfjs.GlobalWorkerOptions.workerSrc = new URL(
        "pdfjs-dist/build/pdf.worker.mjs",
        import.meta.url
      ).toString();
    };
    loadWorker();
  }, []);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768)
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  useEffect(() => {
    // Initialize WebSocket connection
    wsRef.current = new WebSocket('ws://127.0.0.1:8041/ws')

    wsRef.current.onopen = () => {
      console.log('WebSocket connection established')
    }

    wsRef.current.onmessage = (event) => {
    console.log("receoved daea", event.data);
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'json') {
          setJsonContent(data.content)
        } else if (data.type === 'pdf') {
          // Convert base64 to Blob
          const pdfBlob = new Blob([Uint8Array.from(atob(data.content), c => c.charCodeAt(0))], { type: 'application/pdf' })
          setPdfContent(pdfBlob);
          console.log('PDF content received:', pdfBlob);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
        toast({
          title: "Error",
          description: "Failed to process server message. Please try again.",
          variant: "destructive",
        })
      }
    }

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
      toast({
        title: "Connection Error",
        description: "Failed to connect to the server. Please try again.",
        variant: "destructive",
      })
    }

    wsRef.current.onclose = () => {
      console.log('WebSocket connection closed')
    }

    // Clean up WebSocket connection on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const handleJSONChange = (newContent) => {
    setJsonContent(newContent)
    // Send the updated JSON to the backend
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'json', content: newContent }))
    }
  }

  const toggleTerminal = () => setIsTerminalOpen(!isTerminalOpen)

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Vertical button bar */}
      <div className="bg-gray-800 text-white w-12 flex flex-col items-center py-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTerminal}
          aria-label={isTerminalOpen ? "Close Terminal" : "Open Terminal"}
          aria-expanded={isTerminalOpen}
          className="mb-4"
        >
          <Terminal className="h-6 w-6" />
        </Button>
      </div>

      {/* Main content area */}
      <div className="flex-grow flex flex-col md:flex-row">
        {/* PDF Viewer */}
        <div className={`${isMobile ? 'h-1/2' : 'w-1/2'} border-b md:border-r border-gray-300 overflow-hidden`}>
          <PDFViewer content={pdfContent} />
        </div>
        {/* JSON Editor */}
        <div className={isMobile ? 'h-1/2' : 'w-1/2'}>
          <JSONEditor content={jsonContent} onChange={handleJSONChange} />
        </div>
      </div>

      {/* Sliding Terminal */}
      <WebTerminal isOpen={isTerminalOpen} onClose={() => setIsTerminalOpen(false)} />
    </div>
  )
}