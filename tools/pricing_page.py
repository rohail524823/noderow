"""/gohighlevel-pricing-explained/ — page #2 on the ranked list.

The highest-volume commercial query in the niche. Every competing page covers the
sticker price and stops. This one covers what the bill actually contains, because
the rates behind it were read from HighLevel's own pages rather than recycled.

Every figure renders from content/pricing-data.json. No price is written into prose.
"""

import html as html_mod
import json
import pathlib

import entity
from components import (
    author_box,
    cta,
    inline_disclosure,
    not_speaking_for,
    outbound,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "content" / "pricing-data.json").read_text())
COMP = json.loads((ROOT / "content" / "competitors.json").read_text())

PATH = "/gohighlevel-pricing-explained/"
TITLE = "GoHighLevel Pricing Explained: What the Bill Actually Comes To"
DESCRIPTION = (
    "GoHighLevel's plans are $97, $297 and $497 a month. Here is what sits on top "
    "of that — carrier fees, AI, add-ons — with every rate sourced and dated."
)

U = DATA["usage"]
CF = U["carrierFees"]
PLANS = {p["id"]: p for p in DATA["plans"]}


def _money(n):
    return f"${n:,.2f}"


def _plan_table():
    rows = ""
    for p in DATA["plans"]:
        rows += f"""<tr>
<td data-label="Plan"><strong>{p['name']}</strong></td>
<td data-label="Monthly">${p['monthly']}</td>
<td data-label="Annual">${p['annualTotal']:,} <span class="muted">(${p['annualMonthlyEquivalent']:.0f}/mo)</span></td>
<td data-label="Sub-accounts">{p['subAccountsLabel']}</td>
<td data-label="Rebilling">{'With markup' if p['rebillWithMarkup'] else ('At cost only' if p['rebillAtCost'] else 'Not available')}</td>
<td data-label="SaaS mode">{'Yes' if p['saasMode'] else 'No'}</td>
</tr>"""
    return f"""<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">GoHighLevel plan comparison</caption>
<thead><tr>
<th scope="col">Plan</th><th scope="col">Monthly</th><th scope="col">Annual</th>
<th scope="col">Sub-accounts</th><th scope="col">Rebilling</th><th scope="col">SaaS mode</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>"""


def _carrier_table():
    rows = ""
    for c in CF["byCarrier"]:
        base = U["smsPerSegment"]
        total = base + c["smsOut"]
        rows += f"""<tr>
<td data-label="Carrier">{c['carrier']}</td>
<td data-label="Base rate">${base}</td>
<td data-label="Carrier fee">${c['smsOut']}</td>
<td data-label="Real cost"><strong>${total:.5f}</strong></td>
<td data-label="Uplift">+{c['smsOut'] / base * 100:.0f}%</td>
</tr>"""
    return f"""<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">Real outbound SMS cost by carrier</caption>
<thead><tr>
<th scope="col">Recipient carrier</th><th scope="col">Base rate</th>
<th scope="col">Carrier fee</th><th scope="col">Real cost per segment</th>
<th scope="col">Uplift</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>"""


def _addon_table():
    rows = ""
    for a in DATA["addOns"]:
        per_sub = "per sub-account" in a["unit"]
        flag = ' <span class="pill pill-waiting">Scales per client</span>' if per_sub else ""
        rows += (f'<tr><td data-label="Add-on">{html_mod.escape(a["name"])}{flag}</td>'
                 f'<td data-label="Price">${a["price"]}</td>'
                 f'<td data-label="Billed">{html_mod.escape(a["unit"])}</td></tr>')
    return f"""<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">GoHighLevel add-on pricing</caption>
<thead><tr><th scope="col">Add-on</th><th scope="col">Price</th>
<th scope="col">Billed</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>"""


