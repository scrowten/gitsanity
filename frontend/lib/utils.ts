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
  python: 'bg-[#3572A5]/10 text-[#3572A5]',
  typescript: 'bg-[#3178c6]/10 text-[#3178c6]',
  javascript: 'bg-[#f1e05a]/20 text-[#b5a200]',
  rust: 'bg-[#dea584]/20 text-[#9b4b23]',
  go: 'bg-[#00ADD8]/10 text-[#007d9c]',
  java: 'bg-[#b07219]/10 text-[#b07219]',
  'c++': 'bg-[#f34b7d]/10 text-[#c0185d]',
  ruby: 'bg-[#701516]/10 text-[#701516]',
  swift: 'bg-[#F05138]/10 text-[#c23b1e]',
  kotlin: 'bg-[#A97BFF]/10 text-[#7b4fd4]',
  shell: 'bg-[#89e051]/10 text-[#3d7a18]',
  c: 'bg-[#555555]/10 text-[#555555]',
  default: 'bg-[#eaeef2] text-[#57606a]',
}

export function languageColor(lang: string | null): string {
  if (!lang) return LANGUAGE_COLORS.default
  return LANGUAGE_COLORS[lang.toLowerCase()] ?? LANGUAGE_COLORS.default
}
