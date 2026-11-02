# Rollback

**Previous known-good commit:** 7efadbc (test .gitkeep only)  
**Previous release/tag:** none  

## Recovery notes

- This bootstrap only adds documentation and tracking files. No runtime code or database.
- To abandon: revert the merge commit of this PR on `main`.
- After Phase 1: document migration rollback and database restore procedures here.