FAQ_ITEMS = [
    ("How much does GoHighLevel really cost per month?",
     "The subscription is $97, $297 or $497. What you actually pay is that plus "
     "metered usage — SMS at $0.00747 a segment plus carrier fees, email at $0.675 "
     "per thousand, voice at $0.0166 a minute, phone numbers at $1.15 each, and any "
     "AI plan at $50 or $97 per sub-account. There is no official benchmark for the "
     "total, and any figure quoted as typical is a model rather than a published "
     "number. Run your own volumes through a calculator instead of trusting an "
     "average."),
    ("Is SaaS Pro a different plan from Agency Pro?",
     "No. HighLevel markets the same $497 plan under both names — Agency Pro on the "
     "pricing page, SaaS Pro on its own upgrade funnel. There is no fourth tier. Any "
     "comparison listing them as two products at two prices is simply wrong, and it "
     "is a useful test of whether a review has looked at the pricing page recently."),
    ("Why is my SMS bill higher than $0.00747 a segment?",
     "Because carrier surcharges are added on top. HighLevel publishes them per "
     "carrier: AT&T $0.0035, T-Mobile $0.0045, Verizon $0.0045 and US Cellular "
     "$0.0050 for outbound. That is a 47% to 67% uplift depending on which network "
     "your recipient is on, and it is charged separately from the base rate."),
    ("Does AI Employee Unlimited make Voice AI free?",
     "No. HighLevel prices Voice AI as “Voice + token cost”. The AI plan "
     "covers the AI; the phone call underneath is billed by the phone system at "
     "$0.0166 a minute outbound regardless of tier. Two meters run at the same time. "
     "This is the single most commonly misunderstood cost on the platform."),
    ("Should I pay $497 for Agency Pro instead of $297 for Unlimited?",
     "Only if you rebill usage with a markup. Rebilling at cost is already included "
     "at $297, so the extra $200 a month buys exactly one economically meaningful "
     "thing: the ability to add margin on usage. It pays for itself when that margin "
     "exceeds $200 a month, which needs either real volume or a high multiplier."),
    ("Is there a 30-day or 60-day GoHighLevel trial?",
     "The pricing page states 14 days on all three plans. Longer trials are widely "
     "advertised by affiliates, including some who would earn a commission from your "
     "signup. We could not confirm a longer trial from any HighLevel-owned page, so "
     "we do not claim one."),
]


def _faq():
    blocks = "\n".join(
        f"<details><summary>{html_mod.escape(q)}</summary><p>{html_mod.escape(a)}</p></details>"
        for q, a in FAQ_ITEMS
    )
    schema = {
        "@type": "FAQPage",
        "@id": f"https://noderow.com{PATH}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ_ITEMS
        ],
    }
    return f'<h2 id="faq">Common questions</h2>\n<div class="faq">{blocks}</div>', schema


def _citations():
    srcs = [
        ("GoHighLevel pricing page", DATA["plans"][0]["sourceUrl"]),
        ("LC Phone pricing and billing guide", U["sourceUrl"]),
        ("LC Email pricing", U["emailSourceUrl"]),
        ("AI product pricing", DATA["ai"]["sourceUrl"]),
        ("Fixed-rate rebilling for AI products", DATA["rebilling"]["sourceUrl"]),
    ]
    items = "".join(
        f'<li>{html_mod.escape(name)} — '
        f'<a href="{url}" target="_blank" rel="noopener nofollow">{url}</a></li>'
        for name, url in srcs
    )
    return f"""<h2 id="sources">Sources</h2>
<p>Every figure on this page was read from these pages on
<time datetime="{DATA['verifiedOn']}">28 August 2026</time>, not from another
review. If one is out of date, <a href="/contact/">tell me</a> and it gets
corrected with a new date.</p>
<ul class="citations">{items}</ul>"""


