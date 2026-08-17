import pandas as pd, re, json, math

SRC='/root/.claude/uploads/4d0cb0f5-28fc-5af6-972c-95c1e5a3cb68/314662be-efukpidataaug2026.xlsx'
PURCHASED=500

def clean(s):
    if not isinstance(s,str): return ''
    try: s2=s.encode('cp1252','ignore').decode('utf-8','ignore')
    except Exception: s2=s
    return re.sub(r'\s+',' ',(s2 or s)).strip()

k=pd.read_excel(SRC,sheet_name='KPIs'); d=pd.read_excel(SRC,sheet_name='Data')
k['Request_Date']=pd.to_datetime(k.Request_Date)
k['M']=k.Request_Date.dt.to_period('M')
k['t']=k.title.map(clean)
k['tn']=k.t.str.lower().str.replace(r'[^a-z0-9 ]','',regex=True).str.strip().replace('',pd.NA)
k=k.sort_values('Request_Date').reset_index(drop=True)
k['cum']=range(1,len(k)+1)

kpis_m=d.merge(k[['Request_ID','M']],on='Request_ID').groupby('M').size()
LBL={'2025-09':'Sep 25','2025-10':'Oct 25','2025-11':'Nov 25','2025-12':'Dec 25',
     '2026-01':'Jan 26','2026-02':'Feb 26','2026-03':'Mar 26','2026-04':'Apr 26',
     '2026-05':'May 26','2026-06':'Jun 26','2026-07':'Jul 26'}
rows=[];seen=set();seent=set()
for m,g in k.groupby('M'):
    e=set(g.email.str.lower()); nu=len(e-seen); seen|=e
    tt=set(g.tn.dropna()); nt=len(tt-seent); seent|=tt
    rows.append(dict(m=str(m), lbl=LBL[str(m)], req=len(g), users=g.email.nunique(),
                     new_users=nu, cum_users=len(seen), kpis=int(kpis_m.get(m,0)),
                     uniq_t=int(g.tn.nunique()), new_t=nt))
M=pd.DataFrame(rows); M['cum']=M.req.cumsum(); M['util']=(M.cum/PURCHASED*100).round(1)

users=k.groupby(k.email.str.lower()).agg(req=('Request_ID','size'),titles=('tn','nunique'),
        first=('Request_Date','min'),last=('Request_Date','max')).sort_values('req',ascending=False)
users['kpis']=[d[d.Request_ID.isin(k[k.email.str.lower()==e].Request_ID)].shape[0] for e in users.index]
buckets=pd.cut(users.req,[0,1,4,9,19,10**6],labels=['1','2–4','5–9','10–19','20+']).value_counts().reindex(['1','2–4','5–9','10–19','20+'])

kt=k.dropna(subset=['tn'])
vc=kt.groupby('tn').agg(n=('tn','size'),label=('t','first'),users=('email','nunique')).sort_values(['n','label'],ascending=[False,True])
ex=k[k.cum==PURCHASED].iloc[0]

D=dict(purchased=PURCHASED, used=len(k), success=int(d.Request_ID.nunique()),
       failed=len(k)-int(d.Request_ID.nunique()), kpis=len(d), users=int(k.email.str.lower().nunique()),
       util=round(len(k)/PURCHASED*100,1), over=len(k)-PURCHASED,
       exh_date=ex.Request_Date.strftime('%d %b %Y'), active_days=int(k.Request_Date.dt.date.nunique()),
       first=k.Request_Date.min().strftime('%d %b %Y'), last=k.Request_Date.max().strftime('%d %b %Y'),
       months=M.to_dict('records'),
       top_users=[dict(u=e.split('@')[0], req=int(r.req), kpis=int(r.kpis), titles=int(r.titles),
                       span=f"{r['first']:%b %y} – {r['last']:%b %y}") for e,r in users.head(10).iterrows()],
       buckets={str(i):int(v) for i,v in buckets.items()},
       top_titles=[dict(label=r.label,n=int(r.n),users=int(r.users)) for _,r in vc.head(8).iterrows()],
       uniq_t=int(len(vc)), single=int((vc.n==1).sum()), rep=int((vc.n>1).sum()), titled=int(len(kt)),
       top10share=round(users.head(10).req.sum()/len(k)*100,1),
       top20share=round(users.head(20).req.sum()/len(k)*100,1),
       jun=int(M.loc[M.m=='2026-06','req'].iloc[0]), avg_kpi=round(len(d)/int(d.Request_ID.nunique()),1))
json.dump(D,open('data.json','w'),indent=1)
print(json.dumps({x:D[x] for x in ['purchased','used','util','over','exh_date','users','kpis','uniq_t','single','titled','top10share','jun','avg_kpi','failed','active_days']},indent=1))
