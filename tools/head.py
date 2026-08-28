"""The ONE <head> generator.

Every page in the site gets its head from this module. Four diverging
generators is documented technical debt — there is exactly one here.
"""

from site_config import GA4_MEASUREMENT_ID, SITE_NAME, SITE_URL

# Fonts are self-hosted (tools/fetch_fonts.py). No third-party font request:
# nothing outside this origin can slow down, track, or break the page's text.
# Only the two faces used above the fold are preloaded; the rest swap in.
FONT_PRELOAD = "\n".join(
    f'<link rel="preload" href="/fonts/{f}" as="font" type="font/woff2" crossorigin>'
    for f in ("space-grotesk-700.woff2", "inter-400.woff2")
)

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%23111827'/%3E"
    "%3Cpath d='M9 22V10l14 12V10' stroke='%236366f1' stroke-width='2.6' "
    "fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E"
)


def render(
    *,
    path,
    title,
    description,
    schema="",
    og_type="website",
    robots="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1",
):
    canonical = SITE_URL + path
    ga = ""
    if GA4_MEASUREMENT_ID:
        ga = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_MEASUREMENT_ID}');
</script>"""

    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="icon" href="{FAVICON}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="{SITE_URL}/rss.xml">
{FONT_PRELOAD}
<link rel="stylesheet" href="/css/fonts.css?v=1">
<link rel="stylesheet" href="/css/site.css?v=1">{ga}
{schema}"""
