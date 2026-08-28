"""Page content definitions.

Each page is a dict: path, title, description, body, plus optional schema
nodes. The shell (head, header, footer) is applied by build.py — no page
builds its own.
"""

import entity
from components import (
    author_box,
    cta,
    inline_disclosure,
    no_commission_callout,
    outbound,
    pending_link,
    status_pill,
)

TODAY = "2026-08-28"


def _subscribe_block():
    return """<section class="section section-alt" id="subscribe">
<div class="wrap subscribe-inner">
<p class="eyebrow">Get new guides</p>
<h2>One email when something new ships.</h2>
<p class="lede">No drip sequence, no course to sell. Just the write-up, sent when a
build is finished and worth documenting.</p>
<div class="subscribe-body">
<form class="subscribe-form-el" name="subscribe" method="POST" action="/#subscribed"
      data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="subscribe">
  <p class="hp-field"><label>Leave this field blank:
    <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="subscribe-form">
    <label class="sr-only" for="email">Email address</label>
    <input id="email" name="email" type="email" placeholder="you@agency.com"
           autocomplete="email" required>
    <button class="btn btn-primary" type="submit">Subscribe</button>
  </div>
</form>
<p class="fine-print">Unsubscribe anytime. No spam — just occasional field notes.</p>
<p id="subscribed" class="form-success">You're on the list — the next guide lands in
your inbox when it's ready.</p>
</div>
</div>
</section>"""


# ---------------------------------------------------------------- homepage

