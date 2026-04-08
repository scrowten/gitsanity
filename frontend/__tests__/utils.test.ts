import { describe, it, expect } from 'vitest'
import { formatStars, languageColor } from '@/lib/utils'

describe('formatStars', () => {
  it('returns the number as string for < 1000', () => {
    expect(formatStars(0)).toBe('0')
    expect(formatStars(999)).toBe('999')
    expect(formatStars(500)).toBe('500')
  })

  it('formats thousands with k suffix', () => {
    expect(formatStars(1000)).toBe('1.0k')
    expect(formatStars(1500)).toBe('1.5k')
    expect(formatStars(12000)).toBe('12.0k')
    expect(formatStars(100000)).toBe('100.0k')
  })
})

describe('languageColor', () => {
  it('returns default color for null', () => {
    expect(languageColor(null)).toBe('bg-gray-100 text-gray-700')
  })

  it('returns correct color for known languages', () => {
    expect(languageColor('Python')).toBe('bg-blue-100 text-blue-800')
    expect(languageColor('TypeScript')).toBe('bg-sky-100 text-sky-800')
    expect(languageColor('Go')).toBe('bg-cyan-100 text-cyan-800')
    expect(languageColor('Rust')).toBe('bg-orange-100 text-orange-800')
  })

  it('is case-insensitive', () => {
    expect(languageColor('python')).toBe(languageColor('Python'))
    expect(languageColor('TYPESCRIPT')).toBe(languageColor('TypeScript'))
  })

  it('returns default for unknown languages', () => {
    expect(languageColor('Brainfuck')).toBe('bg-gray-100 text-gray-700')
  })
})
