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
    clients, sms, emails, voice, ai_voice = 10, 800, 4000, 200, 120
    sms_cost = clients * sms * u["smsPerSegment"]
    carrier_cost = clients * sms * u["carrierFees"]["averageSmsOutbound"]
    email_cost = clients * emails / 1000 * u["emailPer1000"]
    voice_cost = clients * voice * u["voiceOutboundPerMinute"]
    ai_phone = clients * ai_voice * u["voiceOutboundPerMinute"]
    ai_plan = clients * 97
    usage = sms_cost + carrier_cost + email_cost + voice_cost + ai_phone
    total = 297 + ai_plan + usage
    return f"""<h2 id="worked-example">A worked example: 10 clients</h2>
<p>Ten sub-accounts on the Unlimited plan with AI Employee Unlimited enabled. Each
sends 800 SMS segments and 4,000 emails, makes 200 voice minutes of ordinary calls,
and runs 120 minutes of Voice AI a month. Modest &mdash; not a heavy sender.</p>
<div class="table-scroll">
<table class="cmp">
<thead><tr><th scope="col">Line</th><th scope="col">Volume</th><th scope="col">Cost</th></tr></thead>
<tbody>
<tr><td data-label="Line">Unlimited plan</td><td data-label="Volume">flat</td>
    <td data-label="Cost">$297.00</td></tr>
<tr><td data-label="Line">AI Employee Unlimited</td>
    <td data-label="Volume">{clients} locations &times; $97</td>
    <td data-label="Cost">${ai_plan:,.2f}</td></tr>
<tr><td data-label="Line">SMS segments</td><td data-label="Volume">{clients * sms:,}</td>
    <td data-label="Cost">${sms_cost:,.2f}</td></tr>
<tr><td data-label="Line"><strong>Carrier surcharges on those segments</strong></td>
    <td data-label="Volume">{clients * sms:,}</td>
    <td data-label="Cost"><strong>${carrier_cost:,.2f}</strong></td></tr>
<tr><td data-label="Line">Emails</td><td data-label="Volume">{clients * emails:,}</td>
    <td data-label="Cost">${email_cost:,.2f}</td></tr>
<tr><td data-label="Line">Voice minutes</td><td data-label="Volume">{clients * voice:,}</td>
    <td data-label="Cost">${voice_cost:,.2f}</td></tr>
<tr><td data-label="Line"><strong>Phone minutes under Voice AI</strong></td>
    <td data-label="Volume">{clients * ai_voice:,}</td>
    <td data-label="Cost"><strong>${ai_phone:,.2f}</strong></td></tr>
<tr><td data-label="Line"><strong>Real monthly cost</strong></td>
    <td data-label="Volume">&mdash;</td>
    <td data-label="Cost"><strong>${total:,.2f}</strong></td></tr>
</tbody>
</table>
</div>
<p>The advertised price is $297. The bill is <strong>${total:,.2f}</strong>.</p>
<p>Two lines there are worth pausing on. The carrier surcharge adds
${carrier_cost:,.2f} on top of ${sms_cost:,.2f} of base SMS &mdash; a
{(carrier_cost / sms_cost * 100):.0f}% increase that HighLevel publishes and almost
nobody quotes.</p>
<p>And the phone-minutes line. Those {clients * ai_voice:,} phone minutes sit
<em>underneath</em> Voice AI and are billed by the phone system, not by the AI plan
&mdash; on every tier, including the one called unlimited. HighLevel prices Voice AI
as &ldquo;Voice + token cost&rdquo; in its own documentation. Two meters run at
once.</p>"""


