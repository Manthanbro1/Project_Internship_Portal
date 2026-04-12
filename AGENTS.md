# Project Agent Instructions

## Preferred Skills For This Repo

Use these skills when working on the frontend in this project:

1. `frontend-design`
   Use for any HTML, CSS, JavaScript, page redesign, layout, styling, component polish, or visual UX work.

2. `webapp-testing`
   Use after frontend changes when browser-level verification, UI debugging, screenshots, or interaction testing are needed.

3. `theme-factory`
   Use only when the task explicitly asks for applying or generating a theme across pages.

## Frontend Standard

This repository uses a static frontend in `frontend/` with plain HTML, CSS, and JavaScript.

When editing frontend code:
- preserve the existing multi-page structure unless the task asks for a larger rewrite
- keep API integration aligned with the FastAPI backend in `backend/app`
- favor clear, production-leaning UI over placeholder styling
- avoid generic default aesthetics; use a deliberate visual direction
- verify that pages work on both desktop and mobile

## Execution Order

For frontend tasks in this repo, default to:
1. `frontend-design`
2. `webapp-testing` if verification is needed

## Notes

The `frontend-design` skill is already available in this environment as a preinstalled system skill, so it does not need to be installed into the repository.
