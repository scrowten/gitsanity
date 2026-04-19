# GitSanity — Frontend

Next.js 16 (App Router) frontend for GitSanity.

See the [root README](../README.md) for full setup and deployment instructions.

## Development

```bash
npm install
npm run dev       # http://localhost:3000
npm run build     # production build
npm run test:run  # run vitest tests once
npm test          # vitest watch mode
```

Requires the backend running at `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`).
Use Docker Compose from the repo root for the full stack.
