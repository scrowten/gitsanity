# GitSanity

Personalized GitHub repository discovery. Like [arxiv-sanity](https://arxiv-sanity-lite.com/), but for GitHub repos.

GitSanity learns from your GitHub stars and surfaces repositories you would never find on your own — beyond simple trending lists. It analyzes your starred repos to build a preference profile, then scores and ranks candidates from a curated catalog.

---

## Features

- **GitHub OAuth login** — read-only access, only your public stars
- **Preference profile** — automatically built from your starred repos (languages, topics, keywords)
- **Personalized feed** — repos scored and ranked against your profile with a human-readable reason
- **Language filter** — toggle by language with percentage weights from your profile
- **Save / Dismiss** — bookmark repos to revisit; dismiss ones that don't fit
- **Skeleton loaders + toast notifications** — polished loading states and feedback

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router) + TypeScript |
| Styling | Tailwind CSS v4 |
| State / data fetching | TanStack Query v5 |
| Backend | FastAPI + Python 3.11 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Auth | GitHub OAuth 2.0 + JWT session cookie |
| HTTP client | httpx (async) |
| Rate limiting | SlowAPI |
| Containerization | Docker + Docker Compose |

---

## How It Works

```
User logs in with GitHub
        │
        ▼
Backend fetches all starred repos via GitHub API
        │
        ▼
Preference profile built:
  languages → {python: 0.62, typescript: 0.28, ...}
  topics    → {machine-learning: 0.41, ...}
        │
        ▼
Candidate repos scored against profile:
  score = lang_weight×0.4 + topic_weight×0.4 + keyword_weight×0.2
  freshness boost ×1.2 for repos updated within 90 days
        │
        ▼
Feed returned sorted by score, diversified (max 3 repos per owner)
```

---

## Project Structure

```
gitsanity/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, middleware
│   │   ├── config.py            # Pydantic settings from .env
│   │   ├── routers/
│   │   │   ├── auth.py          # GitHub OAuth, session cookie
│   │   │   ├── feed.py          # Feed, preferences, repo actions
│   │   │   └── saved.py         # Saved repos
│   │   ├── services/
│   │   │   ├── auth.py          # Token exchange, user creation
│   │   │   ├── github.py        # GitHub API client (httpx)
│   │   │   ├── preference.py    # Profile builder from starred repos
│   │   │   └── recommender.py   # Scoring + ranking logic
│   │   ├── models/              # SQLAlchemy ORM models
│   │   └── schemas/             # Pydantic request/response schemas
│   ├── alembic/                 # DB migrations
│   ├── tests/                   # pytest test suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Landing page
│   │   ├── feed/page.tsx        # Main feed with language filter
│   │   └── saved/page.tsx       # Saved repos
│   ├── components/
│   │   ├── NavBar.tsx
│   │   ├── RepoCard.tsx
│   │   ├── RepoCardSkeleton.tsx
│   │   └── Toast.tsx
│   ├── lib/
│   │   ├── api.ts               # Axios client + API functions
│   │   ├── auth.ts              # useAuth hook
│   │   └── useToast.ts
│   └── Dockerfile
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   └── tasks.md
├── docker-compose.yml
├── railway.toml                 # Railway backend deploy config
└── .env.example
```

---

## Local Setup

### Prerequisites

- Docker + Docker Compose
- A GitHub OAuth App (see below)

### 1. Create a GitHub OAuth App

Go to **github.com/settings/developers** → OAuth Apps → New OAuth App:

| Field | Value |
|-------|-------|
| Homepage URL | `http://localhost:3000` |
| Authorization callback URL | `http://localhost:8000/auth/callback` |

Copy the **Client ID** and generate a **Client Secret**.

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in `.env`:

