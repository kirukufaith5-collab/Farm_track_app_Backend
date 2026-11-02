# Current Task

**Task name:** Backend bootstrap + FastAPI foundation  
**Goal:** Replace Firebase Auth + Firestore with a FastAPI + PostgreSQL (PostGIS) backend that supports the existing FarmTrack frontend features, using JWT in HTTP-only cookies.

## Approved scope

### Phase 0 – Bootstrap (this PR)
- [x] Initial repository structure
- [x] `.gitignore`, `README.md`
- [x] `.trackers/` (repo-state, task, rollback)
- [ ] Create `dev` branch after this lands on `main`
- [ ] Establish topic-branch → `dev` → PR to `main` workflow

### Phase 1 – Backend foundation (subsequent PRs)
- FastAPI project at repository root
- PostgreSQL + PostGIS via Docker Compose
- Alembic migrations
- User model with email + phone number (registration collects both)
- JWT authentication via HTTP-only cookies (access + refresh)
- `fields` CRUD API matching frontend data model
- CORS configured for Vercel frontend origin
- Health endpoint
- `.env.example`, Dockerfile, docker-compose.yml
- Render-ready configuration

## Explicitly out of scope (for now)

- WebSockets / real-time push
- File / image uploads
- Admin roles / multi-tenancy beyond per-user ownership
- Email verification / password reset flows (can be added later)
- Frontend changes (handled in the frontend repository)

## Decisions made

- Layout: repository root (no `backend/` subfolder)
- Resource name: `fields` (matches frontend)
- Auth: email + password; registration also collects phone number
- Token delivery: JWT in HTTP-only cookies
- Deployment target: Render
- Workflow: topic branch → `dev` → PR to `main`

## Decisions still required

- Exact cookie names, SameSite, Secure, domain settings for Vercel ↔ Render
- Preferred access/refresh token lifetimes
- Whether phone number is required or optional at registration

## Risks

- CORS + cookie settings across Vercel (frontend) and Render (backend) need care (SameSite=None; Secure)
