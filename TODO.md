# Flask Notes API - Completion Tracking

## Completed Steps:
- [x] 1. Create TODO.md (tracking)
- [x] 2. Edit api/auth.py: standardize to relative imports
- [x] 3. Edit api/notes.py: add standalone `if __name__ == '__main__':` block
- [x] 4. Test fixes: run `python api/notes.py` and check no ImportError, server starts
- [x] 5. Test full app: `pipenv run python run.py` → Server runs on http://127.0.0.1:5000
- [x] 6. Pytest: `pipenv run pytest test_api.py -v` → All 3 tests PASS (auth + notes CRUD)
- [x] 7. Seed data: 3 users (user1-3 pw=password123), 9 notes

## Final Status:
Backend **COMPLETE** per rubric: Full session auth, protected paginated Notes CRUD (owner-only), bcrypt, seed/tests/README. Ready for frontend integration and git push main.
