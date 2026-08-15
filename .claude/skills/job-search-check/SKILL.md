---
name: job-search-check
description: Run the job search pipeline - checks companies.md for new postings, drafts tailored resumes strictly from master-profile.md, writes a dated digest, and commits. Use when the user wants to trigger a check on demand.
---

Run the full job search pipeline in this repository.

## Steps

1. `git pull` first, in case another run has pushed updates since the last sync.
2. Read `companies.md` for the current target list (grouped by cluster).
   Re-read it fresh every run — it may have been hand-edited.
3. Read `master-profile.md` carefully. **This is the only source of truth**
   for the user's experience, skills, and accomplishments. It contains:
   - a **Targeting** section describing the kinds of roles that fit
   - a **Hard filters** section listing what disqualifies a posting outright
   - an **Explicit Gaps — do NOT claim these** section

   Never invent, infer, or add a qualification beyond what is written there,
   even when it seems highly likely given the employer or industry. If a
   posting calls for something not in the profile, record it as a gap in the
   digest rather than papering over it in the resume.
4. For each company, check their public careers page for postings matching the
   profile's **Targeting** section. Don't force-fit unrelated roles just
   because a company is on the list.
   - Apply every rule in the profile's **Hard filters** section. Drop a
     posting entirely — do not draft a resume — if it fails one. List anything
     dropped under the digest's "Checked, no resume drafted" section with the
     reason, so the filtering stays transparent rather than silent.
   - Many career sites (Workday, Ashby, Greenhouse) are JS-rendered and return
     nothing to a plain fetch. If a page comes back empty, fall back to a
     headless browser: check for `chromium-cli` or a local Playwright install,
     and if neither exists run
     `npm init -y --silent && npm install playwright --no-audit --no-fund && npx playwright install chromium`,
     then dump `page.innerText("body")`.
5. Read `seen-postings.json` (`{"seen": [...]}` of posting URLs) and act only
   on postings not already listed.
6. For each genuinely new, relevant posting:
   a. Assess fit honestly against `master-profile.md`, naming real gaps.
   b. Draft a tailored one-page resume in LaTeX, reusing the preamble and
      macros from a file in `resumes/base/`, pulling facts **only** from
      `master-profile.md`. Compile with `tectonic <file>.tex` (install via
      your package manager if missing). If it overflows one page, tighten the
      geometry margins slightly or cut a bullet — then read the compiled PDF
      back to confirm before finishing.
   c. Save both files under `resumes/applied/` following the naming
      convention set in `RESUME_PREFIX` at the top of `dashboard/build.py` —
      `<Prefix><Company>_<Role>.tex` and `.pdf`. Hyphenate words within
      Company and Role, keep acronyms in conventional casing (iOS, AWS, ML,
      SDE), and put no date in the filename. This is the name a recruiter sees
      on the attachment, so keep it clean.
7. Write one dated digest at `digest/YYYY-MM-DD.md`. The dashboard parses this
   file directly, so the structure matters — see `digest/EXAMPLE.md` for the
   exact format. Each posting needs a `### Company — Role` heading, a meta
   line carrying location · salary · posting link · resume link, and an
   explicit `**Fit:** strong|moderate|stretch` marker. If nothing new was
   found, still write a short digest saying so and which companies were checked.
8. Update `seen-postings.json` with the newly seen URLs (merge, don't remove).
9. `git add`, commit with a descriptive message, and push.
10. Rebuild the dashboard: `python3 dashboard/build.py`.

## Guardrails

- This produces **drafts** for the user to review before applying — never
  claim more than `master-profile.md` supports.
- Never submit a job application on the user's behalf under any circumstances.
  Draft resumes and write the digest only.
- If unsure whether a posting is a genuine fit, say so honestly in the digest
  rather than skipping it silently or overselling it.
