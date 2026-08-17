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
DARK_MODE={'rozeegpt':'invert', 'efulife':'none'}

def logo(stem, fallback):
    for ext in ('.svg','.png','.jpg','.jpeg','.webp'):
        f=pathlib.Path('logos')/(stem+ext)
        if f.exists():
            b64=base64.b64encode(f.read_bytes()).decode()
            cls=f'logo-img lg-{stem} dk-'+DARK_MODE.get(stem,'plate')
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
/* --- cover page ---------------------------------------------------------
   The cover commits to one dark treatment in both themes, so every colour
   here is literal rather than tokenised. Everything past it stays quiet. */
.cover{--cv-ink:#f2f6f9; --cv-mute:#8fa3b8; --cv-line:rgba(255,255,255,.12);
  position:relative;overflow:hidden;isolation:isolate;
  display:flex;flex-direction:column;gap:26px;
  background:#0d1319;border-radius:16px;padding:38px 40px 0;
  color:var(--cv-ink);min-height:560px;
  box-shadow:0 2px 4px rgba(0,0,0,.18),0 22px 50px -26px rgba(0,0,0,.55)}
/* faint plot rules bleeding behind the whole panel */
.cover::before{content:"";position:absolute;inset:0;z-index:-1;
  background:radial-gradient(120% 80% at 82% 4%,rgba(57,135,229,.16),transparent 62%),
             radial-gradient(90% 60% at 6% 96%,rgba(224,102,97,.10),transparent 66%)}

