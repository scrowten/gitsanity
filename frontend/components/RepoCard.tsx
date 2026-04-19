'use client'

import { Star, GitFork, ExternalLink, Bookmark, X } from 'lucide-react'
import type { RepoCard as RepoCardType } from '@/types'
import { cn, formatStars, languageColor } from '@/lib/utils'

// M-2: Guard against javascript: URIs — only allow GitHub https links
function safeGitHubUrl(url: string): string | null {
  try {
    const parsed = new URL(url)
    if (parsed.protocol === 'https:' && parsed.hostname === 'github.com') {
      return url
    }
  } catch {
    // invalid URL
  }
  return null
}

interface RepoCardProps {
  repo: RepoCardType
  onSave?: (id: number) => void
  onDismiss?: (id: number) => void
  onUnsave?: (id: number) => void
  saved?: boolean
}

export function RepoCard({ repo, onSave, onDismiss, onUnsave, saved = false }: RepoCardProps) {
  const safeUrl = safeGitHubUrl(repo.html_url)

  return (
    <div className="bg-white border border-[#d0d7de] rounded-md p-5 hover:border-[#0969da] transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-2">
        {safeUrl ? (
          <a
            href={safeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-1.5 font-semibold text-[#0969da] hover:underline"
          >
            <span className="truncate">{repo.full_name}</span>
            <ExternalLink className="w-3.5 h-3.5 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
          </a>
        ) : (
          <span className="font-semibold text-[#1f2328] truncate">{repo.full_name}</span>
        )}

        {/* Stars */}
        <div className="flex items-center gap-1 text-sm text-[#656d76] shrink-0">
          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
          <span>{formatStars(repo.star_count)}</span>
        </div>
      </div>

      {/* Description */}
      {repo.description && (
        <p className="text-sm text-[#656d76] mb-3 line-clamp-2">{repo.description}</p>
      )}

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {repo.primary_language && (
          <span className={cn('text-xs px-2 py-0.5 rounded-full font-medium', languageColor(repo.primary_language))}>
            {repo.primary_language}
          </span>
        )}
        {repo.topics.slice(0, 4).map((topic) => (
          <span key={topic} className="text-xs px-2 py-0.5 rounded-full bg-[#ddf4ff] text-[#0969da] font-medium">
            {topic}
          </span>
        ))}
      </div>

      {/* Reason */}
      <p className="text-xs text-[#656d76] mb-4 italic">{repo.reason}</p>

      {/* Actions */}
      {(onSave || onDismiss) && !saved && (
        <div className="flex gap-2">
          {onSave && (
            <button
              onClick={() => onSave(repo.github_id)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-white bg-[#2da44e] rounded-md hover:bg-[#2c974b] transition-colors"
            >
              <Bookmark className="w-3.5 h-3.5" />
              Save
            </button>
          )}
          {onDismiss && (
            <button
              onClick={() => onDismiss(repo.github_id)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-[#1f2328] bg-[#f6f8fa] border border-[#d0d7de] rounded-md hover:bg-[#eaeef2] transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              Dismiss
            </button>
          )}
        </div>
      )}

      {saved && (
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1 text-xs text-[#2da44e] font-medium">
            <Bookmark className="w-3.5 h-3.5 fill-[#2da44e] text-[#2da44e]" />
            Saved
          </span>
          {onUnsave && (
            <button
              onClick={() => onUnsave(repo.github_id)}
              className="text-xs text-[#656d76] hover:text-red-600 transition-colors"
            >
              Remove
            </button>
          )}
        </div>
      )}
    </div>
  )
}
