"use client"

import { Box } from "lucide-react"
import { DownloadPdfButton } from "./download-pdf-button"
import type { DesignIssue } from "./issues-sidebar"

interface HeaderProps {
  fileName: string | null
  issues: DesignIssue[]
  canDownload: boolean
}

export function Header({ fileName, issues, canDownload }: HeaderProps) {
  return (
    <header className="flex items-center justify-between border-b border-border bg-card px-6 py-4">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Box className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-foreground">CAD Validator</h1>
          <p className="text-xs text-muted-foreground">AI-Powered STEP File Analysis</p>
        </div>
      </div>

      <DownloadPdfButton
        fileName={fileName}
        issues={issues}
        disabled={!canDownload}
      />
    </header>
  )
}