HOME_BODY = f"""
<section class="hero">
<div class="wrap">
<p class="eyebrow">Agency automation, reviewed from the build side</p>
<h1>Most agencies are paying for eight tools that don't talk to each other.</h1>
<p class="lede">NodeRow compares all-in-one platforms against stitched-together
stacks — GoHighLevel, n8n, Make, Zapier — and shows you what each one actually
costs once it's wired up and running. Written by someone who builds these systems
for paying clients and gets the call when they break.</p>
<div class="hero-actions">
  <a class="btn btn-primary" href="/compare/">Compare the stacks</a>
  <a class="btn btn-ghost" href="/build/">Have it built for you</a>
</div>
<div class="credential">
  <span><strong>100+</strong> completed contracts</span>
  <span><strong>100%</strong> job success on Upwork</span>
  <span>Builds in <strong>n8n, Make, Zapier and GoHighLevel</strong> weekly</span>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">The actual decision</p>
<h2>One platform, or a stack you assemble yourself?</h2>
<p>This is the fork every agency hits around the time the spreadsheet stops
working. Both answers are defensible. They fail in different places, and the
failure modes are what nobody writes about.</p>
</div>

<div class="node-grid">
  <article class="node">
    <div class="node-head">
      <span class="node-kicker">Route A</span>
      {status_pill("ok", "Fewest moving parts")}
    </div>
    <h3>One platform that does most of it</h3>
    <p>CRM, pipelines, email and SMS, booking, funnels and client sub-accounts
    billed as one product. You trade depth in any single area for not having to
    integrate anything.</p>
    <p class="node-chain">Lead → CRM → Nurture → Booking → Reporting</p>
  </article>

  <article class="node">
    <div class="node-head">
      <span class="node-kicker">Route B</span>
      {status_pill("waiting", "Most flexible")}
    </div>
    <h3>Best-in-class tools, wired together</h3>
    <p>Pick the best CRM, the best email tool, the best scheduler, then connect
    them with n8n or Make. Better at every individual job. Now you own the
    integration layer, forever.</p>
    <p class="node-chain">Forms → n8n → CRM → ESP → Sheets → Slack</p>
  </article>

  <article class="node">
    <div class="node-head">
      <span class="node-kicker">In practice</span>
      {status_pill("error", "The common failure")}
    </div>
    <h3>Half of one, half of the other</h3>
    <p>Most agencies end up here by accident — a platform for some of it, four
    subscriptions and a fragile Zap for the rest. It's the most expensive
    configuration and the hardest to hand to a new hire.</p>
    <p class="node-chain">Platform + 4 SaaS + 1 Zap nobody documented</p>
  </article>
</div>

<p class="cta-row" style="margin-top:2rem">
  <a class="btn btn-ghost" href="/compare/">See how the routes compare</a>
  <span class="cta-note">The full cost breakdown is being written now.</span>
</p>
</div>
</section>

<section class="section section-alt">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Guides in progress</p>
<h2>Written from client builds, not documentation</h2>
<p>Every guide here has to contain at least one thing you can't get from a docs
page — a real cost figure, a real error, a decision that went wrong on a live
project. These are being written now.</p>
</div>

<div class="node-grid">
  <article class="node">
    <div class="node-head">
      <span class="node-kicker">Comparison</span>
      {status_pill("waiting", "Writing")}
    </div>
    <h3>GoHighLevel vs a stitched-together stack</h3>
    <p>What the all-in-one actually replaces, what it doesn't, and the real
    monthly number once you've added the tools it can't cover.</p>
    <p class="node-chain">All-in-one ⟷ Assembled stack</p>
  </article>

  <article class="node">
    <div class="node-head">
      <span class="node-kicker">Pricing</span>
      {status_pill("waiting", "Writing")}
    </div>
    <h3>GoHighLevel pricing, explained without the pitch</h3>
    <p>What each tier gets you, when the jump is worth it, and the costs that sit
    outside the subscription — sending fees, phone numbers, migration time.</p>
    <p class="node-chain">$97 → $297 → $497</p>
  </article>

  <article class="node">
    <div class="node-head">
      <span class="node-kicker">Build guide</span>
      {status_pill("waiting", "Writing")}
    </div>
    <h3>Automating client onboarding end to end</h3>
    <p>Intake form to CRM to Drive folders to Slack to welcome sequence. The
    actual node shape, and the three places it breaks in production.</p>
    <p class="node-chain">Form → CRM → Drive → Slack → Sequence</p>
  </article>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">How this site makes money</p>
<h2>Said plainly, because you'd work it out anyway.</h2>
</div>
<div class="prose">
<p>NodeRow earns a commission when someone signs up for GoHighLevel through a link
here. That's the main way this site pays for itself, and it's why GoHighLevel
comes up often.</p>
<p>What that does <em>not</em> mean: that it's the answer to everything. It's a
platform, not a connector. If your problem is moving data between arbitrary APIs,
it's the wrong shape and this site will tell you so.</p>
{no_commission_callout("zapier")}
<p>Every recommendation here carries its commission status. Tools that pay nothing
are named anyway, and labelled. See the
<a href="/affiliate-disclosure/">full disclosure</a> for the specifics.</p>
</div>
</div>
</section>

{_subscribe_block()}
"""


# ---------------------------------------------------------------- hubs

COMPARE_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Compare tools</p>
<h1>Automation platform comparisons</h1>
<p class="lede">Head-to-head breakdowns of the platforms agencies actually choose
between, with the pricing modelled at real volume rather than at the sticker
price.</p>
</div>

{inline_disclosure()}

<div class="node-grid">
  <article class="node">
    <div class="node-head"><span class="node-kicker">All-in-one vs stack</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>GoHighLevel vs a stitched-together stack</h3>
    <p>The core decision. What one platform replaces, what it can't, and the true
    monthly cost of each route at agency scale.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">Alternatives</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>GoHighLevel alternatives worth considering</h3>
    <p>Where {outbound("keap", "Keap")} and
    {outbound("activecampaign", "ActiveCampaign")} genuinely fit better, and
    where they leave gaps you'll have to fill.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">Connectors</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>n8n vs Make vs Zapier</h3>
    <p>What a "task", an "operation" and an "execution" each actually mean — and
    why the three prices can't be compared directly.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">Alternatives</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>Zapier alternatives at volume</h3>
    <p>Why teams leave, where they go, and a migration-difficulty rating for each
    destination.</p>
  </article>
