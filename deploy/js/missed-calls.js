/* Missed-call revenue calculator.
 *
 * Layer 1 acquisition asset: the reader arrives with a problem, quantifies it
 * themselves, and only then meets the tool that fixes it.
 *
 * HONESTY CONSTRAINT: this model contains no industry statistics, because we have
 * not measured any. Every rate is the reader's own input with a clearly-labelled
 * starting assumption. The page says so in visible text. A calculator that quietly
 * bakes in a flattering "recovery rate" is a sales tool pretending to be maths.
 */
(function () {
  'use strict';

  var root = document.getElementById('mc');
  if (!root) return;

  var RATES;
  try {
    RATES = JSON.parse(document.getElementById('mc-rates').textContent);
  } catch (e) { return; }

  var WEEKS_PER_MONTH = 52 / 12;   // 4.333…, not 4

  function $(id) { return root.querySelector('#' + id); }
  var f = {
    calls: $('m-calls'), missed: $('m-missed'), value: $('m-value'),
    close: $('m-close'), recovery: $('m-recovery')
  };
  var out = { verdict: $('mc-verdict'), body: $('mc-out') };

  function money(n) {
    if (!isFinite(n)) n = 0;
    var sign = n < 0 ? '\u2212' : '';
    return sign + '$' + Math.abs(n).toLocaleString('en-US',
      { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }
  function money2(n) {
    if (!isFinite(n)) n = 0;
    return '$' + n.toLocaleString('en-US',
      { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function num(el, fb) {
    var v = parseFloat(el && el.value);
    return isFinite(v) && v >= 0 ? v : fb;
  }
  function pct(el, fb) { return Math.min(100, Math.max(0, num(el, fb))); }

  function compute() {
    var callsWeek = num(f.calls, 0);
    var missedPct = pct(f.missed, 0);
    var value = num(f.value, 0);
    var closePct = pct(f.close, 0);
    var recoveryPct = pct(f.recovery, 0);

    var callsMonth = callsWeek * WEEKS_PER_MONTH;
    var missedMonth = callsMonth * (missedPct / 100);

    // A missed call is not a lost customer — only the share you would have closed.
    var lostCustomers = missedMonth * (closePct / 100);
    var lostRevenue = lostCustomers * value;

    var recoveredCustomers = lostCustomers * (recoveryPct / 100);
    var recoveredRevenue = recoveredCustomers * value;

    render({
      callsWeek: callsWeek, callsMonth: callsMonth, missedMonth: missedMonth,
      missedPct: missedPct, value: value, closePct: closePct,
      recoveryPct: recoveryPct,
      lostCustomers: lostCustomers, lostRevenue: lostRevenue,
      recoveredCustomers: recoveredCustomers, recoveredRevenue: recoveredRevenue
    });
  }

  function render(c) {
    var yearly = c.lostRevenue * 12;
    var v = '';

    if (c.lostRevenue <= 0) {
      v = '<p class="calc-headline">Put your numbers in above to see what missed ' +
          'calls are costing you.</p>';
      out.verdict.innerHTML = v;
      out.body.innerHTML = '';
      return;
    }

    v += '<p class="calc-headline">On these numbers you are losing about ' +
      '<strong>' + money(c.lostRevenue) + ' a month</strong> to calls nobody ' +
      'answers &mdash; ' + money(yearly) + ' a year.</p>';

    v += '<p>That is ' + Math.round(c.missedMonth).toLocaleString('en-US') +
      ' missed calls a month, of which you would have closed roughly ' +
      c.lostCustomers.toFixed(1) + ' into customers at ' + money(c.value) +
      ' each.</p>';

    if (c.recoveryPct > 0) {
      v += '<p>If an automatic text-back recovered ' + c.recoveryPct + '% of them, ' +
        'that is <strong>' + money(c.recoveredRevenue) + ' a month</strong> back ' +
        '(' + c.recoveredCustomers.toFixed(1) + ' customers).</p>';
    }

    var impliedAnnualRevenue = (c.lostRevenue / (c.missedPct / 100 || 1)) * 12;
    if (c.lostRevenue * 12 > 250000) {
      v += '<p class="calc-danger"><strong>Sanity-check this.</strong> These inputs ' +
        'imply you are losing ' + money(c.lostRevenue * 12) + ' a year to missed ' +
        'calls alone, from a business turning over roughly ' +
        money(impliedAnnualRevenue) + '. If that does not match your books, the ' +
        'close rate is the input to lower &mdash; most inbound calls are price ' +
        'shoppers, suppliers and wrong numbers, not jobs you would have won.</p>';
    }

    out.verdict.innerHTML = v;

    // Does the tool pay for itself? Compare against the real entry cost.
    var rows = RATES.plans.map(function (p) {
      var net = c.recoveredRevenue - p.monthly;
      return '<tr><td data-label="Plan">' + p.name + '</td>' +
        '<td data-label="Cost">' + money2(p.monthly) + '/mo</td>' +
        '<td data-label="Recovered">' + money(c.recoveredRevenue) + '/mo</td>' +
        '<td data-label="Net"><strong>' +
          (net >= 0
            ? '<span class="net-profit">+' + money(net) + '</span>'
            : '<span class="net-loss">' + money(net) + '</span>') +
        '</strong></td></tr>';
    }).join('');

    var h = '<h3 class="calc-sub">Against what the software costs</h3>';
    h += '<div class="table-scroll"><table class="cmp"><thead><tr>' +
      '<th scope="col">GoHighLevel plan</th><th scope="col">Cost</th>' +
      '<th scope="col">Recovered</th><th scope="col">Net position</th>' +
      '</tr></thead><tbody>' + rows + '</tbody></table></div>';

    var cheapest = RATES.plans[0];
    var multiple = c.recoveredRevenue / (cheapest.monthly || 1);

    if (multiple >= 2) {
      h += '<p class="calc-flag">At these numbers the recovered revenue is ' +
        multiple.toFixed(1) + '&times; the cost of the entry plan, so there is ' +
        'real headroom even if your recovery rate is half what you entered. That ' +
        'assumption is still yours, not a measurement.</p>';
    } else if (multiple > 1) {
      h += '<p class="calc-danger">This is too close to call. The recovered ' +
        'revenue is only ' + multiple.toFixed(1) + '&times; the entry plan, a ' +
        'margin of ' + money(c.recoveredRevenue - cheapest.monthly) + ' a month ' +
        '&mdash; and metered SMS, email and phone-number costs are <em>not</em> in ' +
        'that figure. They would plausibly erase it. Treat this as a no until ' +
        'either your call volume or your customer value goes up.</p>';
    } else {
      h += '<p class="calc-danger">At these numbers the recovered revenue does not ' +
        'cover even the entry plan. Do not buy software for this. Either the ' +
        'volume is too low, or the honest fix is that someone should answer the ' +
        'phone during business hours.</p>';
    }

    h += '<p class="calc-note">Metered usage sits on top of every plan price above. ' +
      'The <a href="/gohighlevel-true-cost-calculator/">true cost calculator</a> ' +
      'models SMS, email, voice and AI at your volume.</p>';

    out.body.innerHTML = h;
  }

  // Home-services presets. These are STARTING POINTS shaped by trade, not survey
  // data — a roofing job is worth more than a drain unblock, and the calculator is
  // useless if it opens on numbers no contractor recognises.
  var PRESETS = {
    roofing:    { calls: 40,  missed: 25, value: 9000,  close: 10 },
    hvac:       { calls: 60,  missed: 25, value: 1400,  close: 20 },
    plumbing:   { calls: 100, missed: 25, value: 450,   close: 30 },
    electrical: { calls: 60,  missed: 25, value: 700,   close: 25 },
    remodeling: { calls: 25,  missed: 20, value: 18000, close: 6  },
    other:      { calls: 100, missed: 20, value: 500,   close: 25 }
  };
  var presetSel = root.querySelector('#m-preset');
  if (presetSel) {
    presetSel.addEventListener('change', function () {
      var v = PRESETS[presetSel.value];
      if (!v) return;
      f.calls.value = v.calls; f.missed.value = v.missed;
      f.value.value = v.value; f.close.value = v.close;
      compute();
    });
  }

  Object.keys(f).forEach(function (k) {
    if (!f[k]) return;
    f[k].addEventListener('input', compute);
    f[k].addEventListener('change', compute);
  });

  root.classList.add('calc-live');
  compute();
})();
