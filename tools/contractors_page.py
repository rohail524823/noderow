"""/crm-for-contractors/ — the home-services vertical page.

Autocomplete confirms the cluster: "crm for contractors" branches into electrical,
general, roofing, government and free.

The differentiating argument, which nobody selling either product makes: field
service software and a marketing CRM are not substitutes. Housecall Pro runs the
job; GoHighLevel runs the lead. Saying so costs us a conversion and buys the
credibility that makes every other recommendation believable.
"""

import html as html_mod
import json
import pathlib

import entity
from components import author_box, cta, inline_disclosure, not_speaking_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "content" / "pricing-data.json").read_text())
C = json.loads((ROOT / "content" / "competitors.json").read_text())
BY = {x["slug"]: x for x in C["competitors"]}
HCP = BY["housecall-pro"]

PATH = "/crm-for-contractors/"
TITLE = "CRM for Contractors: What Home Services Businesses Actually Need"
DESCRIPTION = (
    "Field service software and a marketing CRM do different jobs. What each one "
    "covers, what it costs, and why many contractors end up paying for both."
)

FAQ_ITEMS = [
    ("What is the difference between field service software and a CRM?",
     "Field service software runs the work: scheduling, dispatch, routing, "
     "invoicing, job costing. A marketing CRM runs the lead: capturing enquiries, "
     "following up, nurturing, booking and asking for reviews. Housecall Pro is the "
     "first kind. GoHighLevel is the second. They overlap at the edges and neither "
     "replaces the other."),
    ("Do I need both?",
     "Many contractors do, and most comparison articles will not tell you that "
     "because they are selling one of them. If your problem is that jobs are chaotic "
     "once booked, you need field service software. If your problem is that leads go "
     "cold before they book, you need a marketing CRM. If both are true, you are "
     "looking at roughly $156 to $246 a month combined before usage."),
    ("What is the cheapest CRM for a small contractor?",
     "For lead follow-up specifically, GoHighLevel's entry plan is $97 a month, and "
     "systeme.io does email and funnels for $17 to $97 with no phone system at all. "
     "For job management, Housecall Pro starts at $59 a month billed annually. "
     "Cheapest overall depends entirely on which problem you actually have."),
    ("Does GoHighLevel do job scheduling and invoicing?",
     "It has calendars, booking and basic invoicing, and for a one-van operation "
     "that can be enough. It does not do dispatch, crew routing, or job costing. If "
     "you are sequencing multiple crews across a service area, that gap is the whole "
     "decision."),
    ("Is a CRM worth it for a one-person contracting business?",
     "Often not, at first. If you answer your own phone and remember every job, a "
     "CRM is overhead. It starts paying when you are missing calls while on site, or "
     "when quotes go out and never get followed up. That is a volume threshold, not "
     "a business-size one."),
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


def _split_table():
    rows = [
        ("Capturing an enquiry from a form or ad", "Marketing CRM", "yes", "partial"),
        ("Texting back a missed call", "Marketing CRM", "yes", "partial"),
        ("Following up a quote that went quiet", "Marketing CRM", "yes", "partial"),
        ("Asking for a Google review after the job", "Marketing CRM", "yes", "yes"),
        ("Booking the appointment", "Either", "yes", "yes"),
        ("Scheduling and dispatching a crew", "Field service", "no", "yes"),
        ("Routing jobs to cut drive time", "Field service", "no", "yes"),
        ("Job costing and materials", "Field service", "no", "yes"),
        ("Invoicing and payments", "Either", "partial", "yes"),
    ]
    def cell(v):
        if v == "yes":
            return '<td data-label="GoHighLevel" class="yes">Yes</td>'
        if v == "no":
            return '<td data-label="GoHighLevel" class="no">No</td>'
        return '<td data-label="GoHighLevel">Partial</td>'
    body = ""
    for job, owner, ghl, fs in rows:
        body += (f'<tr><td data-label="The job">{job}</td>'
                 f'<td data-label="Whose job">{owner}</td>'
                 f'{cell(ghl)}'
                 f'{cell(fs).replace("GoHighLevel", "Field service")}</tr>')
    return f"""<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">Which tool covers which job</caption>
<thead><tr><th scope="col">The job</th><th scope="col">Whose job it is</th>
<th scope="col">GoHighLevel</th><th scope="col">Field service software</th></tr></thead>
<tbody>{body}</tbody>
</table>
</div>"""


def build():
    faq_html, faq_schema = _faq()
    ghl = P["plans"][0]["monthly"]
    hcp_low = HCP["tiers"][0]["monthlyAnnualBilled"]
    hcp_high = HCP["tiers"][1]["monthlyAnnualBilled"]

    answer = f"""<div class="answer-block">
<p><strong>Most &ldquo;best CRM for contractors&rdquo; articles compare tools that
do not actually compete.</strong> Field service software — Housecall Pro, Jobber and
similar — runs the work: scheduling, dispatch, routing, invoicing, job costing.
Housecall Pro starts at ${hcp_low} a month billed annually, rising to ${hcp_high}
for five users with ${HCP['tiers'][1]['additionalUserMonthly']} a month per user
after that. A marketing CRM like GoHighLevel, at ${ghl} a month, runs the lead
instead: capturing enquiries, texting back missed calls, chasing quotes that went
quiet, and asking for reviews. Neither replaces the other, and plenty of contractors
end up paying for both — roughly ${ghl + hcp_low} to ${ghl + hcp_high} a month
before usage. Which one you need depends on where work is actually leaking: before
the booking, or after it.</p>
</div>"""

    body = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Home services · Verified <time datetime="{P['verifiedOn']}">28 Aug 2026</time></p>
<h1>CRM for contractors: what you actually need</h1>
</div>

{inline_disclosure()}

<div class="prose">
{answer}

<nav class="toc" aria-labelledby="toc-h">
<h2 id="toc-h" class="toc-h">On this page</h2>
<ol>
<li><a href="#two-tools">The two different tools everyone conflates</a></li>
<li><a href="#which">Which job belongs to which tool</a></li>
<li><a href="#leak">Find out where work is leaking first</a></li>
<li><a href="#cost">What each one costs</a></li>
<li><a href="#trade">It differs by trade</a></li>
<li><a href="#skip">When you need neither</a></li>
<li><a href="#faq">Common questions</a></li>
</ol>
</nav>

<h2 id="two-tools">The two different tools everyone conflates</h2>
<p>Search for a contractor CRM and you get a list mixing Housecall Pro, Jobber,
ServiceTitan, GoHighLevel, HubSpot and Pipedrive as though they are interchangeable.
They are not, and the confusion costs people money in both directions — buying
dispatch software to fix a follow-up problem, or a marketing CRM to fix a scheduling
problem.</p>
<p>The split is clean once you see it. <strong>Field service software owns the job.
A marketing CRM owns the lead.</strong> The handoff between them is the booking.</p>
<p>Everything before the booking — the enquiry, the missed call, the quote nobody
chased, the review request three days later — is CRM territory. Everything after it
— who is driving where, what materials, what invoice — is field service territory.</p>

<h2 id="which">Which job belongs to which tool</h2>
</div>

{_split_table()}

<div class="prose">
<p>Note the two rows where GoHighLevel says &ldquo;No&rdquo;. Crew dispatch and job
costing are not gaps you can close with a clever workflow. If you are sequencing
multiple vans across a service area, no amount of automation substitutes for
purpose-built routing.</p>
<p>Equally, note the three rows where field service software is only partial.
Chasing a quote that went quiet for eleven days is a nurture sequence, and that is
not what dispatch software is built to do.</p>

<h2 id="leak">Find out where work is leaking first</h2>
<p>Before buying either, work out which side of the booking your problem is on. The
question is not &ldquo;which is the best CRM&rdquo; but &ldquo;where does work stop
moving&rdquo;.</p>
<ul>
<li><strong>Leads arrive and go cold.</strong> Calls missed while you are on a roof.
Quotes sent and never followed up. Enquiries from three different places and no
single list. That is a lead problem — a marketing CRM.</li>
<li><strong>Jobs are booked but chaotic.</strong> Two crews sent to the same street
on different days. Invoices going out a fortnight late. No idea which jobs actually
made money. That is a job problem — field service software.</li>
</ul>
<p>If it is the first one, the
<a href="/missed-call-revenue-calculator/">missed-call revenue calculator</a> will
put a number on it in about a minute. Do that before spending anything.</p>

<h2 id="cost">What each one costs</h2>
<p>Verified from each vendor's own pricing page on
<time datetime="{P['verifiedOn']}">28 August 2026</time>:</p>
<div class="table-scroll">
<table class="cmp">
<caption class="sr-only">Cost comparison</caption>
<thead><tr><th scope="col">Tool</th><th scope="col">Entry</th>
<th scope="col">Next tier</th><th scope="col">Watch out for</th></tr></thead>
<tbody>
<tr><td data-label="Tool">Housecall Pro</td>
    <td data-label="Entry">${hcp_low}/mo annual (${HCP['tiers'][0]['monthly']} monthly), 1 user</td>
    <td data-label="Next tier">${hcp_high}/mo annual, 5 users</td>
    <td data-label="Watch out for">${HCP['tiers'][1]['additionalUserMonthly']}/mo per extra user above five</td></tr>
<tr><td data-label="Tool">GoHighLevel</td>
    <td data-label="Entry">${ghl}/mo, 3 sub-accounts</td>
    <td data-label="Next tier">${P['plans'][1]['monthly']}/mo, unlimited</td>
    <td data-label="Watch out for">Metered SMS, email and voice on top of every plan</td></tr>
</tbody>
</table>
</div>
<p>The GoHighLevel figure is the subscription only. SMS runs
${P['usage']['smsPerSegment']} a segment plus carrier fees of roughly
${P['usage']['carrierFees']['averageSmsOutbound']} more, voice
${P['usage']['voiceOutboundPerMinute']} a minute, and each phone number
${P['usage']['localNumberPerMonth']} a month. For a contractor doing modest volume
that is tens of dollars, not hundreds — but it is not zero, and most articles quote
the ${ghl} and stop. The
<a href="/gohighlevel-true-cost-calculator/">true cost calculator</a> models it
properly.</p>

<h2 id="trade">It differs by trade</h2>
<p>The lead-versus-job balance is not the same across home services, and it changes
which tool matters more.</p>
<ul>
<li><strong>Roofing and remodeling.</strong> Few calls, very high job value, long
consideration. A single missed call can be a five-figure job. Follow-up discipline
matters more than routing — the CRM side earns its keep first.</li>
<li><strong>Plumbing and drain work.</strong> High call volume, lower ticket, often
urgent. Whoever answers first wins, and dispatch efficiency compounds. Both sides
matter, and speed of response is the shared constraint.</li>
<li><strong>HVAC.</strong> Seasonal spikes plus a maintenance-contract base. The
reactivation campaign — going back to people you have already served — is a CRM job
and a genuinely underused one.</li>
<li><strong>Electrical.</strong> Mixed. Small domestic jobs behave like plumbing;
commercial work behaves like remodeling.</li>
</ul>

<h2 id="skip">When you need neither</h2>
<p>If you are one person, answering your own phone, running a job book you can hold
in your head, a CRM is overhead you will not use. Software does not fix a business
that is working.</p>
<p>The threshold is not headcount, it is leakage. When calls start going unanswered
because you are on site, or quotes go out and nobody chases them, you have crossed
it. Before that, the honest answer is to keep the money.</p>
<p>That threshold is worth measuring rather than guessing, which is what the
calculator is for.</p>

{faq_html}

{not_speaking_for()}
</div>

{cta("gohighlevel", "See GoHighLevel plans and pricing", placement="contractors-footer",
     dest="pricing",
     note="NodeRow earns a commission on GoHighLevel signups. We earn nothing from Housecall Pro or Jobber.")}

<div class="prose">
<h2 id="related">Related</h2>
<ul>
<li><a href="/missed-call-revenue-calculator/">What are missed calls costing you?</a></li>
<li><a href="/missed-call-text-back/">Missed call text back, explained</a></li>
<li><a href="/gohighlevel-pricing-explained/">GoHighLevel pricing explained</a></li>
<li><a href="/build/">Have the automation built for you</a></li>
</ul>

{author_box()}
</div>

</div>
</section>
"""

    return {
        "path": PATH, "title": TITLE, "description": DESCRIPTION, "body": body,
        "trail": [("Home", "/"), ("Guides", "/guides/"),
                  ("CRM for contractors", PATH)],
        "priority": "0.9",
        "extra_schema": [
            entity.article(PATH, TITLE, DESCRIPTION,
                           published="2026-08-28", modified="2026-08-28"),
            faq_schema,
        ],
    }
