/* GoHighLevel true-cost calculator.
 *
 * Progressive enhancement: the page renders a complete, readable pricing table
 * and worked example with JS off. This script upgrades that into a live model.
 *
 * All rates come from the data-rates JSON block the build writes into the page,
 * which comes from content/pricing-data.json. No number is hardcoded here.
 */
(function () {
  'use strict';

  var root = document.getElementById('calc');
  if (!root) return;

  var RATES;
  try {
    RATES = JSON.parse(document.getElementById('calc-rates').textContent);
  } catch (e) {
    return; // leave the no-JS content in place
  }

  var PLANS = RATES.plans;
  var U = RATES.usage;

  var fields = {
    clients: root.querySelector('#f-clients'),
    sms: root.querySelector('#f-sms'),
    email: root.querySelector('#f-email'),
    ai: root.querySelector('#f-ai'),
    billing: root.querySelector('#f-billing'),
    rebill: root.querySelector('#f-rebill'),
    markup: root.querySelector('#f-markup')
  };

  var out = {
    body: root.querySelector('#calc-out'),
    verdict: root.querySelector('#calc-verdict')
  };

  function money(n) {
    if (!isFinite(n)) n = 0;
    return '$' + n.toLocaleString('en-US', {
      minimumFractionDigits: 2, maximumFractionDigits: 2
    });
  }

  function money0(n) {
    if (!isFinite(n)) n = 0;
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function num(el, fallback) {
    var v = parseFloat(el && el.value);
    return isFinite(v) && v >= 0 ? v : fallback;
  }

  function planBase(plan, annual) {
    return annual ? plan.annualMonthlyEquivalent : plan.monthly;
  }

  function compute() {
    var clients = Math.max(1, Math.round(num(fields.clients, 1)));
    var smsPerClient = num(fields.sms, 0);
    var emailPerClient = num(fields.email, 0);
    var aiPerClient = num(fields.ai, 0);
    var annual = fields.billing.value === 'annual';
    var rebill = fields.rebill.checked;
    var markup = Math.max(1, num(fields.markup, 1));

    // Usage is metered across every sub-account, so it scales with client count.
    var smsTotal = clients * smsPerClient;
    var emailTotal = clients * emailPerClient;
    var aiTotal = clients * aiPerClient;

    var smsCost = smsTotal * U.smsPerSegment;
    var emailCost = (emailTotal / 1000) * U.emailPer1000;
    var aiCost = aiTotal * U.aiConversationPerMessage;
    var usageCost = smsCost + emailCost + aiCost;

    var rows = PLANS.map(function (p) {
      var base = planBase(p, annual);
      var eligible = p.subAccounts === null || clients <= p.subAccounts;

      // Rebilling recovers usage cost. At-cost recovers exactly the usage;
      // markup is only permitted on the tier that unlocks it.
      var recovered = 0;
      if (rebill && p.rebillAtCost) {
        recovered = p.rebillWithMarkup ? usageCost * markup : usageCost;
      }

      var net = base + usageCost - recovered;
      return {
        plan: p, base: base, usage: usageCost,
        recovered: recovered, net: net, eligible: eligible
      };
    });

    var viable = rows.filter(function (r) { return r.eligible; });
    var best = viable.reduce(function (a, b) { return b.net < a.net ? b : a; }, viable[0]);

    render(rows, best, {
      clients: clients, usageCost: usageCost, annual: annual,
      rebill: rebill, markup: markup,
      smsCost: smsCost, emailCost: emailCost, aiCost: aiCost,
      smsTotal: smsTotal, emailTotal: emailTotal, aiTotal: aiTotal
    });
  }

  function render(rows, best, ctx) {
    var html = '';

    html += '<h3 class="calc-sub">Your monthly cost, by plan</h3>';
    html += '<div class="table-scroll"><table class="cmp"><thead><tr>' +
      '<th scope="col">Plan</th><th scope="col">Subscription</th>' +
      '<th scope="col">Usage</th><th scope="col">Rebilled back</th>' +
      '<th scope="col">Net position</th></tr></thead><tbody>';

    rows.forEach(function (r) {
      var cls = r === best ? ' class="calc-best"' : '';
      var bestLabel = best.net < 0 ? 'Best for you' : 'Cheapest for you';
      var name = r.plan.name +
        (r === best ? ' <span class="pill pill-ok">' + bestLabel + '</span>' : '');
      if (!r.eligible) {
        name = r.plan.name + ' <span class="pill pill-error">Too few sub-accounts</span>';
      }
      // A negative net is not a negative cost — it is margin. Showing it as
      // "$-1,183" would be arithmetically true and completely misleading.
      var netCell;
      if (!r.eligible) {
        netCell = '<span class="muted">n/a</span>';
      } else if (r.net < 0) {
        netCell = '<span class="net-profit">+' + money(-r.net) + ' profit</span>';
      } else {
        netCell = money(r.net);
      }

      html += '<tr' + cls + '>' +
        '<td data-label="Plan">' + name + '</td>' +
        '<td data-label="Subscription">' + money0(r.base) + '</td>' +
        '<td data-label="Usage">' + money(r.usage) + '</td>' +
        '<td data-label="Rebilled back">' +
          (r.recovered > 0 ? '&minus;' + money(r.recovered) : '<span class="muted">—</span>') +
        '</td>' +
        '<td data-label="Net position"><strong>' + netCell + '</strong></td>' +
      '</tr>';
    });
    html += '</tbody></table></div>';

    // Usage breakdown — the layer vendors and affiliate reviews leave out.
    html += '<h3 class="calc-sub">Where the usage cost comes from</h3>';
    html += '<ul class="calc-breakdown">';
    html += '<li><span>' + Math.round(ctx.smsTotal).toLocaleString('en-US') +
      ' SMS segments</span><strong>' + money(ctx.smsCost) + '</strong></li>';
    html += '<li><span>' + Math.round(ctx.emailTotal).toLocaleString('en-US') +
      ' emails</span><strong>' + money(ctx.emailCost) + '</strong></li>';
    html += '<li><span>' + Math.round(ctx.aiTotal).toLocaleString('en-US') +
      ' AI messages</span><strong>' + money(ctx.aiCost) + '</strong></li>';
    html += '<li class="calc-total"><span>Total usage, on top of the subscription</span>' +
      '<strong>' + money(ctx.usageCost) + '</strong></li>';
    html += '</ul>';

    out.body.innerHTML = html;
    out.verdict.innerHTML = verdict(rows, best, ctx);
    routeCta(best, ctx);
  }

  /* Point the CTA at the plan the reader's own numbers just recommended.
   * Each destination carries a different campaign affiliate id, so the href and
   * the id attribute have to move together — sending SaaS Pro traffic through
   * the generic link would track under the wrong campaign and pay nothing. */
  function routeCta(best, ctx) {
    var links = RATES.links;
    var cta = document.querySelector('#calc-cta a[data-aff]');
    if (!cta || !links) return;

    var key = 'pricing', label = 'See GoHighLevel plans and pricing';
    if (best.plan.id === 'agency-pro' && links['saas-pro']) {
      key = 'saas-pro';
      label = 'Start a SaaS Pro trial';
    } else if (ctx.annual && links.annual) {
      key = 'annual';
      label = 'See annual pricing';
    }

    var target = links[key];
    if (!target || !target.url) return;
    cta.href = target.url;
    cta.textContent = label;
    cta.setAttribute('data-dest', key);
    if (target.id) cta.setAttribute('data-aff-id', target.id);
  }

  function verdict(rows, best, ctx) {
    var unlimited = rows.filter(function (r) { return r.plan.id === 'unlimited'; })[0];
    var pro = rows.filter(function (r) { return r.plan.id === 'agency-pro'; })[0];
    var starter = rows.filter(function (r) { return r.plan.id === 'starter'; })[0];

    var v;
    if (best.net < 0) {
      v = '<p class="calc-headline">On these numbers, <strong>' + best.plan.name +
        '</strong> puts you ' + money(-best.net) + ' a month <em>ahead</em> — the ' +
        'markup you rebill exceeds the whole subscription.</p>';
    } else {
      v = '<p class="calc-headline">On these numbers, <strong>' + best.plan.name +
        '</strong> costs you ' + money(best.net) + ' a month.</p>';
    }

    var gap = pro.base - unlimited.base;

    // If Starter still fits, the $297-vs-$497 question is not this reader's
    // question yet. Answering it anyway would be noise dressed as thoroughness.
    if (best.plan.id === 'starter') {
      v += '<p>At ' + ctx.clients + ' sub-account' + (ctx.clients === 1 ? '' : 's') +
        ' you fit inside Starter, so you are ' +
        money0(unlimited.base - starter.base) + ' a month cheaper than the plan ' +
        'most comparisons push. Starter cannot rebill usage, so the ' +
        money(ctx.usageCost) + ' of usage is yours to absorb.</p>';
      v += '<p>Move to Unlimited when you pass three clients, need API access, or ' +
        'when passing usage through to clients would save you more than ' +
        money0(unlimited.base - starter.base) + ' a month.</p>';
      return v + usageFlag(ctx, best);
    }

    // The upgrade question that actually matters: Pro's extra $200 only pays
    // for itself if the markup you can charge exceeds it.
    if (ctx.rebill && ctx.markup > 1) {
      var extraRecovered = pro.recovered - unlimited.recovered;
      if (extraRecovered > gap) {
        v += '<p>Agency Pro costs ' + money0(gap) + ' more than Unlimited, but at a ' +
          ctx.markup.toFixed(2) + '&times; markup it rebills ' + money(extraRecovered) +
          ' more back to your clients. It clears the upgrade by ' +
          money(extraRecovered - gap) + ' a month.</p>';
      } else {
        var needed = (gap + ctx.usageCost) / (ctx.usageCost || 1);
        v += '<p>Agency Pro costs ' + money0(gap) + ' more than Unlimited and only ' +
          'rebills ' + money(extraRecovered) + ' more back at a ' + ctx.markup.toFixed(2) +
          '&times; markup. On this usage it does not pay for itself. You would need ' +
          'roughly a ' + (isFinite(needed) ? needed.toFixed(1) : '—') +
          '&times; markup, or more usage, before the upgrade breaks even.</p>';
      }
    } else if (ctx.rebill) {
      v += '<p>You are rebilling at cost, which Unlimited already allows. ' +
        'Agency Pro\'s extra ' + money0(gap) + ' a month buys the ability to add a ' +
        'markup on top — turn on a markup above to see whether that pays here.</p>';
    } else {
      v += '<p>You are not rebilling usage, so ' + money(ctx.usageCost) +
        ' a month is coming out of your own margin. Unlimited and Agency Pro both ' +
        'let you pass that through to clients; only Agency Pro lets you mark it up.</p>';
    }

    return v + usageFlag(ctx, best);
  }

  function usageFlag(ctx, best) {
    var pct = ctx.usageCost / (best.base || 1) * 100;
    if (pct < 25) return '';
    var scale = pct >= 100
      ? 'Usage now costs more than the plan itself'
      : 'Usage is ' + Math.round(pct) + '% of your subscription cost';
    return '<p class="calc-flag">' + scale + ' (' + money(ctx.usageCost) +
      ' a month). Any comparison quoting only the plan price is understating ' +
      'what you actually pay by a wide margin.</p>';
  }

  Object.keys(fields).forEach(function (k) {
    var el = fields[k];
    if (!el) return;
    el.addEventListener('input', compute);
    el.addEventListener('change', compute);
  });

  // Markup control is meaningless unless rebilling is on.
  function syncMarkup() {
    var on = fields.rebill.checked;
    fields.markup.disabled = !on;
    fields.markup.closest('.field').classList.toggle('field-disabled', !on);
  }
  fields.rebill.addEventListener('change', syncMarkup);

  root.classList.add('calc-live');
  syncMarkup();
  compute();
})();
