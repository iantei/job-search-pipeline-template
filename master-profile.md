# Master Profile — Verified Facts Only

This is the single source of truth for every resume the pipeline drafts.
**Only facts listed here may be used.** Do not infer, extrapolate, or add
industry-standard-sounding claims (specific compliance standards, tools,
certifications) that aren't written down — even when they seem highly likely
to be true given the employer or domain. If a posting calls for something not
listed here, it gets flagged as a gap in the digest, never papered over in the
resume.

> **Fill this file in before the first run.** Everything below is a scaffold.
> The more specific and honest it is, the better the drafts — vague inputs
> produce vague resumes. Numbers matter: "cut runtime 10 h → 30 min (95%)"
> beats "improved performance."

Contact: Your Name · City, State · phone · email · linkedin.com/in/you ·
github.com/you

## Targeting — what counts as a relevant posting

List the role families the pipeline should look for, so it doesn't force-fit
unrelated jobs just because a company is on the list.

- e.g. backend services and APIs
- e.g. data/ML infrastructure and pipelines
- e.g. developer tooling and CLIs

## Hard filters — drop a posting entirely if it fails one

Delete what doesn't apply to you; add what does. These are enforced by the
skill on every run, and anything dropped is recorded in the digest with its
reason.

- **Work authorization.** e.g. "Requires visa sponsorship — drop postings
  saying 'must be authorized to work without sponsorship'." *Or,* if you need
  no sponsorship, delete this bullet entirely.
- **Security clearance.** e.g. "Drop anything requiring a clearance or
  clearance eligibility (Secret / TS / TS-SCI / DoE Q or L), or ITAR /
  export-control authorization." Delete if not applicable.
- **Location.** e.g. "Remote or <metro> only" / "open to relocation within
  the US" / "no relocation."
- **Compensation floor.** e.g. "Skip anything posting below $X base."
- **Seniority.** e.g. "Skip roles requiring 10+ years or a PhD."

## Experience

**Job Title — Company — Location — Start–End**
- What you built, with the number attached. One bullet per accomplishment.
- Include the tradeoff you made or the constraint you worked under — that's
  what makes a bullet defensible in an interview.
- **Status caveats go here.** If something is still in review or unshipped,
  write "describe as work driven, not delivered" so no draft overstates it.

**Previous Job Title — Company — Location — Start–End**
- ...

## Leadership

- Mentoring, team lead roles, anything where the accomplishment was other
  people's output rather than your own code.

## Projects & Open Source

- **Project Name** (link) — what it does, the stack, and the hard part.
  Add a **Caveat — do not overstate:** line for anything half-finished, so
  drafts describe it accurately.
- **Open Source** — repo, contribution count, what specifically you shipped.
  Distinguish contributor from maintainer; they are not the same claim.

## Education

- Degree — Institution — Location — Date. GPA only if it helps you.

## Skills (verified only)

- **Languages:**
- **Data & Systems:**
- **Cloud & DevOps:**
- **Domain-specific:**
- **Practices:**

## Awards & Publications

- Award, year, and what it was for.
- Publications in a consistent citation format.

## Explicit Gaps — do NOT claim these

Confirmed **not** to have production or professional experience with:

- (list the technologies people will assume you know but you don't)
- (list anything you touched once in training but can't defend in a screen)

If a posting requires one of these, the digest flags it as a gap. It never
gets papered over in the drafted resume.
