# GitSanity

Personalized GitHub repository discovery. Like arxiv-sanity, but for GitHub repos.

It learns from your GitHub stars and surfaces repositories you would never find on your own.

## Tech Stack

- **Backend**: Python + FastAPI + SQLAlchemy 2.0
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL (Supabase)
- **Auth**: GitHub OAuth

## Project Structure

```
gitsanity/
├── backend/      # FastAPI Python backend
├── frontend/     # Next.js TypeScript frontend
└── docs/         # PRD, architecture, tasks
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Supabase account)
- GitHub OAuth App

### Backend

```bash
cd backend

# Install dependencies
pip install uv
uv sync

# Copy and fill environment variables
cp ../.env.example ../.env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
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

## Docs

- [Product Requirements](docs/prd.md)
- [Architecture](docs/architecture.md)
- [Task List](docs/tasks.md)
