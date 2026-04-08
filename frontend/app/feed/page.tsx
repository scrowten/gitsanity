'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { RefreshCw, Loader2 } from 'lucide-react'
import { NavBar } from '@/components/NavBar'
import { RepoCard } from '@/components/RepoCard'
import { getFeed, repoAction } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import type { RepoCard as RepoCardType } from '@/types'

export default function FeedPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const [page, setPage] = useState(1)
  const [dismissed, setDismissed] = useState<Set<number>>(new Set())
  const queryClient = useQueryClient()

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/')
    }
  }, [authLoading, isAuthenticated, router])

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['feed', page],
    queryFn: () => getFeed(page),
  })

  const actionMutation = useMutation({
    mutationFn: ({ id, action }: { id: number; action: 'saved' | 'dismissed' }) =>
      repoAction(id, action),
    onSuccess: (_, { id, action }) => {
      if (action === 'dismissed') {
        setDismissed((prev) => new Set(prev).add(id))
      } else {
        queryClient.invalidateQueries({ queryKey: ['saved'] })
      }
    },
  })

  const visibleItems = data?.items.filter((r: RepoCardType) => !dismissed.has(r.github_id)) ?? []

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
      </div>
    )
  }

  if (!isAuthenticated) return null

  return (
    <>
      <NavBar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Your Feed</h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Repos matched to your interests
            </p>
          </div>
          <button
            onClick={() => { setPage(1); refetch() }}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>

        {/* States */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-gray-400">
            <Loader2 className="w-8 h-8 animate-spin" />
            <p className="text-sm">Loading your personalized feed...</p>
          </div>
        )}

        {isError && (
          <div className="text-center py-20">
            <p className="text-gray-500 mb-3">Could not load your feed.</p>
            <button
              onClick={() => refetch()}
              className="text-sm text-indigo-600 hover:underline"
            >
              Try again
            </button>
          </div>
        )}

        {!isLoading && !isError && visibleItems.length === 0 && (
          <div className="text-center py-20">
            <p className="text-gray-500 mb-1">No recommendations yet.</p>
            <p className="text-sm text-gray-400">
              Make sure your GitHub account has starred repos so we can learn your preferences.
            </p>
          </div>
        )}

        {/* Repo cards */}
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

        {/* Pagination */}
        {data && data.has_more && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setPage((p) => p + 1)}
              className="px-5 py-2 text-sm font-medium text-indigo-600 border border-indigo-200 rounded-lg hover:bg-indigo-50 transition-colors"
            >
              Load more
            </button>
          </div>
        )}
      </div>
    </>
  )
}