</div>

<div class="prose" style="margin-top:3rem">
<h2>How these comparisons get made</h2>
<p>Every platform on this site is one I've either built on for a client or tested
against a real workload. Pricing is modelled at volumes agencies actually hit, not
at the tier that makes a tool look cheapest. Every price carries the date it was
checked, because they move.</p>
<p>Read the full method on <a href="/how-we-test/">How We Test</a>.</p>
</div>

{author_box()}
</div>
</section>
"""

GUIDES_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Guides</p>
<h1>Build guides and use-case walkthroughs</h1>
<p class="lede">How to actually build the thing — the workflow shape, the apps at
each step, and where it breaks once real data hits it.</p>
</div>

<div class="node-grid">
  <article class="node">
    <div class="node-head"><span class="node-kicker">Onboarding</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>Automate client onboarding</h3>
    <p>Intake form → CRM → Drive folders → Slack → welcome sequence → status
    reporting. Build-it-yourself, buy-the-pack, or have-it-built.</p>
    <p class="node-chain">Form → CRM → Drive → Slack</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">Lead flow</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>Lead capture to CRM, without duplicates</h3>
    <p>Forms and ad platforms into one pipeline: dedupe, enrich, assign, notify.
    The dedupe step is where most builds quietly fail.</p>
    <p class="node-chain">Ads/Forms → Dedupe → Enrich → CRM</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">Documents</span>
    {status_pill("waiting", "Writing")}</div>
    <h3>Email attachments to filed, indexed documents</h3>
    <p>Inbox → parse → rename → file to Drive → index in Sheets → notify. Handles
    duplicates and the odd zip file without dropping anything.</p>
    <p class="node-chain">Gmail → Parse → Drive → Sheets</p>
  </article>
</div>

<div class="prose" style="margin-top:3rem">
<h2>What a guide here has to contain</h2>
<p>At minimum, one thing that can't be written from a documentation page: a real
cost figure, a real error message, a real node configuration, or a decision that
went wrong on a client project. If a draft doesn't have one, it's a commodity
article and it doesn't get published.</p>
</div>

{author_box()}
</div>
</section>
"""

TOOLS_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Tool directory</p>
<h1>Every platform covered on NodeRow</h1>
<p class="lede">One card per platform, with what it's genuinely good at, where it
falls down, and whether NodeRow earns anything if you sign up. The commission line
on each card is generated from the same data that builds the links, so it can't
drift.</p>
</div>

{inline_disclosure()}

<div id="tool-cards" class="node-grid"></div>
</div>
</section>
"""

PACKS_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Workflow packs</p>
<h1>Pre-built workflows you can import today</h1>
<p class="lede">The same systems I build for clients, exported and documented so
you can import them yourself. Each pack targets a specific platform and ships with
the setup notes.</p>
</div>

<!-- Launch pricing note (internal): $39 is a launch position to buy first sales
     and reviews, not a permanent price. Target: 10 sales and 5 testimonials,
     then raise to $79. Do not surface this to readers. -->

<div class="node-grid">
  <article class="node">
    <div class="node-head"><span class="node-kicker">$39</span>
    {status_pill("waiting", "In production")}</div>
    <h3>Client Onboarding Pack</h3>
    <p>Intake form → CRM → Drive folders → Slack → welcome sequence → status
    reporting.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">$39</span>
    {status_pill("waiting", "In production")}</div>
    <h3>Ecommerce Ops Pack</h3>
    <p>Order sync, inventory alerts, bulk price updates and returns triage.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">$39</span>
    {status_pill("waiting", "In production")}</div>
    <h3>Document Automation Pack</h3>
    <p>Email → parse → Drive filing → Sheets index → notification.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">$39</span>
    {status_pill("waiting", "In production")}</div>
    <h3>Lead Capture &amp; CRM Sync Pack</h3>
    <p>Forms and ads → dedupe → enrich → CRM → assignment.</p>
  </article>
  <article class="node">
    <div class="node-head"><span class="node-kicker">$99 bundle</span>
    {status_pill("waiting", "In production")}</div>
    <h3>All Four Bundle</h3>
    <p>Every pack above, versus $156 bought separately.</p>
  </article>
</div>

<div class="prose" style="margin-top:3rem">
<h2>What ships in a pack</h2>
<ul>
<li>The importable workflow file for its target platform</li>
<li>Screenshots of the actual node graph, not a marketing diagram</li>
<li>A setup-time estimate and the list of apps you'll need to connect</li>
<li>An honest "who this is not for" section</li>
</ul>
<p>Packs aren't on sale yet — they're being packaged and tested.
<a href="#subscribe">Get the email</a> when the first one ships.</p>
</div>
</div>
</section>

{_subscribe_block()}
"""

