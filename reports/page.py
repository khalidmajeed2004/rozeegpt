import json
D=json.load(open('data.json')); C=json.load(open('charts.json'))
M=D['months']

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

OV=' class="ov"'
mrows=''.join(
 f'<tr{OV if m["cum"]>D["purchased"] else ""}><td class="mo">{esc(m["lbl"])}</td>'
 f'<td class="n">{m["req"]}</td><td class="n">{m["cum"]:,}</td><td class="n">{m["util"]}%</td>'
 f'<td class="n">{m["kpis"]:,}</td><td class="n">{m["users"]}</td><td class="n">{m["new_users"]}</td>'
 f'<td class="n">{m["uniq_t"]}</td></tr>' for m in M)

urows=''.join(
 f'<tr><td class="rk">{i+1}</td><td class="uid">{esc(u["u"])}</td><td class="n">{u["req"]}</td>'
 f'<td class="n">{u["kpis"]:,}</td><td class="n">{u["titles"]}</td><td class="sp">{esc(u["span"])}</td></tr>'
 for i,u in enumerate(D['top_users']))

trows=''.join(
 f'<tr><td class="ttl">{esc(t["label"])}</td><td class="n">{t["n"]}</td><td class="n">{t["users"]}</td></tr>'
 for t in D['top_titles'])

