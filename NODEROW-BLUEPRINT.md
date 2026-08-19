# noderow.com — complete build prompt

## One strategy note first

GoHighLevel pays **40% recurring for the life of the subscription** on plans of $97, $297 and $497/month — roughly $38.80 to $198.80 per referral, per month, indefinitely. That is structurally different from Make (35% for 12 months) and n8n (30% for 12 months), both of which expire.

What that does to your target:

| To reach $500/month | Active referrals needed |
|---|---|
| Make @ ~$10/mo | ~50, expiring at 12 months |
| n8n @ ~$6/mo | ~80, expiring at 12 months |
| **GoHighLevel @ $118.80/mo ($297 plan)** | **~5, and they don't expire** |

Ten times less traffic for the same money. Two honest caveats: sources disagree on the cookie window (30 vs 90 days — verify on application), and the GHL buyer is a **marketing agency**, not the developer searching "n8n vs Make." Shoehorning GHL into developer content would be obvious and would cost you credibility.

So the prompt below gives GHL a real but bounded home: agency-focused pages, and all-in-one-vs-stitched-stack comparisons. That's where the audiences genuinely overlap.

---

## The prompt

Make sure `NODEROW-BLUEPRINT.md` is in the repo root. Then paste everything below into Claude Code with the noderow repo selected.

