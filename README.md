# GitSanity

Personalized GitHub repository discovery. Like arxiv-sanity, but for GitHub repos.

It learns from your GitHub stars and surfaces repositories you would never find on your own.

## Tech Stack

- **Backend**: Python + FastAPI + SQLAlchemy 2.0
- **Frontend**: Next.js 16 + TypeScript + Tailwind CSS v4
- **Database**: PostgreSQL
- **Auth**: GitHub OAuth
- **Deploy**: Railway (backend) + Vercel (frontend)

## Project Structure

```
gitsanity/
├── backend/      # FastAPI Python backend
├── frontend/     # Next.js TypeScript frontend
└── docs/         # PRD, architecture, tasks
```

## Getting Started

### Option A — Docker Compose (recommended)

```bash
# 1. Copy and fill environment variables
cp .env.example .env

# 2. Start everything (PostgreSQL + backend + frontend)
docker compose up --build
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Option B — Manual setup

**Prerequisites**: Python 3.11+, Node.js 20+, PostgreSQL, GitHub OAuth App

```bash
# Backend
cd backend
pip install uv
uv sync
cp ../.env.example ../.env   # fill in values
alembic upgrade head
uvicorn app.main:app --reload
```

```bash
# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `GITHUB_CLIENT_ID` | GitHub OAuth App client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App client secret |
| `SECRET_KEY` | JWT signing key (min 32 chars) |
| `GITHUB_TOKEN` | Personal access token (for data ingestion) |

### GitHub OAuth App Setup

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Set **Authorization callback URL** to `http://localhost:8000/auth/callback`
4. Copy Client ID and Client Secret to `.env`

## Development

```bash
# Run backend tests
cd backend
pytest --cov=app tests/

# Run frontend tests
cd frontend
npm test
```

## Deployment

### Backend → Railway

1. Connect the repo to a Railway project
2. Railway reads `railway.toml` at the root and builds `backend/Dockerfile`
3. Add environment variables in the Railway dashboard (see `.env.example`)
4. Add a PostgreSQL plugin — Railway injects `DATABASE_URL` automatically

### Frontend → Vercel

1. Import the repo in Vercel; set **Root Directory** to `frontend`
2. Add `NEXT_PUBLIC_API_URL` pointing to your Railway backend URL

## Docs

- [Product Requirements](docs/prd.md)
- [Architecture](docs/architecture.md)
- [Task List](docs/tasks.md)
