#!/usr/bin/env python3
"""Build a self-contained job-search dashboard from the pipeline's own files.

Parses every digest/*.md file plus resumes/applied/ and inlines the result as
JSON into dashboard/index.html (from dashboard/template.html). No network, no
git, no dependencies beyond the Python 3 standard library.

Run it whenever new digests land:  python3 dashboard/build.py
Or just use dashboard/open.sh, which builds and opens the page.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ---- CONFIGURE ME ----------------------------------------------------------
# The prefix your tailored resumes are named with, e.g. a file called
# "Jane_Doe_Resume_Acme_Backend-Engineer.pdf" means RESUME_PREFIX = "Jane_Doe_Resume_".
# Only used to recover company/role from resumes that no digest documents.
RESUME_PREFIX = "Your_Name_Resume_"
# ----------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
DIGEST_DIR = REPO / "digest"
APPLIED_DIR = REPO / "resumes" / "applied"
TEMPLATE = Path(__file__).resolve().parent / "template.html"
OUTPUT = Path(__file__).resolve().parent / "index.html"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FIT_RE = re.compile(r"^\s*\*\*Fit:\*\*\s*(strong|moderate|stretch)\s*$",
                    re.IGNORECASE | re.MULTILINE)
VALID_FITS = ("strong", "moderate", "stretch")


def extract_fit(body: str):
    """Read an explicit '**Fit:** strong|moderate|stretch' marker.

    Prose-sniffing is unreliable: a digest's *gap* section often quotes the
    posting's own requirements ("strong understanding of web frameworks"),
    which the keyword heuristic below would score as a strength and upgrade a
    moderate draft to 'strong'. An explicit marker is authoritative; the
    heuristic stays only as a fallback for digests written before markers.

    Returns (fit_or_None, body_without_marker).
    """
    m = FIT_RE.search(body)
    if not m:
        return None, body
    cleaned = (body[:m.start()] + body[m.end():]).strip()
    return m.group(1).lower(), cleaned


def strip_md_links(text: str) -> str:
    """Turn '[label](url)' into 'label' and drop leftover markdown emphasis."""
    text = LINK_RE.sub(r"\1", text)
    text = text.replace("**", "").replace("`", "")
    return text.strip()


def classify_fit(body: str) -> str:
    """Fallback: heuristically map a digest's prose to a fit level.

    Only used when a posting carries no explicit '**Fit:**' marker. Prefer the
    marker — see extract_fit() for why this heuristic misreads gap sections.
    """
    b = body.lower()
    # Explicit weakness signals win — a "strong domain overlap" that is still a
    # "real stretch" should read as a stretch, not a strong match.
    stretch_signals = [
        "poor fit", "weakest", "real stretch", "stretch application",
        "this is a stretch", "not core tech fit", "significant lifestyle",
        "should weigh carefully",
    ]
    strong_signals = [
        "strongest", "strong match", "genuine match", "genuinely strong",
        "good match", "strong domain overlap", "strong nyc", "strong ",
    ]
    moderate_signals = ["moderate fit", "partial match", "partial", "moderate"]
    # "quals met on paper, but with real gaps" reads as moderate, not unrated.
    qualified_signals = [
        "genuine", "comfortably met", "comfortably meets", "cleared on paper",
        "are all met", "all met", "clears the", "is comfortably", "met via",
    ]
    if any(s in b for s in stretch_signals):
        return "stretch"
    if any(s in b for s in strong_signals):
        return "strong"
    if any(s in b for s in moderate_signals):
        return "moderate"
    if any(s in b for s in qualified_signals):
        return "moderate"
    return "unknown"


def resume_rel_from_link(link: str) -> str:
    """Digest links are '../resumes/applied/x.pdf' (relative to digest/).
    The dashboard lives in dashboard/, which is also one level under the repo
    root, so the same '../resumes/...' form works there too."""
    link = link.strip()
    idx = link.find("resumes/")
    if idx == -1:
        return link
    return "../" + link[idx:]


def parse_meta_line(meta: str):
    """Pull posting URL, resume link, location and salary out of the line that
    follows a '### Company — Role' heading."""
    posting_url = ""
    resume_pdf = ""
    for label, url in LINK_RE.findall(meta):
        low = label.lower()
        if "posting" in low:
            posting_url = url.strip()
        elif "resume" in low:
            resume_pdf = resume_rel_from_link(url)
    plain = strip_md_links(meta)
    # meta pieces are separated by ' · '
    parts = [p.strip() for p in plain.split("·")]
    location = ""
    salary = ""
    for p in parts:
        if p.lower() in ("posting", "resume"):
            continue
        if "$" in p:
            salary = p
        elif not location and p:
            location = p
    return posting_url, resume_pdf, location, salary


def parse_digest(path: Path):
    """Yield one posting dict per '### heading' that has a resume link."""
    date = path.stem  # YYYY-MM-DD
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    cluster = ""
    postings = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and not line.startswith("### "):
            cluster = line[3:].strip()
            i += 1
            continue
        if line.startswith("### "):
            heading = line[4:].strip()
            # meta line = first non-empty line(s) after the heading, up to blank
            j = i + 1
            meta_parts = []
            while j < len(lines) and lines[j].strip() != "":
                meta_parts.append(lines[j].strip())
                j += 1
            meta = " ".join(meta_parts)
            # body = everything until the next heading / hr
            k = j
            body_parts = []
            while k < len(lines):
                nxt = lines[k]
                if nxt.startswith("### ") or (
                    nxt.startswith("## ") and not nxt.startswith("### ")
                ) or nxt.strip() == "---":
                    break
                body_parts.append(nxt)
                k += 1
            body = "\n".join(body_parts).strip()

            fit, body = extract_fit(body)
            if fit is None:
                fit = classify_fit(body)

            posting_url, resume_pdf, location, salary = parse_meta_line(meta)

            if resume_pdf or posting_url:  # drafted OR tracked-but-not-drafted
                if " — " in heading:
                    company, role = heading.split(" — ", 1)
                else:
                    company, role = heading, ""
                postings.append({
                    "id": posting_url or resume_pdf,
                    "date": date,
                    "cluster": cluster,
                    "company": company.strip(),
                    "role": role.strip(),
                    "location": location,
                    "salary": salary,
                    "posting_url": posting_url,
                    "resume_pdf": resume_pdf,
                    "fit": fit,
                    "body": strip_md_links(body),
                })
            i = k
            continue
        i += 1
    return postings


def find_orphan_resumes(seen_pdfs):
    """Applied resumes that no digest documents — surface them so nothing is
    lost from the catalog."""
    orphans = []
    if not APPLIED_DIR.exists():
        return orphans
    seen_names = {Path(p).name for p in seen_pdfs}
    for pdf in sorted(APPLIED_DIR.glob("*.pdf")):
        if pdf.name in seen_names:
            continue
        # Convention: <RESUME_PREFIX><Company>_<Role>  (see top of file)
        m = re.match(rf"^{re.escape(RESUME_PREFIX)}([^_]+)_(.+)$", pdf.stem)
        if m:
            date, company, role_slug = "", m.group(1), m.group(2)
        else:  # fallback: YYYY-MM-DD_company_role-slug
            m2 = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_(.+)", pdf.stem)
            if m2:
                date, company, role_slug = m2.groups()
            else:
                date, company, role_slug = "", pdf.stem, ""
        orphans.append({
            "id": pdf.name,
            "date": date,
            "cluster": "Uncategorized (no digest entry)",
            "company": company.replace("-", " "),
            "role": role_slug.replace("-", " "),
            "location": "",
            "salary": "",
            "posting_url": "",
            "resume_pdf": "../resumes/applied/" + pdf.name,
            "fit": "unknown",
            "body": "No digest entry parsed for this resume draft.",
        })
    return orphans


def main():
    if not DIGEST_DIR.exists():
        print(f"No digest directory at {DIGEST_DIR}", file=sys.stderr)
        sys.exit(1)

    postings = []
    for digest in sorted(DIGEST_DIR.glob("*.md")):
        postings.extend(parse_digest(digest))

    seen_pdfs = [p["resume_pdf"] for p in postings]
    postings.extend(find_orphan_resumes(seen_pdfs))

    # Dedup by id (posting URL). When the same role appears twice — once
    # tracked-but-not-drafted, once with a drafted resume — keep the resume one.
    deduped = {}
    for p in postings:
        existing = deduped.get(p["id"])
        if existing is None or (not existing["resume_pdf"] and p["resume_pdf"]):
            deduped[p["id"]] = p
    postings = list(deduped.values())

    # Newest digest first. Without this, postings render in digest-filename
    # order (oldest first), so the most recent finds land at the bottom of an
    # 80-card column and the newest cluster sits last on the catalog page —
    # exactly backwards. Orphan resumes carry no date, so they sort last.
    postings.sort(key=lambda p: (p["date"] != "", p["date"]), reverse=True)

    data = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "postings": postings,
    }

    template = TEMPLATE.read_text(encoding="utf-8")
    html = template.replace(
        "/*__DATA__*/", json.dumps(data, ensure_ascii=False)
    )
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(REPO)} — {len(postings)} postings "
          f"from {len(list(DIGEST_DIR.glob('*.md')))} digest(s).")


if __name__ == "__main__":
    main()