BUILD_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Get it built</p>
<h1>Have the automation built for you</h1>
<p class="lede">Fixed price, no hourly billing. You describe the outcome, I build
and test it, you get handover notes so it isn't a black box.</p>
</div>

<div class="node-grid">
  <article class="node tier">
    <div class="node-head"><span class="node-kicker">Quick Fix</span></div>
    <p class="tier-price">$50</p>
    <ul>
      <li>One broken or half-finished workflow</li>
      <li>Diagnosed and repaired</li>
      <li>A note on what caused it</li>
      <li class="not">Not a new build from scratch</li>
    </ul>
  </article>
  <article class="node tier">
    <div class="node-head"><span class="node-kicker">Single Workflow</span></div>
    <p class="tier-price">$150</p>
    <ul>
      <li>One automation built and tested</li>
      <li>Up to 3 connected apps</li>
      <li>Error handling on the failure paths</li>
      <li class="not">Not multi-workflow systems</li>
    </ul>
  </article>
  <article class="node tier">
    <div class="node-head"><span class="node-kicker">Workflow System</span></div>
    <p class="tier-price">$300</p>
    <ul>
      <li>3–5 connected workflows</li>
      <li>Up to 6 apps</li>
      <li>Handover notes included</li>
      <li class="not">Not custom app development</li>
    </ul>
  </article>
  <article class="node tier">
    <div class="node-head"><span class="node-kicker">Full Build</span></div>
    <p class="tier-price">$500</p>
    <ul>
      <li>Complete multi-workflow system</li>
      <li>Custom logic and documentation</li>
      <li>Walkthrough recording</li>
      <li class="not">Not ongoing monthly management</li>
    </ul>
  </article>
</div>

<div class="prose" style="margin-top:3rem">
<h2>How it works</h2>
</div>
<div class="flow">
  <div class="flow-step">
    <h3>1. You describe the outcome</h3>
    <p>Not the tool — the result. "Every new client gets a folder, a welcome email
    and a task assigned" is enough to quote from.</p>
  </div>
  <div class="flow-step">
    <h3>2. I confirm scope and price</h3>
    <p>You get the tier, what's included, what isn't, and a turnaround estimate
    before anything starts. If it doesn't fit a tier, I'll say so.</p>
  </div>
  <div class="flow-step">
    <h3>3. Build and test on real data</h3>
    <p>Built on your stack, tested against real records rather than a happy-path
    sample. Turnaround is typically 3–7 days depending on tier.</p>
  </div>
  <div class="flow-step">
    <h3>4. Handover</h3>
    <p>You get the working system plus notes on how it's wired, so your team can
    maintain it without me.</p>
  </div>
</div>

<div class="prose" style="margin-top:2.5rem">
<h2>Proof</h2>
<p>100+ completed contracts with a 100% job success score on Upwork, building in
n8n, Make, Zapier and GoHighLevel. The
<a href="https://www.upwork.com/freelancers/rohailnisaracademy" target="_blank"
   rel="noopener me">Upwork profile</a> carries the contract history and client
