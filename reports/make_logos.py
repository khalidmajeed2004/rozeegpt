"""Build the two cover logos as self-contained SVG.

Wordmarks are converted from live font outlines to vector paths, so the files
carry no font dependency and render identically in the browser and in print.
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity

FDIR='/tmp/claude-0/-home-user-rozeegpt/4d0cb0f5-28fc-5af6-972c-95c1e5a3cb68/scratchpad/node_modules/@fontsource/poppins/files/'

def text_path(text, weight='800', italic=False, size=100, x=0, y=0, tracking=0.0):
    """Return (svg path data, advance width) for `text` laid out at `size` px."""
    f=TTFont(FDIR+f'poppins-latin-{weight}-{"italic" if italic else "normal"}.woff2')
    upem=f['head'].unitsPerEm; gs=f.getGlyphSet(); cmap=f.getBestCmap(); hmtx=f['hmtx']
    kern={}
    if 'kern' in f:
        for st in f['kern'].kernTables: kern.update(st.kernTable)
    s=size/upem
    pen_out=[]; cur=0.0; prev=None
    for ch in text:
        gn=cmap.get(ord(ch))
        if gn is None: continue
        if prev is not None:
            cur+=kern.get((prev,gn),0)
        spen=SVGPathPen(gs)
        # flip Y (font up is +, SVG down is +) and place at the running pen position
        t=Identity.translate(x+cur*s, y).scale(s,-s)
        gs[gn].draw(TransformPen(spen,t))
        d=spen.getCommands()
        if d: pen_out.append(d)
        cur+=hmtx[gn][0]+tracking*upem
        prev=gn
    return ' '.join(pen_out), cur*s

# ---------------------------------------------------------------- rozeegpt.ai
# Circuit-brain mark in a rounded square, then the lowercase wordmark with the
# ".ai" suffix, matching the supplied artwork.
def rozeegpt():
    wm,w = text_path('rozeegpt.ai', weight='800', size=100, x=0, y=0, tracking=-0.012)
    ICON=98; GAP=28
    total=ICON+GAP+w
    H=118
    icon_y=(H-92)/2
    K='#000'
    node=lambda cx,cy,r=4.6: f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{K}"/>'
    L=lambda x1,y1,x2,y2: f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{K}" stroke-width="4.4" stroke-linecap="round" fill="none"/>'
    g=[f'<g transform="translate(0,{icon_y:.1f})">']
    # brain contour, left side
    g.append(f'<path d="M30 14c-9 0-15 5-16 12-7 1-11 6-11 13 0 5 2 9 6 11-2 2-3 5-3 8 0 7 5 13 12 14 1 7 7 12 15 12 4 0 8-2 10-4"'
             f' stroke="{K}" stroke-width="4.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="M14 26c4 2 7 5 8 9M9 50c5 0 9 2 12 5M18 72c3-3 7-5 11-5" stroke="{K}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    # rounded square holding AI
    g.append(f'<rect x="30" y="22" width="44" height="44" rx="11" stroke="{K}" stroke-width="5" fill="none"/>')
    ai,aiw = text_path('AI', weight='800', size=26, x=0, y=0)
    g.append(f'<g transform="translate({30+(44-aiw)/2:.1f},{22+30:.1f})"><path d="{ai}" fill="{K}"/></g>')
    # circuit traces + nodes, right side
    for yy,xx in ((30,74),(44,74),(58,74)):
        g.append(L(xx,yy,xx+12,yy)); g.append(node(xx+16,yy))
    g.append(L(52,22,52,10)); g.append(node(52,6))
    g.append(L(52,66,52,78)); g.append(node(52,82))
    g.append(L(74,30,86,18)); g.append(L(74,58,86,70))
    g.append(node(86,14)); g.append(node(86,74))
    g.append('</g>')
    body=''.join(g)+f'<g transform="translate({ICON+GAP:.1f},{H/2+35:.1f})"><path d="{wm}" fill="{K}"/></g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total:.0f} {H}" '
            f'role="img" aria-label="rozeegpt.ai">{body}</svg>')

# ------------------------------------------------------------------- EFU Life
# White rounded-square app icon: teal disc with a thin inner ring holding the
# "efu" monogram, "LIFE" set in teal beneath it.
def efulife():
    TEAL='#12798D'; S=512; R=114
    efu,ew = text_path('efu', weight='600', italic=True, size=176, x=0, y=0, tracking=-0.02)
    life,lw = text_path('LIFE', weight='700', size=86, x=0, y=0, tracking=0.055)
    cx=S/2; disc_cy=232; disc_r=163
    body=[
      f'<rect width="{S}" height="{S}" rx="{R}" fill="#fff"/>',
      f'<circle cx="{cx}" cy="{disc_cy}" r="{disc_r}" fill="{TEAL}"/>',
      f'<circle cx="{cx}" cy="{disc_cy}" r="{disc_r-17}" fill="none" stroke="#fff" stroke-width="5" opacity=".9"/>',
      f'<g transform="translate({cx-ew/2:.1f},{disc_cy+58:.1f})"><path d="{efu}" fill="#fff"/></g>',
      f'<g transform="translate({cx-lw/2:.1f},{disc_cy+disc_r+96:.1f})"><path d="{life}" fill="{TEAL}"/></g>',
    ]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'role="img" aria-label="EFU Life">{"".join(body)}</svg>')

open('logos/rozeegpt.svg','w').write(rozeegpt())
open('logos/efulife.svg','w').write(efulife())
print('wrote logos/rozeegpt.svg, logos/efulife.svg')
