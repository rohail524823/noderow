"""Shared page furniture.

The affiliate link, the inline disclosure and the no-commission callout are
generated here from products.json flags. None of them are ever hand-written
into a page, so none of them can drift out of sync with the data.
"""

import html
import json
import pathlib

from site_config import (
    DISCLOSURE_INLINE,
    DISCLOSURE_SHORT,
    FOOTER_COLUMNS,
    NAV,
    SITE_NAME,
    AUTHOR_NAME,
    AUTHOR_SAME_AS,
)

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_PRODUCTS = json.loads((_ROOT / "content" / "products.json").read_text())["products"]
BY_SLUG = {p["slug"]: p for p in _PRODUCTS}

# Paths that actually exist. build.py fills this before rendering. Footer and nav
# entries pointing anywhere else render as parked links rather than dead anchors.
PUBLISHED = set()


def set_published(paths):
    PUBLISHED.clear()
    PUBLISHED.update(paths)


def product(slug):
    if slug not in BY_SLUG:
        raise KeyError(f"unknown product slug: {slug!r}")
    return BY_SLUG[slug]


def outbound(slug, anchor, *, placement="body"):
    """Render an outbound product link.

    Monetizable products get the full affiliate treatment: sponsored/nofollow,
    new tab, a tracking hook and the HTML comment marker. Non-monetizable ones
    get a plain link, because pretending otherwise would be a lie.
    """
    p = product(slug)
    href = p.get("affiliateUrl") or p["url"]
    anchor = html.escape(anchor)

    if not p["monetizable"]:
        return (
            f'<a class="out" href="{href}" target="_blank" rel="noopener">'
            f"{anchor}</a>"
        )

    return (
        f"<!-- affiliate-link: {p['slug']} placement={placement} -->\n"
        f'<a class="out out-aff" href="{href}" target="_blank" '
        f'rel="sponsored nofollow noopener" '
        f'data-aff="{p["slug"]}" data-placement="{placement}">{anchor}</a>'
    )


def cta(slug, anchor, *, placement, note=None):
    """A primary call-to-action button wrapping an outbound link."""
    p = product(slug)
    href = p.get("affiliateUrl") or p["url"]
    rel = (
        'rel="sponsored nofollow noopener"'
        if p["monetizable"]
        else 'rel="noopener"'
    )
    marker = (
        f"<!-- affiliate-link: {p['slug']} placement={placement} -->\n"
        if p["monetizable"]
        else ""
    )
    note_html = f'<span class="cta-note">{html.escape(note)}</span>' if note else ""
    return f"""{marker}<p class="cta-row">
<a class="btn btn-primary" href="{href}" target="_blank" {rel}
   data-aff="{p['slug']}" data-placement="{placement}">{html.escape(anchor)}</a>
{note_html}
</p>"""


def inline_disclosure():
    """Sits above the first affiliate link on every page that carries one.

    Footer-only disclosure across a site full of affiliate links is a real FTC
    gap. This is the inline half; the footer line and /affiliate-disclosure/
    are the other two.
    """
    return (
        '<aside class="disclosure" role="note">'
        '<span class="disclosure-tag">Disclosure</span>'
        f"<span>{DISCLOSURE_INLINE}</span>"
        "</aside>"
    )


def no_commission_callout(slug):
    """Generated from monetizable:false. Never hand-written.

    A site that quietly stops recommending the tool that pays it nothing is
    both detectable and dishonest. Saying it out loud is the cheapest trust
    signal available, and it has the advantage of being true.
    """
    p = product(slug)
    if p["monetizable"]:
        raise ValueError(
            f"{slug} is monetizable — the no-commission callout would be false"
        )
    return f"""<aside class="callout callout-integrity" role="note">
<span class="callout-mark" aria-hidden="true">◆</span>
<div>
<strong>We earn no commission if you choose {html.escape(p['name'])}.</strong>
<span>We're recommending it here anyway, because for this job it's the right call.
{html.escape(p['commissionNote'])}</span>
</div>
</aside>"""


