"""Single source of truth for site-wide constants.

Everything that appears on more than one page lives here. No page module
defines its own URL, author name, or nav item.
"""

SITE_URL = "https://noderow.com"
SITE_NAME = "NodeRow"
SITE_TAGLINE = "Automation stacks for agencies, reviewed by someone who builds them"

# Founder identity lives in tools/author_identity.py — the single canonical
# definition shared byte-identically across all five sites. Do not redefine it.
from author_identity import (  # noqa: E402
    DESCRIPTION as AUTHOR_DESCRIPTION,
    EMAIL as AUTHOR_EMAIL,
    GITHUB_URL,
    JOB_TITLE as AUTHOR_JOB_TITLE,
    KNOWS_ABOUT as AUTHOR_KNOWS_ABOUT,
    LINKEDIN_URL,
    NAME as AUTHOR_NAME,
    SAME_AS as AUTHOR_SAME_AS,
    UPWORK_URL,
)

# Exactly five. No dropdowns on mobile.
NAV = [
    ("Compare Tools", "/compare/"),
    ("Guides", "/guides/"),
    ("Workflow Packs", "/packs/"),
    ("Get It Built", "/build/"),
    ("About", "/about/"),
]

FOOTER_COLUMNS = [
    ("Compare", [
        ("GoHighLevel cost calculator", "/gohighlevel-true-cost-calculator/"),
        ("GoHighLevel pricing explained", "/gohighlevel-pricing-explained/"),
        ("All-in-one vs stitched stack", "/compare/gohighlevel-vs-stitched-stack/"),
        ("GoHighLevel alternatives", "/compare/gohighlevel-alternatives/"),
        ("n8n vs Make vs Zapier", "/compare/n8n-vs-make-vs-zapier/"),
        ("Zapier alternatives", "/compare/zapier-alternatives/"),
        ("Compare hub", "/compare/"),
    ]),
    ("Guides", [
        ("Missed call revenue calculator", "/missed-call-revenue-calculator/"),
        ("Missed call text back", "/missed-call-text-back/"),
        ("CRM for contractors", "/crm-for-contractors/"),
        ("Automate client onboarding", "/automate-client-onboarding/"),
        ("GoHighLevel pricing explained", "/gohighlevel-pricing-explained/"),
        ("Lead capture to CRM sync", "/automate-lead-capture/"),
        ("Guides hub", "/guides/"),
    ]),
    ("Products", [
        ("Workflow Packs", "/packs/"),
        ("Get It Built", "/build/"),
    ]),
    ("Site", [
        ("About", "/about/"),
        ("How We Test", "/how-we-test/"),
        ("Affiliate Disclosure", "/affiliate-disclosure/"),
        ("Privacy Policy", "/privacy-policy/"),
        ("Contact", "/contact/"),
    ]),
]

DISCLOSURE_SHORT = (
    "Some links on this site are affiliate links. If you sign up through one, "
    "NodeRow may earn a commission at no extra cost to you."
)

DISCLOSURE_INLINE = (
    "NodeRow earns a 40% recurring commission if you sign up for GoHighLevel "
    "through the links on this page, tracked for 90 days on a last-click basis. "
    "That does not change what it costs you, and it does not change what gets "
    "recommended — tools that pay us nothing are named here too, and labelled "
    "as such."
)

GA4_MEASUREMENT_ID = ""  # set once the property exists; empty ships no analytics tag
