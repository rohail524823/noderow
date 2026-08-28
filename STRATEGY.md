# NodeRow — business strategy

Working document. Written 2026-08-28 from live research, not assumption. Every
factual claim here has a source; where a number could not be verified against the
vendor directly, that is stated rather than hidden.

---

## 1. The one-sentence thesis

**Every site ranking for GoHighLevel commercial keywords is itself a GoHighLevel
affiliate pretending to be neutral. NodeRow wins by being the one that admits it,
and by shipping tools none of them have bothered to build.**

## 2. What the research actually found

### The competitive landscape is uniformly compromised

Search results for the money keywords — "GoHighLevel pricing", "GoHighLevel
alternatives", "GoHighLevel vs" — are dominated by:

`netpartners.marketing` · `oneexpand.com` · `passivesecrets.com` · `ghlprime.com`
· `ghlcrm.me` · `ghlcentral.com` · `autogencrm.com` · `saleoid.com` ·
`hlgrowthpartner.com` · `digitalmarketingsnapshotforghl.com`

Every one of these is an affiliate. Many are titled "honest comparison" or
"unbiased review". None disclose above the fold. Several exist solely to rank for
GHL terms.

**Strategic consequence.** Competing on "more thorough affiliate review" is
competing in a red ocean on their terms. The two things they structurally cannot
copy are (a) visible, mechanical honesty and (b) working tools.

### The three-layer cost model is the content gap

GoHighLevel's real cost is three stacked layers, and almost every competing page
covers only the first:

| Layer | What it is | Typical size |
|---|---|---|
| 1. Subscription | $97 / $297 / $497 per month | Fixed |
| 2. Metered usage | SMS, email, voice — drawn from an auto-recharging wallet | Often 30–100%+ of layer 1 |
| 3. AI | Conversation AI per message, Voice AI per minute | $30–150/mo when leaned on |

A ten-client agency on the $297 plan commonly pays **$370–450/month** all in.

Verified rates (2026-08-28): SMS ≈ **$0.0079/segment**; email ≈ **$0.675–1.00 per
1,000**; plans **$97 / $297 / $497** monthly, roughly **$80 / $247 / $414**
annualised. Base rates did not rise for 2026.

### The single highest-value insight nobody has monetised

**Rebilling usage at cost is already included on the $297 Unlimited plan.
Rebilling with a *markup* requires the $497 Agency Pro plan.**

So the $200/month upgrade buys exactly one economically meaningful thing: margin
on usage. It pays for itself only when that margin exceeds $200/month.

That is arithmetic, and it is the question every agency at the decision point is
actually asking. **No competitor answers it with maths.** They all describe the
feature list instead.

This is why the calculator is the flagship asset, not a nice-to-have.

## 3. Positioning

**For** agency owners and service businesses choosing or outgrowing their stack,
**NodeRow is** the automation publication that shows the real number,
**unlike** the affiliate review farms, **because** it is written by someone who
builds and debugs these systems for paying clients and discloses exactly what it
earns on every recommendation.

**Reader:** an operator with a decision, not yet a problem. They are comparing,
pricing, or migrating.

**Author:** Rohail Nisar Ahmad — 100+ completed contracts, 100% job success on
Upwork, builds in n8n, Make, Zapier and GoHighLevel weekly.

**Not covered here:** monitoring, alerting, incident response. Different job,
different property.

## 4. Revenue model

| Rung | Offer | Price | Economics |
|---|---|---|---|
| 1 | Article | Free | Earns nothing directly |
| 2 | **GoHighLevel affiliate** | Their spend | **40% recurring, does not expire** |
| 2b | Make / n8n Cloud affiliate | Their spend | 35% / 30%, expires at 12 months |
| 3 | Workflow packs | $39–99 | One-time, near-zero marginal cost |
| 4 | Build service | $50–500 | Project revenue, funds the site now |

### Why GoHighLevel is the primary

| To reach $500/month | Active referrals needed |
|---|---|
| Make @ ~$10/mo | ~50, expiring at 12 months |
| n8n @ ~$6/mo | ~80, expiring at 12 months |
| **GoHighLevel @ $118.80/mo ($297 plan)** | **~5, and they don't expire** |

