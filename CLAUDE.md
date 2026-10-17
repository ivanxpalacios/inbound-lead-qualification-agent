@AGENTS.md

## Claude Code specifics

- The protected-paths hook lives in `.claude/hooks/protect_core_paths.py`. If it blocks a write, switch to the hint ladder. Never edit the hook or the settings to get around it.
- The plan is in `PRD.md`. The coding rules are in `CODING_STANDARDS.md`.
- `BRIEF.md` is the historical starting point. Don't update it.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `ivanxpalacios/inbound-lead-qualification-agent`, created with `gh`. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
