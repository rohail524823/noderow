"""The GoHighLevel true-cost calculator page.

The flagship asset. Three things make it different from every competing
"GoHighLevel pricing" page:

1. It models all three cost layers (subscription + metered usage + AI), not just
   the sticker price.
2. It answers the one question agencies actually have — Unlimited at $297 or
   Agency Pro at $497 — with the rebilling break-even maths.
3. Every rate is dated and sourced on the page itself.

It is written to be complete with JavaScript disabled: the static worked example
and the full rate table are real content, not a fallback stub.
"""

import html as html_mod
import json
import pathlib

import entity
from components import author_box, cta, inline_disclosure, no_commission_callout

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "content" / "pricing-data.json").read_text())

PATH = "/gohighlevel-true-cost-calculator/"
TITLE = "GoHighLevel True Cost Calculator: Plan + Usage + AI"
DESCRIPTION = (
    "What GoHighLevel really costs once SMS, email and AI usage are added to the "
    "plan price, and whether the $497 Agency Pro upgrade pays for itself."
)


def _worked_example():
    """A concrete, checkable example that exists without JavaScript."""
    u = DATA["usage"]
    clients, sms, emails, ai = 10, 800, 4000, 300
    sms_cost = clients * sms * u["smsPerSegment"]
    email_cost = clients * emails / 1000 * u["emailPer1000"]
    ai_cost = clients * ai * u["aiConversationPerMessage"]
    usage = sms_cost + email_cost + ai_cost
    unlimited = 297 + usage
    return f"""<h2 id="worked-example">A worked example: 10 clients</h2>
<p>Ten sub-accounts, each sending 800 SMS segments, 4,000 emails and 300 AI
messages a month. That is a modest agency — not a heavy sender.</p>
<div class="table-scroll">
<table class="cmp">
<thead><tr><th scope="col">Line</th><th scope="col">Volume</th><th scope="col">Cost</th></tr></thead>
<tbody>
<tr><td data-label="Line">Unlimited plan</td>
    <td data-label="Volume">flat</td>
    <td data-label="Cost">$297.00</td></tr>
<tr><td data-label="Line">SMS segments</td>
    <td data-label="Volume">{clients * sms:,}</td>
    <td data-label="Cost">${sms_cost:,.2f}</td></tr>
<tr><td data-label="Line">Emails</td>
    <td data-label="Volume">{clients * emails:,}</td>
    <td data-label="Cost">${email_cost:,.2f}</td></tr>
<tr><td data-label="Line">AI messages</td>
    <td data-label="Volume">{clients * ai:,}</td>
    <td data-label="Cost">${ai_cost:,.2f}</td></tr>
<tr><td data-label="Line"><strong>Real monthly cost</strong></td>
    <td data-label="Volume">—</td>
    <td data-label="Cost"><strong>${unlimited:,.2f}</strong></td></tr>
</tbody>
</table>
</div>
<p>The plan price is ${297:,}. The bill is <strong>${unlimited:,.2f}</strong> —
about {(usage / 297 * 100):.0f}% more. That gap is the entire reason this
calculator exists, and it is the line most pricing articles leave out.</p>"""


def _rate_table():
    u = DATA["usage"]
    return f"""<h2 id="rates">The rates this uses</h2>
<p>Every figure below was checked on
<time datetime="{DATA['checkedDate']}">28 August 2026</time>. Prices move; if one
of these is stale, <a href="/contact/">tell me</a> and it gets corrected with a
new date.</p>
<div class="table-scroll">
<table class="cmp">
<thead><tr><th scope="col">Item</th><th scope="col">Rate</th><th scope="col">Notes</th></tr></thead>
<tbody>
<tr><td data-label="Item">Starter plan</td><td data-label="Rate">$97/mo</td>
    <td data-label="Notes">3 sub-accounts. ~$80/mo billed annually.</td></tr>
<tr><td data-label="Item">Unlimited plan</td><td data-label="Rate">$297/mo</td>
    <td data-label="Notes">Unlimited sub-accounts, API access, rebilling at cost. ~$247/mo annually.</td></tr>
<tr><td data-label="Item">Agency Pro</td><td data-label="Rate">$497/mo</td>
    <td data-label="Notes">Adds SaaS mode and rebilling <em>with markup</em>. ~$414/mo annually.</td></tr>
<tr><td data-label="Item">SMS</td><td data-label="Rate">${u['smsPerSegment']}/segment</td>
    <td data-label="Notes">{html_mod.escape(u['smsNote'])}</td></tr>
<tr><td data-label="Item">Email</td><td data-label="Rate">${u['emailPer1000']}/1,000</td>
    <td data-label="Notes">{html_mod.escape(u['emailNote'])}</td></tr>
<tr><td data-label="Item">Conversation AI</td><td data-label="Rate">${u['aiConversationPerMessage']}/message</td>
    <td data-label="Notes">{html_mod.escape(u['aiNote'])}</td></tr>
</tbody>
</table>
</div>
<aside class="callout" role="note">
<span class="callout-mark" aria-hidden="true">◆</span>
<div><strong>How these were verified.</strong>
<span>GoHighLevel's own pricing page could not be fetched directly from the
environment this site is built in, so every figure here was cross-checked against
multiple independent sources rather than read off the vendor page. Treat them as
well-corroborated, not authoritative — confirm against your own invoice before
making a five-figure decision.</span></div>
</aside>"""


