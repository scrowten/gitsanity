export function RepoCardSkeleton() {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 animate-pulse">
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="h-4 bg-gray-200 rounded w-48" />
        <div className="h-4 bg-gray-200 rounded w-12 shrink-0" />
      </div>
      <div className="h-3 bg-gray-200 rounded w-full mb-1.5" />
      <div className="h-3 bg-gray-200 rounded w-3/4 mb-3" />
      <div className="flex gap-1.5 mb-3">
        <div className="h-5 bg-gray-200 rounded-full w-16" />
        <div className="h-5 bg-gray-200 rounded-full w-20" />
        <div className="h-5 bg-gray-200 rounded-full w-14" />
      </div>
      <div className="h-3 bg-gray-200 rounded w-2/3 mb-4" />
      <div className="flex gap-2">
        <div className="h-8 bg-gray-200 rounded-lg w-16" />
        <div className="h-8 bg-gray-200 rounded-lg w-20" />
      </div>
    </div>
  )
}
