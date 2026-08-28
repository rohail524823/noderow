"""Build the site into deploy/.

    python3 tools/build.py

Generates every page, the tool directory, sitemap.xml, rss.xml, llms.txt and
robots.txt, then runs the validate_page() gate. Nothing is written if the gate
fails, so deploy/ never holds a page that would not pass review.
"""

import html as html_mod
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import components  # noqa: E402
import entity  # noqa: E402
import head as head_mod  # noqa: E402
import calculator_page  # noqa: E402
import pricing_page  # noqa: E402
import pages as pages_mod  # noqa: E402
from site_config import SITE_NAME, SITE_URL  # noqa: E402
from validate import validate_page  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEPLOY = ROOT / "deploy"
BUILD_DATE = pages_mod.TODAY


def tool_cards():
    """Render the /tools/ directory from products.json."""
    by_cat = {}
    for p in components._PRODUCTS:
        by_cat.setdefault(p["category"], []).append(p)

    out = []
    for cat in sorted(by_cat):
        out.append(f'<h2 class="tool-cat">{html_mod.escape(cat)}</h2>')
        out.append('<div class="node-grid">')
        for p in by_cat[cat]:
            if p["monetizable"]:
                pill = components.status_pill("ok", "Pays commission")
            else:
                pill = components.status_pill("idle", "No commission")
            link = components.outbound(p["slug"], f"Visit {p['name']}",
                                       placement="tool-directory")
            out.append(f"""<article class="node">
<div class="node-head"><span class="node-kicker">{html_mod.escape(p['vendor'])}</span>
{pill}</div>
<h3>{html_mod.escape(p['name'])}</h3>
<p><strong>Best for:</strong> {html_mod.escape(p['bestFor'])}</p>
<p><strong>Weakness:</strong> {html_mod.escape(p['weakness'])}</p>
<p class="node-chain">{html_mod.escape(p['commissionNote'])}</p>
<p>{link}</p>
</article>""")
        out.append("</div>")
    return "\n".join(out)


def render_page(page):
    path = page["path"]
    body = page["body"]

    if page.get("tool_directory"):
        body = body.replace('<div id="tool-cards" class="node-grid"></div>',
                            tool_cards())

    schema_nodes = [
        entity.organization(),
        entity.person(),
        entity.website(),
        entity.breadcrumbs(page["trail"]),
        entity.webpage(path, page["title"], page["description"],
                       last_reviewed=BUILD_DATE),
    ]
    schema_nodes += page.get("extra_schema", [])
    schema = entity.graph(*schema_nodes)

    head = head_mod.render(
        path=path,
        title=page["title"],
        description=page["description"],
        schema=schema,
        robots=page.get("robots",
                        "index,follow,max-snippet:-1,max-image-preview:large,"
                        "max-video-preview:-1"),
    )

    active = path if any(path == p for _, p in __import__("site_config").NAV) else None
    scripts = "\n".join(
        f'<script src="{src}" defer></script>' for src in page.get("scripts", [])
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body>
{components.header(active=active)}
<main id="main">
{body}
</main>
{components.footer()}
{components.ANALYTICS_JS}
{scripts}
</body>
</html>
"""


def write(rel_path, content):
    dest = DEPLOY / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return dest


def page_file(path):
    if path == "/":
        return "index.html"
    return path.strip("/") + "/index.html"


def build_sitemap(pages):
    urls = "\n".join(
        f"""  <url>
    <loc>{SITE_URL}{p['path']}</loc>
    <lastmod>{BUILD_DATE}</lastmod>
    <priority>{p.get('priority', '0.5')}</priority>
  </url>"""
        for p in pages
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def build_rss(pages):
    items = "\n".join(
        f"""    <item>
      <title>{html_mod.escape(p['title'])}</title>
      <link>{SITE_URL}{p['path']}</link>
      <guid>{SITE_URL}{p['path']}</guid>
      <description>{html_mod.escape(p['description'])}</description>
    </item>"""
        for p in pages
        if p["path"] not in ("/privacy-policy/", "/contact/")
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{SITE_NAME}</title>
    <link>{SITE_URL}/</link>
    <description>Comparisons and build guides for agency automation stacks.</description>
    <language>en</language>
{items}
  </channel>
</rss>
"""


def build_llms(pages):
    lines = [
        f"# {SITE_NAME}",
        "",
        "> Comparisons and build guides for agency automation stacks — GoHighLevel,",
        "> n8n, Make and Zapier. Written by a freelance automation engineer who builds",
        "> these systems for paying clients.",
        "",
        "## Pages",
        "",
    ]
    for p in pages:
        lines.append(f"- [{p['title']}]({SITE_URL}{p['path']}): {p['description']}")
    return "\n".join(lines) + "\n"


AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User",
    "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
    "Google-Extended", "GoogleOther", "Applebot", "Applebot-Extended",
    "Amazonbot", "Bytespider", "CCBot", "cohere-ai", "Diffbot",
    "FacebookBot", "meta-externalagent", "YouBot", "Timpibot",
    "omgili", "ImagesiftBot",
]


def build_robots():
    blocks = "\n\n".join(
        f"User-agent: {ua}\nAllow: /" for ua in AI_CRAWLERS
    )
    return f"""# Every AI crawler is explicitly allowed. Citation is the point.
{blocks}

User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
Host: noderow.com
"""


def main():
    pages = pages_mod.all_pages()
    pages.append(calculator_page.build())
    pages.append(pricing_page.build())
    known = {p["path"] for p in pages}
    known.add("/")
    # Footer/nav entries for pages that do not exist yet render as parked links.
    components.set_published(known)

    rendered = {}
    errors = []
    for page in pages:
        html = render_page(page)
        rendered[page["path"]] = html
        errors += validate_page(page["path"], html, known_paths=known)

    not_found = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_mod.render(
    path="/404.html",
    title="Page Not Found | NodeRow",
    description=(
        "That page does not exist on NodeRow. It may have moved, or it may not be "
        "published yet. Browse the comparisons and build guides instead."
    ),
    schema=entity.graph(entity.organization(), entity.person(), entity.website()),
    robots="noindex,follow",
)}
</head>
<body>
{components.header()}
<main id="main">
{pages_mod.NOT_FOUND_BODY}
</main>
{components.footer()}
</body>
</html>
"""

    if errors:
        print(f"BUILD BLOCKED — {len(errors)} validation failure(s):")
        for e in errors:
            print("  •", e)
        return 1

    for path, html in rendered.items():
        write(page_file(path), html)
    write("404.html", not_found)
    write("sitemap.xml", build_sitemap(pages))
    write("rss.xml", build_rss(pages))
    write("llms.txt", build_llms(pages))
    write("robots.txt", build_robots())

    print(f"PASS — built {len(pages)} pages + 404, sitemap, rss, llms.txt, robots.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
