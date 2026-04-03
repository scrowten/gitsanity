# GitSanity — Product Requirements Document

## Overview

GitSanity is a personalized GitHub repository discovery platform. It learns what you care about from your GitHub stars and surfaces repositories you would never find on your own — beyond simple trending lists.

**Tagline**: "Discover GitHub repos that actually matter to you."

## Problem Statement

GitHub has 400M+ public repositories. Finding good ones is genuinely hard:
- GitHub Trending only shows what is popular *right now*, not what is relevant *to you*
- Keyword search requires knowing what you are looking for
- Awesome lists are fragmented and manually maintained
- No platform combines personalization + quality signals + semantic discovery

## Target Users

- Developers looking to discover new tools, libraries, and frameworks
- Open source enthusiasts who want to stay up to date
- Researchers and technical leads evaluating dependencies

## Core Value Proposition

GitSanity tells you what is **relevant to you**, not just what is popular. It uses your existing GitHub stars as an instant preference profile — zero onboarding friction.

## MVP Feature Set

### Must Have (Phase 1)
- [ ] GitHub OAuth sign in (read:user scope only)
- [ ] Auto-import of user's starred repos on first login
- [ ] Personalized recommendation feed
  - Language-based matching
  - Topic-based matching
  - Keyword-based matching from descriptions
  - Freshness boost for recently updated repos
  - Quality floor (min 10 stars)
- [ ] Repo cards with: name, description, language, stars, topics, reason
- [ ] Save / Dismiss actions per repo
- [ ] Saved repos page
- [ ] Refresh feed for new recommendations

### Out of Scope (Phase 1)
- Search functionality
- Browse/explore page
- Email notifications
- Social features
- Comments or reviews
- Quality score display
- Browser extension

## Success Metrics (MVP)

- Personalized feed loads within 3 seconds
- Recommendations feel relevant (user saves > 10% of shown repos)
- Zero friction signup (GitHub OAuth → personalized feed in < 10 seconds)

## User Journey

```
1. Land on homepage → "Sign in with GitHub"
2. GitHub OAuth → redirect back to /feed
3. See personalized feed (20 repo cards)
4. Each card shows: repo info + "Why recommended" + [Save] [Dismiss]
5. Click "Load more" for next batch
6. Visit /saved to review bookmarks
7. Return next session → recommendations incorporate saves/dismisses
```
