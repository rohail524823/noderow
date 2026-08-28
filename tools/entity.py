"""Schema.org entity graph.

ONE Organization node, referenced by @id everywhere. ONE Person node for the
author — a real practitioner, not an anonymous editorial team.

Never emits aggregateRating. Self-serving review markup without a genuine
first-party review process is a Google spam-policy violation.
"""

import json

from site_config import (
    AUTHOR_JOB_TITLE,
    AUTHOR_KNOWS_ABOUT,
    AUTHOR_NAME,
    AUTHOR_SAME_AS,
    SITE_NAME,
    SITE_URL,
)

ORG_ID = f"{SITE_URL}/#org"
PERSON_ID = f"{SITE_URL}/#rohail"
WEBSITE_ID = f"{SITE_URL}/#website"


def organization():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": SITE_NAME,
        "url": SITE_URL + "/",
        "description": (
            "Reviews, comparisons and build guides for agency automation stacks — "
            "GoHighLevel, n8n, Make and Zapier."
        ),
        "founder": {"@id": PERSON_ID},
        "publishingPrinciples": f"{SITE_URL}/about/",
        "ethicsPolicy": f"{SITE_URL}/affiliate-disclosure/",
    }


def person():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": AUTHOR_NAME,
        "jobTitle": AUTHOR_JOB_TITLE,
        "url": f"{SITE_URL}/about/",
        "worksFor": {"@id": ORG_ID},
        "sameAs": AUTHOR_SAME_AS,
        "knowsAbout": AUTHOR_KNOWS_ABOUT,
    }


def website():
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE_URL + "/",
        "name": SITE_NAME,
        "publisher": {"@id": ORG_ID},
    }


def breadcrumbs(trail):
    """trail: list of (name, path) from home to current page."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": SITE_URL + path,
            }
            for i, (name, path) in enumerate(trail)
        ],
    }


def webpage(path, title, description, last_reviewed=None):
    node = {
        "@type": "WebPage",
        "@id": f"{SITE_URL}{path}#webpage",
        "url": SITE_URL + path,
        "name": title,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID},
    }
    if last_reviewed:
        # Only ever set after a real re-check. Never touched to fake freshness.
        node["lastReviewed"] = last_reviewed
    return node


def article(path, title, description, published, modified=None):
    node = {
        "@type": "Article",
        "@id": f"{SITE_URL}{path}#article",
        "headline": title,
        "description": description,
        "datePublished": published,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": f"{SITE_URL}{path}#webpage"},
    }
    if modified:
        node["dateModified"] = modified
    return node


def service(name, description, tiers):
    """tiers: list of (name, price_usd, description)."""
    return {
        "@type": "Service",
        "@id": f"{SITE_URL}/build/#service",
        "name": name,
        "description": description,
        "provider": {"@id": PERSON_ID},
        "areaServed": "Worldwide",
        "offers": [
            {
                "@type": "Offer",
                "name": tier_name,
                "price": str(price),
                "priceCurrency": "USD",
                "description": desc,
            }
            for tier_name, price, desc in tiers
        ],
    }


def graph(*nodes):
    """Wrap nodes into a single JSON-LD @graph script tag."""
    payload = {
        "@context": "https://schema.org",
        "@graph": [n for n in nodes if n],
    }
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'