feedback.</p>

<h2>Start an enquiry</h2>
<form name="build-enquiry" method="POST" action="/build/#enquiry-sent"
      data-netlify="true" netlify-honeypot="bot-field" data-enquiry>
  <input type="hidden" name="form-name" value="build-enquiry">
  <p class="hp-field"><label>Leave this field blank:
    <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="field">
    <label for="bname">Your name</label>
    <input id="bname" name="name" type="text" autocomplete="name" required>
  </div>
  <div class="field">
    <label for="bemail">Email</label>
    <input id="bemail" name="email" type="email" autocomplete="email" required>
  </div>
  <div class="field">
    <label for="btier">Which tier looks right?</label>
    <select id="btier" name="tier">
      <option>Not sure yet</option>
      <option>Quick Fix — $50</option>
      <option>Single Workflow — $150</option>
      <option>Workflow System — $300</option>
      <option>Full Build — $500</option>
    </select>
  </div>
  <div class="field">
    <label for="bdetail">What should happen automatically?</label>
    <textarea id="bdetail" name="detail" required
      placeholder="Describe the outcome, not the tool."></textarea>
  </div>
  <p class="cta-row">
    <button class="btn btn-primary" type="submit">Send enquiry</button>
    <span class="cta-note">Replies within one working day.</span>
  </p>
</form>
<p id="enquiry-sent" class="form-success">Enquiry received — you'll get a reply
within one working day.</p>
</div>

{author_box()}
</div>
</section>
"""

ABOUT_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">About</p>
<h1>Who writes this, and how it's funded</h1>
</div>
<div class="prose">
<p>NodeRow is written by Rohail Nisar Ahmad, a freelance data integration and
automation engineer. I build workflows in n8n, Make, Zapier and GoHighLevel for
paying clients — 100+ completed contracts with a 100% job success score on
Upwork — and I'm the one who gets the call when a build breaks at 2am.</p>
<p>That's the entire reason this site exists. Most automation content is written by
marketers working from documentation. It reads fine and it's useless the moment
real data hits the workflow, because the person writing it has never watched a
webhook silently drop 400 records.</p>

<h2>Publishing principles</h2>
<ul>
<li><strong>Nothing gets published from documentation alone.</strong> Every guide
has to contain at least one thing that came out of a real build — a cost figure, an
error message, a node configuration, a decision that went wrong.</li>
<li><strong>Commission status is always visible.</strong> Where NodeRow earns
nothing, the page says so in plain language rather than quietly routing you
elsewhere.</li>
<li><strong>Prices carry the date they were checked.</strong> Vendor pricing moves
constantly. An undated price is a guess.</li>
<li><strong>No invented numbers.</strong> No fabricated traffic figures, no fake
testimonials, no revenue claims that can't be evidenced.</li>
<li><strong>Review dates are real.</strong> A page's reviewed date changes only
after someone has actually re-checked it. Touching a date to look fresh is worse
than a stale date.</li>
</ul>

<h2>How the site is funded</h2>
<p>Three ways, in order of how much they matter: affiliate commissions (primarily
GoHighLevel, which pays a recurring commission), workflow packs, and build work.
There are no display ads on this site and there won't be.</p>
<p>The <a href="/affiliate-disclosure/">affiliate disclosure</a> covers exactly
which links earn and which don't.</p>

<h2>What this site doesn't cover</h2>
<p>Monitoring, alerting and incident response for automations that are already
live. That's a different job and a different site. NodeRow is about choosing the
tool and building the thing.</p>
</div>
{author_box()}
</div>
</section>
"""

DISCLOSURE_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Ethics policy</p>
<h1>Affiliate disclosure</h1>
</div>
<div class="prose">
<p>NodeRow earns affiliate commissions. This page says exactly how, because a
disclosure buried in a footer isn't a disclosure.</p>

