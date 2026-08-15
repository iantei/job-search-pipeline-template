# Job Search Pipeline

A private, local job-search tracker driven by Claude Code. You keep a list of
target companies and a file of verified facts about yourself; an agent checks
those companies for new postings, drafts a tailored one-page resume for each
genuine match, and writes a dated digest with an honest fit assessment. A
self-contained HTML dashboard renders the whole thing.

No server, no database, no third-party service. Everything is files in this
repo, and the dashboard is a pure function of them.

## Setup (about 20 minutes)

**1. Requirements**

- Python 3 (standard library only — nothing to install)
- [Claude Code](https://claude.com/claude-code)
- `tectonic` for compiling LaTeX resumes — `brew install tectonic`, or your
  platform's equivalent

**2. Make the repo private**

It will hold your resumes, your contact details, your salary targets, and
blunt written assessments of your own weaknesses. Keep it private.

```
git init && git add -A && git commit -m "Initial pipeline"
gh repo create job-search-pipeline --private --source=. --push
```

**3. Fill in `master-profile.md`** — the most important step

This is the only source of truth the agent may draw on. Everything else is
machinery. Three sections do specific work:

- **Targeting** — the role families to look for, so the agent doesn't
  force-fit unrelated jobs
- **Hard filters** — what disqualifies a posting outright (work
  authorization, clearance, location, comp floor). Enforced on every run,
  with anything dropped recorded in the digest and its reason
- **Explicit Gaps** — what you must *not* claim. This is the guardrail that
  stops drafts from inventing plausible-sounding qualifications

Be specific and attach numbers. Vague inputs produce vague resumes.

**4. Fill in `companies.md`** — target companies grouped into clusters. The
clusters become the shelves in the dashboard's catalog view.

**5. Set your resume naming prefix** — open `dashboard/build.py` and set
`RESUME_PREFIX` at the top, e.g. `"Jane_Doe_Resume_"`. That prefix is what a
recruiter sees on the PDF attachment.

**6. Personalize the base resume** — edit `resumes/base/general.tex`. The
pipeline reuses its preamble and macros for every tailored draft. Add more
variants (`ios-focused.tex`, `data-focused.tex`) as you find you need them.

**7. Delete `digest/EXAMPLE.md`** once you've read it — it documents the exact
format the dashboard parses, then becomes clutter.

## Running it

From inside the repo:

```
claude
> /job-search-check
```

It pulls, reads your two config files, checks each company's careers page,
applies your hard filters, drafts resumes for genuine matches, writes
`digest/YYYY-MM-DD.md`, updates `seen-postings.json` so nothing resurfaces,
and commits.

Then:

```
./dashboard/open.sh      # rebuild + open
```

## The dashboard

`dashboard/index.html` is generated from `digest/*.md` and `resumes/applied/`.
It's gitignored — delete it any time and rebuild.

- **Board** — Kanban across seven stages, drag-and-drop
- **Catalog** — every posting shelved by cluster, with fit badges and a
  click-through to its tailored resume

Your stage tracking lives in the browser's localStorage, keyed separately from
the generated data — so rebuilding never wipes your progress. Use
Export/Import to move it between machines.

## Review before you send

Every file in `resumes/applied/` is a **draft**. The agent is instructed to
tailor emphasis but never to claim beyond `master-profile.md`, and to flag
gaps rather than paper over them. Read the digest's gap section before you
apply — it's the most useful thing in the repo, and it's also your interview
prep for that specific role.

The agent will not submit applications on your behalf.

## Known gaps

- The dashboard is a local file. Viewing it on a phone needs a LAN server
  (`python3 -m http.server`), a tunnel, or a host with real auth in front —
  don't put it on public GitHub Pages, which has no access control outside
  Enterprise Cloud.
