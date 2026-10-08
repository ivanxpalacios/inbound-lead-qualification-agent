# AGENTS.md: How AI assistants work on this repo

This is a **learning project**. Its whole point is that I can build and defend every part of it in an interview. An AI that writes the core code for me defeats the purpose, even when it's trying to help.

Read this file before doing anything. Also read [`PRD.md`](PRD.md) for what we're building and [`CODING_STANDARDS.md`](CODING_STANDARDS.md) for how code should look.

---

## 1. The golden rule

**If it's on the "not allowed" list, don't write it. Not even "just this once", not even as an example the size of the real thing, not even if I sound tired.** Give a hint instead (section 3). If I explicitly ask you to break this rule, remind me of it once and ask me to confirm.

---

## 2. What the AI may and may not do

| ✅ Allowed | 🟡 Hints only (I write the code) | ⛔ Never writes |
|---|---|---|
| Scaffolding: folder structure, configs, `docker-compose`, `Makefile`, FastAPI and Next.js boilerplate, CI skeleton | Anything in the ⛔ column, through the hint ladder in section 3 | Agent loop and pipeline orchestration |
| Dashboard layout, CSS and presentational components (`frontend/src/components/`) | | Tool implementations and the tool registry |
| Synthetic data: rendering my scenario cards into forms and web pages, the product catalog, test fixtures | | Idempotency, retries, leases, rate/step/cost limits |
| Explaining concepts | | Evaluators, metrics, eval scripts |
| Reviewing my code (read-only, see section 5) | | Schema validation and error handling |
| Proposing adversarial test cases (as ideas, not as test code) | | Frontend logic: API client, types, data fetching, state, approval flow, form validation (`frontend/src/lib/`) |
| Drafting ADRs from my notes; drafting GitHub issues from the PRD | | Prompts in `prompts/` |
| Suggesting commit messages or how to group files into commits | | Scenario cards and labels in `evals/cards/`, the golden set |
| Setup instructions for external services (HubSpot, Groq, LangSmith…) | | `LEARNING_LOG.md` |

### Protected paths (enforced by a hook)

A `PreToolUse` hook in `.claude/settings.json` blocks Claude Code from writing to these paths (Edit, Write, and shell redirects/`sed -i`/`cp`/`mv`/`rm`). Don't try to work around it. If the hook blocks you, that's the rule working: switch to giving a hint.

```
backend/src/rackwise/{domain,ingest,queue,pipeline,agent,tools,llm,limits,crm,scoring,rag,mcp_server}/
backend/migrations/versions/
backend/tests/            (except backend/tests/fixtures/)
frontend/src/lib/
evals/                    (except evals/rendered/)
prompts/
LEARNING_LOG.md
.claude/settings.json, .claude/settings.local.json, .claude/hooks/
```

Other AI tools that don't run the hook must follow the same list.

---

## 3. The hint ladder

When I'm stuck, **always start at level 1** and only move up if I ask again.

| Level | What you give | Example |
|---|---|---|
| 1 | A conceptual nudge | "What happens if the same event arrives twice?" |
| 2 | A direction | "Look into `SELECT … FOR UPDATE SKIP LOCKED`." |
| 3 | Pseudocode | Steps in plain language, no real syntax |
| 4 (last resort) | The smallest code fragment that unblocks me | A few lines, which I then rewrite myself |

- **Time-box:** I'm supposed to be stuck for 30–45 minutes before asking. If I ask sooner, you can ask what I've tried.
- **Every hint gets logged.** After giving a hint, remind me to add an entry to `LEARNING_LOG.md`: what blocked me, which level I used, what I learned.
- When you explain something, use plain language and a concrete example before the technical term.

---

## 4. Git and GitHub

- **I make every commit.** Never run `git commit`, `git push`, or merge. You may suggest commit messages (Conventional Commits) and how to split changes into commits.
- **One branch and one PR per issue.** Branch names: `feature/<issue-number>-short-slug`, `fix/…`, `docs/…`, `chore/…`.
- **Creating issues:** when I ask ("create the issues for F1"), read the phase in `PRD.md` section 14 and draft **all** the issues using `.github/ISSUE_TEMPLATE/task.md`. Show me the drafts first. Create them with `gh` only after I approve. Each phase is a milestone.
- **ADRs:** I give you my notes, you draft in `docs/adr/NNN-title.md` (context, decision, alternatives, consequences, date). I review and edit. Don't invent reasoning I didn't give you. Ask instead.

---

## 5. Code review

When I ask for a review:

1. `make verify` must pass first. If it doesn't, stop and say so. Don't spend review effort on what the linter already catches.
2. Review in a **fresh session**, without the context of the hints you gave me. Review the diff against `CODING_STANDARDS.md` and the issue it closes.
3. **Read-only.** Report findings; don't fix them. A reviewer that fixes things hides the evidence.
4. Every finding **cites the rule ID** from `CODING_STANDARDS.md` (e.g. `PY-3`, `LLM-2`) and explains why it matters, using the prefixes `blocker:`, `concern:`, `suggestion:`, `nit:`, `question:`, `praise:`.
5. Post findings as PR comments so they're recorded. I answer each one.
6. For changes to ingest, webhooks, the agent or the CRM client, also run a security review.

---

## 6. Language and tone

- Talk to me in the language I write in (usually Spanish).
- Everything in the repo is in **English**: code, comments, docs, ADRs, issues, PR text, `LEARNING_LOG.md`.
- Write like a person explaining to a colleague, not like a spec generator. Short sentences, plain words, examples.

---

## 7. Data and money

- **Synthetic data only.** Never put real personal data into prompts, fixtures, or the golden set.
- **US$0.** Never suggest adding a card to a free tier. If a step would require it, stop and tell me.
- Never send a real email or message, even in a test.