Roughly an order of magnitude less traffic for the same revenue. There is also a
**5% second-tier commission** on affiliates recruited, which is a later lever, not
a launch one.

### The honest constraint

GoHighLevel's buyer is a **marketing agency**, not the developer searching "n8n vs
Make". Pushing GHL into developer content would be transparent and would cost the
credibility the whole site runs on. GHL leads on agency-shaped pages —
all-in-one vs stack, agency workflows, CRM-adjacent use cases. Developer content
routes to Make and n8n, and to Zapier where Zapier genuinely wins, earning nothing.

**No display ads, ever.** Affiliate and product revenue are worth an order of
magnitude more per visitor, and ads would compete with both while signalling
low-quality content.

## 5. The moat: three things competitors can't copy cheaply

1. **Working calculators.** Interactive, dated, sourced. Expensive to build,
   trivially linkable, and the natural conversion point — a reader who has just
   modelled their own cost is at maximum intent. The true-cost calculator is
   live; a Zapier-vs-Make-vs-n8n volume calculator is the obvious second.

2. **Mechanical honesty.** The no-commission callout is *generated from data*, not
   written by hand. Commission status appears on every tool card. Disclosure sits
   above the first affiliate link, enforced by the build gate — a page carrying an
   affiliate link literally cannot ship without it. Competitors would have to
   rebuild their publishing pipeline to match this, and it would cost them
   conversions to do so.

3. **Practitioner specifics.** Every article must contain at least one thing that
   cannot be written from documentation: a real cost figure, a real error message,
   a real node configuration, a decision that went wrong on a client project. A
   draft without one is a commodity article and does not publish.

## 6. Content plan

### Priority order, by revenue-per-effort

**Tier 1 — build first (highest intent, GHL-monetisable)**
1. ✅ GoHighLevel True Cost Calculator — *live*
2. GoHighLevel vs a stitched-together stack — the core decision page
3. GoHighLevel pricing explained — captures the highest-volume GHL query
4. GoHighLevel alternatives — highest-converting archetype in SaaS affiliate
5. Is GoHighLevel worth it? — the "honest" framing that earns clicks

**Tier 2 — high intent, mixed monetisation**
6. Migration pages (Zapier→Make, Zapier→n8n, Make→n8n) — highest intent on the site
7. n8n vs Make vs Zapier — biggest raw traffic in the niche
8. Zapier alternatives — Zapier pays nothing, so this must route honestly

**Tier 3 — supporting**
9. Use-case build guides (onboarding, lead capture, document filing) → packs
10. Tool profiles, one per platform in `products.json`

**Never publish:** definitional "what is X" pages. They rank at position 34–58
with effectively zero clicks. Also never: certification roundups, course reviews,
monitoring/incident-response guides — those belong to other properties.

### Cadence

**One page per day, maximum.** Publishing faster builds a backlog of pages Google
discovers and declines to crawl, which is worse than publishing slower.

### Article structure (fixed)

answer block → TOC → comparison table (high) → body → recommendation cards →
FAQ → citations → CTA band → author box → related links

The answer block is first, ≥90 words, names its subjects rather than using
pronouns, carries concrete numbers, and is self-contained enough to be lifted
whole by an AI search engine. Every claim in it must also appear in the body.

## 7. Technical position (as of 2026-08-28)

| Check | Result |
|---|---|
| axe-core violations, 13 pages × light + dark | **0** |
| Cumulative Layout Shift | **0.0000** |
| DOMContentLoaded | **53 ms** |
| Third-party requests | **0** (fonts self-hosted) |
| Page weight, heaviest page | 255 KB (199 KB of it cached fonts) |
| Schema | One `#org` + Person, referenced by `@id`; FAQPage, Article, Service |
| `aggregateRating` | Rejected by the build gate — spam-policy violation |

The build gate blocks publication on: missing/duplicate `h1`, missing canonical or
description, description outside 120–175 chars, unresolvable asset paths,
unresolvable internal links, missing trailing slashes, affiliate links without
`rel="sponsored nofollow"`, and any page carrying an affiliate link without an
inline disclosure.

## 8. Affiliate program — verified from the dashboard, 2026-08-28

### Links are routed per destination, because the id changes per campaign

This is the single easiest way to lose money silently, and it is now handled in
code. GoHighLevel issues a **different affiliate id per campaign**:

