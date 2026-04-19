# GitSanity — Roadmap

Current status: **v0.1 — self-hosted, core discovery loop working.**

---

## Now (v0.1) ✅

- GitHub OAuth login (read-only stars)
- Star sync → preference profile (languages, topics, keywords)
- Personalized feed with scoring + human-readable reasons
- Language filter with preference weights
- Save / Dismiss actions
- GitHub-themed UI
- Docker Compose self-hosted deployment
- Tailscale-accessible on home server

---

## Next (v0.2) — Feed Quality

> Make the feed feel smarter and more useful day-to-day.

- [ ] **Re-sync stars button** — manually trigger a re-sync when you've starred new repos, without logging out
- [ ] **Topic filter** — toggle topics alongside languages (machine-learning, cli-tool, etc.)
- [ ] **Exclude already-starred repos** — filter out repos you've already starred from the feed
- [ ] **Scheduled catalog refresh** — background job to ingest new trending repos daily so the feed doesn't go stale
- [ ] **Seen tracking** — mark feed items as seen across sessions (currently resets on refresh)
- [ ] **Score explanation tooltip** — hover a card to see the breakdown: lang 40% + topic 40% + keyword 20%

---

## Soon (v0.3) — Profile & Insights

> Let the user understand and control their preference profile.

- [ ] **Preference profile page** (`/profile`) — visual breakdown of your top languages, topics, keywords with weights as bar charts
- [ ] **Edit preferences** — manually boost or suppress a language/topic weight
- [ ] **Star history timeline** — when you started starring Python repos, TypeScript repos, etc.
- [ ] **Feed diversity control** — slider between "safe picks" (high match) and "explore" (low match, serendipitous)

---

## Later (v0.4) — Discovery

> Expand beyond the scoring model.

- [ ] **"More like this"** — click a saved repo and get 10 similar repos based on its language + topics
- [ ] **Search** — full-text search across the catalog with preference-aware ranking
- [ ] **Similar users** — collaborative filtering: "users who starred the same repos as you also liked..."
- [ ] **Trending this week** — a separate tab showing what's popular right now, filtered to your languages

---

## Future (v1.0) — Platform

> If this becomes useful to others beyond personal use.

- [ ] **Weekly email digest** — top 5 picks for the week, opt-in
- [ ] **Browser extension** — save to GitSanity directly from a GitHub repo page
- [ ] **Public profiles** — shareable preference profile and feed (opt-in)
- [ ] **Import from other sources** — Hacker News saves, Lobsters, DEV.to bookmarks
- [ ] **Mobile PWA** — installable, works offline for saved repos

---

## Technical Debt

- [ ] Increase test coverage to 80%+ (currently backend has unit tests, frontend has minimal)
- [ ] Add E2E test for the OAuth → feed flow
- [ ] Catalog ingestion pipeline (currently relies on users' own starred repos as the corpus)
- [ ] Database connection pooling tuning for multi-user load
- [ ] Add `updated_at` tracking for re-syncing changed repos

---

## Won't Do

- Write access to GitHub (star, fork) — out of scope, privacy risk
- Social feed / following other users — scope creep
- Mobile native app — PWA is sufficient
