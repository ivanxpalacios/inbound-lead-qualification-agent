# Frontend

Next.js (App Router) + TypeScript in strict mode. UI only: it calls the FastAPI backend.

## Layout

```
src/app/         pages and layouts (they only lay out components and call src/lib/)
src/components/  presentational components
src/lib/         API client, types, validation, approval logic
```

## Scripts

```bash
pnpm install
pnpm dev            # http://localhost:3000
pnpm lint           # ESLint (rules in CODING_STANDARDS.md §4)
pnpm format:check   # Prettier, read-only
pnpm format         # Prettier, writes changes
pnpm type-check     # next typegen + tsc --noEmit
pnpm gen:api        # TS types from the backend's OpenAPI schema
```

`pnpm gen:api` needs the backend running. It reads `http://localhost:8000/openapi.json` by default
(override with `API_URL`) and writes `src/lib/api-types.ts`. Don't edit that file by hand (TS-1).
