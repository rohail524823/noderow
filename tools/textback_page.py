"""/missed-call-text-back/ — the layer-2 bridge page.

The reader knows the MECHANISM but not the product. Autocomplete confirms the exact
term: "missed call text back" returns software, calculator, automation, service,
roi calculator, ghl and software free.

Sits between the problem calculator (layer 1) and the pricing pages (layer 3).
"""

import html as html_mod
import json
import pathlib

import entity
from components import author_box, cta, inline_disclosure, not_speaking_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "content" / "pricing-data.json").read_text())
U = P["usage"]
CF = U["carrierFees"]

PATH = "/missed-call-text-back/"
TITLE = "Missed Call Text Back: How It Works and What It Costs"
DESCRIPTION = (
    "What missed-call text-back actually does, the real per-message cost including "
    "carrier fees, and when answering the phone is the better answer."
)

FAQ_ITEMS = [
    ("What is missed call text back?",
     "An automation that fires when an inbound call goes unanswered and sends the "
     "caller an SMS from the same number — typically an apology and an offer to "
     "help. The caller replies by text and the conversation continues there. It is "
     "a workflow, not a product category, and most CRM platforms with a phone "
     "system can do it."),
    ("How much does missed call text back cost per message?",
     "About a cent. On GoHighLevel the base rate is $0.00747 per SMS segment, and "
     "the recipient's carrier adds a surcharge on top — $0.0035 for AT&T, $0.0045 "
     "for T-Mobile and Verizon, $0.0050 for US Cellular. So roughly $0.011 to "
     "$0.012 per message in practice. The subscription is the real cost, not the "
     "messages."),
    ("Is there free missed call text back software?",
     "Not meaningfully. Some phone systems include a basic version, but anything "
     "that also stores the conversation, routes it to a person and tracks whether "
     "the lead converted needs a CRM behind it, and those start around $97 a month. "
     "A free tool that texts and forgets solves the smaller half of the problem."),
    ("Does the reply come from my real business number?",
     "It should. If the text arrives from a different number the caller has no "
     "reason to trust it, and replies land somewhere nobody reads. This is why the "
     "feature is normally tied to a platform that owns your phone number rather "
     "than a bolt-on."),
    ("Is automated texting legal?",
     "In the US it falls under TCPA. Replying to someone who has just called you is "
     "a very different situation from texting a purchased list, and the second one "
     "is what gets businesses sued. Sending SMS at any volume in the US also "
     "requires A2P 10DLC registration, which takes time and carries its own fees."),
    ("How fast does the text need to go out?",
     "Immediately. The entire value is catching the caller before they dial the "
     "next business on their list. A text that arrives an hour later is a follow-up, "
     "not a save, and it competes with whoever already answered."),
]


def _faq():
    blocks = "\n".join(
        f"<details><summary>{html_mod.escape(q)}</summary><p>{html_mod.escape(a)}</p></details>"
        for q, a in FAQ_ITEMS)
    schema = {
        "@type": "FAQPage",
        "@id": f"https://noderow.com{PATH}#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in FAQ_ITEMS],
    }
    return f'<h2 id="faq">Common questions</h2>\n<div class="faq">{blocks}</div>', schema


def _cost_table():
    rows = ""
    for c in CF["byCarrier"]:
        total = U["smsPerSegment"] + c["smsOut"]
        rows += (f'<tr><td data-label="Carrier">{c["carrier"]}</td>'
                 f'<td data-label="Base">${U["smsPerSegment"]}</td>'
                 f'<td data-label="Carrier fee">${c["smsOut"]}</td>'
                 f'<td data-label="Real cost"><strong>${total:.5f}</strong></td></tr>')
    return f"""<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">Real cost per SMS segment by recipient carrier</caption>
<thead><tr><th scope="col">Recipient carrier</th><th scope="col">Base rate</th>
<th scope="col">Carrier fee</th><th scope="col">Real cost per segment</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>"""


