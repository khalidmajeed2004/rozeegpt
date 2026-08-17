import json
D=json.load(open('data.json'))
M=D['months']; P=D['purchased']

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def ylab(v):
    return f'{v:,}'

def grid(x0,x1,y0,y1,ymax,steps):
    o=[]
    for i in range(steps+1):
        v=ymax*i/steps; y=y1-(y1-y0)*i/steps
        o.append(f'<line class="grid" x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}"/>')
        o.append(f'<text class="ax ax-y" x="{x0-8}" y="{y+3.5:.1f}">{ylab(int(v))}</text>')
    return ''.join(o)

# ---------- Chart A: cumulative burn vs entitlement ----------
def chart_a():
    W,H=720,214; x0,x1,y0,y1=52,700,18,186; ymax=900
    n=len(M); dx=(x1-x0)/(n-1)
    X=lambda i:x0+dx*i; Y=lambda v:y1-(y1-y0)*v/ymax
    pts=[(X(i),Y(m['cum'])) for i,m in enumerate(M)]
    line=' '.join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i,(x,y) in enumerate(pts))
    area=line+f' L{x1:.1f},{y1} L{x0:.1f},{y1} Z'
    yth=Y(P)
    o=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cumulative credits consumed against the 500-credit entitlement">']
    o.append(f'<defs><clipPath id="cA-in"><rect x="{x0}" y="{yth:.1f}" width="{x1-x0}" height="{y1-yth:.1f}"/></clipPath>'
             f'<clipPath id="cA-over"><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{yth-y0:.1f}"/></clipPath></defs>')
    o.append(grid(x0,x1,y0,y1,ymax,6))
    o.append(f'<path class="fill-in" d="{area}" clip-path="url(#cA-in)"/>')
    o.append(f'<path class="fill-over" d="{area}" clip-path="url(#cA-over)"/>')
    o.append(f'<line class="thresh" x1="{x0}" y1="{yth:.1f}" x2="{x1}" y2="{yth:.1f}"/>')
    o.append(f'<text class="thresh-lbl" x="{x0+6}" y="{yth-8:.1f}">PURCHASED BALANCE — 500 CREDITS</text>')
    o.append(f'<path class="ln-in" d="{line}" clip-path="url(#cA-in)"/>')
    o.append(f'<path class="ln-over" d="{line}" clip-path="url(#cA-over)"/>')
    for i,(x,y) in enumerate(pts):
        m=M[i]; over=m['cum']>P
        o.append(f'<circle class="dot {"over" if over else "in"}" cx="{x:.1f}" cy="{y:.1f}" r="4" '
                 f'data-t="{esc(m["lbl"])}" data-v="{m["cum"]:,} of 500 consumed · {m["util"]}%"/>')
        o.append(f'<text class="ax ax-x" x="{x:.1f}" y="{y1+18}">{esc(m["lbl"])}</text>')
    # exhaustion marker
    xi=next(i for i,m in enumerate(M) if m['cum']>P)
    prev=M[xi-1]['cum']; cur=M[xi]['cum']
    xe=X(xi-1)+dx*(P-prev)/(cur-prev)
    o.append(f'<line class="exh" x1="{xe:.1f}" y1="{yth:.1f}" x2="{xe:.1f}" y2="{y1}"/>')
    o.append(f'<circle class="exh-dot" cx="{xe:.1f}" cy="{yth:.1f}" r="4.5"/>')
    o.append(f'<text class="note-lbl" x="{xe-8:.1f}" y="{yth-24:.1f}" text-anchor="end">EXHAUSTED 10 JUN 2026</text>')
    o.append(f'<text class="pk" x="{X(n-1):.1f}" y="{Y(852)-14:.1f}" text-anchor="end">852</text>')
    o.append(f'<line class="axis" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    o.append('</svg>')
    return ''.join(o)

# ---------- Chart B: monthly tickets, split in/over ----------
def chart_b():
    W,H=720,194; x0,x1,y0,y1=52,700,20,166; ymax=600
    n=len(M); band=(x1-x0)/n; bw=min(38,band*0.56)
    Y=lambda v:y1-(y1-y0)*v/ymax
    o=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Credits utilised each month, split by within and beyond entitlement">']
    o.append(grid(x0,x1,y0,y1,ymax,4))
    run=0
    for i,m in enumerate(M):
        cx=x0+band*(i+0.5); r=m['req']
        inn=max(0,min(r,P-run)); ov=r-inn; run+=r
        yb=y1
        if inn>0:
            h=(y1-y0)*inn/ymax
            o.append(f'<rect class="bar in" x="{cx-bw/2:.1f}" y="{yb-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" '
                     f'data-t="{esc(m["lbl"])}" data-v="{inn} credits within entitlement"/>')
            yb-=h+ (2 if ov>0 else 0)
        if ov>0:
            h=(y1-y0)*ov/ymax
            o.append(f'<rect class="bar over" x="{cx-bw/2:.1f}" y="{yb-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" '
                     f'data-t="{esc(m["lbl"])}" data-v="{ov} credits beyond entitlement"/>')
            yb-=h
        o.append(f'<text class="val" x="{cx:.1f}" y="{yb-7:.1f}">{r}</text>')
        o.append(f'<text class="ax ax-x" x="{cx:.1f}" y="{y1+18}">{esc(m["lbl"])}</text>')
    o.append(f'<line class="axis" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    o.append('</svg>')
    return ''.join(o)

# ---------- Chart C: user adoption ----------
def chart_c():
    W,H=720,194; x0,x1,y0,y1=52,700,20,166; ymax=100
    n=len(M); band=(x1-x0)/n; bw=min(30,band*0.46)
    Y=lambda v:y1-(y1-y0)*v/ymax
    o=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Active users each month and cumulative unique users">']
    o.append(grid(x0,x1,y0,y1,ymax,4))
    for i,m in enumerate(M):
        cx=x0+band*(i+0.5); h=(y1-y0)*m['users']/ymax
        o.append(f'<rect class="bar in" x="{cx-bw/2:.1f}" y="{y1-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" '
                 f'data-t="{esc(m["lbl"])}" data-v="{m["users"]} users active · {m["new_users"]} first-time"/>')
        o.append(f'<text class="ax ax-x" x="{cx:.1f}" y="{y1+18}">{esc(m["lbl"])}</text>')
    pts=[(x0+band*(i+0.5),Y(m['cum_users'])) for i,m in enumerate(M)]
    o.append('<path class="ln-2" d="'+' '.join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i,(x,y) in enumerate(pts))+'"/>')
    for i,(x,y) in enumerate(pts):
        o.append(f'<circle class="dot2" cx="{x:.1f}" cy="{y:.1f}" r="3.6" data-t="{esc(M[i]["lbl"])}" '
                 f'data-v="{M[i]["cum_users"]} unique users to date"/>')
    o.append(f'<text class="pk2" x="{pts[-1][0]:.1f}" y="{pts[-1][1]-12:.1f}" text-anchor="end">93</text>')
    o.append(f'<line class="axis" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    o.append('</svg>')
    return ''.join(o)

# ---------- Chart D: user depth buckets ----------
def chart_d():
    B=D['buckets']; keys=list(B); W,H=340,168; x0,x1,y0=118,326,10; rowh=32; bw=18
    mx=max(B.values())
    o=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Users grouped by how many credits they used">']
    for i,kx in enumerate(keys):
        y=y0+rowh*i; w=(x1-x0)*B[kx]/mx; lab=kx+(' credit' if kx=='1' else ' credits')
        o.append(f'<text class="ax ax-r" x="{x0-10}" y="{y+bw/2+4}">{esc(lab)}</text>')
        o.append(f'<rect class="bar in" x="{x0}" y="{y}" width="{max(w,2):.1f}" height="{bw}" rx="3" '
                 f'data-t="{esc(lab)}" data-v="{B[kx]} users"/>')
        o.append(f'<text class="val val-r" x="{x0+w+8:.1f}" y="{y+bw/2+4}">{B[kx]}</text>')
    o.append('</svg>')
    return ''.join(o)

CH=dict(a=chart_a(),b=chart_b(),c=chart_c(),d=chart_d())
json.dump(CH,open('charts.json','w'))
print('ok', {x:len(v) for x,v in CH.items()})