```
Build noderow.com. NODEROW-BLUEPRINT.md is in this repo — a full audit of a sibling
site I run (bestaicertifications.com), written by the session that built it. Read it
completely before writing any code. Sections A–G are validated patterns to copy.
Section I is a list of real mistakes not to repeat.

Work in the phases below. STOP at the end of each phase for my review. Do not run ahead.

=============================================================
WHAT THIS SITE IS
=============================================================
noderow.com helps people CHOOSE the right automation tool and BUILD the thing.

It is deliberately not a maintenance or monitoring site — that is a separate property
I own (opsuptime.com). noderow catches the reader BEFORE the automation exists, while
they are deciding and building. opsuptime catches them after, when it breaks. Do not
write reliability, monitoring, or incident-response content here; a single handoff line
at the end of build guides is the only crossover.

Reader: an operator, agency owner, or developer choosing between automation platforms
or trying to build a specific workflow. They have a decision, not yet a problem.

Author: Rohail Nisar Ahmad — freelance data integration and automation engineer,
100+ completed contracts, 100% job success on Upwork, builds in n8n, Make and Zapier
for clients weekly. This is the entire differentiator. Most competing content is
written by marketers reading documentation. Surface this credibility on every page
without bragging.

CONFIRM WITH ME before you commit: the exact display name to use as author.

=============================================================
THE FOUR-RUNG REVENUE LADDER
=============================================================
Every page should route the reader to the rung that fits their budget and intent.

  1. Article                        free           earns nothing yet
  2. Affiliate signup — they DIY    their spend    30–40% commission
  3. Workflow pack — pre-built      $39–99         one-time, zero work for me
  4. Build service — I do it        $50–500        project revenue

Rungs 3 and 4 are the near-term revenue. Rung 2 compounds into next year.

WHICH PAGES PUSH WHICH — build this into the templates:
  Comparison + pricing pages  → affiliate primary, pack secondary
  Alternatives pages          → affiliate primary
  Use-case / "how to automate X" pages → pack primary, build service secondary
  Migration pages             → both equally; highest intent on the site
  Agency-focused pages        → GoHighLevel affiliate + build service

=============================================================
COMMERCIAL FACTS — drive link and content decisions
=============================================================
GoHighLevel  40% RECURRING FOR LIFE on $97/$297/$497 plans. Highest-value referral
             on the site by an order of magnitude. Audience is marketing agencies and
             service businesses — NOT developers. Only feature it where an agency
             reader genuinely is: agency workflow pages, all-in-one vs stack
             comparisons, CRM-adjacent use cases. Do not insert it into n8n/Make
             developer content.
Make         35% for 12 months. Open program. Clock starts at REGISTRATION, not first
             payment.
n8n Cloud    30% for 12 months, 90-day cookie. CLOUD ONLY — self-hosted pays nothing.
Zapier       NO public cash affiliate program. Zero revenue, ever. Biggest search
             volume in the niche.

Strategic consequence: Zapier-intent queries are the cheapest traffic available and are
only monetizable when a page honestly routes toward Make, n8n or GoHighLevel. That is
honest because those genuinely are cheaper or better-fitted at volume — never pretend
otherwise, and keep recommending Zapier where Zapier actually wins.

NO ADSENSE OR DISPLAY ADS. Do not add ad slots, ad JS, or placeholders. Affiliate and
product revenue are worth 12–25x more per visitor here and ads would compete with both.

=============================================================
PHASE 1 — Scaffolding. STOP when done.
=============================================================
Follow NODEROW-BLUEPRINT.md Section J1 Phase 1. Specifically:

1. deploy/ is the Netlify publish root and IS the site. No framework, no build step,
   no bundler. Plain HTML + CSS + minimal vanilla JS.
2. deploy/netlify.toml from blueprint D4 — headers and 404 catch-all verbatim.
3. deploy/robots.txt from blueprint D1 — all 24 AI crawlers explicitly allowed, host
   changed to noderow.com.
4. tools/entity.py from blueprint C2, WITH THESE CHANGES:
     - Author is a PERSON, not an anonymous editorial team. Blueprint E6 calls the
       anonymous team that site's weakest dimension. We have a real practitioner.
     - Person node: name, jobTitle "Automation & Data Integration Engineer",
       worksFor the Organization, and a POPULATED sameAs:
         https://www.upwork.com/freelancers/rohailnisaracademy
         https://www.linkedin.com/in/rohailnisarahmad
     - knowsAbout: workflow automation, n8n, Make.com, Zapier, GoHighLevel,
       API integration, webhooks, data pipelines, AI agents, no-code automation
     - Organization keeps publishingPrinciples → /about/ and ethicsPolicy →
       /affiliate-disclosure/. Both pages must genuinely state those policies.
5. ONE head.py template module emitting the full <head> from blueprint B5, including
   max-snippet:-1. One module imported by everything. Blueprint I2 documents four
   diverging generators as real technical debt — do not repeat it.
6. Exactly ONE stylesheet: /css/site.css?v=1. Never create a second. Blueprint I1 is a
   dead second stylesheet that made a session fix a bug that did not exist.
7. Port publish_next.py's validate_page() gate from blueprint A5 in full, including the
   asset-path check. Nothing publishes without passing it.
8. Port the parked-link mechanism from blueprint B7:
   <span class="pending-link" data-link-to="/slug/">anchor</span> converted to a real
   <a> the day the target publishes.
9. GA4 + Search Console + Bing + IndexNow. Ship the affiliate_click listener from
   blueprint G4 AND register product, placement, link_url as GA4 custom dimensions the
   same day — blueprint I5 is two of three parameters silently discarded for want of
   this. Add matching pack_click and build_enquiry events.

STOP. Show me the file tree, entity.py, and head.py.

=============================================================
PHASE 2 — Navigation and site architecture. STOP when done.
=============================================================
PRIMARY NAV — exactly five items, no dropdowns on mobile:

  Compare Tools   /compare/
  Guides          /guides/
  Workflow Packs  /packs/
  Get It Built    /build/
  About           /about/

URL STRUCTURE:
  /                      homepage
  /compare/              hub — every tool comparison and alternatives page
  /compare/<slug>/       e.g. /compare/n8n-vs-make-vs-zapier/
  /guides/               hub — build guides and use-case articles
  /<slug>/               guides live flat at root, e.g. /automate-client-onboarding/
  /packs/                product index
  /packs/<slug>/         individual pack sales page
  /build/                service page with tiers and enquiry form
  /tools/                directory of every platform covered, one card each
  /tools/<slug>/         individual tool profile
  /about/  /how-we-test/  /affiliate-disclosure/  /privacy-policy/  /contact/

Trailing slash always. Directory + index.html. Self-referential canonical on every page.

FOOTER — four columns:
  Compare      top 5 comparison pages
  Guides       top 5 guides
  Products     Workflow Packs, Get It Built
  Site         About, How We Test, Affiliate Disclosure, Privacy, Contact
  Plus: LinkedIn and Upwork links, and the sitewide disclosure line.

Build /compare/, /guides/, /tools/, /packs/, /build/ as real hub pages now, even with
few children. They are the internal-link spine. Blueprint B7 shows footer/nav placement
produced a 20x inbound-link advantage over editorial linking — design that deliberately
rather than by accident.

DESIGN DIRECTION:
Commit to one deliberate direction. Avoid the three AI-default looks: cream background
with serif display and terracotta accent; near-black with a single acid accent;
broadsheet layout with hairline rules. The subject has its own vernacular — node
graphs, connection lines, execution logs, branching paths, status states. Mine that.
One characterful display face with a clean body face, a real type scale, self-hosted
woff2 fonts preloaded. Responsive to mobile, visible keyboard focus, prefers-reduced-
motion respected. Comparison tables must reflow to labelled cards on mobile with
data-label on every cell (blueprint F4).

STOP. Show me the nav, the homepage, and one hub page.

=============================================================
PHASE 3 — Products data and monetization. STOP when done.
=============================================================
content/products.json — one entry per platform:
  name, slug, vendor, category, url, affiliateUrl, monetizable (bool),
  commissionNote, pricingModel, tiers[], freeTier, bestFor, weakness,
  priceSource, priceCheckedDate, versionChecked, supersededUrls[], retiredNames[]

USE PLAIN VENDOR URLS FOR NOW — affiliate links are not approved yet. Put every one in
affiliateUrl so tools/affiliate.py can swap them in one command later. Never hardcode a
URL into page HTML; always read from products.json.

  General automation / iPaaS
    Zapier              https://zapier.com                    monetizable: false
    Make                https://www.make.com                  35% / 12 months
    n8n Cloud           https://n8n.io                        30% / 12 months
    n8n self-hosted     https://docs.n8n.io/hosting/          monetizable: false
    Pipedream           https://pipedream.com
    Activepieces        https://www.activepieces.com
    Pabbly Connect      https://www.pabbly.com/connect/
    Latenode            https://latenode.com
    Albato              https://albato.com
    Integrately         https://integrately.com

  Agency / CRM platforms
    GoHighLevel         https://www.gohighlevel.com           40% RECURRING, LIFETIME
    Keap                https://keap.com
    ActiveCampaign      https://www.activecampaign.com

  AI agent builders
    Lindy               https://www.lindy.ai
    Gumloop             https://www.gumloop.com
    Relay.app           https://www.relay.app
    Flowise             https://flowiseai.com
    Dify                https://dify.ai

  Developer-first
    Trigger.dev         https://trigger.dev
    Windmill            https://www.windmill.dev
    Inngest             https://www.inngest.com

  Voice agents
    Vapi                https://vapi.ai
    Retell AI           https://www.retellai.com

  Hosting (for self-host guides)
    Hetzner             https://www.hetzner.com
    DigitalOcean        https://www.digitalocean.com
    Railway             https://railway.app
    Render              https://render.com

THE INTEGRITY MECHANISM — build this properly, it is load-bearing.
When a page's honest recommendation has monetizable:false, render a visible callout,
generated from the flag, never hand-written:

  "We earn no commission if you choose Zapier. We're recommending it here anyway,
   because for this job it's the right call."

Zapier pays us nothing. A site that quietly stops recommending Zapier is both
detectable and dishonest. This turns the weakness into the strongest trust signal on
the site, and it has the advantage of being true.

AFFILIATE LINK RULES:
  rel="sponsored nofollow noopener", target="_blank", preceded by the HTML comment
  marker from blueprint G1. LOWER density than the sibling site — 553 links across 121
  pages was scatter. Concentrate CTAs on comparison, alternatives, pricing and
  migration pages. Guides may carry one or none.

DISCLOSURE — blueprint G3 documents footer-only disclosure across 553 links as a real
FTC gap. Ours is inline, above the first affiliate link on every page carrying one,
plus the footer line, plus /affiliate-disclosure/. Build it into the template now;
retrofitting across 100+ pages is painful.

WORKFLOW PACKS — /packs/
Deliberately priced ~50% below the market ($29 simple / $99–149 mid / $199–499 bundles).
This is a launch position to buy first sales and reviews, not a permanent price. Note
that on the page for me, not for readers.

  Client Onboarding Pack        $39   intake form → CRM → Drive folders → Slack →
                                      welcome sequence → status reporting
  Ecommerce Ops Pack            $39   order sync, inventory alerts, bulk price updates,
                                      returns triage
  Document Automation Pack      $39   email → parse → Drive filing → Sheets index →
                                      notification
  Lead Capture & CRM Sync Pack  $39   forms/ads → dedupe → enrich → CRM → assignment
  All Four Bundle               $99   (vs $156 separately)

Each pack page: what's inside, which platform it targets, screenshots of the actual
node graph, a setup-time estimate, what apps it needs, and an honest "who this is NOT
for". Product + Offer schema — legitimate here because we are genuinely selling.

BUILD SERVICE — /build/
Four tiers, fixed price, no hourly:
  Quick Fix         $50    one broken or half-finished workflow, diagnosed and repaired
  Single Workflow   $150   one automation built and tested, up to 3 connected apps
  Workflow System   $300   3–5 connected workflows, up to 6 apps, handover notes
  Full Build        $500   complete multi-workflow system, custom logic, documentation
                           and a walkthrough recording

Page must include: what's included at each tier, what's explicitly not, turnaround time,
how it works step by step, the Upwork profile as proof, and a simple enquiry form
(Netlify Forms — no backend). Service + Offer schema.

STOP. Show me products.json, one pack page, and /build/.

=============================================================
PHASE 4 — SEO and GEO. STOP when done.
=============================================================
Follow blueprint Sections B, C, D and F exactly. Non-negotiables:

  - One <h1> per page. Title formula per B1: median ~48 chars, honesty hook, year only
    where it earns its place. Meta description 140–160 chars per B2.
  - Full <head> from B5 including max-snippet:-1, OG, Twitter, canonical, preloaded
    fonts, RSS alternate.
  - Schema per C: ONE #org entity referenced by @id everywhere; Person author;
    BreadcrumbList on all; Article on editorial; ItemList with per-item ANCHOR urls on
    ranked lists; FAQPage where a visible FAQ exists; SoftwareApplication on tool
    profiles; Product + Offer on packs; Service on /build/; WebPage with lastReviewed.
    NEVER aggregateRating — blueprint C6 explains why that is a spam-policy violation.
  - Sitemap generated and appended atomically on publish, never hand-edited. RSS too.
  - llms.txt generated from the published index. Blueprint D3 is clear the evidence is
    against it mattering; include it only because generation is free. Not a lever.
  - IndexNow submission on publish, fail-open so it can never break a publish.

GEO / AI-CITATION — per blueprint F:
  - Front-loaded answer block FIRST on every article, before the TOC. ≥90 words, opens
    by naming the subjects (never a pronoun), self-contained enough to be lifted alone,
    contains concrete numbers. Every claim in it must already appear in the page body.
  - Question-shaped H2/H3 where it genuinely fits, each followed immediately by a
    direct 1–2 sentence answer before elaboration.
  - Comparison tables HIGH on the page — the most liftable artifact there is.
  - All dates as <time datetime="ISO">. Prices carry a checked date. Software claims
    carry a version: "Tested on n8n 1.x, {date}" beats "Updated {month}".
  - lastReviewed only after a real re-check. NEVER touch dateModified to fake freshness
    — blueprint F5 explains the penalty is worse than a stale date.

STOP. Show me one page's full head and JSON-LD.

=============================================================
PHASE 5 — Write three complete articles. STOP after each.
=============================================================
Section order per blueprint E2, exactly:
  answer block → TOC → comparison table (HIGH) → H2 body → recommendation cards →
  FAQ (<details>/<summary>, no JS) → citations → CTA band → author box → related links

Target 1,600–2,000 words of body. Every article must contain at least one thing that
cannot be written from documentation — a real cost figure, a real error message, a real
node configuration, a decision that actually went wrong on a client project. If a draft
has none, it is a commodity article; rewrite it.

ARTICLE 1 — /compare/n8n-vs-make-vs-zapier/
  Archetype: three-way comparison. Highest-traffic query in the niche.
  Must include: a full feature/pricing table; what one "task", "operation" and
  "execution" actually mean and why they aren't comparable; who each tool genuinely
  wins for; the no-commission callout on Zapier; honest treatment of n8n's learning
  curve. ItemList schema with anchor URLs. Affiliate primary, pack secondary.

ARTICLE 2 — /compare/zapier-alternatives/
  Archetype: alternatives page — the highest-converting type in SaaS affiliate.
  Must include: WHY people leave Zapier (cost at volume, task limits), then 6–8
  alternatives each with who it suits and who it doesn't. Cover Make, n8n, Pipedream,
  Activepieces, Pabbly, Latenode. Include GoHighLevel in a clearly-labelled separate
  section for agency readers who want all-in-one rather than a stitched stack — do not
  pretend it is a like-for-like Zapier swap. A migration-difficulty column.

ARTICLE 3 — /automate-client-onboarding/
  Archetype: use-case guide. Pack primary, build service secondary.
  Must include: the actual workflow shape step by step; which apps at each step; where
  it breaks in practice; a build-it-yourself path AND a "get the pack" path AND a
  "have it built" path. Agency-focused, so GoHighLevel belongs here honestly alongside
  the n8n/Make approach. One closing handoff line to opsuptime.com for upkeep, no more.

STOP after each article for my review.

=============================================================
PHASE 6 — Queue the rest
=============================================================
Build content/queue.json with 40 titles across these pillars, scored with the blueprint
E3 logic:

  Migration            10   Zapier→Make, Zapier→n8n, Make→n8n, auditing Zaps first
  Cost & pricing       10   what an operation is, real cost at 10k/100k/1M runs,
                            which tier you need, GoHighLevel pricing explained
  Alternatives          9   Make alternatives, n8n alternatives, GoHighLevel
                            alternatives
  Comparison            9   n8n vs Make, Make vs Zapier, GoHighLevel vs stitched stack
  Use-case guides       8   automate invoicing, lead routing, order sync, reporting,
                            recruiting pipeline, support triage
  Tool profiles         7   one per platform in products.json
  AI agents in build    6   LLM nodes without burning API budget, RAG in n8n, when an
                            agent is the wrong answer
  Definitional/what-is  SKIP ENTIRELY — blueprint E3 proves these sit at position
                        34–58 with zero clicks. Do not queue one.

Add the parked-link demand bonus from the blueprint: a queued page N published articles
already want to link to gets +N.

Publish at 1/day maximum. Blueprint I6: the sibling site ran 3/day and built a backlog
of pages Google discovered and declined to crawl.

=============================================================
KEYWORD SEPARATION — I own three sites, enforce this
=============================================================
  bestaicertifications.com  "what should I learn?"      certifications, courses
  noderow.com               "what should I build with?" tools, comparisons, builds
  opsuptime.com             "how do I keep it alive?"   monitoring, reliability

noderow NEVER publishes: a certification roundup, a course review, a "how to become an
X engineer" article, or a monitoring/incident-response guide. AI agents here means
building and orchestrating them, never the credential angle. If a title could plausibly
sit on two of these sites, it belongs on neither.

=============================================================
WRITING STANDARD
=============================================================
Plain, specific, active voice. No "leverage", "seamless", "game-changing", "unlock".
Name what you would NOT recommend and why — the sibling site's data shows honest and
"is it worth it" framings earn the clicks. No invented metrics, no fake testimonials,
no traffic or revenue numbers we do not have. Every price carries a checked date.
```

---

## Two things to do yourself

Apply to the GoHighLevel affiliate program this week. It's the highest-value referral on the site by a wide margin and, unlike Make and n8n, the commission doesn't expire at 12 months. Verify the cookie window on application — sources disagree between 30 and 90 days.

Confirm the author display name in Phase 1 before it gets baked into schema across every page. Changing it later means touching every file.

## One honest note on the pack pricing

Pricing 50% below market buys you velocity and first reviews, which you need. It also caps revenue and, in B2B, can read as lower quality. Treat $39 as a launch price, not a permanent one — get to ten sales and five testimonials, then raise to $79. The prompt notes this in the page comments so you don't forget.