```bash
# Generate a random password for Postgres
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_hex(16))")

# Generate a JWT signing key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

GITHUB_CLIENT_ID=<from OAuth App>
GITHUB_CLIENT_SECRET=<from OAuth App>
GITHUB_REDIRECT_URI=http://localhost:8000/auth/callback

PRODUCTION=false
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000"]
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start everything

```bash
docker compose up --build
```

Startup order: PostgreSQL → migrations → backend → frontend.

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `POSTGRES_PASSWORD` | Yes | Password for the `gitsanity` Postgres user |
| `DATABASE_URL` | Yes | Full asyncpg connection string (auto-set in Docker) |
| `GITHUB_CLIENT_ID` | Yes | GitHub OAuth App client ID |
| `GITHUB_CLIENT_SECRET` | Yes | GitHub OAuth App client secret |
| `GITHUB_REDIRECT_URI` | Yes | Must match the callback URL in your OAuth App |
| `SECRET_KEY` | Yes | JWT signing key — generate with `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `GITHUB_TOKEN` | No | Personal access token to raise GitHub API rate limits during ingestion |
| `PRODUCTION` | No | `true` enables `secure` cookies and `samesite=none` for cross-domain deploys |
| `FRONTEND_URL` | No | Used for OAuth redirect after login (default: `http://localhost:3000`) |
| `CORS_ORIGINS` | No | JSON array of allowed origins (default: `["http://localhost:3000"]`) |
| `NEXT_PUBLIC_API_URL` | No | Backend base URL baked into the frontend build |

---

## Running Tests

```bash
# Backend (inside Docker)
docker compose run --rm backend uv run pytest --cov=app tests/

# Frontend
cd frontend && npm run test:run
```

---

## Self-Hosted Deployment (Tailscale)

If you have a home server accessible via Tailscale:

### 1. Find your Tailscale IP
```bash
tailscale ip -4   # e.g. 100.94.x.x
```

### 2. Create a GitHub OAuth App with your Tailscale IP as callback
```
Authorization callback URL: http://100.94.x.x:8000/auth/callback
```

### 3. Set up `.env` on the server
```bash
PRODUCTION=false        # HTTP is fine — no HTTPS needed on local network
FRONTEND_URL=http://100.94.x.x:3000
CORS_ORIGINS=["http://100.94.x.x:3000"]
GITHUB_REDIRECT_URI=http://100.94.x.x:8000/auth/callback
NEXT_PUBLIC_API_URL=http://100.94.x.x:8000
```

### 4. Deploy
```bash
git clone <repo> ~/gitsanity && cd ~/gitsanity
# fill in .env
docker compose up -d --build
```

### 5. Auto-start on reboot
```ini
# /etc/systemd/system/gitsanity.service
[Unit]
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/<user>/gitsanity
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=<user>
Group=docker

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now gitsanity.service
```

### Updating
```bash
ssh user@100.94.x.x
cd ~/gitsanity && git pull
docker compose up -d --build
```

---

## Cloud Deployment (Railway + Vercel)

### Backend → Railway

1. Connect repo to a Railway project
2. Railway reads `railway.toml` and builds `backend/Dockerfile` automatically
3. Add a **PostgreSQL** service — copy the connection string and change `postgresql://` → `postgresql+asyncpg://`
4. Set environment variables in the Railway dashboard:

```
PRODUCTION=true
DATABASE_URL=postgresql+asyncpg://...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GITHUB_REDIRECT_URI=https://<your-backend>.up.railway.app/auth/callback
SECRET_KEY=<random 32-byte hex>
FRONTEND_URL=https://<your-app>.vercel.app
CORS_ORIGINS=["https://<your-app>.vercel.app"]
```

### Frontend → Vercel

1. Import repo in Vercel → set **Root Directory** to `frontend`
2. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://<your-backend>.up.railway.app
   ```
3. Update your GitHub OAuth App callback URL to the Railway backend URL

> **Note**: With `PRODUCTION=true`, session cookies use `samesite=none; secure` to work across the Railway/Vercel domain boundary.

---

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | — | Health check |
| `GET` | `/auth/login` | — | Start GitHub OAuth flow |
| `GET` | `/auth/callback` | — | GitHub OAuth callback |
| `GET` | `/auth/me` | ✓ | Current user info |
| `POST` | `/auth/logout` | ✓ | Clear session cookie |
| `GET` | `/feed` | ✓ | Personalized repo feed (paginated) |
| `GET` | `/feed/preferences` | ✓ | User's language preferences with weights |
| `POST` | `/feed/{id}/action` | ✓ | Save / dismiss / click a repo |
| `GET` | `/saved` | ✓ | List saved repos |

Full interactive docs at `/docs` (Swagger UI) when running locally.

---

## Docs

- [Product Requirements](docs/prd.md)
- [Architecture](docs/architecture.md)
- [Task List](docs/tasks.md)
