'use client'

import { Star, GitFork, ExternalLink, Bookmark, X } from 'lucide-react'
import type { RepoCard as RepoCardType } from '@/types'
import { cn, formatStars, languageColor } from '@/lib/utils'

interface RepoCardProps {
  repo: RepoCardType
  onSave?: (id: number) => void
  onDismiss?: (id: number) => void
  onUnsave?: (id: number) => void
  saved?: boolean
}

export function RepoCard({ repo, onSave, onDismiss, onUnsave, saved = false }: RepoCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-2">
        <a
          href={repo.html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="group flex items-center gap-1.5 font-semibold text-gray-900 hover:text-blue-600 transition-colors"
        >
          <span className="truncate">{repo.full_name}</span>
          <ExternalLink className="w-3.5 h-3.5 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
        </a>

        {/* Stars */}
        <div className="flex items-center gap-1 text-sm text-gray-500 shrink-0">
          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
          <span>{formatStars(repo.star_count)}</span>
        </div>
      </div>

      {/* Description */}
      {repo.description && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">{repo.description}</p>
      )}

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {repo.primary_language && (
          <span className={cn('text-xs px-2 py-0.5 rounded-full font-medium', languageColor(repo.primary_language))}>
            {repo.primary_language}
          </span>
        )}
        {repo.topics.slice(0, 4).map((topic) => (
          <span key={topic} className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
            {topic}
          </span>
        ))}
      </div>

      {/* Reason */}
      <p className="text-xs text-indigo-600 mb-4 italic">{repo.reason}</p>

      {/* Actions */}
      {(onSave || onDismiss) && !saved && (
        <div className="flex gap-2">
          {onSave && (
            <button
              onClick={() => onSave(repo.github_id)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <Bookmark className="w-3.5 h-3.5" />
              Save
            </button>
          )}
          {onDismiss && (
            <button
              onClick={() => onDismiss(repo.github_id)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              Dismiss
            </button>
          )}
        </div>
      )}

      {saved && (
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1 text-xs text-green-700 font-medium">
            <Bookmark className="w-3.5 h-3.5 fill-green-600 text-green-600" />
            Saved
          </span>
          {onUnsave && (
            <button
              onClick={() => onUnsave(repo.github_id)}
              className="text-xs text-gray-400 hover:text-red-500 transition-colors"
            >
              Remove
            </button>
          )}
        </div>
      )}
    </div>
  )
}
