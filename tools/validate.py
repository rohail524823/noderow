"""The publish gate. Nothing ships without passing every check here.

Run standalone to audit what is already in deploy/:
    python3 tools/validate.py
"""

import pathlib
import re
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEPLOY = _ROOT / "deploy"

# Assets that must resolve to a real file on disk.
_LOCAL_ASSET = re.compile(r'(?:href|src)="(/(?:css|js|img|fonts)/[^"#?]+)')
_INTERNAL_LINK = re.compile(r'href="(/[^"#?]*)"')


def validate_page(path, html, *, known_paths=None):
    """Return a list of failure strings. Empty list means the page may publish."""
    errors = []

    def fail(msg):
        errors.append(f"{path}: {msg}")

    # --- structural ---
    if "<!DOCTYPE html>" not in html:
        fail("missing doctype")
    if html.count("<h1") != 1:
        fail(f"expected exactly one <h1>, found {html.count('<h1')}")
    if "<title>" not in html:
        fail("missing <title>")
    if 'rel="canonical"' not in html:
        fail("missing canonical")
    if 'name="description"' not in html:
        fail("missing meta description")
    # Snippet directives only mean anything on an indexable page.
    indexable = 'content="noindex' not in html
    if indexable and "max-snippet:-1" not in html:
        fail("missing max-snippet:-1 in robots meta")
    if indexable and 'rel="canonical"' in html:
        canon = re.search(r'rel="canonical" href="([^"]+)"', html)
        if canon and not canon.group(1).startswith("https://"):
            fail("canonical is not absolute")
    if 'lang="en"' not in html:
        fail("missing lang attribute")

    # --- description length (B2: 140-160 chars) ---
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if m:
        n = len(m.group(1))
        if not 120 <= n <= 175:
            fail(f"meta description is {n} chars, want 120-175")

    # --- title length sanity ---
    m = re.search(r"<title>([^<]*)</title>", html)
    if m and len(m.group(1)) > 70:
        fail(f"title is {len(m.group(1))} chars, want <= 70")

    # --- schema ---
    if 'type="application/ld+json"' not in html:
        fail("missing JSON-LD")
    if "aggregateRating" in html:
        fail("aggregateRating present — spam-policy violation, never emit it")

    # --- affiliate link hygiene ---
    for tag in re.findall(r"<a\b[^>]*data-aff=[^>]*>", html):
        if "sponsored" not in tag or "nofollow" not in tag:
            # Only monetizable products carry data-aff, so this must be marked.
            if 'data-aff="zapier"' not in tag:
                fail(f"affiliate link missing rel=sponsored nofollow: {tag[:90]}")
        if "noopener" not in tag:
            fail(f"outbound link missing noopener: {tag[:90]}")

    # Any page with an affiliate link must carry the inline disclosure.
    if "out-aff" in html or 'class="btn btn-primary" href="http' in html:
        if "affiliate-link:" in html and 'class="disclosure"' not in html:
            fail("page has affiliate links but no inline disclosure block")

    # --- asset paths resolve ---
    for asset in set(_LOCAL_ASSET.findall(html)):
        if not (DEPLOY / asset.lstrip("/")).exists():
            fail(f"asset does not exist on disk: {asset}")

    # --- internal links point at pages we know about ---
    if known_paths is not None:
        for link in set(_INTERNAL_LINK.findall(html)):
            if not link.endswith("/"):
                continue
            if link not in known_paths:
                fail(f"internal link to unknown page: {link}")

    # --- trailing-slash discipline ---
    for link in set(_INTERNAL_LINK.findall(html)):
        if link != "/" and not link.endswith("/") and "." not in link.rsplit("/", 1)[-1]:
            fail(f"internal link missing trailing slash: {link}")

    return errors


def audit_deploy():
    files = sorted(DEPLOY.rglob("*.html"))
    if not files:
        print("no HTML in deploy/ — run tools/build.py first")
        return 1
    known = {"/"}
    for f in files:
        rel = "/" + str(f.relative_to(DEPLOY)).replace("index.html", "")
        known.add(rel if rel.endswith("/") else rel)
    all_errors = []
    for f in files:
        rel = "/" + str(f.relative_to(DEPLOY)).replace("index.html", "")
        all_errors += validate_page(rel, f.read_text(), known_paths=known)
    if all_errors:
        print(f"FAIL — {len(all_errors)} problem(s):")
        for e in all_errors:
            print("  •", e)
        return 1
    print(f"PASS — {len(files)} pages validated")
    return 0


if __name__ == "__main__":
    sys.exit(audit_deploy())
