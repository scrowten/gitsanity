export interface RepoCard {
  github_id: number
  full_name: string
  description: string | null
  primary_language: string | null
  topics: string[]
  star_count: number
  html_url: string
  score: number
  reason: string
}

export interface FeedResponse {
  items: RepoCard[]
  total: number
  page: number
  has_more: boolean
}

export interface User {
  id: string
  github_username: string
  display_name: string | null
  avatar_url: string | null
}

export interface LanguagePreference {
  name: string
  weight: number
}

export interface Preferences {
  languages: LanguagePreference[]
}
