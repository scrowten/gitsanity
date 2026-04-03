'use client'

import { useQuery } from '@tanstack/react-query'
import { Bookmark, Loader2 } from 'lucide-react'
import { NavBar } from '@/components/NavBar'
import { RepoCard } from '@/components/RepoCard'
import { getSaved } from '@/lib/api'

export default function SavedPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['saved'],
    queryFn: getSaved,
  })

  return (
    <>
      <NavBar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Saved Repos</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            {data ? `${data.length} repo${data.length !== 1 ? 's' : ''} saved` : 'Your bookmarked repositories'}
          </p>
        </div>

        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20 gap-3 text-gray-400">
            <Loader2 className="w-8 h-8 animate-spin" />
            <p className="text-sm">Loading saved repos...</p>
          </div>
        )}

        {isError && (
          <div className="text-center py-20 text-gray-500">
            Could not load saved repos.
          </div>
        )}

        {!isLoading && !isError && data?.length === 0 && (
          <div className="text-center py-20">
            <Bookmark className="w-10 h-10 text-gray-200 mx-auto mb-3" />
            <p className="text-gray-500 mb-1">No saved repos yet.</p>
            <p className="text-sm text-gray-400">
              Hit <strong>Save</strong> on repos from your feed to bookmark them here.
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4">
          {data?.map((repo) => (
            <RepoCard key={repo.github_id} repo={repo} saved />
          ))}
        </div>
      </div>
    </>
  )
}