def pending_link(anchor, target):
    """A link to a page that does not exist yet.

    Renders as plain text with no click affordance. tools/publish.py rewrites
    these into real anchors on the day the target publishes.
    """
    return (
        f'<span class="pending-link" data-link-to="{target}">'
        f"{html.escape(anchor)}</span>"
    )


def status_pill(state, label):
    """state: ok | waiting | error | idle"""
    return f'<span class="pill pill-{state}">{html.escape(label)}</span>'


def header(active=None):
    def nav_item(label, path):
        current = ' aria-current="page"' if path == active else ""
        return f'<li><a href="{path}"{current}>{html.escape(label)}</a></li>'

    items = "\n".join(nav_item(label, path) for label, path in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="/">
      <svg class="wordmark-glyph" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
        <path d="M9 22V10l14 12V10" fill="none" stroke="currentColor"
              stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span>{SITE_NAME}</span>
    </a>
    <nav aria-label="Primary">
      <ul class="site-nav">
{items}
      </ul>
    </nav>
  </div>
</header>"""


def footer():
    def entry(label, path):
        if PUBLISHED and path not in PUBLISHED:
            return f"<li>{pending_link(label, path)}</li>"
        return f'<li><a href="{path}">{html.escape(label)}</a></li>'

    cols = []
    for title, links in FOOTER_COLUMNS:
        items = "\n".join(entry(label, path) for label, path in links)
        cols.append(
            f'<div class="footer-col"><h2>{html.escape(title)}</h2>'
            f"<ul>{items}</ul></div>"
        )
    upwork, linkedin = AUTHOR_SAME_AS[0], AUTHOR_SAME_AS[1]
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
{"".join(cols)}
    </div>
    <div class="footer-base">
      <p class="footer-brand">{SITE_NAME}</p>
      <p class="footer-social">
        <a href="{linkedin}" target="_blank" rel="noopener me">LinkedIn</a>
        <a href="{upwork}" target="_blank" rel="noopener me">Upwork</a>
      </p>
      <p class="footer-disclosure">{html.escape(DISCLOSURE_SHORT)}</p>
      <p class="footer-copy">&copy; 2026 {SITE_NAME}. Written by {html.escape(AUTHOR_NAME)}.</p>
    </div>
  </div>
</footer>"""


def author_box():
    upwork, linkedin = AUTHOR_SAME_AS[0], AUTHOR_SAME_AS[1]
    return f"""<aside class="author-box">
  <div class="author-meta">
    <p class="author-name">{html.escape(AUTHOR_NAME)}</p>
    <p class="author-role">Automation &amp; Data Integration Engineer</p>
  </div>
  <p class="author-bio">Builds automation in n8n, Make, Zapier and GoHighLevel for
  paying clients — 100+ completed contracts with a 100% job success score on Upwork.
  Everything here comes out of client work, not a content calendar.</p>
  <p class="author-links">
    <a href="{upwork}" target="_blank" rel="noopener me">Upwork profile</a>
    <a href="{linkedin}" target="_blank" rel="noopener me">LinkedIn</a>
    <a href="/about/">About NodeRow</a>
  </p>
</aside>"""


ANALYTICS_JS = """<script>
(function () {
  function send(name, params) {
    if (typeof window.gtag === 'function') { window.gtag('event', name, params); }
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-aff]');
    if (a) {
      send('affiliate_click', {
        product: a.dataset.aff,
        placement: a.dataset.placement || 'body',
        link_url: a.href
      });
      return;
    }
    var pack = e.target.closest('a[data-pack]');
    if (pack) {
      send('pack_click', {
        product: pack.dataset.pack,
        placement: pack.dataset.placement || 'body',
        link_url: pack.href
      });
    }
  });
  var form = document.querySelector('form[data-enquiry]');
  if (form) {
    form.addEventListener('submit', function () {
      send('build_enquiry', {
        product: 'build-service',
        placement: 'build-page',
        link_url: location.pathname
      });
    });
  }
})();
</script>"""
