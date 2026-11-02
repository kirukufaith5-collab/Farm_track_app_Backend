# Current Task

**Task name:** FastAPI + PostGIS foundation (Phase 1)  
**Goal:** Replace Firebase Auth + Firestore with FastAPI + PostgreSQL (PostGIS), JWT in HTTP-only cookies, registration with email + phone.

## Approved scope

### Phase 0 – Bootstrap
- [x] Done (PR #1 merged)

### Phase 1 – Backend foundation (this branch)
- [x] FastAPI project at repository root
- [x] PostgreSQL + PostGIS via Docker Compose
- [x] Alembic scaffolding
- [x] User model (email, phone, password, full_name)
- [x] JWT authentication via HTTP-only cookies (access + refresh)
- [x] `fields` CRUD with PostGIS polygons
- [x] CORS with credentials for Vercel
- [x] Health endpoint
- [x] `.env.example`, Dockerfile, docker-compose.yml
- [x] README

## Explicitly out of scope (for now)

- WebSockets / real-time push
- File / image uploads
- Admin roles
- Email verification / password reset
- Frontend changes
- Production Render deployment (config ready, deploy later)

## Decisions made

- Layout: repository root
- Resource name: `fields`
- Auth: email + password; registration also collects phone
- Token delivery: JWT in HTTP-only cookies
- Deployment target: Render
- Workflow: topic branch → `dev` → PR to `main`

## Remaining / follow-ups

- Create initial Alembic migration after first successful local run
- Confirm cookie SameSite/Secure values for production Vercel ↔ Render
- Frontend migration off Firebase (separate repo/task)
- Phone number: currently required at registration

## Risks

- Cross-origin cookies (Vercel ↔ Render) require Secure + SameSite=None
- create_all used in development; production should rely on Alembic only
