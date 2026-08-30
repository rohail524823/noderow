"""The canonical founder identity. Defined ONCE, imported everywhere.

The same person runs five sites. The goal is that search engines and answer
engines resolve all five to ONE entity rather than five anonymous publishers.
That reconciliation happens through the shared `sameAs` profiles — NOT through
links between the sites, which would be a private-network footprint and would
pass no authority anyway.

╔══════════════════════════════════════════════════════════════════════════════╗
║  SHARED — must be BYTE-IDENTICAL across all five sites.                       ║
║  A differing string is a different person to a parser. Do not "tidy" these:   ║
║  not the trailing slash on the LinkedIn URL, not the spelling of the name.    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

NAME = "Rohail Nisar"
EMAIL = "rohail.nisar786@gmail.com"
SAME_AS = [
    "https://www.linkedin.com/in/rohailnisarahmad/",
    "https://github.com/rohail524823",
    "https://www.upwork.com/freelancers/rohailnisaracademy",
]

# ---------------------------------------------------------------------------
# SITE-SPECIFIC — these SHOULD differ per property.
# ---------------------------------------------------------------------------

# Accurate for this site. NodeRow is a one-person publication; "Founder" is the
# honest role. "Editor" would imply an editorial process that does not exist.
JOB_TITLE = "Founder"

DESCRIPTION = (
    "Runs NodeRow, which works out what agency automation platforms actually "
    "cost once metered usage is counted. Builds the same workflows in n8n, "
    "Make, Zapier and GoHighLevel for paying clients."
)

# Only what THIS site demonstrably covers. Not a CV.
KNOWS_ABOUT = [
    "workflow automation",
    "GoHighLevel",
    "n8n",
    "Make.com",
    "Zapier",
    "SaaS pricing analysis",
    "marketing automation for home services",
]

# Convenience handles for prose, so the visible page and the structured data
# cannot drift apart.
LINKEDIN_URL = SAME_AS[0]
GITHUB_URL = SAME_AS[1]
UPWORK_URL = SAME_AS[2]


def person_node(person_id, org_id, url):
    """The full Person node.

    Emitted on EVERY page rather than referenced from one canonical page: a page
    read in isolation must still carry the whole entity, and an @id referenced
    but never defined on that page is a dangling reference.

    Deliberately absent, and why:
      - years of experience: the profiles say 15, the listed dates imply ~16y8m
      - education: the MBA is attributed to two different institutions
      - certifications: the two on file are Excel, irrelevant here
      - platform metrics: real, but they drift, and a copied number goes stale
        where nobody is watching. The profile link carries the live figure.
    """
    return {
        "@type": "Person",
        "@id": person_id,
        "name": NAME,
        "url": url,
        "jobTitle": JOB_TITLE,
        "description": DESCRIPTION,
        "email": EMAIL,
        "worksFor": {"@id": org_id},
        "sameAs": list(SAME_AS),
        "knowsAbout": list(KNOWS_ABOUT),
    }
