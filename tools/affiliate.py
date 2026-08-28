"""Swap a plain vendor URL for a real affiliate link, in one command.

    python3 tools/affiliate.py gohighlevel "https://www.gohighlevel.com/?fp_ref=YOURID"
    python3 tools/affiliate.py --clear gohighlevel
    python3 tools/affiliate.py --list

Writes affiliateUrl into content/products.json. Every page reads its outbound
URLs from that file, so a rebuild picks the new link up everywhere at once —
there is no URL hardcoded in any page to hunt down.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"


def load():
    return json.loads(PRODUCTS.read_text())


def save(data):
    PRODUCTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def show():
    data = load()
    width = max(len(p["slug"]) for p in data["products"])
    for p in data["products"]:
        state = p.get("affiliateUrl") or ("— not set —" if p["monetizable"]
                                          else "n/a (no program)")
        flag = "$" if p["monetizable"] else " "
        print(f" {flag} {p['slug']:<{width}}  {state}")


def set_url(slug, url):
    data = load()
    for p in data["products"]:
        if p["slug"] != slug:
            continue
        if not p["monetizable"] and url is not None:
            print(f"refusing: {slug} is marked monetizable:false — "
                  f"flip that flag first if the program really exists")
            return 1
        p["affiliateUrl"] = url
        save(data)
        print(f"{slug}.affiliateUrl = {url!r}")
        print("now run: python3 tools/build.py")
        return 0
    print(f"unknown slug: {slug}")
    return 1


def main(argv):
    if not argv or argv[0] == "--list":
        show()
        return 0
    if argv[0] == "--clear":
        if len(argv) != 2:
            print(__doc__)
            return 1
        return set_url(argv[1], None)
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
