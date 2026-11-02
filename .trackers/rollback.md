# Rollback

**Previous known-good commit:** e94532d (merge of bootstrap PR #1)  
**Previous release/tag:** none  

## Recovery notes

- This Phase 1 introduces the full application code but no production database yet.
- To roll back before any Render deploy: revert the merge commit of the Phase 1 PR on `main` / `dev`.
- After a production database exists: document `alembic downgrade` steps and backup restore here.