def _rate_table():
    u = DATA["usage"]
    rows = [
        ("Starter", "$97/mo", "3 sub-accounts. $970/yr &mdash; two months free."),
        ("Unlimited", "$297/mo",
         "Unlimited sub-accounts, API, rebilling at cost. $2,970/yr."),
        ("Agency Pro", "$497/mo",
         "Adds SaaS mode and rebilling <em>with markup</em>. $4,970/yr. HighLevel "
         "also markets this as &ldquo;SaaS Pro&rdquo; on its own upgrade funnel &mdash; "
         "it is the same plan, not a separate fourth tier."),
        ("SMS", f"${u['smsPerSegment']}/segment", html_mod.escape(u["smsNote"])),
        ("Email", f"${u['emailPer1000']}/1,000", html_mod.escape(u["emailNote"])),
        ("SMS carrier surcharge",
         f"~${u['carrierFees']['averageSmsOutbound']}/segment",
         html_mod.escape(u["carrierFees"]["note"])),
        ("Voice, outbound US", f"${u['voiceOutboundPerMinute']}/min",
         html_mod.escape(u["voiceOutboundBreakdown"])),
        ("Voice, inbound", f"${u['voiceInboundPerMinute']}/min",
         html_mod.escape(u["voiceTwoLegNote"])),
        ("Call transcription", f"${u['callTranscriptionPerMinute']}/min",
         html_mod.escape(u["transcriptionNote"])),
        ("Phone number", f"${u['localNumberPerMonth']}/mo",
         f"Local number rental. Toll-free is ${u['tollFreeNumberPerMonth']}/mo."),
        ("Premium workflow actions",
         f"${u['premiumWorkflowActionPerExecution']}/execution",
         html_mod.escape(u["premiumWorkflowNote"])),
        ("AI Employee Growth", "$50/mo per location",
         "Includes 1,000 Conversation AI responses and 100 Voice AI minutes."),
        ("AI Employee Unlimited", "$97/mo per location",
         "Unlimited Conversation and Voice AI, subject to a fair-use clause."),
    ]
    body = "".join(
        f'<tr><td data-label="Item">{name}</td><td data-label="Rate">{rate}</td>'
        f'<td data-label="Notes">{note}</td></tr>'
        for name, rate, note in rows
    )
    unverified = "".join(f"<li>{html_mod.escape(x)}</li>" for x in DATA["unverified"])
    return f"""<h2 id="rates">The rates this uses</h2>
<p>Every figure below carries the date it was checked:
<time datetime="{DATA['verifiedOn']}">28 August 2026</time>. Prices move. If one is
stale, <a href="/contact/">tell me</a> and it gets corrected with a new date.</p>
<div class="table-scroll">
<table class="cmp">
<thead><tr><th scope="col">Item</th><th scope="col">Rate</th><th scope="col">Notes</th></tr></thead>
<tbody>{body}</tbody>
</table>
</div>

<aside class="callout" role="note">
<span class="callout-mark" aria-hidden="true">&#9670;</span>
<div><strong>How these were verified.</strong>
<span>Every figure above was read directly from HighLevel&rsquo;s own pricing page
and help-centre billing articles on 28 August 2026 &mdash; not from a secondary
source or another review. The source URL for each block is recorded in this
site&rsquo;s pricing data file. Vendor pricing still moves, so check your own
invoice before making a five-figure decision.</span></div>
</aside>

<h3 id="unverified">What this deliberately does not claim</h3>
<p>The following circulate widely in GoHighLevel content and none could be confirmed
against a primary source. They are absent from the calculator rather than
estimated:</p>
<ul>{unverified}</ul>"""


