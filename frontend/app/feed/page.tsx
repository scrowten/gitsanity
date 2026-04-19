'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { RefreshCw, Loader2 } from 'lucide-react'
import { NavBar } from '@/components/NavBar'
import { RepoCard } from '@/components/RepoCard'
import { RepoCardSkeleton } from '@/components/RepoCardSkeleton'
import { Toaster } from '@/components/Toast'
import { getFeed, getPreferences, repoAction } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { useToast } from '@/lib/useToast'
import { cn } from '@/lib/utils'
import type { RepoCard as RepoCardType } from '@/types'

export default function FeedPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const [page, setPage] = useState(1)
  const [dismissed, setDismissed] = useState<Set<number>>(new Set())
  const [activeLangs, setActiveLangs] = useState<Set<string>>(new Set())
  const queryClient = useQueryClient()
  const { toasts, show: showToast, close: closeToast } = useToast()

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/')
    }
  }, [authLoading, isAuthenticated, router])

  const { data, isLoading, isError } = useQuery({
    queryKey: ['feed', page],
    queryFn: () => getFeed(page),
    enabled: isAuthenticated,
  })

  const { data: preferences } = useQuery({
    queryKey: ['preferences'],
    queryFn: getPreferences,
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  })

  const actionMutation = useMutation({
    mutationFn: ({ id, action }: { id: number; action: 'saved' | 'dismissed' }) =>
      repoAction(id, action),
    onSuccess: (_, { id, action }) => {
      if (action === 'dismissed') {
        setDismissed((prev) => new Set(prev).add(id))
        showToast('Dismissed', 'info')
      } else {
        queryClient.invalidateQueries({ queryKey: ['saved'] })
        showToast('Saved to bookmarks')
      }
    },
    onError: () => showToast('Something went wrong — please try again', 'info'),
  })

  const handleRefresh = () => {
    setPage(1)
    queryClient.invalidateQueries({ queryKey: ['feed'] })
  }

  const toggleLang = (lang: string) => {
    setActiveLangs((prev) => {
      const next = new Set(prev)
      if (next.has(lang)) {
        next.delete(lang)
      } else {
        next.add(lang)
      }
      return next
    })
  }

  const visibleItems = (data?.items ?? [])
    .filter((r: RepoCardType) => !dismissed.has(r.github_id))
    .filter((r: RepoCardType) =>
      activeLangs.size === 0 ||
      (r.primary_language !== null && activeLangs.has(r.primary_language))
    )

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-[#2da44e]" />
      </div>
    )
  }

  if (!isAuthenticated) return null

  return (
    <>
      <NavBar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-[#1f2328]">Your Feed</h1>
            <p className="text-sm text-[#656d76] mt-0.5">Repos matched to your interests</p>
          </div>
          <button
            onClick={handleRefresh}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-[#1f2328] bg-white border border-[#d0d7de] rounded-md hover:bg-[#f6f8fa] transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>

        {/* Language filter bar */}
        {preferences && preferences.languages.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 mb-6 pb-4 border-b border-[#d0d7de]">
            <span className="text-xs text-[#656d76] font-medium shrink-0">Filter:</span>
            <button
              onClick={() => setActiveLangs(new Set())}
              className={cn(
                'text-xs px-3 py-1 rounded-full font-medium border transition-colors',
                activeLangs.size === 0
                  ? 'bg-[#2da44e] text-white border-[#2da44e]'
                  : 'bg-white text-[#1f2328] border-[#d0d7de] hover:bg-[#f6f8fa]'
              )}
            >
              All
            </button>
            {preferences.languages.map((lang) => (
              <button
                key={lang.name}
                onClick={() => toggleLang(lang.name)}
                className={cn(
                  'text-xs px-3 py-1 rounded-full font-medium border transition-colors',
                  activeLangs.has(lang.name)
                    ? 'bg-[#2da44e] text-white border-[#2da44e]'
                    : 'bg-white text-[#1f2328] border-[#d0d7de] hover:bg-[#f6f8fa]'
                )}
              >
                {lang.name}
                <span className={cn(
                  'ml-1.5 text-[10px]',
                  activeLangs.has(lang.name) ? 'text-green-100' : 'text-[#656d76]'
                )}>
                  {Math.round(lang.weight * 100)}%
                </span>
              </button>
            ))}
          </div>
        )}

        {/* Skeleton loading */}
        {isLoading && (
          <div className="grid grid-cols-1 gap-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <RepoCardSkeleton key={i} />
            ))}
          </div>
        )}

        {isError && (
          <div className="text-center py-20">
            <p className="text-[#656d76] mb-3">Could not load your feed.</p>
            <button onClick={handleRefresh} className="text-sm text-[#0969da] hover:underline">
              Try again
            </button>
          </div>
        )}

        {!isLoading && !isError && visibleItems.length === 0 && (
          <div className="text-center py-20">
            <p className="text-[#656d76] mb-1">
              {activeLangs.size > 0
                ? `No repos found for selected language${activeLangs.size > 1 ? 's' : ''}.`
                : 'No recommendations yet.'}
            </p>
            <p className="text-sm text-[#656d76]">
              {activeLangs.size > 0
                ? 'Try selecting a different language or click All.'
                : 'Make sure your GitHub account has starred repos so we can learn your preferences.'}
            </p>
          </div>
        )}

        {/* Repo cards */}
        {!isLoading && (
          <div className="grid grid-cols-1 gap-4">
            {visibleItems.map((repo: RepoCardType) => (
              <RepoCard
                key={repo.github_id}
                repo={repo}
                onSave={(id) => actionMutation.mutate({ id, action: 'saved' })}
                onDismiss={(id) => actionMutation.mutate({ id, action: 'dismissed' })}
              />
            ))}
          </div>
        )}

        {/* Pagination */}
        {data && data.has_more && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setPage((p) => p + 1)}
              className="px-5 py-2 text-sm font-medium text-[#0969da] border border-[#d0d7de] rounded-md hover:bg-[#f6f8fa] transition-colors"
            >
              Load more
            </button>
          </div>
        )}
      </div>

      <Toaster toasts={toasts} onClose={closeToast} />
    </>
  )
}
