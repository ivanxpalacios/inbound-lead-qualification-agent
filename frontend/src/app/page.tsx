import type { ReactElement } from 'react';

// Placeholder until the forms and the dashboard exist.
export default function Home(): ReactElement {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center gap-4 px-6 py-24">
      <p className="font-mono text-sm text-zinc-500">F0 · scaffold</p>
      <h1 className="text-3xl font-semibold tracking-tight">Inbound Lead Qualification</h1>
      <p className="text-lg leading-8 text-zinc-600 dark:text-zinc-400">
        An agent that researches inbound B2B leads, scores them and drafts the next step. A human
        approves every action. The forms and the dashboard will live here.
      </p>
    </main>
  );
}
