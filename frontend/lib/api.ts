import axios from 'axios'
import type { FeedResponse, Preferences, RepoCard, User } from '@/types'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

export async function getFeed(page = 1): Promise<FeedResponse> {
  const { data } = await api.get<FeedResponse>('/feed', { params: { page, limit: 20 } })
  return data
}

export async function getSaved(): Promise<RepoCard[]> {
  const { data } = await api.get<RepoCard[]>('/saved')
  return data
}

export async function repoAction(githubId: number, action: 'saved' | 'dismissed' | 'clicked') {
  await api.post(`/feed/${githubId}/action`, null, { params: { action } })
}

export async function getPreferences(): Promise<Preferences> {
  const { data } = await api.get<Preferences>('/feed/preferences')
  return data
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>('/auth/me')
  return data
}

export function getLoginUrl() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  return `${base}/auth/login`
}

export async function logout() {
  await api.post('/auth/logout')
}
