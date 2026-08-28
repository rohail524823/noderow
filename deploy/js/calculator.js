/* GoHighLevel true-cost calculator.
 *
 * Progressive enhancement: the page renders a complete, readable pricing table
 * and worked example with JS off. This script upgrades that into a live model.
 *
 * All rates come from the data-rates JSON block the build writes into the page,
 * which comes from content/pricing-data.json. No number is hardcoded here.
 *
 * Models three things competitors' static tables do not:
 *   1. Metered usage as a first-class layer, not a footnote
 *   2. The two-meter AI trap — Voice AI minutes still incur phone minutes
 *   3. The flat-rate rebilling margin trap — HighLevel bills the agency on
 *      actuals regardless of what the agency charges the sub-account
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
  var AI = RATES.ai;

  function $(id) { return root.querySelector('#' + id); }

  var f = {
    clients: $('f-clients'), sms: $('f-sms'), email: $('f-email'),
    voice: $('f-voice'), numbers: $('f-numbers'), premium: $('f-premium'),
    aiModel: $('f-ai-model'), aiMsgs: $('f-ai-msgs'), aiVoice: $('f-ai-voice'),
    billing: $('f-billing'), rebill: $('f-rebill'),
    rebillMode: $('f-rebill-mode'), markup: $('f-markup'), flatRate: $('f-flat'),
    carrier: $('f-carrier')
  };

  var out = { body: $('calc-out'), verdict: $('calc-verdict') };

  function money(n) {
    if (!isFinite(n)) n = 0;
    return '$' + n.toLocaleString('en-US',
      { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function money0(n) {
    if (!isFinite(n)) n = 0;
    return '$' + Math.round(n).toLocaleString('en-US');
  }
  function int(n) { return Math.round(n).toLocaleString('en-US'); }
  function rate(n) {
    if (!isFinite(n)) n = 0;
    return '$' + n.toLocaleString('en-US',
      { minimumFractionDigits: 4, maximumFractionDigits: 5 });
  }
  function num(el, fallback) {
    var v = parseFloat(el && el.value);
    return isFinite(v) && v >= 0 ? v : fallback;
  }
  function aiModel(id) {
    for (var i = 0; i < AI.models.length; i++) {
      if (AI.models[i].id === id) return AI.models[i];
    }
    return AI.models[0];
  }

  function compute() {
    var clients = Math.max(1, Math.round(num(f.clients, 1)));
    var annual = f.billing.value === 'annual';
    var rebill = f.rebill.checked;
    var mode = f.rebillMode.value;
    var markup = Math.max(1, num(f.markup, 1));
    var flatRate = Math.max(0, num(f.flatRate, 0));

    // Per-client volumes scale across sub-accounts.
    var smsSeg = clients * num(f.sms, 0);
    var emails = clients * num(f.email, 0);
    var voiceMin = clients * num(f.voice, 0);
    var numbers = clients * num(f.numbers, 0);
    var premium = clients * num(f.premium, 0);
    var aiMsgs = clients * num(f.aiMsgs, 0);
    var aiVoiceMin = clients * num(f.aiVoice, 0);

    var model = aiModel(f.aiModel.value);

    // --- metered layer ---
    // Carrier surcharges are passed through by the recipient's carrier ON TOP of
    // the base segment rate. They roughly double the real cost of an SMS and are
    // the line almost every competing pricing page omits entirely.
    var carrierRate = f.carrier.checked ? U.carrierFees.averageSmsOutbound : 0;
    var smsBaseCost = smsSeg * U.smsPerSegment;
    var smsCarrierCost = smsSeg * carrierRate;
    var smsCost = smsBaseCost + smsCarrierCost;
    var emailCost = (emails / 1000) * U.emailPer1000;
    var numberCost = numbers * U.localNumberPerMonth;
    var premiumCost = premium * U.premiumWorkflowActionPerExecution;

    // THE TWO-METER TRAP. Voice AI minutes are billed by the AI product, but the
    // phone call underneath is billed separately by LC Phone — on every tier,
    // including "unlimited". Both meters run.
    var aiVoicePhoneCost = aiVoiceMin * U.voiceOutboundPerMinute;
    var plainVoiceCost = voiceMin * U.voiceOutboundPerMinute;
    var voiceCost = plainVoiceCost + aiVoicePhoneCost;

    // --- AI layer ---
    var aiSubscription = 0, aiMetered = 0, aiOverageNote = null;
    if (model.id === 'pay-per-use') {
      aiMetered = aiMsgs * model.conversationPerMessageEstimate
        + aiVoiceMin * (model.voiceEnginePerMinute + model.ttsPerMinuteLow);
    } else {
      aiSubscription = clients * model.monthlyPerLocation;
      if (model.includedConversationResponses !== null) {
        var overMsgs = Math.max(0, aiMsgs - clients * model.includedConversationResponses);
        var overVoice = Math.max(0, aiVoiceMin - clients * model.includedVoiceMinutes);
        if (overMsgs > 0 || overVoice > 0) {
          var pu = aiModel('pay-per-use');
          aiMetered = overMsgs * pu.conversationPerMessageEstimate
            + overVoice * (pu.voiceEnginePerMinute + pu.ttsPerMinuteLow);
          aiOverageNote = int(overMsgs) + ' AI messages and ' + int(overVoice) +
            ' Voice AI minutes exceed what ' + model.name + ' includes, so they ' +
            'fall back to pay-per-use rates.';
        }
      }
    }

    var usageCost = smsCost + emailCost + voiceCost + numberCost + premiumCost + aiMetered;
    var billableUnits = smsSeg + emails + voiceMin + aiVoiceMin + aiMsgs + premium;

    var rows = PLANS.map(function (p) {
      var base = annual ? p.annualMonthlyEquivalent : p.monthly;
      var eligible = p.subAccounts === null || clients <= p.subAccounts;

      var recovered = 0, shortfall = 0;
      if (rebill && p.rebillAtCost) {
        if (!p.rebillWithMarkup) {
          recovered = usageCost;                      // at cost only
        } else if (mode === 'fixed-rate') {
          // THE MARGIN TRAP: you charge a flat rate per unit, HighLevel still
          // bills you on actuals. Below cost, every unit loses money.
          recovered = billableUnits * flatRate;
          if (recovered < usageCost) shortfall = usageCost - recovered;
        } else {
          recovered = usageCost * markup;
        }
      }

      return {
        plan: p, base: base, usage: usageCost, aiSub: aiSubscription,
        recovered: recovered, shortfall: shortfall,
        net: base + aiSubscription + usageCost - recovered, eligible: eligible
      };
    });

    var viable = rows.filter(function (r) { return r.eligible; });
    var best = viable.reduce(function (a, b) { return b.net < a.net ? b : a; }, viable[0]);

    render(rows, best, {
      clients: clients, annual: annual, rebill: rebill, mode: mode,
      markup: markup, flatRate: flatRate, model: model,
      usageCost: usageCost, aiSubscription: aiSubscription,
      billableUnits: billableUnits, aiOverageNote: aiOverageNote,
      smsCost: smsCost, emailCost: emailCost, voiceCost: voiceCost,
      numberCost: numberCost, premiumCost: premiumCost, aiMetered: aiMetered,
      smsBaseCost: smsBaseCost, smsCarrierCost: smsCarrierCost,
      carrierOn: f.carrier.checked,
      smsSeg: smsSeg, emails: emails, voiceMin: voiceMin, numbers: numbers,
      premium: premium, aiMsgs: aiMsgs, aiVoiceMin: aiVoiceMin,
      aiVoicePhoneCost: aiVoicePhoneCost
    });
  }

  function render(rows, best, c) {
    var h = '';

    h += '<h3 class="calc-sub">Your monthly cost, by plan</h3>';
    h += '<div class="table-scroll"><table class="cmp"><thead><tr>' +
      '<th scope="col">Plan</th><th scope="col">Subscription</th>' +
      '<th scope="col">AI plan</th><th scope="col">Usage</th>' +
      '<th scope="col">Rebilled back</th><th scope="col">Net position</th>' +
      '</tr></thead><tbody>';

    var bestLabel = best.net < 0 ? 'Best for you' : 'Cheapest for you';
    rows.forEach(function (r) {
      var name = r.plan.name;
      if (!r.eligible) {
        name += ' <span class="pill pill-error">Too few sub-accounts</span>';
      } else if (r === best) {
        name += ' <span class="pill pill-ok">' + bestLabel + '</span>';
      }
      var netCell = !r.eligible ? '<span class="muted">n/a</span>'
        : r.net < 0 ? '<span class="net-profit">+' + money(-r.net) + ' profit</span>'
        : money(r.net);
      h += '<tr' + (r === best ? ' class="calc-best"' : '') + '>' +
        '<td data-label="Plan">' + name + '</td>' +
        '<td data-label="Subscription">' + money0(r.base) + '</td>' +
        '<td data-label="AI plan">' + (r.aiSub ? money(r.aiSub) : '<span class="muted">—</span>') + '</td>' +
        '<td data-label="Usage">' + money(r.usage) + '</td>' +
        '<td data-label="Rebilled back">' +
          (r.recovered > 0 ? '&minus;' + money(r.recovered) : '<span class="muted">—</span>') +
        '</td>' +
        '<td data-label="Net position"><strong>' + netCell + '</strong></td></tr>';
    });
    h += '</tbody></table></div>';

    h += '<h3 class="calc-sub">Where the usage cost comes from</h3><ul class="calc-breakdown">';
    function row(label, cost, cls) {
      h += '<li' + (cls ? ' class="' + cls + '"' : '') + '><span>' + label +
        '</span><strong>' + money(cost) + '</strong></li>';
    }
    row(int(c.smsSeg) + ' SMS segments, base rate', c.smsBaseCost);
    if (c.smsCarrierCost > 0) {
      row('&nbsp;&nbsp;&#8627; carrier surcharges on those segments',
          c.smsCarrierCost, 'calc-trap');
    }
    row(int(c.emails) + ' emails', c.emailCost);
    if (c.voiceMin) row(int(c.voiceMin) + ' voice minutes', c.voiceMin * RATES.usage.voiceOutboundPerMinute);
    if (c.aiVoiceMin) {
      row(int(c.aiVoiceMin) + ' phone minutes <em>under</em> Voice AI',
          c.aiVoicePhoneCost, 'calc-trap');
    }
    if (c.numbers) row(int(c.numbers) + ' phone numbers rented', c.numberCost);
    if (c.premium) row(int(c.premium) + ' premium workflow actions', c.premiumCost);
    if (c.aiMetered) row('AI metered usage', c.aiMetered);
    h += '<li class="calc-total"><span>Total metered usage</span><strong>' +
      money(c.usageCost) + '</strong></li></ul>';

    if (c.smsCarrierCost > 0) {
      var pctUp = c.smsCarrierCost / (c.smsBaseCost || 1) * 100;
      h += '<p class="calc-flag"><strong>Carrier surcharges add ' +
        Math.round(pctUp) + '% to your SMS bill.</strong> ' + U.carrierFees.note +
        ' The rate used here is a blended average across the major US carriers; ' +
        'your real figure depends on your recipients\' carrier mix.</p>';
    }
    if (c.aiVoiceMin > 0) {
      h += '<p class="calc-flag"><strong>Two meters are running.</strong> ' +
        AI.twoMeterWarning + ' That is ' + money(c.aiVoicePhoneCost) +
        ' of phone charges on this page that your AI plan does not cover.</p>';
    }
    if (c.aiOverageNote) {
      h += '<p class="calc-flag">' + c.aiOverageNote + '</p>';
    }

    out.body.innerHTML = h;
    out.verdict.innerHTML = verdict(rows, best, c);
    routeCta(best, c);
  }

  function verdict(rows, best, c) {
    function byId(id) {
      return rows.filter(function (r) { return r.plan.id === id; })[0];
    }
    var unlimited = byId('unlimited'), pro = byId('agency-pro'), starter = byId('starter');
    var v;

    if (best.net < 0) {
      v = '<p class="calc-headline">On these numbers, <strong>' + best.plan.name +
        '</strong> puts you ' + money(-best.net) + ' a month <em>ahead</em> — what ' +
        'you rebill exceeds what you pay.</p>';
    } else {
      v = '<p class="calc-headline">On these numbers, <strong>' + best.plan.name +
        '</strong> costs you ' + money(best.net) + ' a month.</p>';
    }

    // The margin trap gets top billing whenever it is actually biting.
    if (c.rebill && c.mode === 'fixed-rate' && pro.shortfall > 0) {
      v += '<p class="calc-danger"><strong>Your flat rate is below cost.</strong> ' +
        'On Agency Pro you would charge ' + rate(c.flatRate) + ' per billable unit ' +
        'while HighLevel bills you on actual consumption, so you absorb ' +
        money(pro.shortfall) + ' a month. ' + RATES.rebilling.marginTrapWarning +
        ' Break-even is about ' + rate(c.usageCost / (c.billableUnits || 1)) +
        ' per unit.</p>';
    }

    var gap = pro.base - unlimited.base;

    if (best.plan.id === 'starter') {
      v += '<p>At ' + c.clients + ' sub-account' + (c.clients === 1 ? '' : 's') +
        ' you fit inside Starter, so you are ' + money0(unlimited.base - starter.base) +
        ' a month cheaper than the plan most comparisons push. Starter cannot rebill ' +
        'usage at all, so the ' + money(c.usageCost) + ' of usage is yours to absorb.</p>';
      return v + usageFlag(c, best);
    }

    if (c.rebill && c.mode === 'multiplier' && c.markup > 1) {
      var extra = pro.recovered - unlimited.recovered;
      if (extra > gap) {
        v += '<p>Agency Pro costs ' + money0(gap) + ' more than Unlimited, and at a ' +
          c.markup.toFixed(2) + '&times; markup it rebills ' + money(extra) +
          ' more back to your clients. It clears the upgrade by ' + money(extra - gap) +
          ' a month.</p>';
      } else {
        var needed = (gap + c.usageCost) / (c.usageCost || 1);
        v += '<p>Agency Pro costs ' + money0(gap) + ' more than Unlimited and rebills ' +
          'only ' + money(extra) + ' more back at a ' + c.markup.toFixed(2) +
          '&times; markup. On this usage it does not pay for itself — you would need ' +
          'roughly a ' + (isFinite(needed) ? needed.toFixed(1) : '—') +
          '&times; markup, or more usage, to break even.</p>';
      }
    } else if (c.rebill && c.mode === 'fixed-rate') {
      v += '<p>Fixed-rate rebilling requires Agency Pro. At ' + rate(c.flatRate) +
        ' per unit across ' + int(c.billableUnits) + ' billable units you recover ' +
        money(pro.recovered) + ' against ' + money(c.usageCost) + ' of real cost.</p>';
    } else if (c.rebill) {
      v += '<p>You are rebilling at cost, which Unlimited already allows. Agency Pro\'s ' +
        'extra ' + money0(gap) + ' a month buys the ability to add margin on top.</p>';
    } else {
      v += '<p>You are not rebilling, so ' + money(c.usageCost) + ' a month comes out ' +
        'of your own margin. Unlimited lets you pass it through at cost; only Agency ' +
        'Pro lets you mark it up.</p>';
    }

    if (c.aiSubscription > 0) {
      v += '<p class="calc-note">' + c.model.name + ' is counted as your agency cost ' +
        'at ' + money(c.aiSubscription) + ' a month (' + c.clients + ' locations). ' +
        'Whether you can rebill that per-location fee is a separate question from ' +
        'usage rebilling, so this model does not assume you recover it.</p>';
    }
    if (c.model.id !== 'pay-per-use' && c.model.commissionable === false) {
      v += '<p class="calc-note">' + c.model.name + ' earns NodeRow no commission. ' +
        'We are recommending it here because it fits your volume.</p>';
    }

    return v + usageFlag(c, best);
  }

  function usageFlag(c, best) {
    var denom = best.base + c.aiSubscription;
    var pct = c.usageCost / (denom || 1) * 100;
    if (pct < 25) return '';
    var scale = pct >= 100
      ? 'Metered usage now costs more than your subscription'
      : 'Metered usage is ' + Math.round(pct) + '% of your subscription cost';
    return '<p class="calc-flag">' + scale + ' (' + money(c.usageCost) +
      ' a month). Any comparison quoting only the plan price is understating what ' +
      'you actually pay by a wide margin.</p>';
  }

  function routeCta(best, c) {
    var links = RATES.links;
    var cta = document.querySelector('#calc-cta a[data-aff]');
    if (!cta || !links) return;
    var key = 'pricing', label = 'See GoHighLevel plans and pricing';
    if (best.plan.id === 'agency-pro' && links['saas-pro']) {
      key = 'saas-pro'; label = 'Start a SaaS Pro trial';
    } else if (c.annual && links.annual) {
      key = 'annual'; label = 'See annual pricing';
    }
    var t = links[key];
    if (!t || !t.url) return;
    cta.href = t.url;
    cta.textContent = label;
    cta.setAttribute('data-dest', key);
    if (t.id) cta.setAttribute('data-aff-id', t.id);
  }

  function syncModes() {
    var on = f.rebill.checked;
    var fixed = f.rebillMode.value === 'fixed-rate';
    [f.rebillMode, f.markup, f.flatRate].forEach(function (el) {
      el.disabled = !on;
      el.closest('.field').classList.toggle('field-disabled', !on);
    });
    f.markup.closest('.field').hidden = fixed;
    f.flatRate.closest('.field').hidden = !fixed;

    var sub = f.aiModel.value !== 'pay-per-use';
    f.aiVoice.closest('.field').hidden = false;
    root.querySelector('#ai-sub-note').hidden = !sub;
  }

  Object.keys(f).forEach(function (k) {
    if (!f[k]) return;
    f[k].addEventListener('input', compute);
    f[k].addEventListener('change', compute);
  });
  [f.rebill, f.rebillMode, f.aiModel].forEach(function (el) {
    el.addEventListener('change', syncModes);
  });

  root.classList.add('calc-live');
  syncModes();
  compute();
})();
