# GitSanity — Architecture

## System Overview

```
┌─────────────────────────────────────────────────┐
│                   Client                         │
│  Next.js (App Router) + Tailwind + TanStack Query │
│  http://localhost:3000                           │
└───────────────────┬─────────────────────────────┘
                    │ HTTP + cookies
┌───────────────────▼─────────────────────────────┐
│                  Backend                         │
│  FastAPI + SQLAlchemy 2.0 (async)                │
│  http://localhost:8000                           │
└──────────┬──────────────────┬───────────────────┘
           │                  │
┌──────────▼──────┐  ┌────────▼────────┐
│   PostgreSQL     │  │  GitHub API     │
│   (Supabase)     │  │  (httpx)        │
│   users          │  │  - starred repos│
│   repositories   │  │  - repo search  │
│   preferences    │  │  - trending     │
│   recommendations│  └─────────────────┘
└─────────────────┘
```

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | Next.js 14 (App Router) | SSR for SEO |
| Styling | Tailwind CSS | Utility-first |
| State | TanStack Query | Server state + caching |
| Backend | FastAPI | Async Python |
| ORM | SQLAlchemy 2.0 | Async sessions |
| Migrations | Alembic | Schema versioning |
| Database | PostgreSQL | Via Supabase (managed) |
| Auth | GitHub OAuth + JWT cookie | HTTP-only session cookie |
| GitHub API | httpx + custom client | Rate-limited |
| Hosting (fe) | Vercel | Zero-config |
| Hosting (be) | Railway | Docker-based |

## Database Schema

```
users
├── id (UUID PK)
├── github_id (unique)
├── github_username
├── display_name
├── avatar_url
├── email
├── github_access_token (encrypted in prod)
├── created_at
└── last_login_at

repositories
├── id (UUID PK)
├── github_id (unique)
├── full_name
├── description
├── primary_language
├── topics (text[])
├── star_count
├── fork_count
├── readme_summary
├── html_url
├── repo_created_at
├── repo_updated_at
├── last_indexed_at
└── quality_score

user_preferences
├── id (UUID PK)
├── user_id (FK)
├── preference_type (language | topic | keyword)
├── preference_value
├── weight (0.0–1.0)
└── updated_at

starred_repos
├── id (UUID PK)
├── user_id (FK)
├── repo_github_id
├── repo_full_name
└── synced_at

recommendations
├── id (UUID PK)
├── user_id (FK)
├── repo_id (FK)
├── score
├── reason
├── generated_at
├── seen
└── action (saved | dismissed | clicked)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /auth/login | Redirect to GitHub OAuth |
| GET | /auth/callback | Handle OAuth callback, set session cookie |
| POST | /auth/logout | Clear session cookie |
| GET | /feed?page=1&limit=20 | Personalized recommendation feed |
| POST | /feed/{github_id}/action | Save/dismiss/click a repo |
| GET | /saved | User's saved repos |

## Recommendation Algorithm (v1)

```python
score = (language_match × 0.4) + (topic_overlap × 0.4) + (keyword_overlap × 0.2)
if recently_updated: score *= 1.2  # freshness boost
if stars < 10: exclude  # quality floor
```

Weights are normalized to [0, 1] based on frequency in user's starred repos.
Diversification: max 3 repos per owner in any result set.

## Auth Flow

```
1. GET /auth/login → 302 to GitHub OAuth
2. User approves → GitHub → GET /auth/callback?code=xxx
3. Backend exchanges code for access_token
4. Fetch GitHub user profile
5. Upsert user in database
6. Issue JWT in HTTP-only cookie
7. Background task: sync starred repos + build preference profile
8. 302 redirect to frontend /feed
```

## Monorepo Layout

```
gitsanity/
├── backend/          # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   ├── alembic/
│   └── tests/
├── frontend/         # Next.js TypeScript
│   └── src/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── types/
└── docs/
```
