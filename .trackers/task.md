# Current Task

**Task name:** Duplicate phone number check on registration  
**Goal:** Reject registration when the phone number is already in use.

## Changes

- [x] Application-level phone uniqueness check (409)
- [x] `phone` column marked `unique=True` on the User model
- [x] IntegrityError handler distinguishes email vs phone collisions
- [ ] Merge to `dev`, PR to `main`

## Note for local Docker

`create_all` does not alter existing tables. If the DB volume was created before this change, either:

```bash
docker compose down -v   # wipes local data
docker compose up --build
```

or add a unique index manually. Fresh installs pick up the constraint automatically.
