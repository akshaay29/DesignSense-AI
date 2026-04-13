"use client"

import { useCallback, useState } from "react"
import { Upload, File, X, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface FileUploaderProps {
  onFileUpload: (file: File) => void
  isProcessing: boolean
}

export function FileUploader({ onFileUpload, isProcessing }: FileUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)

      const files = e.dataTransfer.files
      if (files.length > 0) {
        const file = files[0]
        if (
          file.name.toLowerCase().endsWith(".step") ||
          file.name.toLowerCase().endsWith(".stp")
        ) {
          setUploadedFile(file)
          onFileUpload(file)
        }
      }
    },
    [onFileUpload]
  )

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files
      if (files && files.length > 0) {
        const file = files[0]
        setUploadedFile(file)
        onFileUpload(file)
      }
    },
    [onFileUpload]
  )

  const clearFile = useCallback(() => {
    setUploadedFile(null)
  }, [])

  return (
    <div className="w-full">
      {!uploadedFile ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-all duration-200",
            isDragging
              ? "border-primary bg-primary/10"
              : "border-border bg-card hover:border-primary/50 hover:bg-card/80"
          )}
        >
          <div className="flex flex-col items-center gap-4">
            <div
              className={cn(
                "flex h-16 w-16 items-center justify-center rounded-full transition-colors",
                isDragging ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
              )}
            >
              <Upload className="h-8 w-8" />
            </div>
            <div className="text-center">
              <p className="text-lg font-medium text-foreground">
                Drag and drop your STEP file here
              </p>
              <p className="mt-1 text-sm text-muted-foreground">
                or click to browse
              </p>
              <p className="mt-2 text-xs text-muted-foreground">
                Supports .step and .stp files
              </p>
            </div>
            <input
              type="file"
              accept=".step,.stp"
              onChange={handleFileSelect}
              className="absolute inset-0 cursor-pointer opacity-0"
            />
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-between rounded-lg border border-border bg-card p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/20">
              <File className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="font-medium text-foreground">{uploadedFile.name}</p>
              <p className="text-sm text-muted-foreground">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {isProcessing ? (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                Analyzing...
              </div>
            ) : (
              <CheckCircle2 className="h-5 w-5 text-severity-success" />
            )}
            <button
              onClick={clearFile}
              className="rounded-md p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
