"use client"

import { useState, useCallback } from "react"
import { Header } from "@/components/header"
import { FileUploader } from "@/components/file-uploader"
import { IssuesSidebar, type DesignIssue } from "@/components/issues-sidebar"
import { Cog, Layers, Ruler, Box } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"

export default function Home() {
  const [issues, setIssues] = useState<DesignIssue[]>([])
  const [summary, setSummary] = useState<string>("")
  const [filename, setFilename] = useState<string>("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>("")
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleFileUpload = useCallback(async (file: File) => {
    setLoading(true)
    setError("")
    setIssues([])
    setSummary("")
    setFilename(file.name)
    setUploadedFile(file)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch(`${API_BASE}/validate`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      // map backend issues to frontend DesignIssue shape
      const mapped: DesignIssue[] = (data.issues || []).map((issue: any) => ({
        id:           issue.issue_id || String(issue.face_index),
        title:        issue.title || issue.rule_id || "Design Issue",  // ← uses new title field
        description:  issue.description || "",
        severity:     (issue.severity?.toLowerCase() ?? "info") as Severity,
        aiSuggestion: issue.ai_suggestion || issue.fix || "",
        location:     `Face #${issue.face_index}`,
      }))

      setIssues(mapped)
      setSummary(data.summary || "")
    } catch (err: any) {
      setError(err.message || "Failed to validate file. Is your backend running?")
    } finally {
      setLoading(false)
    }
  }, [])

  const handleDownloadPDF = async () => {
    if (!uploadedFile) return
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append("file", uploadedFile)

      const response = await fetch(`${API_BASE}/report`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) throw new Error("PDF generation failed")

      const blob = await response.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement("a")
      a.href     = url
      a.download = `validation_${filename}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const stats = {
    critical: issues.filter(i => i.severity === "critical").length,
    major:    issues.filter(i => i.severity === "major").length,
    minor:    issues.filter(i => i.severity === "minor").length,
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 py-8">

        {/* stat cards */}
        {issues.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[
              { label: "Total Issues", value: issues.length,   icon: Layers, color: "text-foreground" },
              { label: "Critical",     value: stats.critical,  icon: Box,    color: "text-red-500"    },
              { label: "Major",        value: stats.major,     icon: Ruler,  color: "text-amber-500"  },
              { label: "Minor",        value: stats.minor,     icon: Cog,    color: "text-green-500"  },
            ].map(s => (
              <div key={s.label} className="rounded-lg border bg-card p-4">
                <div className="flex items-center gap-2 mb-1">
                  <s.icon className={`w-4 h-4 ${s.color}`} />
                  <span className="text-xs text-muted-foreground">{s.label}</span>
                </div>
                <div className={`text-2xl font-medium ${s.color}`}>{s.value}</div>
              </div>
            ))}
          </div>
        )}

        {/* AI summary */}
        {summary && (
          <div className="rounded-lg border bg-blue-50 dark:bg-blue-950 p-4 mb-6">
            <p className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-1">
              AI Executive Summary
            </p>
            <p className="text-sm text-blue-700 dark:text-blue-300">{summary}</p>
          </div>
        )}

        {/* error */}
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 mb-6 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* loading */}
        {loading && (
          <div className="rounded-lg border bg-card p-6 mb-6 text-center">
            <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto mb-3" />
            <p className="text-sm text-muted-foreground">
              Analysing design with AI...
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-4">
            <FileUploader onFileUpload={handleFileUpload} />

            {/* download PDF button */}
            {issues.length > 0 && uploadedFile && (
              <button
                onClick={handleDownloadPDF}
                disabled={loading}
                className="w-full rounded-lg border border-primary bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:opacity-90 disabled:opacity-50"
              >
                Download PDF Report
              </button>
            )}
          </div>

          <div className="lg:col-span-2">
            <IssuesSidebar issues={issues.length > 0 ? issues : []} />
          </div>
        </div>
      </main>
    </div>
  )
}