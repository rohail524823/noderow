"""/missed-call-revenue-calculator/ — the first layer-1 acquisition asset.

Targets people who have the PROBLEM and do not yet know the tool. Autocomplete
confirms the demand: "missed call text back" returns software, calculator,
automation, service, roi calculator, ghl and software free.

The funnel: reader quantifies their own loss here, meets the mechanism, then lands
on the true-cost calculator to see what fixing it actually costs.

HONESTY CONSTRAINT: contains no industry statistics. Every rate is a reader input
with a labelled starting assumption, and the page says so in visible text.
"""

import html as html_mod
import json
import pathlib

import entity
from components import author_box, cta, inline_disclosure

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRICING = json.loads((ROOT / "content" / "pricing-data.json").read_text())

PATH = "/missed-call-revenue-calculator/"
TITLE = "Missed Call Revenue Calculator: What Unanswered Calls Cost You"
DESCRIPTION = (
    "Work out what unanswered phone calls cost your business each month, and "
    "whether automatic text-back would recover more than the software costs."
)

FAQ_ITEMS = [
    ("What is missed-call text-back?",
     "An automation that sends an SMS the moment a call goes unanswered — usually "
     "something like “Sorry we missed you, how can we help?” The caller replies by "
     "text and the conversation continues there instead of them phoning the next "
     "business on the list. It is a small piece of automation, not a product "
     "category, and several platforms include it."),
    ("How much does missed-call text-back cost to run?",
     "Two costs. The platform subscription, which starts at $97 a month on "
     "GoHighLevel's entry plan, and the SMS itself at $0.00747 a segment plus "
     "carrier surcharges of roughly $0.0042 more. At a few hundred missed calls a "
     "month the messaging cost is a few dollars; the subscription is the real line "
     "item."),
    ("Is the recovery rate in this calculator a real statistic?",
     "No, and that matters. It is an input with a starting value, not a measured "
     "figure. We have not run a controlled study and neither has anyone else "
     "publishing numbers on this. Treat any site quoting a precise recovery rate as "
     "an unsourced marketing claim until they show you the method."),
    ("Do I need software, or should I just answer the phone?",
     "If the calculator shows recovered revenue below the cost of the subscription, "
     "answer the phone. Automation is worth buying when the volume is high enough "
     "that a human genuinely cannot catch every call — not as a substitute for "
     "someone picking up during business hours."),
    ("Will texting people back annoy them?",
     "It can, if the message reads like a robot or arrives hours late. It works when "
     "it is immediate, plainly written, and a real person takes over the "
     "conversation. Automated follow-up also has to respect consent rules — in the "
     "US that means TCPA, and replying to an inbound call is a different situation "
     "from cold-texting a list."),
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


def build():
    faq_html, faq_schema = _faq()
    u = PRICING["usage"]
    rates_json = json.dumps(
        {"plans": [{"name": p["name"], "monthly": p["monthly"]}
                   for p in PRICING["plans"]]},
        separators=(",", ":"),
    )

    answer = """<div class="answer-block">
<p><strong>An unanswered phone call is not a lost call — it is a lost customer, and
only the share you would have closed actually costs you money.</strong> The
arithmetic is: calls per month, times the proportion you miss, times the rate you
close the ones you do answer, times what a customer is worth. A business taking 100
calls a week, missing a fifth of them, closing a third and worth $500 a customer is
losing roughly $14,400 a month. Automatic text-back — an SMS sent the moment a call
goes unanswered — is the usual fix, and it costs a subscription plus about
$0.01 per message once carrier fees are counted. The calculator below runs your own
numbers and tells you whether the recovery would exceed the software cost, or
whether you would be better off answering the phone.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Free calculator</p>
<h1>What are missed calls costing you?</h1>
</div>

{inline_disclosure()}

<div class="prose">
{answer}
</div>

<div id="mc" class="calc">
  <script type="application/json" id="mc-rates">{rates_json}</script>

  <form class="calc-inputs" aria-labelledby="mc-inputs-h">
    <h2 id="mc-inputs-h" class="calc-sub">Your numbers</h2>

    <div class="field">
      <label for="m-preset">Start from your trade</label>
      <select id="m-preset">
        <option value="">Choose a trade&hellip;</option>
        <option value="roofing">Roofing</option>
        <option value="hvac">HVAC</option>
        <option value="plumbing">Plumbing</option>
        <option value="electrical">Electrical</option>
        <option value="remodeling">Remodeling</option>
        <option value="other">Something else</option>
      </select>
    </div>
    <p class="field-note">Presets are starting points shaped by trade, not survey
    data. A roofing job is worth more than a drain unblock. Change every number to
    match your business.</p>

    <div class="field">
      <label for="m-calls">Inbound calls per week</label>
      <input id="m-calls" type="number" min="0" max="10000" step="5" value="100" inputmode="numeric">
    </div>
    <div class="field">
      <label for="m-missed">Percentage you miss</label>
      <input id="m-missed" type="number" min="0" max="100" step="1" value="20" inputmode="numeric">
    </div>
    <div class="field">
      <label for="m-value">What a customer is worth to you</label>
      <input id="m-value" type="number" min="0" max="1000000" step="50" value="500" inputmode="numeric">
    </div>
    <div class="field">
      <label for="m-close">Close rate on calls you <em>do</em> answer (%)</label>
      <input id="m-close" type="number" min="0" max="100" step="1" value="33" inputmode="numeric">
    </div>

    <h3 class="calc-sub calc-group">The assumption</h3>
    <div class="field">
      <label for="m-recovery">Percentage a text-back would recover (%)</label>
      <input id="m-recovery" type="number" min="0" max="100" step="1" value="30" inputmode="numeric">
    </div>
    <p class="field-note">This one is a guess, and it is yours to make. We have not
    measured it and nor has anyone else publishing figures on this. Move it up and
    down to see how much the case depends on it.</p>
  </form>

  <div class="calc-results" role="region" aria-live="polite" aria-atomic="true"
       aria-labelledby="mc-results-h">
    <h2 id="mc-results-h" class="sr-only">Your result</h2>
    <div id="mc-verdict" class="calc-verdict"></div>
    <div id="mc-out"></div>
  </div>

  <noscript>
    <p class="calc-noscript">The interactive calculator needs JavaScript. The
    arithmetic is written out below so you can do it on paper.</p>
  </noscript>
</div>

<div class="prose">
<h2 id="maths">The arithmetic, written out</h2>
<p>No black box. Four numbers and two multiplications:</p>
<ol>
<li>Calls a month = calls a week &times; 4.33</li>
<li>Missed calls = that &times; your miss rate</li>
<li><strong>Lost customers</strong> = missed calls &times; the rate you close
answered calls. This is the step most versions of this calculator skip, and skipping
it inflates the number badly — a missed call from someone who was never going to buy
costs you nothing.</li>
<li>Lost revenue = lost customers &times; customer value</li>
</ol>
<p>Recovery is then a fifth number you supply: what share of those you think a text
would win back. There is no defensible published figure for this, so the calculator
refuses to pick one for you.</p>

<h2 id="why">Why calls go unanswered</h2>
<p>In the businesses where this matters most — trades, clinics, salons, anything
where the person who answers the phone is also doing the work — the pattern is
consistent. Calls arrive while someone is on a roof, with a patient, or already on
another line. Nobody is being careless. The phone is simply not the thing they are
paid to hold.</p>
<p>Which is why "hire a receptionist" and "just answer it" are weaker answers than
they sound. The call arrives at the exact moment attention is elsewhere.</p>

<h2 id="mechanism">What text-back actually does</h2>
<p>The mechanism is unglamorous. A call comes in and goes unanswered. A workflow
fires and sends an SMS from the same number: an apology and an offer to help. The
caller replies by text, which they can do from the top of a ladder or a waiting
room, and the conversation continues there.</p>
<p>The value is not the message. It is that the caller stops dialling the next
business on their list. You have converted a lost call into a slow conversation
rather than a fast one.</p>
<p>It is a small automation, not a product category. Several platforms include it,
and the honest framing is that you are buying the platform, not the feature.</p>

<h2 id="cost">What it costs to run</h2>
<p>Two layers. The subscription, and the messages.</p>
<p>On GoHighLevel the entry plan is ${PRICING['plans'][0]['monthly']} a month. The
SMS itself is ${u['smsPerSegment']} per segment, plus a carrier surcharge of roughly
${u['carrierFees']['averageSmsOutbound']} that most pricing pages leave out — so
call it about a cent a message in practice.</p>
<p>At a few hundred missed calls a month the messaging is a rounding error and the
subscription is the real decision. That is worth knowing before anyone sells you on
per-message pricing as though it were the main cost.</p>

<h2 id="honest">When this is not worth automating</h2>
<p>If the calculator shows recovered revenue below the subscription, do not buy
software. Either your volume is too low, or your customer value is too low, or the
honest fix is that someone should answer the phone during business hours.</p>
<p>The same applies if you only miss calls out of hours and your customers are happy
to leave a voicemail. Automation earns its place when the volume genuinely exceeds
what a person can catch — not as a way to avoid picking up.</p>
<p>One legal note worth taking seriously: automated messaging in the US falls under
TCPA. Replying to someone who just called you is a different situation from texting
a purchased list, and the second one gets people sued.</p>

{faq_html}

<h2 id="next">If the numbers say yes</h2>
<p>The platform is the cost, not the feature. Before committing, work out what it
actually comes to at your volume — the subscription is only part of the bill, and
metered usage is where the surprises live.</p>
</div>

{cta("gohighlevel", "See GoHighLevel plans and pricing", placement="missed-calls-footer",
     dest="pricing",
     note="NodeRow earns a commission if you subscribe. It costs you nothing extra.")}

<div class="prose">
<h2 id="related">Related</h2>
<ul>
<li><a href="/gohighlevel-true-cost-calculator/">GoHighLevel true cost calculator</a>
&mdash; what the platform costs once usage is counted</li>
<li><a href="/gohighlevel-pricing-explained/">GoHighLevel pricing explained</a>
&mdash; every plan and metered rate, sourced and dated</li>
<li><a href="/build/">Have the automation built for you</a></li>
</ul>

{author_box()}
</div>

</div>
</section>
"""

    return {
        "path": PATH,
        "title": TITLE,
        "description": DESCRIPTION,
        "body": body,
        "trail": [("Home", "/"), ("Guides", "/guides/"),
                  ("Missed call revenue calculator", PATH)],
        "priority": "1.0",
        "scripts": ["/js/missed-calls.js"],
        "extra_schema": [
            entity.article(PATH, TITLE, DESCRIPTION,
                           published="2026-08-28", modified="2026-08-28"),
            faq_schema,
        ],
    }
