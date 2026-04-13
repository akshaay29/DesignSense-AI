"use client"

import { useState } from "react"
import { ChevronDown, ChevronRight, Lightbulb, AlertTriangle, AlertCircle, CheckCircle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

export type Severity = "critical" | "major" | "minor" | "info" | "warning" | "passed"

export interface DesignIssue {
  id: string
  title: string
  description: string
  severity: Severity
  aiSuggestion: string
  location?: string
}

interface IssuesSidebarProps {
  issues: DesignIssue[]
  isLoading?: boolean
}

function SeverityBadge({ severity }: { severity: Severity }) {
  const config: Record<string, { label: string; className: string; Icon: any }> = {
    critical: { label: "Critical", className: "bg-red-100 text-red-800 border-red-200",    Icon: AlertCircle   },
    major:    { label: "Major",    className: "bg-amber-100 text-amber-800 border-amber-200", Icon: AlertTriangle },
    minor:    { label: "Minor",    className: "bg-green-100 text-green-800 border-green-200", Icon: CheckCircle   },
    info:     { label: "Info",     className: "bg-blue-100 text-blue-800 border-blue-200",   Icon: Info          },
    warning:  { label: "Warning",  className: "bg-amber-100 text-amber-800 border-amber-200", Icon: AlertTriangle },
    passed:   { label: "Passed",   className: "bg-green-100 text-green-800 border-green-200", Icon: CheckCircle   },
  }

  const entry = config[severity] ?? config["info"]
  const { label, className, Icon } = entry

  return (
    <span className={cn("inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium", className)}>
      <Icon className="h-3 w-3" />
      {label}
    </span>
  )
}

function IssueCard({ issue }: { issue: DesignIssue }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="rounded-lg border border-border bg-card overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex w-full items-start gap-3 p-4 text-left transition-colors hover:bg-muted/50"
      >
        <div className="mt-0.5 text-muted-foreground">
          {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-medium text-foreground leading-tight">{issue.title}</h3>
            <SeverityBadge severity={issue.severity} />
          </div>
          {issue.location && (
            <p className="mt-1 text-xs text-muted-foreground font-mono">{issue.location}</p>
          )}
        </div>
      </button>

      {isExpanded && (
        <div className="border-t border-border px-4 py-4 space-y-4">
          <div>
            <h4 className="text-xs font-medium uppercase tracking-wide text-muted-foreground mb-2">
              Description
            </h4>
            <p className="text-sm text-foreground leading-relaxed">{issue.description}</p>
          </div>

          {issue.aiSuggestion && (
            <div className="rounded-lg bg-primary/10 border border-primary/20 p-3">
              <div className="flex items-start gap-2">
                <Lightbulb className="h-4 w-4 text-primary mt-0.5 shrink-0" />
                <div>
                  <h4 className="text-xs font-medium uppercase tracking-wide text-primary mb-1">
                    AI Fix Suggestion
                  </h4>
                  <p className="text-sm text-foreground leading-relaxed">{issue.aiSuggestion}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export function IssuesSidebar({ issues, isLoading = false }: IssuesSidebarProps) {
  const criticalCount = issues.filter(i => i.severity === "critical").length
  const majorCount    = issues.filter(i => i.severity === "major").length
  const minorCount    = issues.filter(i => i.severity === "minor").length

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-border p-4">
        <h2 className="text-lg font-semibold text-foreground">Design Issues</h2>
        {!isLoading && issues.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {criticalCount > 0 && (
              <span className="inline-flex items-center gap-1.5 rounded-md bg-red-100 px-2 py-1 text-xs font-medium text-red-800">
                <AlertCircle className="h-3 w-3" />{criticalCount} Critical
              </span>
            )}
            {majorCount > 0 && (
              <span className="inline-flex items-center gap-1.5 rounded-md bg-amber-100 px-2 py-1 text-xs font-medium text-amber-800">
                <AlertTriangle className="h-3 w-3" />{majorCount} Major
              </span>
            )}
            {minorCount > 0 && (
              <span className="inline-flex items-center gap-1.5 rounded-md bg-green-100 px-2 py-1 text-xs font-medium text-green-800">
                <CheckCircle className="h-3 w-3" />{minorCount} Minor
              </span>
            )}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="animate-pulse rounded-lg border border-border bg-card p-4">
                <div className="flex items-start justify-between">
                  <div className="h-4 w-3/4 rounded bg-muted" />
                  <div className="h-5 w-16 rounded-full bg-muted" />
                </div>
                <div className="mt-2 h-3 w-1/2 rounded bg-muted" />
              </div>
            ))}
          </div>
        ) : issues.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="rounded-full bg-muted p-4">
              <AlertTriangle className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              Upload a STEP file to see design issues
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {issues.map(issue => <IssueCard key={issue.id} issue={issue} />)}
          </div>
        )}
      </div>
    </div>
  )
}