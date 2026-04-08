import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { RepoCard } from '@/components/RepoCard'
import type { RepoCard as RepoCardType } from '@/types'

const mockRepo: RepoCardType = {
  github_id: 1,
  full_name: 'owner/awesome-repo',
  description: 'An awesome repository for testing',
  primary_language: 'TypeScript',
  topics: ['testing', 'vitest', 'frontend'],
  star_count: 1250,
  html_url: 'https://github.com/owner/awesome-repo',
  score: 0.85,
  reason: 'Because it matches your interest in TypeScript',
}

describe('RepoCard', () => {
  it('renders repo name', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('owner/awesome-repo')).toBeInTheDocument()
  })

  it('renders description', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('An awesome repository for testing')).toBeInTheDocument()
  })

  it('renders formatted star count', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('1.3k')).toBeInTheDocument()
  })

  it('renders language badge', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('TypeScript')).toBeInTheDocument()
  })

  it('renders topics (up to 4)', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('testing')).toBeInTheDocument()
    expect(screen.getByText('vitest')).toBeInTheDocument()
    expect(screen.getByText('frontend')).toBeInTheDocument()
  })

  it('renders reason', () => {
    render(<RepoCard repo={mockRepo} />)
    expect(screen.getByText('Because it matches your interest in TypeScript')).toBeInTheDocument()
  })

  it('calls onSave with github_id when Save clicked', () => {
    const onSave = vi.fn()
    render(<RepoCard repo={mockRepo} onSave={onSave} onDismiss={vi.fn()} />)
    fireEvent.click(screen.getByText('Save'))
    expect(onSave).toHaveBeenCalledWith(1)
  })

  it('calls onDismiss with github_id when Dismiss clicked', () => {
    const onDismiss = vi.fn()
    render(<RepoCard repo={mockRepo} onSave={vi.fn()} onDismiss={onDismiss} />)
    fireEvent.click(screen.getByText('Dismiss'))
    expect(onDismiss).toHaveBeenCalledWith(1)
  })

  it('hides action buttons when saved=true', () => {
    render(<RepoCard repo={mockRepo} onSave={vi.fn()} onDismiss={vi.fn()} saved />)
    expect(screen.queryByText('Save')).not.toBeInTheDocument()
    expect(screen.queryByText('Dismiss')).not.toBeInTheDocument()
    expect(screen.getByText('Saved')).toBeInTheDocument()
  })

  it('renders repo link with correct href', () => {
    render(<RepoCard repo={mockRepo} />)
    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', 'https://github.com/owner/awesome-repo')
  })

  it('handles null description gracefully', () => {
    render(<RepoCard repo={{ ...mockRepo, description: null }} />)
    expect(screen.getByText('owner/awesome-repo')).toBeInTheDocument()
  })
})
