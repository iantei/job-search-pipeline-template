# Digest — EXAMPLE (delete this file after your first real run)

This file exists to show the exact structure `dashboard/build.py` parses.
It will appear in your dashboard as two sample cards until you delete it.

The parser is strict about four things:

1. `## Heading` becomes a **cluster** (the shelf a card sits on).
2. `### Company — Role` becomes a **posting**. The separator must be an em
   dash surrounded by spaces (` — `), or the whole heading is read as the
   company with no role.
3. The **line immediately below** the heading is the meta line. Pieces are
   separated by ` · `. A `[posting](url)` link and a `[resume](path)` link are
   recognized by their label text; anything containing `$` is read as salary,
   and the first remaining piece is read as location.
4. `**Fit:** strong|moderate|stretch` on its own line sets the badge. Without
   it the build falls back to guessing from prose, which is unreliable —
   always write the marker.

Everything between the meta line and the next heading becomes the card body.

## Developer Tooling — Batch 1

### Acme Corp — Senior Backend Engineer
Remote (US) · $180K–$220K · [posting](https://example.com/jobs/123) · [resume](../resumes/applied/Your_Name_Resume_Acme_Senior-Backend-Engineer.pdf)

**Fit:** strong

Two or three honest sentences on why this matches. Name the specific
requirements that line up with real entries in `master-profile.md`, rather
than asserting a general fit.

**Gaps:** the requirements you don't meet, stated plainly. This section is the
point of the whole digest — it's what stops a drafted resume from overselling,
and it's what you'll want in front of you before a screen.

### Globex — Platform Engineer
New York, NY (hybrid) · [posting](https://example.com/jobs/456)

**Fit:** stretch

A posting tracked but **not drafted** — note that this entry has no resume
link. The dashboard still shows it, marked "no resume yet," so you keep a
record of what you saw and decided against without generating a file for it.

**Gaps:** why you skipped it.

---

## Checked, no resume drafted

Anything dropped by a hard filter from `master-profile.md` goes here with its
reason, so the filtering is visible rather than silent:

- **Initech — Systems Engineer** — requires an active security clearance.
- **Umbrella Co — SRE** — "must be authorized to work without sponsorship."