<h2>What NodeRow earns from</h2>
<p><strong>GoHighLevel</strong> is the main one. If you sign up through a link on
this site, NodeRow receives a recurring commission for as long as you stay
subscribed. It costs you nothing extra. This is the primary way the site is
funded, and it's why GoHighLevel is covered in depth here.</p>
<p><strong>Make</strong> and <strong>n8n Cloud</strong> pay a commission for a
limited period after signup. Where those links appear, they're marked the same way.</p>

<h2>What NodeRow earns nothing from</h2>
<p>Zapier has no public affiliate program. NodeRow has never earned and will never
earn a penny from a Zapier signup. Self-hosted n8n pays nothing either — the
commission is cloud-only.</p>
{no_commission_callout("zapier")}
<p>Both still get recommended here wherever they're genuinely the better answer,
and those recommendations carry a visible note saying we earn nothing. That note is
generated automatically from the commission data, so it can't quietly go missing.</p>

<h2>How this affects what gets recommended</h2>
<p>Honestly: it affects what gets <em>covered</em>. GoHighLevel gets more articles
than a tool that pays nothing, because those articles pay for the site.</p>
<p>What it doesn't affect is what gets <em>recommended within</em> an article. A
platform that's wrong for your situation is described as wrong for your situation.
GoHighLevel is an all-in-one platform, not a connector — if your problem is moving
data between arbitrary APIs, this site will point you at n8n or Make, which pay
less, or Zapier, which pays nothing at all.</p>

<h2>How links are marked</h2>
<ul>
<li>Every affiliate link carries <code>rel="sponsored nofollow"</code>.</li>
<li>Every page containing one shows a disclosure above the first link, not just in
the footer.</li>
<li>The sitewide disclosure line appears in the footer of every page.</li>
</ul>

<h2>Questions</h2>
<p>If something here looks like it's been shaded by a commission, say so — the
<a href="/contact/">contact page</a> goes straight to me.</p>
</div>
</div>
</section>
"""

HOW_WE_TEST_BODY = f"""
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Method</p>
<h1>How platforms get tested</h1>
<p class="lede">The short version: nothing gets recommended here that hasn't been
built on, and pricing is modelled at volumes agencies actually reach.</p>
</div>
<div class="prose">
<h2>Hands on the tool</h2>
<p>Every platform covered is one I've either used on a paying client project or
built a genuine test workload on. "Genuine" means real records with real edge
cases — duplicates, missing fields, rate limits — not a five-record happy path.</p>

<h2>Pricing modelled at volume</h2>
<p>Vendors quote the tier that makes them look cheapest. Comparisons here model
cost at the volumes that actually matter, and state the assumptions. Where two
tools count usage differently — a Zapier task is not a Make operation is not an
n8n execution — the difference is explained rather than papered over.</p>

<h2>Dates on everything</h2>
<p>Every price carries the date it was checked. Software behaviour carries a
version where it matters: "tested on n8n 1.x, {TODAY}" is useful, "updated
recently" is not.</p>

<h2>What gets said about weaknesses</h2>
<p>Every tool profile names what the tool is bad at. A review that can't say what a
product does poorly isn't a review.</p>

<h2>Corrections</h2>
<p>Vendors change pricing and features constantly. If something here is out of
date, <a href="/contact/">tell me</a> and it gets fixed with the date updated. A
page's reviewed date only moves after a real re-check.</p>
</div>
</div>
</section>
"""

PRIVACY_BODY = """
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Legal</p>
<h1>Privacy policy</h1>
</div>
<div class="prose">
<h2>What gets collected</h2>
<p>If you subscribe to the email list or send a build enquiry, NodeRow stores the
details you type into that form. Nothing else is collected from you directly.</p>

<h2>Analytics</h2>
<p>NodeRow uses privacy-respecting aggregate analytics to see which pages get read
and which links get clicked. This records page paths and click events, not
personally identifying profiles.</p>

