# FarmTrack Backend

FastAPI + PostgreSQL (PostGIS) backend for the FarmTrack farm parcel mapping application.

Replaces the previous Firebase Auth + Firestore stack used by the frontend.

## Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI |
| ORM | SQLModel (SQLAlchemy 2) |
| Database | PostgreSQL 16 + PostGIS 3.4 |
| Migrations | Alembic |
| Auth | Email + password, JWT in **HTTP-only cookies** |
| Deploy target | Render |

## Features (Phase 1)

- User registration (email, phone, password, optional full name)
- Login / logout / refresh via HTTP-only cookies
- CRUD for `fields` (farm parcels) with PostGIS polygons
- CORS configured for credentials (Vercel frontend)
- Health check endpoint
- Docker Compose for local development

## API overview

Base path: `/api/v1`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health + DB status |
| POST | `/auth/register` | Register (sets cookies) |
| POST | `/auth/login` | Login (sets cookies) |
| POST | `/auth/logout` | Clear cookies |
| POST | `/auth/refresh` | Rotate tokens |
| GET | `/auth/me` | Current user |
| GET | `/fields` | List my parcels |
| POST | `/fields` | Create parcel |
| GET | `/fields/{id}` | Get one parcel |
| PATCH | `/fields/{id}` | Update parcel |
| DELETE | `/fields/{id}` | Delete parcel |

Interactive docs: `http://localhost:8000/docs`

## Local development

```bash
# 1. Copy env
cp .env.example .env
# Edit SECRET_KEY and CORS_ORIGINS (add your Vercel URL)

# 2. Start PostGIS + API
docker compose up --build

# 3. API is at http://localhost:8000
```

Without Docker (API only, Postgres already running):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Set DATABASE_URL in .env to your local PostGIS
uvicorn app.main:app --reload
```

## Auth cookies

| Cookie | Purpose | Default lifetime |
|--------|---------|------------------|
| `ft_access` | Access token | 30 minutes |
| `ft_refresh` | Refresh token | 14 days |

Flags (configurable via env):

- `HttpOnly` always
- `Secure` — set `COOKIE_SECURE=true` in production
- `SameSite` — use `none` when frontend (Vercel) and backend (Render) are on different sites
- `Domain` — leave empty for host-only cookies

For Vercel ↔ Render you will typically need:

```
COOKIE_SECURE=true
COOKIE_SAMESITE=none
CORS_ORIGINS=https://your-app.vercel.app
```

## Workflow

1. Topic branches for each unit of work
2. Merge into `dev`
3. Open Pull Request `dev` → `main` for review

## Frontend

- Repo: https://github.com/mburumanasseh/Farm_track_app_faith
- Deployed on Vercel

## License

Private / to be determined.