.crest{display:flex;align-items:stretch;gap:26px;flex-wrap:wrap}
.crest .slot{display:flex;flex-direction:column;gap:9px;min-width:150px}
.crest .mark{display:flex;align-items:center;height:56px}
.crest .role{font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--cv-mute);font-weight:660}
.crest .divider{width:1px;align-self:stretch;background:var(--cv-line)}
.logo-img{width:auto;height:auto;object-fit:contain;display:block}
.lg-rozeegpt{max-height:42px;max-width:206px;filter:invert(1)}
.lg-efulife{max-height:56px;max-width:56px;border-radius:12px}
.wordmark{font-size:25px;font-weight:700;letter-spacing:-.03em;line-height:1;color:var(--cv-ink)}
.wm-a{color:#5b9bec} .wm-b{color:var(--cv-mute);font-weight:500;margin-left:.16em}

.cover-body{display:flex;flex-direction:column;gap:15px;margin-top:auto}
.cv-lede{font-size:14px;line-height:1.55;color:var(--cv-mute);max-width:44ch;margin:-2px 0 2px}
.cover .eyebrow{color:var(--cv-mute);letter-spacing:.16em}
.cover h1{font-size:44px;line-height:1.06;letter-spacing:-.032em;font-weight:690;
  color:var(--cv-ink);text-wrap:initial}
.cover h1 em{font-style:normal;color:var(--cv-mute);font-weight:400}
.period{display:inline-flex;align-items:center;gap:14px;align-self:flex-start;
  border:1px solid var(--cv-line);border-radius:999px;padding:8px 18px 8px 14px}
.period .pl{font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--cv-mute);font-weight:660}
.period .pv{font-family:var(--mono);font-size:13px;letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.period .pd{color:var(--cv-mute);margin:0 7px}

/* the burn curve, bleeding to both edges */
.curve{display:flex;flex-direction:column-reverse;gap:12px;margin:4px -40px 0}
.curve>svg{display:block;width:100%;height:172px}
.curve-tag{display:flex;align-items:center;gap:9px;margin-left:40px;font-size:9px;
  letter-spacing:.14em;text-transform:uppercase;font-weight:680;color:#e88b87}
.curve-tag::before{content:"";width:22px;height:2px;border-radius:1px;background:#e06661}

.cover-figures{display:grid;grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--cv-line);margin:0 -40px;padding:0 40px}
.cf{display:flex;flex-direction:column;gap:4px;padding:16px 0 22px;position:relative}
.cf+.cf{padding-left:22px}
.cf+.cf::before{content:"";position:absolute;left:0;top:16px;bottom:22px;width:1px;background:var(--cv-line)}
.cfl{font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--cv-mute);font-weight:660}
.cfv{font-family:var(--mono);font-size:26px;line-height:1.05;letter-spacing:-.035em;font-weight:600;
  display:flex;align-items:baseline;gap:9px}
.cf.over .cfv{color:#f08984}
.cfv em{font-style:normal;font-size:12px;letter-spacing:-.01em;color:var(--cv-mute);font-weight:500}

@media (max-width:680px){
  .cover{padding:26px 22px 0;min-height:0;gap:20px}
  .cover h1{font-size:30px}
  .cv-lede{font-size:13px}
  .curve{margin:4px -22px 0} .curve>svg{height:120px} .curve-tag{margin-left:22px}
  .cover-figures{grid-template-columns:repeat(2,1fr);margin:0 -22px;padding:0 22px}
  .cf+.cf{padding-left:0} .cf+.cf::before{display:none}
  .cf:nth-child(even){padding-left:22px}
  .cf:nth-child(even)::before{content:"";position:absolute;left:0;top:16px;bottom:22px;width:1px;background:var(--cv-line);display:block}
  .crest .divider{display:none}
}
@media print{
  .cover{min-height:271mm;padding:30px 34px 0;break-after:page;border-radius:14px;
    box-shadow:none;gap:20px}
  .cover h1{font-size:37px}
  .cv-lede{font-size:12px;max-width:46ch}
  .crest .mark{height:52px}
  .lg-rozeegpt{max-height:39px;max-width:192px}
  .lg-efulife{max-height:52px;max-width:52px}
  .curve{margin:4px -34px 0} .curve>svg{height:232px} .curve-tag{margin-left:34px}
  .cover-figures{margin:0 -34px;padding:0 34px}
  .cfv{font-size:24px}
}
</style>'''

HTML=f'''<title>EFU Utilisation Statement</title>
{STYLE}{EXTRA}

<div class="wrap">

<section class="cover">
  <div class="crest">
    <div class="slot"><span class="role">Prepared by</span><span class="mark">{ROZEE}</span></div>
    <div class="divider"></div>
    <div class="slot"><span class="role">Prepared for</span><span class="mark">{EFU}</span></div>
  </div>

  <div class="cover-body">
    <div class="eyebrow">Account Utilisation Report</div>
    <h1>KPI Generator<br>credit utilisation<br><em>&amp; user summary</em></h1>
    <p class="cv-lede">Consumption of EFU Life's contracted credit balance, month by month,
      alongside the number of users generating KPIs across the period.</p>
    <div class="period">
      <span class="pl">Report period</span>
      <span class="pv">{D['first']}<span class="pd">—</span>{D['last']}</span>
    </div>
  </div>

  <div class="curve">
    {C['cover']}
    <span class="curve-tag">Balance exhausted {D['exh_date']}</span>
  </div>

  <div class="cover-figures">
    <div class="cf"><span class="cfl">Credits purchased</span><span class="cfv">500</span></div>
    <div class="cf over"><span class="cfl">Credits utilised</span><span class="cfv">{D['used']}<em>{D['util']}%</em></span></div>
    <div class="cf"><span class="cfl">Unique users</span><span class="cfv">{D['users']}</span></div>
    <div class="cf"><span class="cfl">KPIs generated</span><span class="cfv">{D['kpis']:,}</span></div>
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
    <li><strong>Credits purchased (500)</strong> is a contract figure supplied separately; it does not form part of the platform's usage records.</li>
    <li><strong>Users</strong> are distinct email addresses recorded against the account. All {D['used']} requests sit under the EFU Life account on the efulife.com domain.</li>
    <li>Figures are drawn from KPI Generator usage records for the EFU Life account and cover {D['first']} to {D['last']}. KPI-level detail is unavailable for Sep–Oct 2025, so those two months show 8 requests with no KPI breakdown.</li>
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