def _faq():
    items = [
        ("Does GoHighLevel really cost more than the advertised price?",
         "Yes, for almost everyone. The plan fee is one of three layers. SMS, "
         "email, voice and AI are metered separately and drawn from a wallet that "
         "auto-recharges. A ten-client agency on the $297 plan commonly pays "
         "$370–$450 a month once usage is counted."),
        ("Is Agency Pro at $497 worth it over Unlimited at $297?",
         "Only if you rebill usage with a markup. Rebilling at cost is already "
         "available on Unlimited; the extra $200 a month buys the ability to add "
         "margin on top. So the upgrade pays for itself when your markup earns "
         "more than $200 a month — which needs either high usage or a high "
         "multiplier. Below that, it is a $200 monthly loss."),
        ("Why is an SMS billed per segment rather than per message?",
         "A message over 160 GSM characters is split into multiple segments and "
         "billed for each one. Adding an emoji switches the encoding and drops the "
         "limit to 70 characters, which can quietly triple the cost of a campaign "
         "that looked fine in testing."),
        ("Can I avoid the usage costs entirely?",
         "No, but you can pass them through. On Unlimited and above you can rebill "
         "usage to clients at cost, which makes it their line item rather than "
         "yours. Agencies that skip this are absorbing a variable cost against a "
         "fixed retainer, which is where margins quietly disappear."),
    ]
    blocks = "\n".join(
        f"<details><summary>{html_mod.escape(q)}</summary><p>{html_mod.escape(a)}</p></details>"
        for q, a in items
    )
    faq_schema = {
        "@type": "FAQPage",
        "@id": f"https://noderow.com{PATH}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }
    return f'<h2 id="faq">Questions</h2>\n<div class="faq">{blocks}</div>', faq_schema


def build():
    faq_html, faq_schema = _faq()
    rates_json = json.dumps(
        {"plans": DATA["plans"], "usage": DATA["usage"]}, separators=(",", ":")
    )

    # Answer block: front-loaded, names its subjects, carries concrete numbers,
    # and every claim in it appears again in the body below.
    answer = """<div class="answer-block">
<p><strong>GoHighLevel costs more than its advertised price for almost every
agency.</strong> The plans are $97 (Starter, 3 sub-accounts), $297 (Unlimited)
and $497 (Agency Pro) per month, but SMS, email, voice and AI are metered on top
of all three. SMS runs about $0.0079 per segment and email about $0.675 per
thousand, so a ten-client agency on the $297 plan typically pays $370–$450 a
month all in. The upgrade from Unlimited to Agency Pro is the decision that
matters most: rebilling usage <em>at cost</em> is already included at $297, and
the extra $200 a month only buys the ability to add a <em>markup</em> on top. It
pays for itself only when that markup earns more than $200 a month. The
calculator below models all three layers and tells you which plan is actually
cheapest at your volume.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Calculator · Updated <time datetime="{DATA['checkedDate']}">28 Aug 2026</time></p>
<h1>What GoHighLevel actually costs</h1>
</div>

<div class="prose">
{answer}
</div>

{inline_disclosure()}

<div id="calc" class="calc">
  <script type="application/json" id="calc-rates">{rates_json}</script>

  <form class="calc-inputs" aria-labelledby="calc-inputs-h">
    <h2 id="calc-inputs-h" class="calc-sub">Your numbers</h2>

    <div class="field">
      <label for="f-clients">Client sub-accounts</label>
      <input id="f-clients" type="number" min="1" max="500" step="1" value="10" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-sms">SMS segments per client, per month</label>
      <input id="f-sms" type="number" min="0" max="200000" step="50" value="800" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-email">Emails per client, per month</label>
      <input id="f-email" type="number" min="0" max="1000000" step="500" value="4000" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-ai">AI messages per client, per month</label>
      <input id="f-ai" type="number" min="0" max="200000" step="50" value="300" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-billing">Billing</label>
      <select id="f-billing">
        <option value="monthly">Monthly</option>
        <option value="annual">Annual (discounted)</option>
      </select>
    </div>
    <div class="field field-check">
      <label for="f-rebill">
        <input id="f-rebill" type="checkbox" checked>
        I rebill usage to clients
      </label>
    </div>
    <div class="field">
      <label for="f-markup">Rebilling markup (Agency Pro only)</label>
      <input id="f-markup" type="number" min="1" max="10" step="0.05" value="2" inputmode="decimal">
    </div>
  </form>

  <div class="calc-results" role="region" aria-live="polite" aria-atomic="true"
       aria-labelledby="calc-results-h">
    <h2 id="calc-results-h" class="sr-only">Your result</h2>
    <div id="calc-verdict" class="calc-verdict"></div>
    <div id="calc-out"></div>
  </div>

  <noscript>
    <p class="calc-noscript">The interactive calculator needs JavaScript. The
    worked example and full rate table below are the same maths, done by hand.</p>
  </noscript>
</div>

{cta("gohighlevel", "Start a GoHighLevel trial", placement="calculator-primary",
     note="14-day trial. NodeRow earns a commission if you subscribe.")}

<div class="prose">
{_worked_example()}

<h2 id="which-plan">Which plan you actually need</h2>
<p>Most of the advice on this is backwards. The tiers are not "small, medium,
large" — they unlock three specific capabilities, and the right plan is the
cheapest one that unlocks what you need.</p>
<ul>
<li><strong>Starter, $97.</strong> Three sub-accounts. Fine for a single business
or an agency with up to three clients. No API access, no white-label.</li>
<li><strong>Unlimited, $297.</strong> The jump you make at client four, or the
moment you need API access. Includes white-label and rebilling usage at cost.</li>
<li><strong>Agency Pro, $497.</strong> Buys exactly one economically meaningful
thing: the ability to rebill usage <em>with a markup</em>, plus SaaS mode for
selling the platform under your own brand.</li>
</ul>

<h2 id="break-even">The $297 vs $497 break-even</h2>
<p>This is the question worth getting right, and it is arithmetic rather than
opinion. Agency Pro costs $200 a month more. Rebilling at cost is already yours
at $297. So the only thing the extra $200 buys is margin on usage.</p>
<p>If your clients collectively generate $150 a month of usage and you mark it up
2&times;, you recover an extra $150 — you are $50 a month <em>worse off</em> on
Agency Pro. At $500 of usage and the same markup you recover an extra $500, and
the upgrade clears by $300. The calculator does this for your numbers; the short
version is that Agency Pro rarely pays below roughly $200 a month of billable
usage.</p>

<h2 id="what-this-ignores">What this calculator deliberately ignores</h2>
<p>It models recurring platform cost, not total cost of ownership. It does not
include your time migrating in, which is the single most underestimated cost of
switching platforms — budget days, not hours. It does not include phone number
rental, dedicated IPs, paid snapshots, or third-party tools you will still need.
And it assumes usage spreads evenly across sub-accounts, which real client rosters
never do.</p>
<p>If precision matters more than a fast estimate, take your last invoice and
work forward from it rather than from any calculator, including this one.</p>

{_rate_table()}

{faq_html}

<h2 id="honest-note">Should you buy it at all?</h2>
<p>GoHighLevel is worth it when you are running several clients who each need CRM,
pipelines, booking and messaging, and the alternative is stitching four
subscriptions together per client. The consolidation is real and the sub-account
model is genuinely good.</p>
<p>It is the wrong tool if you are one business with one pipeline — you are paying
for an agency architecture you will not use, and a focused CRM will cost less and
annoy you less. It is also the wrong tool if your actual problem is moving data
between arbitrary APIs. It is a platform, not a connector, and you will end up
bolting n8n or Make onto it anyway.</p>
{no_commission_callout("zapier")}
</div>

{author_box()}
</div>
</section>
"""

    return {
        "path": PATH,
        "title": TITLE,
        "description": DESCRIPTION,
        "body": body,
        "trail": [("Home", "/"), ("Compare Tools", "/compare/"),
                  ("GoHighLevel True Cost Calculator", PATH)],
        "priority": "1.0",
        "scripts": ["/js/calculator.js"],
        "extra_schema": [
            entity.article(
                PATH, TITLE, DESCRIPTION,
                published="2026-08-28", modified="2026-08-28",
            ),
            faq_schema,
        ],
    }
