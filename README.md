# FarmTrack Backend

FastAPI + PostgreSQL (PostGIS) backend for the FarmTrack farm parcel mapping application.

## Status

Bootstrap phase. See `.trackers/` for current task state.

## Stack (planned)

- **FastAPI** – API framework
- **PostgreSQL + PostGIS** – spatial data store
- **SQLModel / SQLAlchemy 2** + **Alembic** – ORM & migrations
- **JWT in HTTP-only cookies** – authentication
- **Docker / Docker Compose** – local development
- **Render** – planned production deployment

## Frontend

- Repository: https://github.com/mburumanasseh/Farm_track_app_faith
- Deployed on Vercel

## Development workflow

1. All work happens on topic branches.
2. Topic branches are merged into `dev`.
3. `dev` is promoted to `main` via Pull Request for review.

## Local setup (coming soon)

```bash
# After Phase 1 lands
cp .env.example .env
docker compose up --build
```

## License

Private / to be determined.