<h2>Affiliate links</h2>
<p>Clicking an affiliate link sends you to the vendor's own site, which will set
its own cookies under its own privacy policy. NodeRow doesn't receive your personal
details from that process — only whether a signup was attributed.</p>

<h2>Email</h2>
<p>Your address is used to send new articles and nothing else. It isn't sold or
shared. Every email carries an unsubscribe link, and unsubscribing removes the
address.</p>

<h2>Your data</h2>
<p>To see, correct or delete anything held about you, use the
<a href="/contact/">contact page</a>.</p>
</div>
</div>
</section>
"""

CONTACT_BODY = """
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">Contact</p>
<h1>Get in touch</h1>
<p class="lede">Corrections, build enquiries, or a disagreement with something
written here — all welcome.</p>
</div>
<div class="prose">
<form name="contact" method="POST" action="/contact/#sent"
      data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="contact">
  <p class="hp-field"><label>Leave this field blank:
    <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="field">
    <label for="cname">Your name</label>
    <input id="cname" name="name" type="text" autocomplete="name" required>
  </div>
  <div class="field">
    <label for="cemail">Email</label>
    <input id="cemail" name="email" type="email" autocomplete="email" required>
  </div>
  <div class="field">
    <label for="cmsg">Message</label>
    <textarea id="cmsg" name="message" required></textarea>
  </div>
  <p class="cta-row">
    <button class="btn btn-primary" type="submit">Send</button>
  </p>
</form>
<p id="sent" class="form-success">Message sent — you'll get a reply within one
working day.</p>

<h2>Other places</h2>
<p>For paid work, the
<a href="https://www.upwork.com/freelancers/rohailnisaracademy" target="_blank"
   rel="noopener me">Upwork profile</a> is the fastest route, and it carries the
contract history. Otherwise
<a href="https://www.linkedin.com/in/rohailnisarahmad" target="_blank"
   rel="noopener me">LinkedIn</a> works.</p>
</div>
</div>
</section>
"""

NOT_FOUND_BODY = """
<section class="section">
<div class="wrap">
<div class="section-head">
<p class="eyebrow">404</p>
<h1>That page doesn't exist</h1>
<p class="lede">The link is wrong, or the page hasn't been published yet. Both
happen.</p>
</div>
<p class="cta-row">
  <a class="btn btn-primary" href="/">Back to the homepage</a>
  <a class="btn btn-ghost" href="/compare/">Browse comparisons</a>