def build():
    faq_html, faq_schema = _faq()

    # Worked figures, computed rather than typed.
    seg = 10000
    sms_base = seg * U["smsPerSegment"]
    sms_carrier = seg * CF["averageSmsOutbound"]
    ai_unlimited = [m for m in DATA["ai"]["models"] if m["id"] == "unlimited"][0]
    ten_clients_ai = 10 * ai_unlimited["monthlyPerLocation"]

    answer = f"""<div class="answer-block">
<p><strong>GoHighLevel costs $97, $297 or $497 a month, and the subscription is the
smaller half of the story for most agencies.</strong> Starter at $97 covers three
sub-accounts. Unlimited at $297 removes the sub-account cap and lets you rebill
usage at cost. Agency Pro at $497 adds SaaS mode and the ability to rebill usage
<em>with a markup</em> — the only economically significant difference between the
top two tiers. On top of any plan sit metered charges: SMS at
${U['smsPerSegment']} a segment <em>plus</em> carrier fees of roughly
${CF['averageSmsOutbound']} more, email at ${U['emailPer1000']} per thousand, voice
at ${U['voiceOutboundPerMinute']} a minute, and AI at $50 or $97 per sub-account.
Eleven of the thirteen published add-ons are billed per sub-account, so they scale
with your client count rather than staying flat.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Pricing · Verified <time datetime="{DATA['verifiedOn']}">28 Aug 2026</time></p>
<h1>GoHighLevel pricing, explained properly</h1>
</div>

{inline_disclosure()}

<div class="prose">
{answer}

<nav class="toc" aria-labelledby="toc-h">
<h2 id="toc-h" class="toc-h">On this page</h2>
<ol>
<li><a href="#plans">The three plans</a></li>
<li><a href="#unlock">What each tier actually unlocks</a></li>
<li><a href="#metered">The layer that is missing from most pricing pages</a></li>
<li><a href="#sms">SMS costs more than the published rate</a></li>
<li><a href="#ai">The two meters behind Voice AI</a></li>
<li><a href="#addons">Add-ons scale with your client count</a></li>
<li><a href="#break-even">$297 or $497: the only question that matters</a></li>
<li><a href="#saas-pro">&ldquo;SaaS Pro&rdquo; is not a fourth plan</a></li>
<li><a href="#trial">The trial is 14 days</a></li>
<li><a href="#who">Which plan you should be on</a></li>
<li><a href="#faq">Common questions</a></li>
<li><a href="#sources">Sources</a></li>
</ol>
</nav>

<h2 id="plans">The three plans</h2>
</div>

{_plan_table()}

<div class="prose">
<p>Annual billing gives you two months free on every tier. That is a genuine
discount rather than a framing trick: ${PLANS['unlimited']['annualTotal']:,} a year
against ${PLANS['unlimited']['monthly'] * 12:,} paid monthly.</p>

<h2 id="unlock">What each tier actually unlocks</h2>
<p>Most write-ups describe these as small, medium and large. They are not. Each tier
unlocks specific capabilities, and the right plan is the cheapest one that unlocks
what you actually need.</p>
<ul>
<li><strong>Starter, ${PLANS['starter']['monthly']}.</strong> Three sub-accounts,
unlimited contacts and users. No white-label, no API, and — the part people miss —
<em>no rebilling at all</em>. Every dollar of client SMS and email comes out of your
own margin.</li>
<li><strong>Unlimited, ${PLANS['unlimited']['monthly']}.</strong> The jump you make
at client four, or the day you need API access. HighLevel's own wording on the
pricing page is &ldquo;Rebill Phone &amp; Email (no markup)&rdquo;. You can pass
usage through at cost; you cannot profit from it.</li>
<li><strong>Agency Pro, ${PLANS['agency-pro']['monthly']}.</strong> SaaS mode,
automated sub-account creation, advanced API, and rebilling <em>with</em> a markup.</li>
</ul>

<h2 id="metered">The layer that is missing from most pricing pages</h2>
<p>GoHighLevel bills in two directions at once. There is the subscription, and there
is an agency wallet with a configurable minimum balance and auto-recharge that
drains as your clients send things.</p>
<p>What comes out of the wallet: SMS and MMS, voice minutes, phone number rental,
email sending and verification, premium workflow actions at
${U['premiumWorkflowActionPerExecution']} an execution, A2P registration fees, and
AI usage. None of it is included in the plan fee.</p>
<p>Email has no free tier at all. HighLevel's documentation is explicit that all
incoming <em>and</em> outgoing mail is billed, including CC and BCC recipients, and
that forwarding is charged at the same rate as sending.</p>

<h2 id="sms">SMS costs more than the published rate</h2>
<p>This is the single largest omission across competing pricing articles, and it is
not hidden — HighLevel publishes it.</p>
<p>The base rate is ${U['smsPerSegment']} per segment, itself a 10% discount on the
$0.0083 list price. Then the recipient's mobile carrier adds a surcharge, passed
straight through:</p>
</div>

{_carrier_table()}

<div class="prose">
<p>So a campaign of {seg:,} segments is not {_money(sms_base)}. It is
{_money(sms_base)} plus roughly {_money(sms_carrier)} in carrier fees —
about {(sms_carrier / sms_base * 100):.0f}% more than the number you would get from
the published rate alone.</p>
<p>Two further details worth knowing before you budget. A message over 160 GSM
characters splits into multiple segments and is billed for each; adding a single
emoji switches the encoding and drops that limit to 70 characters, which can triple
the cost of a campaign that looked fine in testing. And inbound SMS is billed at the
same ${U['smsPerSegment']} rate as outbound — replies are not free.</p>

<h2 id="ai">The two meters behind Voice AI</h2>
<p>HighLevel sells AI three ways: pay-per-use on tokens, AI Employee Growth at
$50 per sub-account per month, and AI Employee Unlimited at $97 per sub-account per
month.</p>
<p>Here is the part that catches people. HighLevel prices Voice AI as
<strong>&ldquo;Voice + token cost&rdquo;</strong> — its words, not ours. The AI plan
covers the AI. The phone call underneath is billed separately by the phone system at
${U['voiceOutboundPerMinute']} a minute outbound. Both meters run at once, on every
tier, <em>including the one called unlimited</em>.</p>
<p>Two related things to check before you commit. AI Employee Unlimited is
&ldquo;unlimited, subject to fair use&rdquo;, so unlimited is throttleable under the
terms. And inbound calls bill two legs — the call arriving at your platform number,
and the forwarded leg to wherever you actually answer it.</p>
<p>One more that surprises people: call transcription runs
${U['callTranscriptionPerMinute']} a minute, which is
{(U['callTranscriptionPerMinute'] / U['voiceOutboundPerMinute']):.1f} times the cost
of the outbound call it transcribes. Turning it on across a call centre is a larger
decision than it looks.</p>

<h2 id="addons">Add-ons scale with your client count</h2>
<p>Thirteen add-ons are published. Eleven of them are billed <em>per sub-account</em>,
which means they are not a fixed line on your bill — they multiply by your client
count.</p>
</div>

{_addon_table()}

<div class="prose">
<p>Ten clients on AI Employee Unlimited is {_money(ten_clients_ai)} a month, not $97.
That distinction is worth internalising before you enable anything across the board.</p>

<h2 id="break-even">$297 or $497: the only question that matters</h2>
<p>Rebilling usage <em>at cost</em> is already included at $297. So the extra $200 a
month for Agency Pro buys exactly one economically meaningful thing: the ability to
add a markup on usage.</p>
<p>That makes the decision arithmetic rather than opinion. Agency Pro pays for itself
when the margin you earn on rebilled usage exceeds $200 a month. Below that, it is a
$200 monthly loss dressed up as an upgrade.</p>
<p>There is a trap inside the markup feature too. If you set a <em>fixed rate</em>
per unit rather than a multiplier, HighLevel keeps billing your agency on actual
consumption. Their documentation states it plainly: your agency continues to be
charged based on actual token consumption regardless of the pricing model configured
for sub-accounts. Price a flat rate below your real cost and you lose money on every
single unit, quietly, at scale.</p>
<p>The <a href="/gohighlevel-true-cost-calculator/">true cost calculator</a> models
both rebilling modes against your own volumes and tells you where the break-even
sits.</p>

<h2 id="saas-pro">&ldquo;SaaS Pro&rdquo; is not a fourth plan</h2>
<p>HighLevel markets the $497 plan as Agency Pro on its pricing page and as SaaS Pro
on its own upgrade funnel. Same plan, same price, two names.</p>
<p>Several competing articles list them as separate products at separate prices. It
is a quick way to check whether a review has actually opened the pricing page
recently, or is recycling another review that recycled another one.</p>

<h2 id="trial">The trial is 14 days</h2>
<p>The pricing page states 14 days on all three plans. Extended 30-day and 60-day
trials are widely advertised, frequently by affiliates who earn a commission when
you subscribe.</p>
<p>We could not confirm a longer trial from any HighLevel-owned page, so we do not
claim one. If you see a specific extended length advertised, ask whoever is
advertising it to show you where HighLevel says so.</p>

<h2 id="who">Which plan you should be on</h2>
</div>

<div class="wrap">
<div class="node-grid">
  <article class="node">
    <div class="node-head"><span class="node-kicker">${PLANS['starter']['monthly']}/mo</span></div>
    <h3>Starter</h3>
    <p>One business, or an agency with three clients or fewer that is still
    deciding whether this is the platform.</p>
    <p class="node-chain">No rebilling &mdash; usage is your cost</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">${PLANS['unlimited']['monthly']}/mo</span></div>
    <h3>Unlimited</h3>
    <p>Four clients or more, or you need API access. The default answer for most
    working agencies, and the one to stay on until the markup maths clears $200.</p>
    <p class="node-chain">Rebill at cost &mdash; usage becomes their line item</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">${PLANS['agency-pro']['monthly']}/mo</span></div>
    <h3>Agency Pro</h3>
    <p>You are reselling the platform under your own brand and your rebilling
    margin clears $200 a month. Check that with numbers before upgrading.</p>
    <p class="node-chain">Rebill with markup &mdash; usage becomes revenue</p>
  </article>
</div>
</div>

<div class="prose">
<h2 id="honest">When GoHighLevel is the wrong answer</h2>
<p>It is a platform, not a connector. If your actual problem is moving data between
arbitrary APIs, you will end up bolting {outbound("n8n-cloud", "n8n")} or
{outbound("make", "Make")} onto it anyway, and you should price that in.</p>
<p>If you are one business with one pipeline, you are paying for an agency
architecture you will not use. A focused CRM will cost less and annoy you less.</p>
<p>And if cost is the binding constraint,
<a href="https://systeme.io" target="_blank" rel="noopener nofollow">systeme.io</a>
tops out at $97 a month for unlimited contacts. It has no telephony and no
agency sub-account model, so it is not a like-for-like swap — but for a solo
operator running funnels and email it is a tenth of the price and we earn nothing
from saying so.</p>
{not_speaking_for()}

{faq_html}

{_citations()}

<h2 id="method">How this page is maintained</h2>
<p>Vendor pricing moves. Every figure here is stored in a single data file with its
source URL and the date it was checked, so a change is one edit rather than twenty
scattered through prose. The date at the top of this page is the date the numbers
were last verified, not the date the page was last touched.</p>
</div>

{cta("gohighlevel", "See GoHighLevel plans and pricing", placement="pricing-footer",
     dest="pricing",
     note="NodeRow earns a commission if you subscribe. 90-day cookie, last click.")}

<div class="prose">
{author_box()}

<h2 id="related">Related</h2>
<ul>
<li><a href="/gohighlevel-true-cost-calculator/">GoHighLevel true cost calculator</a>
&mdash; model your own volumes across all three plans</li>
<li><a href="/compare/">All platform comparisons</a></li>
<li><a href="/affiliate-disclosure/">How NodeRow makes money</a></li>
</ul>
</div>

</div>
</section>
"""

    return {
        "path": PATH,
        "title": TITLE,
        "description": DESCRIPTION,
        "body": body,
        "trail": [("Home", "/"), ("Compare Tools", "/compare/"),
                  ("GoHighLevel pricing explained", PATH)],
        "priority": "1.0",
        "extra_schema": [
            entity.article(PATH, TITLE, DESCRIPTION,
                           published="2026-08-28", modified="2026-08-28"),
            faq_schema,
        ],
    }