HTML=f'''<title>EFU Utilisation Statement</title>
<style>
:root{{
  color-scheme:light;
  --paper:#f4f6f7; --card:#ffffff; --ink:#141a21; --ink-2:#3f4a56; --mute:#6b7683;
  --rule:#e0e4e7; --rule-2:#eef1f3; --band:#161d26; --band-ink:#eef2f5;
  --blue:#2a78d6; --blue-soft:rgba(42,120,214,.14); --red:#c9342f; --red-soft:rgba(201,52,47,.16);
  --amber:#eb6834; --chip:#eef3fa; --chip-ink:#1c5cab; --chip-r:#fbeeed; --chip-r-ink:#a52a26;
  --shadow:0 1px 2px rgba(20,26,33,.05),0 6px 18px -10px rgba(20,26,33,.14);
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,"Liberation Mono",monospace;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  color-scheme:dark;
  --paper:#101316; --card:#171b1f; --ink:#eef1f4; --ink-2:#c0c8d0; --mute:#8d97a3;
  --rule:#2a3037; --rule-2:#21262b; --band:#080a0c; --band-ink:#eef2f5;
  --blue:#3987e5; --blue-soft:rgba(57,135,229,.20); --red:#e06661; --red-soft:rgba(224,102,97,.20);
  --amber:#d95926; --chip:#16283e; --chip-ink:#8dbcf2; --chip-r:#3a1e1d; --chip-r-ink:#f0a29e;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 6px 18px -10px rgba(0,0,0,.6);
}}}}
:root[data-theme="dark"]{{
  color-scheme:dark;
  --paper:#101316; --card:#171b1f; --ink:#eef1f4; --ink-2:#c0c8d0; --mute:#8d97a3;
  --rule:#2a3037; --rule-2:#21262b; --band:#080a0c; --band-ink:#eef2f5;
  --blue:#3987e5; --blue-soft:rgba(57,135,229,.20); --red:#e06661; --red-soft:rgba(224,102,97,.20);
  --amber:#d95926; --chip:#16283e; --chip-ink:#8dbcf2; --chip-r:#3a1e1d; --chip-r-ink:#f0a29e;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 6px 18px -10px rgba(0,0,0,.6);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:860px;margin:0 auto;padding:28px 22px 56px;display:flex;flex-direction:column;gap:26px}}
.eyebrow{{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--mute);font-weight:650}}
h1{{font-size:29px;line-height:1.15;letter-spacing:-.022em;font-weight:680;margin:0;text-wrap:balance}}
h2{{font-size:17px;letter-spacing:-.012em;font-weight:670;margin:0}}
h3{{font-size:13.5px;letter-spacing:-.005em;font-weight:660;margin:0}}
p{{margin:0;color:var(--ink-2);max-width:66ch}}
.num{{font-family:var(--mono);font-variant-numeric:tabular-nums}}

/* masthead */
.mast{{background:var(--band);color:var(--band-ink);border-radius:12px;padding:26px 28px;
  display:flex;flex-direction:column;gap:14px}}
.mast .eyebrow{{color:#8fa3b8}}
.mast h1{{color:var(--band-ink)}}
.mast-meta{{display:flex;flex-wrap:wrap;gap:10px 26px;border-top:1px solid rgba(255,255,255,.13);padding-top:13px}}
.mm{{display:flex;flex-direction:column;gap:1px}}
.mm dt{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#8fa3b8;font-weight:650}}
.mm dd{{margin:0;font-family:var(--mono);font-size:12.5px;color:var(--band-ink)}}

/* verdict */
.verdict{{display:flex;align-items:flex-start;gap:14px;background:var(--card);border:1px solid var(--rule);
  border-left:4px solid var(--red);border-radius:10px;padding:15px 18px;box-shadow:var(--shadow)}}
.verdict svg{{flex:none;margin-top:2px}}
.verdict .vt{{font-weight:670;color:var(--ink);font-size:14.5px;margin-bottom:2px}}
.verdict p{{font-size:13.5px}}

/* tiles */
.tiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.tile{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;
  display:flex;flex-direction:column;gap:3px;box-shadow:var(--shadow)}}
.tile .lab{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);font-weight:650}}
.tile .fig{{font-family:var(--mono);font-size:27px;line-height:1.1;letter-spacing:-.03em;font-weight:600}}
.tile .sub{{font-size:11.5px;color:var(--mute)}}
.tile.crit .fig{{color:var(--red)}}

/* section + figure */
section{{display:flex;flex-direction:column;gap:14px}}
.shead{{display:flex;flex-direction:column;gap:3px;border-top:2px solid var(--ink);padding-top:11px}}
figure{{margin:0;background:var(--card);border:1px solid var(--rule);border-radius:10px;
  padding:16px 18px 8px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}}
figcaption{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}}
figcaption .ft{{font-size:13.5px;font-weight:660;letter-spacing:-.005em}}
.legend{{display:flex;gap:14px;flex-wrap:wrap}}
.lg{{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--ink-2)}}
.sw{{width:11px;height:11px;border-radius:3px;flex:none}}
.sw.b{{background:var(--blue)}} .sw.r{{background:var(--red)}} .sw.a{{background:var(--amber)}}
.sw.ln{{height:3px;border-radius:2px;width:16px}}
figure>svg,.panel>svg{{display:block;width:100%;height:auto;overflow:visible}}
.verdict>svg{{width:19px;height:19px;flex:none}}

/* svg classes */
.grid{{stroke:var(--rule-2);stroke-width:1}}
.axis{{stroke:var(--rule);stroke-width:1}}
.ax{{font-family:var(--mono);font-size:10px;fill:var(--mute)}}
.ax-y{{text-anchor:end}} .ax-x{{text-anchor:middle}} .ax-r{{text-anchor:end;font-family:var(--sans);font-size:11px}}
.ax-title{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;fill:var(--mute);font-weight:650;font-family:var(--sans)}}
.val{{font-family:var(--mono);font-size:10.5px;fill:var(--ink-2);text-anchor:middle;font-weight:600}}
.val-r{{text-anchor:start}}
.fill-in{{fill:var(--blue-soft)}} .fill-over{{fill:var(--red-soft)}}
.ln-in{{fill:none;stroke:var(--blue);stroke-width:2.2;stroke-linejoin:round}}
.ln-over{{fill:none;stroke:var(--red);stroke-width:2.2;stroke-linejoin:round}}
.ln-2{{fill:none;stroke:var(--amber);stroke-width:2.2;stroke-linejoin:round}}
.dot{{stroke:var(--card);stroke-width:2}} .dot.in{{fill:var(--blue)}} .dot.over{{fill:var(--red)}}
.dot2{{fill:var(--amber);stroke:var(--card);stroke-width:2}}
.bar{{stroke:var(--card);stroke-width:0}} .bar.in{{fill:var(--blue)}} .bar.over{{fill:var(--red)}} .bar.t{{fill:var(--blue)}}
.bar:hover,.dot:hover,.dot2:hover{{opacity:.78}}
.thresh{{stroke:var(--ink);stroke-width:1.4;stroke-dasharray:5 4;opacity:.7}}
.thresh-lbl{{font-size:9.5px;letter-spacing:.11em;fill:var(--ink-2);font-weight:660;font-family:var(--sans)}}
.exh{{stroke:var(--red);stroke-width:1.2;stroke-dasharray:3 3}}
.exh-dot{{fill:var(--red);stroke:var(--card);stroke-width:2}}
.note-lbl{{font-size:9.5px;letter-spacing:.09em;fill:var(--red);font-weight:680;font-family:var(--sans)}}
.pk{{font-family:var(--mono);font-size:13px;font-weight:650;fill:var(--red)}}
.pk2{{font-family:var(--mono);font-size:12px;font-weight:650;fill:var(--amber)}}

/* tables */
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--rule);border-radius:10px;box-shadow:var(--shadow)}}
table{{border-collapse:collapse;width:100%;font-size:12.5px}}
th{{text-align:right;font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--mute);
  font-weight:660;padding:11px 12px;border-bottom:1px solid var(--rule);white-space:nowrap}}
th:first-child,th.l{{text-align:left}}
td{{padding:8px 12px;border-bottom:1px solid var(--rule-2);white-space:nowrap}}
tbody tr:last-child td{{border-bottom:0}}
td.n{{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums}}
td.mo,td.uid,td.ttl{{font-weight:600}}
td.uid{{font-family:var(--mono);font-size:12px}}
td.rk{{font-family:var(--mono);color:var(--mute);width:1%}}
td.sp,td.ttl{{color:var(--ink-2);font-weight:400}}
td.sp{{font-family:var(--mono);font-size:11.5px;color:var(--mute)}}
tr.ov td{{background:var(--red-soft)}}
tfoot td{{border-top:1px solid var(--rule);font-weight:680;background:var(--rule-2)}}
.cap{{margin:0;padding:9px 13px 11px;font-size:11px;line-height:1.45;color:var(--mute);border-top:1px solid var(--rule);max-width:none}}

/* split + notes */
.split{{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}}
.panel{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:16px 18px;
  box-shadow:var(--shadow);display:flex;flex-direction:column;gap:10px}}
.stat-line{{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px solid var(--rule-2);font-size:12.5px}}
.stat-line:last-child{{border-bottom:0}}
.stat-line b{{font-family:var(--mono);font-weight:600}}
.chip{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:10.5px;font-weight:650;
  letter-spacing:.03em;background:var(--chip);color:var(--chip-ink)}}
.chip.r{{background:var(--chip-r);color:var(--chip-r-ink)}}
.note{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 18px;
  font-size:12px;color:var(--ink-2);display:flex;flex-direction:column;gap:7px}}
.note ul{{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:5px}}
.note code{{font-family:var(--mono);font-size:11.5px;background:var(--rule-2);padding:1px 5px;border-radius:4px}}
footer{{border-top:1px solid var(--rule);padding-top:12px;font-size:11px;color:var(--mute);
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
#tip{{position:fixed;pointer-events:none;opacity:0;transition:opacity .1s;background:var(--band);
  color:var(--band-ink);padding:6px 10px;border-radius:7px;font-size:11.5px;z-index:9;max-width:240px;
  box-shadow:0 6px 20px -6px rgba(0,0,0,.45)}}
#tip b{{display:block;font-family:var(--mono);font-size:10.5px;color:#8fa3b8;font-weight:650;
  letter-spacing:.07em;text-transform:uppercase}}
@media (max-width:680px){{.tiles{{grid-template-columns:repeat(2,1fr)}}.split{{grid-template-columns:1fr}}h1{{font-size:24px}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
@media print{{
  :root{{--paper:#fff;--card:#fff}}
  body{{background:#fff;font-size:10.5px;line-height:1.42}}
  .wrap{{max-width:none;padding:0;gap:7px}}
  figure,.panel,.tile,.note,.verdict,.mast{{box-shadow:none;break-inside:avoid}}
  .tw{{box-shadow:none;break-inside:auto}}
  .tw.keep{{break-inside:avoid}}
  tfoot{{display:table-row-group}}
  thead{{display:table-header-group}} tr{{break-inside:avoid}}
  .shead{{break-after:avoid}} figcaption{{break-after:avoid}}
  section{{gap:7px;break-inside:auto}}
  .mast{{padding:15px 18px;gap:9px;border-radius:8px}}
  h1{{font-size:21px}} h2{{font-size:14px}} h3{{font-size:12px}}
  .tiles{{gap:8px}} .tile{{padding:9px 11px}} .tile .fig{{font-size:20px}}
  .verdict{{padding:10px 13px;gap:10px}}
  figure{{padding:9px 11px 6px;gap:5px}}
  .tiles{{grid-template-columns:repeat(4,1fr)}}
  figcaption .ft{{font-size:11.5px}}
  .panel{{padding:10px 12px;gap:6px}}
  .split{{gap:9px}}
  .shead{{padding-top:7px}}
  table{{font-size:10px}} th{{padding:6px 8px;font-size:8.5px}} td{{padding:4px 8px}}
  .cap{{padding:5px 9px 5px;font-size:8.5px}}
  .note{{padding:7px 11px;font-size:8.5px;line-height:1.38;gap:3px}}
  .note ul{{display:block;column-count:2;column-gap:16px;padding-left:15px}}
  .note li{{margin-bottom:3px}}
  .note li{{break-inside:avoid}}
  .stat-line{{padding:2px 0;font-size:10px}}
  p{{max-width:none}}
  footer{{padding-top:3px;font-size:8px}}
  #tip{{display:none}}
  .pb{{break-before:auto}}
}}
@page{{size:A4;margin:10mm 10mm 8mm}}
</style>

<div class="wrap">

<header class="mast">
  <div class="eyebrow">Rozee KPI Generator · Account Utilisation Statement</div>
  <h1>EFU Life — utilisation &amp; user summary</h1>
  <dl class="mast-meta">
    <div class="mm"><dt>Account</dt><dd>EFU Life (company_id 630)</dd></div>
    <div class="mm"><dt>Period covered</dt><dd>{D['first']} – {D['last']}</dd></div>
    <div class="mm"><dt>Source</dt><dd>efukpidataaug2026.xlsx</dd></div>
    <div class="mm"><dt>Prepared</dt><dd>17 Aug 2026</dd></div>
  </dl>
</header>

<div class="verdict">
  <svg width="19" height="19" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6 19 17.4H1z" fill="none" stroke="var(--red)" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 7.2v4.6" stroke="var(--red)" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="14.5" r="1.05" fill="var(--red)"/></svg>
  <div>
    <div class="vt">The 500-ticket entitlement is fully consumed and over-drawn by {D['over']}.</div>
    <p>The 500th ticket was used on <strong>{D['exh_date']}</strong>. A further {D['over']} requests were served after that date — {D['util']}% of entitlement. A top-up or renewal is required to keep the service open.</p>
  </div>
</div>

<div class="tiles">
  <div class="tile"><span class="lab">Tickets purchased</span><span class="fig num">500</span><span class="sub">Contracted entitlement</span></div>
  <div class="tile crit"><span class="lab">Tickets utilised</span><span class="fig num">{D['used']}</span><span class="sub">{D['util']}% of entitlement</span></div>
  <div class="tile"><span class="lab">Unique users</span><span class="fig num">{D['users']}</span><span class="sub">All @efulife.com</span></div>
  <div class="tile"><span class="lab">KPIs generated</span><span class="fig num">{D['kpis']:,}</span><span class="sub">{D['avg_kpi']} per request</span></div>
</div>

<section>
  <div class="shead"><h2>1 · Ticket consumption against entitlement</h2>
  <p>Consumption tracked steadily below entitlement for eight months, then the June 2026 KPI-setting cycle consumed {D['jun']} tickets in a single month.</p></div>
  <figure>
    <figcaption><span class="ft">Cumulative tickets consumed vs. 500-ticket entitlement</span>
      <span class="legend"><span class="lg"><span class="sw ln b"></span>Within entitlement</span><span class="lg"><span class="sw ln r"></span>Beyond entitlement</span></span>
    </figcaption>
    {C['a']}
  </figure>
  <figure>
    <figcaption><span class="ft">Tickets utilised per month</span>
      <span class="legend"><span class="lg"><span class="sw b"></span>Within entitlement</span><span class="lg"><span class="sw r"></span>Beyond entitlement</span></span>
    </figcaption>
    {C['b']}
  </figure>
</section>

<section>
  <div class="shead"><h2>2 · Month-wise utilisation</h2></div>
  <div class="tw keep"><table>
    <thead><tr><th>Month</th><th>Tickets used</th><th>Cumulative</th><th>% of 500</th><th>KPIs generated</th><th>Active users</th><th>First-time users</th><th>Distinct titles</th></tr></thead>
    <tbody>{mrows}</tbody>
    <tfoot><tr><td>Total</td><td class="n">{D['used']}</td><td class="n">{D['used']}</td><td class="n">{D['util']}%</td><td class="n">{D['kpis']:,}</td><td class="n">{D['users']}</td><td class="n">{D['users']}</td><td class="n">{D['uniq_t']}</td></tr></tfoot>
  </table><p class="cap">Shaded rows are months in which cumulative consumption exceeded the 500-ticket entitlement. Active-users and distinct-titles totals are de-duplicated across the period, so they do not equal the column sums.</p></div>
</section>

<section class="pb">
  <div class="shead"><h2>3 · User base</h2>
  <p>{D['users']} distinct EFU users generated KPIs across {D['active_days']} active days. Adoption is broad but consumption is concentrated: the ten heaviest users account for {D['top10share']}% of all tickets.</p></div>
  <figure>
    <figcaption><span class="ft">Monthly active users and cumulative unique users</span>
      <span class="legend"><span class="lg"><span class="sw b"></span>Active in month</span><span class="lg"><span class="sw ln a"></span>Cumulative unique</span></span>
    </figcaption>
    {C['c']}
  </figure>
  <div class="split">
    <div class="panel"><h3>Depth of use</h3>{C['d']}</div>
    <div class="panel"><h3>User base at a glance</h3>
      <div class="stat-line"><span>Total unique users</span><b>{D['users']}</b></div>
      <div class="stat-line"><span>Median tickets per user</span><b>5</b></div>
      <div class="stat-line"><span>Users with 10+ tickets</span><b>25</b></div>
      <div class="stat-line"><span>Single-use users</span><b>{D['buckets']['1']}</b></div>
      <div class="stat-line"><span>Top 10 users' share</span><b>{D['top10share']}%</b></div>
      <div class="stat-line"><span>Top 20 users' share</span><b>{D['top20share']}%</b></div>
      <div class="stat-line"><span>Joined in June 2026</span><b>45</b></div>
    </div>
  </div>
  <div class="tw"><table>
    <thead><tr><th>#</th><th class="l">User</th><th>Tickets</th><th>KPIs generated</th><th>Distinct titles</th><th>Active span</th></tr></thead>
    <tbody>{urows}</tbody>
  </table><p class="cap">Top 10 users by tickets consumed. Usernames shown without the @efulife.com domain.</p></div>
</section>

<section class="pb">
  <div class="shead"><h2>4 · Unique job titles</h2>
  <p>Of {D['titled']} titled requests, <strong>{D['uniq_t']} distinct titles</strong> were submitted — {D['single']} used exactly once and {D['rep']} submitted more than once. Roughly {round(100-D['uniq_t']/D['titled']*100)}% of requests re-ran a title already seen, largely draft-and-refine cycles rather than new roles.</p></div>
  <figure>
    <figcaption><span class="ft">New unique titles first seen each month</span>
      <span class="legend"><span class="lg"><span class="sw b"></span>Titles not seen in any earlier month</span></span>
    </figcaption>
    {C['e']}
  </figure>
  <div class="split">
    <div class="panel"><h3>Title composition</h3>
      <div class="stat-line"><span>Titled requests</span><b>{D['titled']}</b></div>
      <div class="stat-line"><span>Distinct titles</span><b>{D['uniq_t']}</b></div>
      <div class="stat-line"><span>Titles used once</span><b>{D['single']}</b></div>
      <div class="stat-line"><span>Titles re-submitted</span><b>{D['rep']}</b></div>
      <div class="stat-line"><span>New titles in June 2026</span><b>307</b></div>
      <div class="stat-line"><span>Requests with no title</span><b>9</b></div>
    </div>
    <div class="panel"><h3>Structured job descriptions</h3>
      <p style="font-size:12.5px">21 requests were submitted on EFU's structured JD template, which carries an explicit <code>Position Title</code> and <code>Designation</code>. Titles captured there:</p>
      <div class="stat-line"><span>Fluctuations &amp; Coordinator</span><b>6</b></div>
      <div class="stat-line"><span>Sales Administration Section Head</span><b>3</b></div>
      <div class="stat-line"><span>Life Underwriter</span><b>2</b></div>
      <div class="stat-line"><span>Manager</span><b>2</b></div>
      <div class="stat-line"><span>Associate Claims Examiner</span><b>1</b></div>
      <p style="font-size:12px;color:var(--mute)">Designations recorded: Assistant Manager (9), Executive Officer (7), Deputy Manager (3), Manager (2).</p>
    </div>
  </div>
  <div class="tw"><table>
    <thead><tr><th class="l">Most re-submitted titles</th><th>Requests</th><th>Users</th></tr></thead>
    <tbody>{trows}</tbody>
  </table><p class="cap">The title is captured by the platform from the opening words of each submitted request, so a repeated title indicates the same source document re-run — not necessarily the same role.</p></div>
</section>

<div class="note">
  <span class="eyebrow">Basis of preparation</span>
  <ul>
    <li><strong>Ticket = one KPI-generation request.</strong> 852 requests were submitted; 838 returned KPIs and 14 returned none. Utilisation is stated on all 852 requests; on successful requests only it is 838 (167.6%).</li>
    <li><strong>Tickets purchased (500)</strong> is a contract figure supplied separately — the raw data sheet holds no entitlement or commercial fields.</li>
    <li><strong>Users</strong> are distinct email addresses in the <code>KPIs</code> sheet. All 852 requests sit under <code>company_id 630</code> on the efulife.com domain.</li>
    <li><strong>Job titles</strong> are taken from the <code>title</code> column. This value is generated by the platform from the opening words of the submitted request rather than entered as a role name, so it is a reliable count of <em>distinct submissions</em> and an approximate count of distinct roles. Only 21 requests used the structured JD template that carries a true position title.</li>
    <li>Figures cover {D['first']} to {D['last']}. KPI detail for Sep–Oct 2025 is not present in the <code>Data</code> sheet, so those two months show 8 requests with no KPI rows.</li>
  </ul>
</div>

<footer><span>Rozee KPI Generator · EFU Life account utilisation</span><span>Prepared 17 August 2026</span></footer>
</div>

<div id="tip" role="status"></div>
<script>
(function(){{
  var tip=document.getElementById('tip');
  function show(e){{
    var t=e.target.getAttribute('data-t'), v=e.target.getAttribute('data-v');
    if(!t) return;
    tip.innerHTML='<b>'+t+'</b>'+v;
    tip.style.opacity='1';
    move(e);
  }}
  function move(e){{
    var x=e.clientX+14, y=e.clientY+14, r=tip.getBoundingClientRect();
    if(x+r.width>innerWidth-8) x=e.clientX-r.width-14;
    if(y+r.height>innerHeight-8) y=e.clientY-r.height-14;
    tip.style.left=x+'px'; tip.style.top=y+'px';
  }}
  document.querySelectorAll('[data-t]').forEach(function(el){{
    el.addEventListener('mouseenter',show);
    el.addEventListener('mousemove',move);
    el.addEventListener('mouseleave',function(){{tip.style.opacity='0';}});
  }});
}})();
</script>
'''
open('efu-utilisation-summary.html','w').write(HTML)
print('written', len(HTML))