</p>
</div>
</section>
"""


def all_pages():
    """Every page in the site, in sitemap order."""
    return [
        {
            "path": "/",
            "title": "NodeRow — Agency Automation Stacks, Reviewed From the Build Side",
            "description": (
                "Comparisons and build guides for agency automation stacks — "
                "GoHighLevel, n8n, Make and Zapier — written by an engineer who "
                "builds and debugs these systems for paying clients."
            ),
            "body": HOME_BODY,
            "trail": [("Home", "/")],
            "priority": "1.0",
        },
        {
            "path": "/compare/",
            "title": "Automation Platform Comparisons for Agencies | NodeRow",
            "description": (
                "Head-to-head comparisons of GoHighLevel, n8n, Make and Zapier, with "
                "pricing modelled at real agency volume rather than the sticker price."
            ),
            "body": COMPARE_BODY,
            "trail": [("Home", "/"), ("Compare Tools", "/compare/")],
            "priority": "0.9",
        },
        {
            "path": "/guides/",
            "title": "Automation Build Guides and Use-Case Walkthroughs | NodeRow",
            "description": (
                "Step-by-step build guides for client onboarding, lead capture and "
                "document automation — the workflow shape, the apps, and where each "
                "one breaks in production."
            ),
            "body": GUIDES_BODY,
            "trail": [("Home", "/"), ("Guides", "/guides/")],
            "priority": "0.9",
        },
        {
            "path": "/tools/",
            "title": "Automation Tool Directory | NodeRow",
            "description": (
                "Every automation platform covered on NodeRow, with what each is good "
                "at, where it falls down, and whether NodeRow earns a commission."
            ),
            "body": TOOLS_BODY,
            "trail": [("Home", "/"), ("Tools", "/tools/")],
            "priority": "0.7",
            "tool_directory": True,
        },
        {
            "path": "/packs/",
            "title": "Pre-Built Automation Workflow Packs | NodeRow",
            "description": (
                "Importable workflow packs for client onboarding, ecommerce ops, "
                "document automation and lead capture — the same systems built for "
                "paying clients."
            ),
            "body": PACKS_BODY,
            "trail": [("Home", "/"), ("Workflow Packs", "/packs/")],
            "priority": "0.8",
        },
        {
            "path": "/build/",
            "title": "Automation Built For You — Fixed Price From $50 | NodeRow",
            "description": (
                "Fixed-price automation builds in n8n, Make, Zapier and GoHighLevel. "
                "Four tiers from a $50 quick fix to a $500 full multi-workflow system."
            ),
            "body": BUILD_BODY,
            "trail": [("Home", "/"), ("Get It Built", "/build/")],
            "priority": "0.9",
            "extra_schema": [
                entity.service(
                    "Automation build service",
                    "Fixed-price workflow automation builds in n8n, Make, Zapier "
                    "and GoHighLevel.",
                    [
                        ("Quick Fix", 50,
                         "One broken or half-finished workflow, diagnosed and repaired."),
                        ("Single Workflow", 150,
                         "One automation built and tested, up to 3 connected apps."),
                        ("Workflow System", 300,
                         "3-5 connected workflows, up to 6 apps, handover notes."),
                        ("Full Build", 500,
                         "Complete multi-workflow system, custom logic, documentation "
                         "and a walkthrough recording."),
                    ],
                )
            ],
        },
        {
            "path": "/about/",
            "title": "About NodeRow and Its Publishing Principles",
            "description": (
                "NodeRow is written by Rohail Nisar Ahmad, a freelance automation "
                "engineer with 100+ completed contracts. How the site works and how "
                "it is funded."
            ),
            "body": ABOUT_BODY,
            "trail": [("Home", "/"), ("About", "/about/")],
            "priority": "0.7",
        },
        {
            "path": "/how-we-test/",
            "title": "How NodeRow Tests Automation Platforms",
            "description": (
                "The method behind NodeRow's comparisons: hands-on builds, pricing "
                "modelled at real volume, dated prices, and named weaknesses."
            ),
            "body": HOW_WE_TEST_BODY,
            "trail": [("Home", "/"), ("How We Test", "/how-we-test/")],
            "priority": "0.6",
        },
        {
            "path": "/affiliate-disclosure/",
            "title": "Affiliate Disclosure | NodeRow",
            "description": (
                "Exactly which links on NodeRow earn a commission, which earn "
                "nothing, and how that does and doesn't affect what gets recommended."
            ),
            "body": DISCLOSURE_BODY,
            "trail": [("Home", "/"), ("Affiliate Disclosure", "/affiliate-disclosure/")],
            "priority": "0.6",
        },
        {
            "path": "/privacy-policy/",
            "title": "Privacy Policy | NodeRow",
            "description": (
                "What NodeRow collects when you subscribe or send an enquiry, how "
                "analytics and affiliate links work, and how to have your data "
                "corrected or removed."
            ),
            "body": PRIVACY_BODY,
            "trail": [("Home", "/"), ("Privacy Policy", "/privacy-policy/")],
            "priority": "0.4",
        },
        {
            "path": "/contact/",
            "title": "Contact NodeRow",
            "description": (
                "Get in touch with NodeRow about corrections, fixed-price automation "
                "build enquiries, or a disagreement with something written here. "
                "Replies within one working day."
            ),
            "body": CONTACT_BODY,
            "trail": [("Home", "/"), ("Contact", "/contact/")],
            "priority": "0.5",
        },
    ]
