"""Single source of truth for site-wide constants.

Everything that appears on more than one page lives here. No page module
defines its own URL, author name, or nav item.
"""

SITE_URL = "https://noderow.com"
SITE_NAME = "NodeRow"
SITE_TAGLINE = "Automation stacks for agencies, reviewed by someone who builds them"

# Confirm before this gets baked into schema across every page (blueprint Phase 1).
AUTHOR_NAME = "Rohail Nisar Ahmad"
AUTHOR_JOB_TITLE = "Automation & Data Integration Engineer"
AUTHOR_SAME_AS = [
    "https://www.upwork.com/freelancers/rohailnisaracademy",
    "https://www.linkedin.com/in/rohailnisarahmad",
]
AUTHOR_KNOWS_ABOUT = [
    "workflow automation",
    "n8n",
    "Make.com",
    "Zapier",
    "GoHighLevel",
    "API integration",
    "webhooks",
    "data pipelines",
    "AI agents",
    "no-code automation",
]

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
