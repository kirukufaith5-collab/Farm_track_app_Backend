# Current Task

**Task name:** Harden duplicate email registration check  
**Goal:** Ensure registration rejects duplicate emails reliably (case-insensitive + race-safe).

## Approved scope

- [x] Normalize email to lowercase before lookup and insert
- [x] Return 409 Conflict with clear message
- [x] Catch IntegrityError on commit for concurrent registrations
- [ ] Merge to `dev`, PR to `main`

## Explicitly out of scope

- Duplicate phone checks
- Frontend changes