| Destination | Campaign | Affiliate id |
|---|---|---|
| `default`, `pricing`, `annual`, `ai`, `bootcamp` | HighLevel Affiliate Program | `…30` |
| `saas-pro` | Supercharged SaaS Program | **`…65`** |
| `certification` | HighLevel Certification Program | **`…33`** |

Sending SaaS Pro traffic through the main campaign's link would track under the
wrong campaign and pay nothing, with no visible symptom. `components.resolve_link()`
routes by intent; the calculator swaps its CTA to `saas-pro` (id `…65`) the moment
a reader's own numbers recommend Agency Pro.

Note there are two distinct pro-trial paths: `/protrial` (id `…30`) on the main
campaign and `/pro-trial` (id `…65`) on the SaaS campaign. They are not
interchangeable.

### Terms

| Term | Value |
|---|---|
| Commission | 40% recurring + 5% second tier |
| Duration | No fixed term stated in the dashboard. Not capped at 12 months like Make and n8n — but "lifetime" is not the dashboard's word, so the site does not use it |
| Cookie | **90 days, last-click** |
| Payout | Monthly, Net-15, $50 threshold |
| Cancellation | Attribution survives 30 days past cancellation |

### Non-commissionable — matters for content planning

- Prospecting Tool — no reward at all
- **AI Employee Pay-Per-Use** and **AI Employee Growth ($50/mo)** — earn nothing.
  Only AI Employee Unlimited ($97/mo per location) qualifies
- **Metered usage earns nothing.** The calculator models SMS/email/AI spend in
  detail and none of it pays us. Worth saying out loud on the site — it is the
  cheapest credibility available and it happens to be true

### Operational risk to Rohail personally

**Self-referrals are prohibited** and risk termination plus forfeiture of accrued
commissions. Two live hazards given the build service:

1. Do not sign up your own agency through your own link.
2. When setting up a client, the **client** must click the link and complete
   signup with their own information, device and payment method. Signing up on
   their behalf in a way that misrepresents the purchaser is a policy breach.

The full Affiliate Policy is referenced in the dashboard FAQ but not exposed as a
clickable URL, so paid-search, brand-bidding and coupon-site restrictions remain
unverified. Ask the Affiliate Manager for the document before running paid traffic.

## 9. Open items — things only Rohail can do

1. **Confirm the author display name** before it is baked into schema everywhere.
   Currently `Rohail Nisar Ahmad`; the GHL account says `Rohail Nisar`.
2. **Spot-check the pricing figures against a real invoice.** `gohighlevel.com` is
   unreachable from the build environment, so all rates were verified against
   independent secondary sources. Well-corroborated, not authoritative.
3. **Get the full Affiliate Policy** from the Affiliate Manager — the promotional
   restrictions are not surfaced in the dashboard.
4. **Confirm whether WLMA and HIPAA promotions are currently live** in the
   Affiliate Community before writing anything that promotes them.
5. Complete the Affiliate Welcome Survey and book the Affiliate Manager call
   (`speakwith.us/expandteam`) — free distribution leverage sitting unused.

## Sources

- [GoHighLevel Pricing 2026: $97, $297 or $497 Plan Compared](https://netpartners.marketing/gohighlevel-pricing-plans-explained-features-value-cost-comparison-2026/)
- [GoHighLevel Hidden Costs 2026: The Complete True Pricing Breakdown](https://www.nextgenchannels.com/gohighlevel-hidden-costs/)
- [GoHighLevel SMS Pricing: Cost Per Message (2026)](https://autogencrm.com/gohighlevel-sms-pricing/)
- [GoHighLevel Agency Pro: SaaS Pricing Plan Explained 2026](https://ghlcrm.me/gohighlevel-saas-pricing/)
- [GoHighLevel Affiliate Program: Commission & Cookie Details](https://www.affililist.com/affiliate/gohighlevel)
- [GoHighLevel SaaS Mode: How Agencies Turn Retainers Into Recurring Software Revenue](https://digitalmarketingsnapshotforghl.com/blog/gohighlevel-saas-mode-recurring-revenue-for-agencies/)
- [12 Best GoHighLevel Alternatives in 2026](https://inflowave.io/resources/gohighlevel-alternatives-2026)
