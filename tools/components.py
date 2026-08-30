"""Shared page furniture.

The affiliate link, the inline disclosure and the no-commission callout are
generated here from products.json flags. None of them are ever hand-written
into a page, so none of them can drift out of sync with the data.
"""

import html
import json
import pathlib

from site_config import (
    AUTHOR_DESCRIPTION,
    AUTHOR_JOB_TITLE,
    GITHUB_URL,
    LINKEDIN_URL,
    UPWORK_URL,
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


def resolve_link(slug, dest="default"):
    """Return (href, affiliate_id) for a product, routed by destination.

    The affiliate id is NOT constant across a program's campaigns. GoHighLevel
    issues a different id per campaign, so sending SaaS Pro traffic through the
    main campaign's link silently drops that campaign's commission — the click
    works, the signup completes, and nothing is ever paid. Routing by intent is
    therefore a correctness requirement, not an optimisation.
    """
    p = product(slug)
    links = p.get("affiliateLinks")
    if not links:
        # Single-link programs (and unmonetized products) keep the simple shape.
        return p.get("affiliateUrl") or p["url"], None
    if dest not in links:
        raise KeyError(
            f"{slug} has no affiliate link destination {dest!r}. "
            f"Known: {sorted(links)}"
        )
    entry = links[dest]
    return entry["url"], entry.get("affiliateId")


def outbound(slug, anchor, *, placement="body", dest="default"):
    """Render an outbound product link.

    Monetizable products get the full affiliate treatment: sponsored/nofollow,
    new tab, a tracking hook and the HTML comment marker. Non-monetizable ones
    get a plain link, because pretending otherwise would be a lie.
    """
    p = product(slug)
    href, aff_id = resolve_link(slug, dest)
    anchor = html.escape(anchor)

    if not p["monetizable"]:
        return (
            f'<a class="out" href="{href}" target="_blank" rel="noopener">'
            f"{anchor}</a>"
        )

    id_attr = f' data-aff-id="{aff_id}"' if aff_id else ""
    return (
        f"<!-- affiliate-link: {p['slug']} dest={dest} placement={placement} -->\n"
        f'<a class="out out-aff" href="{href}" target="_blank" '
        f'rel="sponsored nofollow noopener" '
        f'data-aff="{p["slug"]}" data-dest="{dest}"{id_attr} '
        f'data-placement="{placement}">{anchor}</a>'
    )


def cta(slug, anchor, *, placement, note=None, dest="default"):
    """A primary call-to-action button wrapping an outbound link."""
    p = product(slug)
    href, aff_id = resolve_link(slug, dest)
    rel = (
        'rel="sponsored nofollow noopener"'
        if p["monetizable"]
        else 'rel="noopener"'
    )
    marker = (
        f"<!-- affiliate-link: {p['slug']} dest={dest} placement={placement} -->\n"
        if p["monetizable"]
        else ""
    )
    id_attr = f' data-aff-id="{aff_id}"' if aff_id else ""
    note_html = f'<span class="cta-note">{html.escape(note)}</span>' if note else ""
    return f"""{marker}<p class="cta-row">
<a class="btn btn-primary" href="{href}" target="_blank" {rel}
   data-aff="{p['slug']}" data-dest="{dest}"{id_attr}
   data-placement="{placement}">{html.escape(anchor)}</a>
{note_html}
</p>"""


def inline_disclosure():
    """Sits at the TOP of the page, before the main content.

    HighLevel's program rules are specific and stricter than "somewhere on the
    page": place it "at the top of the post before the main content", in plain
    language, not hidden in a footer. They also name the wording that fails —
    "affiliate link" and "commissionable link" are called out as NOT clear
    enough, so this says "earns a commission" explicitly.
    """
    return (
        '<aside class="disclosure" role="note">'
        '<span class="disclosure-tag">Disclosure</span>'
        f"<span>{DISCLOSURE_INLINE}</span>"
        "</aside>"
    )


def not_speaking_for(vendor="HighLevel"):
    """Required whenever the page comments on a vendor's competitors.

    Program rules: "If you comment on HighLevel competitors, make clear you're
    not speaking for HighLevel, and keep it truthful and fair."
    """
    return (
        '<p class="speaking-note"><strong>Independence note.</strong> '
        f'NodeRow does not speak for {html.escape(vendor)} and is not affiliated '
        'with it beyond earning an affiliate commission. Comparisons here are our '
        'own assessment.</p>'
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
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
{"".join(cols)}
    </div>
    <div class="footer-base">
      <p class="footer-brand">{SITE_NAME}</p>
      <p class="footer-social">
        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener me">LinkedIn</a>
        <a href="{UPWORK_URL}" target="_blank" rel="noopener me">Upwork</a>
        <a href="{GITHUB_URL}" target="_blank" rel="noopener me">GitHub</a>
      </p>
      <p class="footer-disclosure">{html.escape(DISCLOSURE_SHORT)}</p>
      <p class="footer-copy">&copy; 2026 {SITE_NAME}. Written by {html.escape(AUTHOR_NAME)}.</p>
    </div>
  </div>
</footer>"""


def author_box():
    """Visible counterpart to the Person node in the JSON-LD.

    The same profile URLs appear here as clickable links. Structured data a
    human cannot see is half the job, and a LinkedIn URL that exists only inside
    an ld+json block is not verifiable by a reader.

    No platform metrics — job-success score, contract counts. They are real but
    they drift, and a number copied here goes stale where nobody is watching.
    The profile link carries the live figure.
    """
    return f"""<aside class="author-box">
  <div class="author-meta">
    <p class="author-name">{html.escape(AUTHOR_NAME)}</p>
    <p class="author-role">{html.escape(AUTHOR_JOB_TITLE)}, {SITE_NAME}</p>
  </div>
  <p class="author-bio">{html.escape(AUTHOR_DESCRIPTION)}</p>
  <p class="author-links">
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener me">LinkedIn</a>
    <a href="{UPWORK_URL}" target="_blank" rel="noopener me">Upwork</a>
    <a href="{GITHUB_URL}" target="_blank" rel="noopener me">GitHub</a>
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
        destination: a.dataset.dest || 'default',
        affiliate_id: a.dataset.affId || '',
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
