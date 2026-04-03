# GitSanity — Task List

## Phase 0: Foundation (Current)

### Backend Setup
- [x] Project structure (monorepo)
- [x] FastAPI app skeleton
- [x] PostgreSQL models (User, Repository, Recommendations)
- [x] Alembic migrations setup
- [x] GitHub OAuth endpoints (login, callback, logout)
- [x] GitHub API client (httpx)
- [x] Preference extraction service
- [x] Recommendation scoring service
- [x] Feed API endpoint
- [x] Saved repos API endpoint
- [ ] Install dependencies (uv/pip)
- [ ] Create initial Alembic migration
- [ ] Set up Supabase project + get DATABASE_URL
- [ ] Create GitHub OAuth App + get client_id/secret
- [ ] Run backend locally and test /health

### Frontend Setup
- [ ] Initialize Next.js project (npx create-next-app)
- [ ] Install Tailwind CSS, TanStack Query, shadcn/ui
- [ ] Landing page (/) with "Sign in with GitHub" button
- [ ] Auth callback handler
- [ ] Feed page (/feed) with RepoCard component
- [ ] Saved page (/saved)
- [ ] NavBar component
- [ ] API client (lib/api.ts)

### Tests
- [x] test_preference.py (unit tests)
- [x] test_recommender.py (unit tests)
- [ ] Run tests and verify passing

## Phase 1: MVP Polish

- [ ] Loading states and error handling in frontend
- [ ] Empty state (no recommendations yet)
- [ ] Responsive design (mobile-friendly)
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Set up production environment variables
- [ ] Test end-to-end OAuth flow in production

## Phase 2: Personalization Improvements

- [ ] Collaborative filtering (users who starred X also starred Y)
- [ ] Weekly email digest (Resend)
- [ ] "More like this" button on repo cards
- [ ] Preference profile page (show detected interests)
- [ ] Re-sync GitHub stars button
- [ ] Browser extension (add quality badge to GitHub pages)

## Phase 3: Discovery Features

- [ ] Search page (semantic + full-text)
- [ ] Browse by topic/language
- [ ] Quality score computation and display
- [ ] "Rising Stars" detection
- [ ] Public API

## Backlog

- [ ] User profile page
- [ ] Collections / curated lists
- [ ] Repo comparison
- [ ] Ecosystem maps
- [ ] Telegram/Discord bot
