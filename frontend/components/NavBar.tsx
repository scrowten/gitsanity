'use client'

import Link from 'next/link'
import Image from 'next/image'
import { usePathname, useRouter } from 'next/navigation'
import { Telescope, Bookmark, LogOut, LogIn, Rss } from 'lucide-react'
import { cn } from '@/lib/utils'
import { logout, getLoginUrl } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { useQueryClient } from '@tanstack/react-query'

export function NavBar() {
  const pathname = usePathname()
  const router = useRouter()
  const queryClient = useQueryClient()
  const { user, isAuthenticated } = useAuth()

  const handleLogout = async () => {
    await logout()
    queryClient.clear()
    router.push('/')
  }

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-gray-900 hover:text-indigo-600 transition-colors">
          <Telescope className="w-5 h-5 text-indigo-600" />
          <span>GitSanity</span>
        </Link>

        <div className="flex items-center gap-0.5 sm:gap-1">
          {isAuthenticated && (
            <>
              <Link
                href="/feed"
                className={cn(
                  'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  pathname === '/feed'
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                )}
              >
                <Rss className="w-4 h-4 shrink-0" />
                <span className="hidden sm:inline">Feed</span>
              </Link>
              <Link
                href="/saved"
                className={cn(
                  'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  pathname === '/saved'
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                )}
              >
                <Bookmark className="w-4 h-4 shrink-0" />
                <span className="hidden sm:inline">Saved</span>
              </Link>
            </>
          )}

          {isAuthenticated && user ? (
            <div className="flex items-center gap-1.5 ml-1 sm:ml-2">
              {user.avatar_url && (
                <Image
                  src={user.avatar_url}
                  alt={user.display_name ?? user.github_username}
                  width={28}
                  height={28}
                  className="rounded-full"
                />
              )}
              <span className="text-sm text-gray-700 hidden sm:block">
                {user.display_name ?? user.github_username}
              </span>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:block">Sign out</span>
              </button>
            </div>
          ) : (
            <a
              href={getLoginUrl()}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-indigo-600 hover:bg-indigo-50 transition-colors"
            >
              <LogIn className="w-4 h-4" />
              Sign in
            </a>
          )}
        </div>
      </div>
    </nav>
  )
}
