"""Inspect and manage affiliate links.

    python3 tools/affiliate.py --list          # every product's link state
    python3 tools/affiliate.py --audit         # check every link is well-formed
    python3 tools/affiliate.py <slug> <url>    # set a single-link product
    python3 tools/affiliate.py --clear <slug>

Products with a single program keep an `affiliateUrl` string. Programs that
issue a different affiliate id per campaign — GoHighLevel does — use an
`affiliateLinks` map keyed by destination instead, and are edited in
content/products.json directly so each entry keeps its campaign and id on
record. --audit is what protects that map.
"""

import json
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
TRACKING_PARAMS = ("fp_ref", "am_id", "ref", "aff", "via")


def load():
    return json.loads(PRODUCTS.read_text())


def save(data):
    PRODUCTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def show():
    data = load()
    width = max(len(p["slug"]) for p in data["products"])
    for p in data["products"]:
        flag = "$" if p["monetizable"] else " "
        if p.get("affiliateLinks"):
            ids = sorted({v.get("affiliateId") for v in p["affiliateLinks"].values()})
            print(f" {flag} {p['slug']:<{width}}  {len(p['affiliateLinks'])} routed "
                  f"destinations, ids: {', '.join(i for i in ids if i)}")
            for dest, entry in p["affiliateLinks"].items():
                print(f"     {dest:<14} {entry['url']}")
        else:
            state = p.get("affiliateUrl") or (
                "— not set —" if p["monetizable"] else "n/a (no program)")
            print(f" {flag} {p['slug']:<{width}}  {state}")


def audit():
    """Every failure here is one that would cost real money in silence."""
    data = load()
    problems = []

    for p in data["products"]:
        links = p.get("affiliateLinks") or {}
        single = p.get("affiliateUrl")
        entries = list(links.items())
        if single:
            entries.append(("default", {"url": single}))

        for dest, entry in entries:
            url = entry["url"]
            parsed = urllib.parse.urlparse(url)
            q = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

            if parsed.scheme != "https":
                problems.append(f"{p['slug']}/{dest}: not https — {url}")

            found = [k for k in TRACKING_PARAMS if k in q]
            if not found:
                problems.append(
                    f"{p['slug']}/{dest}: no tracking parameter — this link earns "
                    f"nothing: {url}")
            for k in found:
                if not any(v.strip() for v in q[k]):
                    problems.append(
                        f"{p['slug']}/{dest}: {k}= is EMPTY, tracks nothing — {url}")

            if " " in url or url != url.strip():
                problems.append(f"{p['slug']}/{dest}: whitespace in URL")

            declared = entry.get("affiliateId")
            if declared and declared not in url:
                problems.append(
                    f"{p['slug']}/{dest}: declared affiliateId {declared!r} does not "
                    f"appear in the URL — one of the two is wrong")

    # A program using several ids is legitimate but worth surfacing every run:
    # it is the single easiest thing to get quietly wrong.
    for p in data["products"]:
        links = p.get("affiliateLinks") or {}
        ids = {v.get("affiliateId") for v in links.values() if v.get("affiliateId")}
        if len(ids) > 1:
            print(f"note: {p['slug']} uses {len(ids)} affiliate ids across campaigns "
                  f"({', '.join(sorted(ids))}). Each destination must keep its own.")

    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for x in problems:
            print("  •", x)
        return 1
    total = sum(len(p.get("affiliateLinks") or {}) or bool(p.get("affiliateUrl"))
                for p in data["products"])
    print(f"PASS — {total} affiliate link(s) well-formed")
    return 0


def set_url(slug, url):
    data = load()
    for p in data["products"]:
        if p["slug"] != slug:
            continue
        if p.get("affiliateLinks"):
            print(f"{slug} uses a routed affiliateLinks map ("
                  f"{', '.join(sorted(p['affiliateLinks']))}).")
            print("Edit content/products.json directly so each destination keeps its "
                  "campaign and affiliate id, then run --audit.")
            return 1
        if not p["monetizable"] and url is not None:
            print(f"refusing: {slug} is marked monetizable:false — "
                  f"flip that flag first if the program really exists")
            return 1
        p["affiliateUrl"] = url
        save(data)
        print(f"{slug}.affiliateUrl = {url!r}")
        print("now run: python3 tools/affiliate.py --audit && python3 tools/build.py")
        return 0
    print(f"unknown slug: {slug}")
    return 1


def main(argv):
    if not argv or argv[0] == "--list":
        show()
        return 0
    if argv[0] == "--audit":
        return audit()
    if argv[0] == "--clear":
        return set_url(argv[1], None) if len(argv) == 2 else (print(__doc__) or 1)
    if len(argv) != 2:
        print(__doc__)
        return 1
    slug, url = argv
    if not url.startswith("https://"):
        print("affiliate URL must start with https://")
        return 1
    return set_url(slug, url)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
