import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatStars(count: number): string {
  if (count >= 1000) return `${(count / 1000).toFixed(1)}k`
  return String(count)
}

const LANGUAGE_COLORS: Record<string, string> = {
  python: 'bg-blue-100 text-blue-800',
  typescript: 'bg-sky-100 text-sky-800',
  javascript: 'bg-yellow-100 text-yellow-800',
  rust: 'bg-orange-100 text-orange-800',
  go: 'bg-cyan-100 text-cyan-800',
  java: 'bg-red-100 text-red-800',
  'c++': 'bg-pink-100 text-pink-800',
  ruby: 'bg-rose-100 text-rose-800',
  swift: 'bg-orange-100 text-orange-800',
  kotlin: 'bg-purple-100 text-purple-800',
  default: 'bg-gray-100 text-gray-700',
}

export function languageColor(lang: string | null): string {
  if (!lang) return LANGUAGE_COLORS.default
  return LANGUAGE_COLORS[lang.toLowerCase()] ?? LANGUAGE_COLORS.default
}