def _faq():
    items = [
        ("Does GoHighLevel really cost more than the advertised price?",
         "Yes, for almost everyone. The plan fee is one layer of several. SMS, "
         "email, voice, phone number rental, premium workflow actions and AI are "
         "metered separately and drawn from an agency wallet that auto-recharges. "
         "There is no official benchmark for the total, and any figure you see "
         "quoted as typical is a model rather than a published number."),
        ("Do Voice AI minutes include the phone call?",
         "No, and this is the most commonly misunderstood cost on the platform. "
         "Voice AI is billed by the AI product; the call underneath is billed by "
         "LC Phone at $0.0166 a minute outbound. Both meters run at the same time, "
         "on every tier, including AI Employee Unlimited. An \u201cunlimited\u201d "
         "AI plan does not make the telephony free."),
        ("Is Agency Pro at $497 worth it over Unlimited at $297?",
         "Only if you rebill usage with a markup. Rebilling at cost is already "
         "available on Unlimited, so the extra $200 a month buys the ability to add "
         "margin on top and nothing else that is economically significant. It pays "
         "for itself when that margin exceeds $200 a month."),
        ("What is the flat-rate rebilling trap?",
         "If you charge sub-accounts a fixed rate per unit, HighLevel still bills "
         "your agency on actual consumption. Their own documentation says so: your "
         "agency is charged based on actual token consumption regardless of the "
         "pricing model configured for sub-accounts. Set the flat rate below real "
         "cost and you lose money on every unit, silently, at scale."),
        ("Why is an SMS billed per segment rather than per message?",
         "A message over 160 GSM characters splits into multiple segments and is "
         "billed for each. Adding a single emoji switches the encoding and drops "
         "the limit to 70 characters, which can quietly triple the cost of a "
         "campaign that looked fine in testing."),
        ("Is \u201cSaaS Pro\u201d a separate plan from Agency Pro?",
         "No. HighLevel uses SaaS Pro as an alternate marketing label for the same "
         "$497 Agency Pro plan on its own upgrade funnel. Any comparison listing "
         "them as two products at two prices is factually wrong."),
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
    # The calculator swaps its CTA to match whichever plan the reader's own
    # numbers just recommended. Each destination carries its own campaign id, so
    # this is about being paid correctly as much as about relevance.
    import components as _c
    link_map = {
        key: {"url": _c.resolve_link("gohighlevel", key)[0],
              "id": _c.resolve_link("gohighlevel", key)[1]}
        for key in ("pricing", "annual", "saas-pro", "bootcamp")
    }
    rates_json = json.dumps(
        {
            "plans": DATA["plans"],
            "usage": DATA["usage"],
            "ai": DATA["ai"],
            "rebilling": DATA["rebilling"],
            "links": link_map,
        },
        separators=(",", ":"),
    )

    # Answer block: front-loaded, names its subjects, carries concrete numbers,
    # and every claim in it appears again in the body below.
    answer = """<div class="answer-block">
<p><strong>GoHighLevel costs more than its advertised price for almost every
agency.</strong> The plans are $97 (Starter, 3 sub-accounts), $297 (Unlimited) and
$497 (Agency Pro) per month, but SMS, email, voice, phone numbers, premium workflow
actions and AI are all metered on top of every tier. SMS runs $0.00747 per segment,
email $0.675 per thousand, and outbound US voice $0.0166 a minute. Two costs catch
people out. First, Voice AI minutes do not include the phone call underneath &mdash;
LC Phone bills those separately even on the plan named &ldquo;unlimited&rdquo;, so
two meters run at once. Second, rebilling usage <em>at cost</em> is already included
at $297, so Agency Pro&rsquo;s extra $200 a month buys only the ability to add a
<em>markup</em>, and pays for itself only when that markup earns more than $200. The
calculator below models every layer at your own volume.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Calculator · Updated <time datetime="{DATA['verifiedOn']}">28 Aug 2026</time></p>
<h1>What GoHighLevel actually costs</h1>
</div>

{inline_disclosure()}

<div class="prose">
{answer}
</div>

<div id="calc" class="calc">
  <script type="application/json" id="calc-rates">{rates_json}</script>

  <form class="calc-inputs" aria-labelledby="calc-inputs-h">
    <h2 id="calc-inputs-h" class="calc-sub">Your numbers</h2>

    <div class="field">
      <label for="f-clients">Client sub-accounts</label>
      <input id="f-clients" type="number" min="1" max="500" step="1" value="10" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-sms">SMS segments per client / month</label>
      <input id="f-sms" type="number" min="0" max="200000" step="50" value="800" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-email">Emails per client / month</label>
      <input id="f-email" type="number" min="0" max="1000000" step="500" value="4000" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-voice">Voice minutes per client / month</label>
      <input id="f-voice" type="number" min="0" max="100000" step="50" value="200" inputmode="numeric">
    </div>
    <div class="field field-check">
      <label for="f-carrier">
        <input id="f-carrier" type="checkbox" checked>
        Include carrier surcharges
      </label>
    </div>
    <div class="field">
      <label for="f-numbers">Phone numbers per client</label>
      <input id="f-numbers" type="number" min="0" max="100" step="1" value="1" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-premium">Premium workflow actions per client / month</label>
      <input id="f-premium" type="number" min="0" max="500000" step="100" value="500" inputmode="numeric">
    </div>

    <h3 class="calc-sub calc-group">AI</h3>
    <div class="field">
      <label for="f-ai-model">AI plan</label>
      <select id="f-ai-model">
        <option value="pay-per-use">Pay-per-use (token billed)</option>
        <option value="growth">AI Employee Growth &mdash; $50/location</option>
        <option value="unlimited">AI Employee Unlimited &mdash; $97/location</option>
      </select>
    </div>
    <div class="field">
      <label for="f-ai-msgs">Conversation AI messages per client / month</label>
      <input id="f-ai-msgs" type="number" min="0" max="500000" step="100" value="1200" inputmode="numeric">
    </div>
    <div class="field">
      <label for="f-ai-voice">Voice AI minutes per client / month</label>
      <input id="f-ai-voice" type="number" min="0" max="100000" step="10" value="120" inputmode="numeric">
    </div>
    <p id="ai-sub-note" class="field-note">Phone minutes are billed separately from
    Voice AI, even on an unlimited AI plan. Both meters run.</p>

    <h3 class="calc-sub calc-group">Billing and rebilling</h3>
    <div class="field">
      <label for="f-billing">Billing</label>
      <select id="f-billing">
        <option value="monthly">Monthly</option>
        <option value="annual">Annual (two months free)</option>
      </select>
    </div>
    <div class="field field-check">
      <label for="f-rebill">
        <input id="f-rebill" type="checkbox" checked>
        I rebill usage to clients
      </label>
    </div>
    <div class="field">
      <label for="f-rebill-mode">Rebilling model</label>
      <select id="f-rebill-mode">
        <option value="multiplier">Multiplier (cost &times; N)</option>
        <option value="fixed-rate">Fixed rate per unit</option>
      </select>
    </div>
    <div class="field">
      <label for="f-markup">Markup multiplier</label>
      <input id="f-markup" type="number" min="1" max="10" step="0.05" value="2" inputmode="decimal">
    </div>
    <div class="field" hidden>
      <label for="f-flat">Flat rate charged per billable unit</label>
      <input id="f-flat" type="number" min="0" max="5" step="0.001" value="0.02" inputmode="decimal">
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

<div class="calc-cta" id="calc-cta">
{cta("gohighlevel", "See GoHighLevel plans and pricing", placement="calculator-primary",
     dest="pricing",
     note="NodeRow earns a commission if you subscribe. 90-day cookie, last click.")}
</div>

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
