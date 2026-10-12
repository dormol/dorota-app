# ART MENTOR STUDIO
## by Dorota Mol @Molgallery

# Project Progress and Technical Checkpoints

This document records confirmed development milestones, tests, GitHub checkpoints, open issues, and the next planned actions. It supplements the Design Bible and Git history; it does not replace either.

## 10/11/26 — Portrait / Face: Intermediate and Advanced

### Work completed
- Added exercise entries for Intermediate and Advanced levels.
- Covered four portrait views: front, three-quarter, profile, and comparative.
- Added level-specific guidance concerning structure, proportions, perspective, anatomy, and form.
- Updated the form to preserve the selected level, view, and entered subject.
- Escaped the entered subject before displaying it in HTML.

### Verification
- Python syntax check: passed.
- `git diff --check`: passed.
- Twelve level/view combinations tested: 12/12 passed.
- HTML escaping test for entered subject: passed.
- These tests cover the tested portrait routes and form behavior; they do not establish that every application module is fully tested.

### GitHub checkpoint
- Backup commit: `93003d3` — Backup before portrait level and form fixes 10/11/26
- Implementation commit: `fe1bf2b` — Complete portrait exercises for Intermediate and Advanced
- Remote branch: `origin/main`
- Confirmed local and remote commit: `fe1bf2bb83f2e5bc8a04cd5afe3a61739d90f236`
- Working tree was clean after the push.

### Important limitations and open work
1. Intermediate and Advanced exercises currently build on the Beginner exercise structures with additional level-specific guidance. Review whether the teaching tasks are sufficiently distinct for each level.
2. Mentor Voice text is displayed, but actual audio playback has not been verified by these tests.
3. Test the remaining application modules and their main user flows.
4. Review local files not tracked by Git before deciding whether any are important project assets that should be preserved in the repository.
5. Review the nested `voice_ai_app` application and its assets separately before changing or reorganizing them.

## Repository Preservation Policy

- Preserve important project decisions, documentation, source code, and meaningful recovery copies in GitHub.
- Before substantial code changes, create a clearly named backup checkpoint when appropriate.
- After changes, run relevant tests, inspect the diff, commit the work, push to `origin/main`, and verify synchronization.
- Do not commit virtual environments, compiled Python files, editor swap files, or other temporary artifacts without a specific reason.
- Do not delete or overwrite existing project material without reviewing its purpose and preserving any valuable content.
- Keep the Design Bible, project vision, technical implementation, and progress log as separate complementary records.

## Next checkpoint
Continue the repository inventory. Assess important local files that are not tracked by Git, then verify the relevant application modules and update this log after each meaningful milestone.