def build():
    faq_html, faq_schema = _faq()
    per_msg_low = U["smsPerSegment"] + 0.0035
    per_msg_high = U["smsPerSegment"] + 0.005
    monthly_200 = 200 * (U["smsPerSegment"] + CF["averageSmsOutbound"])

    answer = f"""<div class="answer-block">
<p><strong>Missed-call text-back is a workflow, not a product: when an inbound call
goes unanswered, an SMS goes out from the same number offering to help, and the
conversation moves to text.</strong> The point is not the message. It is that the
caller stops dialling the next business on their list. Running it costs two things —
a platform subscription starting around $97 a month, and the message itself at
${U['smsPerSegment']} per segment plus a carrier surcharge of $0.0035 to $0.005,
so roughly ${per_msg_low:.4f}&ndash;${per_msg_high:.4f} each. At 200 missed calls a
month the messaging comes to about ${monthly_200:.2f}; the subscription is the real
decision. It is worth automating when your call volume genuinely exceeds what a
person can catch, and not before.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">How it works · Verified <time datetime="{P['verifiedOn']}">28 Aug 2026</time></p>
<h1>Missed call text back, explained</h1>
</div>

{inline_disclosure()}

<div class="prose">
{answer}

<nav class="toc" aria-labelledby="toc-h">
<h2 id="toc-h" class="toc-h">On this page</h2>
<ol>
<li><a href="#what">What actually happens</a></li>
<li><a href="#cost">What it costs per message</a></li>
<li><a href="#platform">Why the subscription is the real cost</a></li>
<li><a href="#a2p">The registration nobody warns you about</a></li>
<li><a href="#wrong">When it does not work</a></li>
<li><a href="#faq">Common questions</a></li>
</ol>
</nav>

<h2 id="what">What actually happens</h2>
<p>Four steps, and none of them are clever:</p>
<ol>
<li>A call comes into your business number and nobody picks up.</li>
<li>The phone system fires a trigger on the missed-call event.</li>
<li>A workflow sends an SMS <em>from that same number</em> — something like
&ldquo;Sorry we missed your call, what can we help with?&rdquo;</li>
<li>The caller replies by text. That reply lands in an inbox a human actually
watches, and the conversation continues.</li>
</ol>
<p>Step three is where most cheap implementations fail. If the text arrives from a
different number, the caller has no reason to trust it and their reply goes
somewhere nobody reads.</p>
<p>Step four is where most <em>expensive</em> implementations fail. A text that
starts a conversation nobody answers is worse than no text, because now you have
annoyed someone who was already trying to give you money.</p>

<h2 id="cost">What it costs per message</h2>
<p>The base rate is ${U['smsPerSegment']} per segment. The recipient's mobile
carrier then adds a surcharge, passed straight through and published per carrier:</p>
</div>

{_cost_table()}

<div class="prose">
<p>So call it a cent a message. At 200 missed calls a month that is
${monthly_200:.2f} in messaging — genuinely trivial.</p>
<p>Two things inflate it if you are careless. A message over 160 GSM characters
splits into multiple segments and bills for each, and a single emoji switches the
encoding and drops that limit to 70 characters. Keep the text short and plain and
you stay at one segment.</p>

<h2 id="platform">Why the subscription is the real cost</h2>
<p>Nobody sells missed-call text-back on its own for long, because on its own it is
half a feature. To be useful it needs a phone number it controls, a place the reply
lands, a person assigned to answer, and a record of whether the lead converted.
That is a CRM.</p>
<p>On GoHighLevel that is ${P['plans'][0]['monthly']} a month for the entry plan.
The messaging is a rounding error next to it. Which means the honest question is not
&ldquo;is text-back worth a cent a message&rdquo; — it obviously is — but
&ldquo;is the platform worth ${P['plans'][0]['monthly']} a month to me&rdquo;.</p>
<p>Work that out with your own numbers on the
<a href="/missed-call-revenue-calculator/">missed-call revenue calculator</a>. If
the recovered revenue does not clear the subscription with room to spare, the answer
is no.</p>

<h2 id="a2p">The registration nobody warns you about</h2>
<p>Sending application-to-person SMS in the US requires A2P 10DLC registration:
your brand and campaign have to be registered with The Campaign Registry before
carriers will reliably deliver your messages.</p>
<p>There are fees — for a sole proprietor, up to
${P['a2p']['soleProprietor']['oneTimeRegistrationMax']} one-time and up to
${P['a2p']['soleProprietor']['monthlyCampaignFeeMax']} a month per campaign, with a
{P['a2p']['soleProprietor']['dailySegmentLimit']:,}-segment daily cap. There is also
a waiting period, and campaigns get rejected for fixable but non-obvious reasons.</p>
<p>Budget for this before you promise anyone a launch date. It is the single most
common reason a text-back rollout slips.</p>

<h2 id="wrong">When it does not work</h2>
<p>Three situations where this is the wrong purchase:</p>
<ul>
<li><strong>Your volume is low.</strong> If you miss a handful of calls a week, the
recovered revenue will not cover a subscription. Answer the phone.</li>
<li><strong>Your customers do not text.</strong> Some demographics and some B2B
buyers will not engage over SMS, and a text to them is noise.</li>
<li><strong>Nobody is going to answer the replies.</strong> The automation opens
conversations; it does not have them. If there is no one to pick those up within
minutes, you have automated a way to disappoint people faster.</li>
</ul>
<p>The honest version of the pitch is narrow: this is worth buying when your call
volume genuinely exceeds what a person can catch, and someone is ready to take over
the conversation the moment it starts.</p>

{faq_html}

{not_speaking_for()}
</div>

{cta("gohighlevel", "See GoHighLevel plans and pricing", placement="textback-footer",
     dest="pricing",
     note="NodeRow earns a commission if you subscribe. It costs you nothing extra.")}

<div class="prose">
<h2 id="related">Related</h2>
<ul>
<li><a href="/missed-call-revenue-calculator/">What are missed calls costing you?</a>
&mdash; run your own numbers first</li>
<li><a href="/crm-for-contractors/">CRM for contractors</a> &mdash; what home
services businesses actually need</li>
<li><a href="/gohighlevel-pricing-explained/">GoHighLevel pricing explained</a></li>
</ul>

{author_box()}
</div>

</div>
</section>
"""

    return {
        "path": PATH, "title": TITLE, "description": DESCRIPTION, "body": body,
        "trail": [("Home", "/"), ("Guides", "/guides/"),
                  ("Missed call text back", PATH)],
        "priority": "0.9",
        "extra_schema": [
            entity.article(PATH, TITLE, DESCRIPTION,
                           published="2026-08-28", modified="2026-08-28"),
            faq_schema,
        ],
    }
