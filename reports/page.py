import json, base64, pathlib
D=json.load(open('data.json')); C=json.load(open('charts.json'))
M=D['months']
STYLE='<style>\n'+open('report.css').read()+'</style>'

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# ---- logo slots -------------------------------------------------------------
# Drop a real logo file into logos/ (rozeegpt.* / efulife.*) and re-run; it is
# embedded as a data URI. Without one, a typographic lockup is used instead.
MIME={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.webp':'image/webp'}

# Dark-mode treatment per logo. The cover card is near-black in dark mode, so a
# dark monochrome logo needs help:
#   'invert' — flip a black-on-transparent mark to white (monochrome marks only)
#   'plate'  — sit the logo on a white rounded plate (correct for colour marks)
#   'none'   — the mark already reads on a dark ground
DARK_MODE={'rozeegpt':'invert', 'efulife':'plate'}

def logo(stem, fallback):
    for ext in ('.svg','.png','.jpg','.jpeg','.webp'):
        f=pathlib.Path('logos')/(stem+ext)
        if f.exists():
            b64=base64.b64encode(f.read_bytes()).decode()
            cls='logo-img dk-'+DARK_MODE.get(stem,'plate')
            return (f'<img class="{cls}" src="data:{MIME[ext]};base64,{b64}" '
                    f'alt="{stem} logo">')
    return fallback

ROZEE=logo('rozeegpt','<span class="wordmark">rozeegpt<span class="wm-a">.ai</span></span>')
EFU=logo('efulife','<span class="wordmark">EFU<span class="wm-b">Life</span></span>')

mrows=''.join(
 f'<tr{OV if m["cum"]>D["purchased"] else ""}><td class="mo">{esc(m["lbl"])}</td>'
 f'<td class="n">{m["req"]}</td><td class="n">{m["cum"]:,}</td><td class="n">{m["util"]}%</td>'
 f'<td class="n">{m["kpis"]:,}</td><td class="n">{m["users"]}</td><td class="n">{m["new_users"]}</td></tr>'
 for m in M) if (OV:=' class="ov"') else ''

urows=''.join(
 f'<tr><td class="rk">{i+1}</td><td class="uid">{esc(u["u"])}</td><td class="n">{u["req"]}</td>'
 f'<td class="n">{u["kpis"]:,}</td><td class="sp">{esc(u["span"])}</td></tr>'
 for i,u in enumerate(D['top_users']))

EXTRA='''
<style>
/* --- cover page --- */
.cover{display:flex;flex-direction:column;justify-content:space-between;gap:44px;
  background:var(--card);border:1px solid var(--rule);border-radius:14px;
  padding:38px 40px 32px;box-shadow:var(--shadow);min-height:520px}
.crest{display:flex;align-items:center;gap:26px;flex-wrap:wrap}
.crest .slot{display:flex;flex-direction:column;gap:7px;min-width:150px}
.crest .role{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--mute);font-weight:660}
.crest .divider{width:1px;align-self:stretch;background:var(--rule);min-height:44px}
.logo-img{max-height:46px;max-width:190px;width:auto;height:auto;object-fit:contain;display:block}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .dk-invert{filter:invert(1)}
  :root:not([data-theme="light"]) .dk-plate{background:#fff;border-radius:6px;padding:5px 8px}}
:root[data-theme="dark"] .dk-invert{filter:invert(1)}
:root[data-theme="dark"] .dk-plate{background:#fff;border-radius:6px;padding:5px 8px}
@media print{.dk-invert{filter:none}.dk-plate{background:none;padding:0}}
.wordmark{font-size:25px;font-weight:700;letter-spacing:-.03em;line-height:1;color:var(--ink)}
.wm-a{color:var(--blue)} .wm-b{color:var(--mute);font-weight:500;margin-left:.16em}
.cover-foot{display:flex;flex-direction:column;gap:30px}
.cover-body{display:flex;flex-direction:column;gap:14px}
.cover h1{font-size:40px;line-height:1.08;letter-spacing:-.028em}
.cover .lede{font-size:15px;color:var(--ink-2);max-width:52ch}
.duration{display:inline-flex;align-items:baseline;gap:11px;align-self:flex-start;
  background:var(--band);color:var(--band-ink);border-radius:9px;padding:11px 17px;margin-top:4px}
.duration .dl{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:#8fa3b8;font-weight:660}
.duration .dv{font-family:var(--mono);font-size:16px;letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.cover-meta{display:grid;grid-template-columns:repeat(4,1fr);gap:14px 22px;
  border-top:1px solid var(--rule);padding-top:16px}
.cover-meta dt{font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--mute);font-weight:660}
.cover-meta dd{margin:2px 0 0;font-family:var(--mono);font-size:12.5px;color:var(--ink)}
@media (max-width:680px){.cover{padding:26px 22px;min-height:0}.cover h1{font-size:29px}
  .cover-meta{grid-template-columns:repeat(2,1fr)}.crest .divider{display:none}}
@media print{
  .cover{min-height:273mm;padding:30px 32px;break-after:page;box-shadow:none}
  .cover-foot{gap:24px}
  .cover h1{font-size:32px} .cover .lede{font-size:12.5px}
  .duration .dv{font-size:13px}
  .cover-meta dd{font-size:10.5px}
  .logo-img{max-height:40px}
}
</style>'''

HTML=f'''<title>EFU Utilisation Statement</title>
{STYLE}{EXTRA}

<div class="wrap">

<section class="cover">
  <div class="crest">
    <div class="slot"><span class="role">Prepared by</span>{ROZEE}</div>
    <div class="divider"></div>
    <div class="slot"><span class="role">Prepared for</span>{EFU}</div>
  </div>

  <div class="cover-foot">
    <div class="cover-body">
      <div class="eyebrow">Account Utilisation Report</div>
      <h1>KPI Generator credit utilisation &amp; user summary</h1>
      <p class="lede">Consumption of EFU Life's contracted credit balance, month by
        month, with the number of users who generated KPIs over the period.</p>
      <div class="duration">
        <span class="dl">Report period</span>
        <span class="dv">{D['first']} — {D['last']}</span>
      </div>
    </div>

    <dl class="cover-meta">
      <div><dt>Account</dt><dd>EFU Life</dd></div>
      <div><dt>Company ID</dt><dd>630</dd></div>
      <div><dt>Credits purchased</dt><dd>500</dd></div>
      <div><dt>Credits utilised</dt><dd>{D['used']} ({D['util']}%)</dd></div>
      <div><dt>Unique users</dt><dd>{D['users']}</dd></div>
      <div><dt>KPIs generated</dt><dd>{D['kpis']:,}</dd></div>
      <div><dt>Data source</dt><dd>efukpidataaug2026.xlsx</dd></div>
      <div><dt>Prepared</dt><dd>17 Aug 2026</dd></div>
    </dl>
  </div>
</section>

<div class="verdict">
  <svg width="19" height="19" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6 19 17.4H1z" fill="none" stroke="var(--red)" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 7.2v4.6" stroke="var(--red)" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="14.5" r="1.05" fill="var(--red)"/></svg>
  <div>
    <div class="vt">The 500-credit balance is fully consumed and over-drawn by {D['over']}.</div>
    <p>The 500th credit was used on <strong>{D['exh_date']}</strong>. A further {D['over']} requests were served after that date — {D['util']}% of the purchased balance. A top-up or renewal is required to keep the service open.</p>
  </div>
</div>

<div class="tiles">
  <div class="tile"><span class="lab">Credits purchased</span><span class="fig num">500</span><span class="sub">Contracted balance</span></div>
  <div class="tile crit"><span class="lab">Credits utilised</span><span class="fig num">{D['used']}</span><span class="sub">{D['util']}% of balance</span></div>
  <div class="tile"><span class="lab">Unique users</span><span class="fig num">{D['users']}</span><span class="sub">All @efulife.com</span></div>
  <div class="tile"><span class="lab">KPIs generated</span><span class="fig num">{D['kpis']:,}</span><span class="sub">{D['avg_kpi']} per request</span></div>
</div>

<section>
  <div class="shead"><h2>1 · Credit consumption against balance</h2>
  <p>Consumption tracked steadily below the purchased balance for eight months, then the June 2026 KPI-setting cycle consumed {D['jun']} credits in a single month.</p></div>
  <figure>
    <figcaption><span class="ft">Cumulative credits consumed vs. 500-credit balance</span>
      <span class="legend"><span class="lg"><span class="sw ln b"></span>Within balance</span><span class="lg"><span class="sw ln r"></span>Beyond balance</span></span>
    </figcaption>
    {C['a']}
  </figure>
  <figure>
    <figcaption><span class="ft">Credits utilised per month</span>
      <span class="legend"><span class="lg"><span class="sw b"></span>Within balance</span><span class="lg"><span class="sw r"></span>Beyond balance</span></span>
    </figcaption>
    {C['b']}
  </figure>
</section>

<section>
  <div class="shead"><h2>2 · Month-wise utilisation</h2></div>
  <div class="tw"><table>
    <thead><tr><th>Month</th><th>Credits used</th><th>Cumulative</th><th>% of 500</th><th>KPIs generated</th><th>Active users</th><th>First-time users</th></tr></thead>
    <tbody>{mrows}</tbody>
    <tfoot><tr><td>Total</td><td class="n">{D['used']}</td><td class="n">{D['used']}</td><td class="n">{D['util']}%</td><td class="n">{D['kpis']:,}</td><td class="n">{D['users']}</td><td class="n">{D['users']}</td></tr></tfoot>
  </table><p class="cap">Shaded rows are months in which cumulative consumption exceeded the 500-credit balance. The active-users total is de-duplicated across the period, so it does not equal the column sum.</p></div>
</section>

<section>
  <div class="shead"><h2>3 · User base</h2>
  <p>{D['users']} distinct EFU users generated KPIs across {D['active_days']} active days. Adoption is broad but consumption is concentrated: the ten heaviest users account for {D['top10share']}% of all credits.</p></div>
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
      <div class="stat-line"><span>Median credits per user</span><b>{D['median']}</b></div>
      <div class="stat-line"><span>Users with 10+ credits</span><b>{D['ten_plus']}</b></div>
      <div class="stat-line"><span>Single-use users</span><b>{D['buckets']['1']}</b></div>
      <div class="stat-line"><span>Top 10 users' share</span><b>{D['top10share']}%</b></div>
      <div class="stat-line"><span>Top 20 users' share</span><b>{D['top20share']}%</b></div>
      <div class="stat-line"><span>Joined in June 2026</span><b>{D['jun_new_users']}</b></div>
    </div>
  </div>
  <div class="tw"><table>
    <thead><tr><th>#</th><th class="l">User</th><th>Credits</th><th>KPIs generated</th><th>Active span</th></tr></thead>
    <tbody>{urows}</tbody>
  </table><p class="cap">Top 10 users by credits consumed. Usernames shown without the @efulife.com domain.</p></div>
</section>

<div class="note">
  <span class="eyebrow">Basis of preparation</span>
  <ul>
    <li><strong>Credit = one KPI-generation request.</strong> {D['used']} requests were submitted; {D['success']} returned KPIs and {D['failed']} returned none. Utilisation is stated on all {D['used']} requests; on successful requests only it is {D['success']} ({D['util_success']}%).</li>
    <li><strong>Credits purchased (500)</strong> is a contract figure supplied separately — the raw data sheet holds no balance or commercial fields.</li>
    <li><strong>Users</strong> are distinct email addresses in the <code>KPIs</code> sheet. All {D['used']} requests sit under <code>company_id 630</code> on the efulife.com domain.</li>
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
