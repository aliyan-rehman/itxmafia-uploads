"""EP12 — What if every ocean was as salty as the Dead Sea? (sitcom-toon look, Kokoro voices)"""
import math, json, sys, os, subprocess, cairo, numpy as np
from multiprocessing import Pool
from toonline import Toon, hexc, mixc, ellipse_pts, rect, star, LINE, W, H
from toonchars import draw_nova, draw_kiko, walk_legs, land_sq, tq, swim_ring
from world import swirl

TL = json.load(open('/home/claude/pw/ep12/timeline.json'))
TOTAL = TL['total']; LN = {l['id']: l for l in TL['lines']}
FPS = 24

def S(i): return LN[i]['s']
def E(i): return LN[i]['e']
def at(i, f): return S(i) + (E(i) - S(i))*f
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(u): u = clamp(u); return u*u*(3 - 2*u)
def back(u, k=1.3):
    u = clamp(u); return 1 + (k + 1)*(u - 1)**3 + k*(u - 1)**2

def lip(who, t):
    for l in TL['lines']:
        if l['who'] == who and l['s'] <= t <= l['e']:
            i = int((tq(t) - l['s'])*24)
            return l['lip'][min(max(i, 0), len(l['lip']) - 1)]
    return 0.0

def blinkf(t, period, off=0.0): return ((t + off) % period) > period - 0.12

# ---------------------------------------------------------------- shot list (start times)
CUT = {
    'beach0': 0.0,
    'arrive': S('n2'),
    'glass': at('n2', 0.60),
    'kcu1': S('k1') - 0.12,
    'float': S('n3') - 0.1,
    'kcu2': S('k2') - 0.12,
    'ncu': S('n4') - 0.12,
    'under': at('n4', 0.19),
    'kcu3': S('k3') - 0.12,
    'red': E('k3') + 0.36,
    'card': at('n5', 0.47),
    'end': S('n6') - 0.15,
}
ORDER = sorted(CUT, key=CUT.get)
def shot_at(t):
    cur = ORDER[0]
    for k in ORDER:
        if t >= CUT[k]: cur = k
    return cur

# ---------------------------------------------------------------- palettes
OUR = dict(sky=[mixc('#2f7fe0', '#bfe4ff', k/5) for k in range(6)], sea='#2f8fd8', sea2='#58aee6', sand='#f6d48a', sand_s='#e2b866')
PAR = dict(sky=[mixc('#3b1f8c', '#ff9fd1', k/5) for k in range(6)], sea='#a6e8de', sea2='#d4f6ef', sand='#f2d6a8', sand_s='#ddb98a')
RED = dict(sky=['#3a1640', '#5e1d4f', '#8c2a50', '#c2404f', '#ea6a4a', '#ffa45c'], sea='#c8324a', sea2='#e2607a', sand='#f2d6a8', sand_s='#ddb98a')
def lerp_pal(A, B, k):
    return dict(sky=[mixc(a, b, k) for a, b in zip(A['sky'], B['sky'])], sea=mixc(A['sea'], B['sea'], k), sea2=mixc(A['sea2'], B['sea2'], k), sand=A['sand'], sand_s=A['sand_s'])

HZ, SHORE = 860, 1270     # horizon and shoreline (world y)

def sky(T, pal, t, moons=True, sun=False):
    edges = [-1500, 150, 300, 450, 600, 750, HZ + 5]
    for i, col in enumerate(pal['sky']):
        T.flat(rect(-1500, edges[i], 4080, edges[i + 1] - edges[i] + 2), col)
    if sun:
        T.glow(820, 300, 90, '#fff6b0'); T.shape(ellipse_pts(820, 300, 90, 90), '#ffe066', shadow='#ffc93c', shade_dir=(1, 0.5), shade_w=0.2, lw=7)
        for (cx, cy, s) in ((230, 260, 1.0), (640, 470, 0.7)):
            T.shape([(cx - 110*s, cy + 30*s), (cx - 80*s, cy - 20*s), (cx - 20*s, cy - 50*s), (cx + 50*s, cy - 30*s), (cx + 110*s, cy + 30*s)], '#ffffff', lw=7)
    if moons:
        for (x, y, r, col, sh) in ((820, 260, 95, '#fff2c8', '#e7c98f'), (640, 170, 42, '#c9f3ff', '#9fd6ea')):
            T.glow(x, y, r, col); T.shape(ellipse_pts(x, y, r, r), col, shadow=sh, shade_dir=(1, 0.5), shade_w=0.25, lw=7)
        bob = 8*math.sin(t*1.3)
        T.shape([(120, 520 + bob), (330, 505 + bob), (300, 560 + bob), (240, 640 + bob), (200, 600 + bob), (150, 565 + bob)], '#7a4a8a', shadow='#5c3570', lw=7)
        T.shape([(110, 525 + bob), (340, 505 + bob), (332, 530 + bob), (118, 545 + bob)], '#47c2a0', lw=7)

def sea(T, pal, t, salt=True, top=HZ, bottom=SHORE):
    T.shape([(-1500, top), (2580, top), (2580, bottom + 400), (-1500, bottom + 400)], pal['sea'], lw=7)
    for k in range(4):   # flat lighter wave strokes
        y = top + 50 + k*95; ph = tq(t)*1.5 + k
        for j in range(5):
            x0 = -100 + j*280 + (k % 2)*140 + 25*math.sin(ph + j)
            T.stroke([(x0, y), (x0 + 60, y - 10), (x0 + 120, y)], lw=7, col=pal['sea2'])
    T.shape([(-1500, top - 4), (2580, top - 4), (2580, top + 10), (-1500, top + 10)], pal['sea2'], line=False)

def shore(T, pal, t, salt=True, y0=SHORE):
    T.shape([(-1500, y0)] + [(x, y0 + 14*math.sin(x/120)) for x in range(-1500, 2600, 60)] + [(2580, 3600), (-1500, 3600)], pal['sand'], lw=7)
    if salt:   # white salt crust along the waterline + salt pillars (Dead Sea look)
        T.shape([(-1500, y0 - 4)] + [(x, y0 + 14*math.sin(x/120) + 26 + 8*math.sin(x/37)) for x in range(-1500, 2600, 50)] + [(2580, y0 + 70), (2580, y0 - 4)], '#fbf8f0', lw=6)
        for (x, y, s) in ((80, y0 + 190, 1.0), (980, y0 + 150, 0.8), (-60, y0 + 420, 1.3), (1120, y0 + 380, 1.2)):
            T.shape([(x - 50*s, y), (x - 40*s, y - 90*s), (x - 60*s, y - 120*s), (x - 20*s, y - 170*s), (x + 30*s, y - 150*s), (x + 55*s, y - 110*s), (x + 40*s, y - 70*s), (x + 50*s, y)], '#fbf8f0', shadow='#d9d4e6', shade_dir=(1, 0.2), shade_w=0.3, lw=7)
    # pebbles/shells for depth
    for (x, y) in ((300, y0 + 330), (720, y0 + 260), (520, y0 + 520)):
        T.shape(ellipse_pts(x, y, 22, 12, 16), pal['sand_s'], lw=5)

def water_front(T, pal, t, y, x0=-1500, x1=2580):
    """water surface drawn in front of a floating character"""
    pts = [(x, y + 7*math.sin(x/45 + tq(t)*5)) for x in range(int(x0), int(x1), 30)]
    T.shape(pts + [(x1, 3600), (x0, 3600)], pal['sea'], lw=7)
    for j in range(6):
        xx = 250 + j*120
        T.stroke([(xx, y + 40 + (j % 2)*30), (xx + 50, y + 34 + (j % 2)*30)], lw=7, col=pal['sea2'])

def front_shore(T, xs):
    """sand in the foreground: a diagonal beach from the bottom-left up to the shoreline on the right"""
    edge = [(-1500, 1560), (200, 1540), (xs - 60, SHORE + 120), (xs, SHORE + 34), (2580, SHORE - 10)]
    T.shape(edge + [(2580, 3600), (-1500, 3600)], PAR['sand'], lw=7, seed=901)
    T.shape(edge + [(p[0], p[1] + 30) for p in edge[::-1]], '#fbf8f0', lw=6, seed=902)
    for (x, y) in ((260, 1720), (900, 1500), (640, 1800)):
        T.shape(ellipse_pts(x, y, 22, 12, 16), PAR['sand_s'], lw=5)

def portal(T, t, cx, cy, R, open_k=1.0, spin=0.0):
    if open_k <= 0.01: return
    R = R*open_k
    T.glow(cx, cy, R, '#ffd84d', ((1.35, 0.10), (1.18, 0.16)), sy=1.25)
    rim = [(cx + R*(1 + 0.05*math.sin(5*a + t*2))*math.cos(a), cy + 1.25*R*(1 + 0.05*math.sin(5*a + t*2))*math.sin(a)) for a in np.linspace(0, 2*math.pi, 60)]
    T.shape(rim, '#ffd84d', lw=9, seed=11)
    inner = [(cx + 0.86*(x - cx), cy + 0.86*(y - cy)) for x, y in rim]
    T.shape(inner, '#7a2fbf', line=False, seed=12, amp=0)
    c = T.c; c.save(); T._path(T.X(inner)); c.clip()
    for arm, col in enumerate(['#ff4fa3', '#4fd8ff', '#ff4fa3', '#4fd8ff']):
        pts = []
        for i in range(50):
            u = i/49; ang = arm*math.pi/2 + u*3.4 + t*2.2 + spin; r = R*0.86*u
            pts.append((cx + r*math.cos(ang), cy + 1.25*r*math.sin(ang)))
        c.set_source_rgba(*hexc(col)); c.set_line_width(46*R/230*T.z); c.set_line_cap(cairo.LINE_CAP_ROUND)
        T._path(T.X(pts), False); c.stroke()
    c.restore()
    T.shape(ellipse_pts(cx, cy, 62*R/230, 78*R/230), '#fff7e0', line=False, amp=0)
    for i in range(6):
        a = t*1.5 + i*1.05; r = R*1.22
        T.shape(star(cx + r*math.cos(a), cy + 1.25*r*math.sin(a)*0.95, 15, 6, 4, a), '#fff2a8', lw=5)

def duck(T, x, y, s=1.0, t=0.0):
    """generic rubber duck toy"""
    b = 4*math.sin(tq(t)*6)
    T.shape([(x - 60*s, y + b), (x - 70*s, y - 40*s + b), (x - 20*s, y - 60*s + b), (x + 60*s, y - 50*s + b), (x + 70*s, y + b)], '#ffd43b', shadow='#f0b400', shade_dir=(1, 0.3), shade_w=0.25, lw=7)
    T.shape(ellipse_pts(x + 30*s, y - 85*s + b, 38*s, 36*s), '#ffd43b', shadow='#f0b400', shade_dir=(1, 0.3), shade_w=0.25, lw=7)
    T.shape([(x + 62*s, y - 90*s + b), (x + 98*s, y - 82*s + b), (x + 64*s, y - 70*s + b)], '#ff8a1f', lw=6)
    T.dot(*T_noop(x + 42*s, y - 95*s + b), 6*s)

def T_noop(x, y): return (x, y)

# ---------------------------------------------------------------- screen-space overlays
FONT = 'Fredoka'
def cap_lines():
    """split every voice line into caption phrases with times"""
    out = []
    for l in TL['lines']:
        txt = l['text'].replace('nineteen ninety-two', '1992').replace('three and a half percent', '3.5%')
        import re
        parts = [p.strip() for p in re.split(r'(?<=[.?!,])\s+', txt) if p.strip()]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) + len(p) < 24 and not merged[-1].endswith(('.', '?', '!')): merged[-1] += ' ' + p
            else: merged.append(p)
        fin = []
        for p in merged:
            if len(p) > 30:
                w = p.split(); half = len(w)//2
                fin += [' '.join(w[:half]), ' '.join(w[half:])]
            else: fin.append(p)
        tot = sum(len(p) for p in fin); t0 = l['s']
        for p in fin:
            d = (l['e'] - l['s'])*len(p)/tot
            out.append((t0, t0 + d + 0.12, p, l['who'])); t0 += d
    return out
CAPS = cap_lines()

def caption(c, t):
    for (a, b, txt, who) in CAPS:
        if a <= t < b:
            col = '#3a3f8f' if who == 'NOVA' else '#1e7a4c'
            c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(66)
            words = txt.split(); sp = c.text_extents('  ').x_advance*0.75
            wid = sum(c.text_extents(w).x_advance for w in words) + sp*(len(words) - 1)
            if wid > 980:
                c.set_font_size(66*980/wid); sp = c.text_extents('  ').x_advance*0.75
                wid = sum(c.text_extents(w).x_advance for w in words) + sp*(len(words) - 1)
            x = (W - wid)/2; y = 1790
            pop = 1 + 0.08*math.exp(-(t - a)*18)
            c.save(); c.translate(W/2, y - 20); c.scale(pop, pop); c.translate(-W/2, -(y - 20))
            for w in words:
                c.move_to(x, y); c.text_path(w); x += c.text_extents(w).x_advance + sp
            c.set_source_rgb(*LINE); c.set_line_width(20); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
            c.set_source_rgb(1, 1, 1); c.fill()
            # speaker pill above, left aligned
            c.set_font_size(32); e2 = c.text_extents(who); px = (W - wid)/2; py = y - 120; w2 = e2.x_advance + 40; r = 24
            c.new_path(); c.arc(px + r, py + r, r, math.pi/2, 3*math.pi/2); c.arc(px + w2 - r, py + r, r, -math.pi/2, math.pi/2); c.close_path()
            c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(6); c.stroke()
            c.move_to(px + 20, py + 36); c.set_source_rgb(1, 1, 1); c.show_text(who)
            c.restore()
            return

def tag(c, t, text, t0, col='#4fd8ff', y=150):
    n = int(clamp((t - t0)/0.9)*len(text))
    if n <= 0: return
    s = text[:n] + ('_' if (t*4) % 1 < 0.5 and n < len(text) else '')
    c.select_font_face('DejaVu Sans Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(36)
    w = c.text_extents(text).x_advance
    c.set_source_rgba(0.06, 0.04, 0.12, 0.8); c.rectangle((W - w)/2 - 22, y - 44, w + 44, 62); c.fill()
    c.move_to((W - w)/2, y); c.set_source_rgba(*hexc(col)); c.show_text(s)

def brand(c, t):
    c.new_path()
    swirl(c, W/2, 70, 34, 0.95, t)

def kinetic(c, t, word, t0, x, y, size=150, col='#ffd43b', rot=0.0):
    if t < t0: return
    k = back((t - t0)/0.25, 2.0)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    c.select_font_face('Luckiest Guy'); c.set_font_size(size)
    e = c.text_extents(word); c.move_to(-e.x_advance/2, e.height/2); c.text_path(word)
    c.set_source_rgb(*LINE); c.set_line_width(26); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*hexc(col)); c.fill(); c.restore()

def swirl_wipe(c, t, tc, d=0.32):
    """full-screen Swirlverse spiral: closes over the old shot until tc, opens on the new one after"""
    u = (t - (tc - d))/(2*d)
    if u <= 0 or u >= 1: return
    R = math.hypot(W, H)*0.62
    if u < 0.5: r_out, r_in = R*ease(u*2), 0
    else: r_out, r_in = R, R*ease((u - 0.5)*2)
    c.save(); c.translate(W/2, H/2)
    c.new_path(); c.arc(0, 0, r_out, 0, 2*math.pi)
    if r_in > 0: c.new_sub_path(); c.arc_negative(0, 0, r_in, 2*math.pi, 0)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_source_rgba(*hexc('#5a1f9a')); c.paint()
    rot = t*9
    for arm, col in enumerate(['#ff4fa3', '#4fd8ff', '#ffd84d', '#ff4fa3', '#4fd8ff', '#ffd84d']):
        c.new_path()
        for i in range(60):
            v = i/59; a = arm*math.pi/3 + v*4.2 + rot; r = R*1.1*v
            (c.move_to if i == 0 else c.line_to)(r*math.cos(a), r*math.sin(a))
        c.set_source_rgba(*hexc(col)); c.set_line_width(70); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.arc(0, 0, 70, 0, 2*math.pi); c.set_source_rgb(1, 0.97, 0.88); c.fill()
    c.restore()

def flash(c, t, t0, d=0.12, a=0.5):
    if t0 <= t < t0 + d:
        c.set_source_rgba(1, 1, 1, a*(1 - (t - t0)/d)); c.paint()

# ---------------------------------------------------------------- shots
def nova_talk(t, extra=None):
    o = lip('NOVA', t)
    P = dict(t=t, o=o*0.95, nod=o*7, blink=blinkf(t, 3.4), sm=0.45)
    if extra: P.update(extra)
    return P
def kiko_talk(t, extra=None):
    o = lip('KIKO', t)
    P = dict(t=t, o=o*1.1, nod=o*7, blink=blinkf(t, 2.9, 1.1))
    if extra: P.update(extra)
    return P

def sh_beach0(T, t):
    u = t - CUT['beach0']
    po_t = at('n1', 0.80)               # portal opens (clicker press just before)
    rush = clamp((t - (E('n1') - 0.05))/0.55)
    z = 1.0 + 0.2*(1 - ease(u/1.4)) + 0.03*u/4 + 2.2*ease(rush)**2
    PX, PY = 560, 1080
    T.cx, T.cy, T.z = 540 + (PX - 540)*ease(rush), 960 + (PY - 960)*ease(rush), z
    sky(T, OUR, t, moons=False, sun=True); sea(T, OUR, t); shore(T, OUR, t, salt=False)
    ok = back((t - po_t)/0.35, 1.0) if t > po_t else 0
    portal(T, t, PX, PY, 200, ok)
    press = 1.0 if po_t - 0.25 < t < po_t + 0.1 else 0.0
    look_n = (-0.1, 0.1) if t < po_t else (-0.9, -0.1)
    draw_kiko(T, kiko_talk(t, dict(x=250, y=1600, s=0.92, look=(0.6, -0.1) if t < po_t else (0.9, -0.2), sweat=t > po_t, tremble=0, jit=(math.sin(int(t*12)*12.9898)*43758.5 % 1 - 0.5)*5 if t > po_t else 0, ring=True,
                                       armF=((10, 150), -30), armB=((-10, 150), 30), brow=-0.7, sm=-0.3)))
    if t > po_t - 0.6: armF = ((-150, -40), 40)
    else:
        g = math.sin(tq(t)*2.2)
        armF = ((-150 - 20*g, -120 + 30*g), 50)       # open-palm 'what if' gesture
    draw_nova(T, nova_talk(t, dict(x=820, y=1600, s=0.92, face=1, look=look_n, armF=armF, hold='clicker' if t > po_t - 0.6 else None, press=press,
                                    brow=0.8)))

def sh_arrive(T, t):
    u = t - CUT['arrive']
    T.cx, T.cy, T.z = 540, 980 - 20*ease(u/2.0), 1.0 + 0.03*u
    sky(T, PAR, t); sea(T, PAR, t); shore(T, PAR, t)
    pk = 1 - clamp((u - 1.2)/0.4)
    portal(T, t, 560, 1080, 200, pk)
    # both hop out of the portal and land
    for who in ('kiko', 'nova'):
        t0 = 0.05 if who == 'nova' else 0.25; t1 = t0 + 0.45
        a = (560, 1080); b = (820, 1600) if who == 'nova' else (260, 1600)
        v = clamp((u - t0)/(t1 - t0))
        x = a[0] + (b[0] - a[0])*v; y = a[1] + (b[1] - a[1])*v - math.sin(v*math.pi)*260
        s = 0.92*(0.4 + 0.6*v)
        sq = land_sq(u, t1)
        vis = u > t0
        if not vis: continue
        if who == 'nova':
            draw_nova(T, nova_talk(t, dict(x=x, y=y, s=s, sq=sq, look=(0.3, 0.2) if v >= 1 else (0, -0.3), armF=((-60, 140), -20) if v >= 1 else ((-120, -60), 30),
                                            armB=((120, -40), -30) if v < 1 else ((40, 170), 18), brow=0.9)))
        else:
            draw_kiko(T, kiko_talk(t, dict(x=x, y=y, s=s, sq=sq, ring=True, look=(0.7, -0.2), sweat=True, brow=-0.6, o=0.5 if v < 1 else 0, armF=((-100, -80), 30) if v < 1 else ((10, 150), -30),
                                            armB=((100, -80), -30) if v < 1 else ((-10, 150), 30), er=46 if v < 1 else 40)))

def glass(T, x, y, label, fill_k, salt_k, col, t, big=False):
    w, h = 260, 420
    T.shape([(x - w/2, y - h), (x + w/2, y - h), (x + w/2 - 20, y), (x - w/2 + 20, y)], '#e8fbff', lw=8, alpha=0.9)
    lvl = y - h*0.8*fill_k
    T.shape([(x - w/2 + 6 + 20*(1 - (y - lvl)/h), lvl), (x + w/2 - 6 - 20*(1 - (y - lvl)/h), lvl), (x + w/2 - 26, y - 6), (x - w/2 + 26, y - 6)], col, line=False)
    # salt pile on the bottom: a dome that grows
    if salt_k > 0:
        ph = (60 if not big else 230)*salt_k
        T.shape([(x - w/2 + 30, y - 8)] + [(x + (w/2 - 30)*math.cos(a), y - 8 - ph*math.sin(a)) for a in np.linspace(math.pi, 0, 14)] + [(x + w/2 - 30, y - 8)], '#ffffff', shadow='#d9d4e6', shade_dir=(1, 0.2), shade_w=0.25, lw=6)
    T.stroke([(x - w/2 + 30, y - h + 30), (x - w/2 + 40, y - 60)], lw=10, col='#ffffff', alpha=0.8)

def sh_glass(T, t):
    u = t - CUT['glass']
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    T.flat(rect(-200, -200, 1500, 2400), '#2a1f4a')
    for k in range(-2, 16):
        T.flat(rect(-200, 200*k + (tq(t)*30 % 200), 1500, 3), '#3a2e63')
    c = T.c
    k1 = back(u/0.3, 1.5); k2 = back((u - 0.25)/0.3, 1.5)
    t_x10 = E('n2') - 0.9
    # right glass gets 10x the salt: cubes rain in
    salt_r = ease((u - 0.9)/(t_x10 - CUT['glass'] - 0.9))
    if k1 > 0.01: glass(T, 300, 1260, '3.5%', 1.0, 0.25*ease(u/0.6), '#7fd0ff', t)
    if k2 > 0.01: glass(T, 780, 1260, '34%', 1.0, salt_r, '#a6e8de', t, big=True)
    for i in range(14):   # falling salt cubes
        t0 = 0.9 + i*0.17
        if u > t0:
            v = (u - t0)/0.45
            if v < 1:
                x = 700 + (i*53 % 160); y = 520 + v*620
                T.shape(rect(x - 16, y - 16, 32, 32), '#ffffff', lw=5)
    def label(txt, x, y, col, k):
        if k <= 0.01: return
        c.save(); c.translate(x, y); c.scale(k, k); c.select_font_face('Luckiest Guy'); c.set_font_size(110)
        e = c.text_extents(txt); c.move_to(-e.x_advance/2, 0); c.text_path(txt)
        c.set_source_rgb(*LINE); c.set_line_width(22); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve(); c.set_source_rgba(*hexc(col)); c.fill()
        c.set_font_size(42); e = c.text_extents(sub[txt]); c.move_to(-e.x_advance/2, 70); c.text_path(sub[txt]); c.set_source_rgb(*LINE); c.set_line_width(12); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill(); c.restore()
    sub = {'3.5%': 'OUR OCEAN', '34%': 'DEAD SEA'}
    label('3.5%', 300, 1450, '#7fd0ff', back(u/0.3, 1.5))
    label('34%', 780, 1450, '#ffd43b', back((u - 0.9)/0.3, 1.5))
    if t > t_x10:
        kinetic(c, t, 'x10 SALTIER!', t_x10, 540, 560, 120, '#ff4fa3', -0.06)

def sh_kcu(T, t, which):
    u = t - CUT[which]
    if which == 'kcu1':
        T.cx, T.cy, T.z = 300, 1090, 2.05 + 0.05*u
        sky(T, PAR, t); sea(T, PAR, t); shore(T, PAR, t)
        jit = (math.sin(int(t*12)*12.9898)*43758.5 % 1 - 0.5)*6
        draw_kiko(T, kiko_talk(t, dict(x=300, y=1600, s=0.92, ring=True, look=(-0.5, -0.4), sweat=True, brow=-0.9, sm=-0.4, jit=jit,
                                        tremble=(math.sin(int(t*12)*78.2) % 1 - 0.5)*5, armF=((20, 150), -30), armB=((-20, 150), 30))))
    elif which == 'kcu2':
        T.cx, T.cy, T.z = 520, 820, 2.0
        sky(T, PAR, t); sea(T, PAR, t, top=HZ)
        y = 1240 + 6*math.sin(tq(t)*4)
        draw_kiko(T, kiko_talk(t, dict(x=520, y=y, s=0.92, rot=-0.18, ring=True, closed=lip('KIKO', t) < 0.25, brow=0.8, sm=0.9, look=(0, -0.2),
                                        armF=((150, -170), -60), armB=((-150, -170), 60), legs=False)))
        water_front(T, PAR, t, y - 0.92*235*math.cos(0.18))
        k0 = S('k2'); d = E('k2') - S('k2')
        for i, w in enumerate(('BEST.', 'OCEAN.', 'EVER!')):
            kinetic(T.c, t, w, k0 + d*(0.02 + i*0.3), 540, 380 + i*170, 150, ('#ffd43b', '#4fd8ff', '#ff4fa3')[i], (-0.05, 0.04, -0.03)[i])
    else:   # kcu3: panic
        shake_k = 1.0 if at('k3', 0.55) < t < at('k3', 0.85) else 0.25
        T.shake = (math.sin(t*90)*14*shake_k, math.cos(t*77)*10*shake_k)
        T.cx, T.cy, T.z = 520, 780, 2.5 + 0.08*(t - CUT['kcu3'])
        sky(T, PAR, t); sea(T, PAR, t)
        y = 1240 + 6*math.sin(tq(t)*4)
        draw_kiko(T, kiko_talk(t, dict(x=520, y=y, s=0.92, rot=-0.05, ring=True, er=50, brow=-1.0, sweat=True, tremble=(math.sin(int(t*12)*78.2) % 1 - 0.5)*7,
                                        look=(0, 0), armF=((-20, -260), 20), armB=((20, -260), -20), legs=False)))
        water_front(T, PAR, t, y - 0.92*235)

def sh_float(T, t):
    u = t - CUT['float']
    T.cx, T.cy, T.z = 540, 1000, 0.95 + 0.02*u
    sky(T, PAR, t); sea(T, PAR, t)
    t_jump, t_land = CUT['float'] + 0.35, CUT['float'] + 1.05
    # Kiko: jumps from the shore into the sea, then floats high like a cork
    if t < t_land:
        v = clamp((t - t_jump)/(t_land - t_jump))
        x = 250 + 150*v; y = 1590 + (1215 - 1590)*v - math.sin(v*math.pi)*420
        rot = -0.5*v if t > t_jump else 0
        water_front(T, PAR, t, 1215 - 0.62*235, x1=SHORE + 2000)
        front_shore(T, 700)
        crouch = 0.9 if t_jump - 0.2 < t < t_jump else 1.0
        draw_kiko(T, dict(t=t, x=x, y=y, s=0.62, sq=crouch, rot=rot, ring=True, er=48, o=0.6 if t > t_jump else 0, brow=-0.8, sweat=True, look=(0.5, 0.3),
                          armF=((-80, -160), 30), armB=((80, -160), -30), legL=(-20, -20) if t > t_jump else (0, 0), legR=(30, -40) if t > t_jump else (0, 0)))
    else:
        wl = 1215 - 0.62*235 + 5*math.sin(tq(t)*4)
        sq = land_sq(t, t_land)
        draw_kiko(T, dict(t=t, x=400, y=1215 + 5*math.sin(tq(t)*4), s=0.62, sq=sq, rot=-0.2, ring=True, closed=t > t_land + 1.2, sm=0.8 if t > t_land + 0.8 else -0.2,
                          er=46 if t < t_land + 0.8 else 40, brow=0.6 if t > t_land + 0.8 else -0.5, look=(0, -0.3), legs=False,
                          armF=((150, -170), -60) if t > t_land + 1.0 else ((-110, -40), 30), armB=((-150, -170), 60) if t > t_land + 1.0 else ((110, -40), -30)))
        water_front(T, PAR, t, wl, x1=SHORE + 2000)
        # rubber duck pops up next to him
        td = at('n3', 0.78)
        if t > td:
            k = back((t - td)/0.3, 1.8); duck(T, 580, wl + 20 - 30*k + 30, 0.9*k, t)
        # shore over the water (sand in front) on the right
        front_shore(T, 700)
    if t < t_land:
        pass
    # splash ring (flat, no noise) on landing
    if t_land <= t < t_land + 0.6:
        k = (t - t_land)/0.6
        for j in range(3):
            T.shape(ellipse_pts(400, 1080, 120 + 260*k + j*40, 26 + 60*k + j*8, 30), None, lw=max(1, 8*(1 - k)))
        for j in range(6):
            a = math.pi*(1.1 + j*0.16); r = 140 + 300*k
            T.shape(ellipse_pts(400 + r*math.cos(a), 1080 + r*0.6*math.sin(a) - 200*math.sin(k*math.pi), 16, 22, 12), PAR['sea2'], lw=5)
    # Nova walks in from the right along the shore, then stops and talks to camera
    tw0, tw1 = CUT['float'] + 0.2, CUT['float'] + 2.0
    v = ease((t - tw0)/(tw1 - tw0))
    walking = tw0 < t < tw1
    lL, lR, bob = walk_legs(t, walking, 30)
    nx = 1260 + (850 - 1260)*v
    if t >= t_land:
        draw_nova(T, nova_talk(t, dict(x=nx, y=1640, s=0.85, face=-1 if walking else 1, legL=lL, legR=lR, bob=bob, lean=0.06 if walking else 0,
                                        look=(-0.8, 0.1), armF=((40, 150), -25) if walking else ((-120, 60), 40), armB=((-40, 150), 25) if walking else ((40, 170), 18), brow=0.7)))
    else:
        draw_nova(T, nova_talk(t, dict(x=nx, y=1640, s=0.85, face=-1, legL=lL, legR=lR, bob=bob, lean=0.06, look=(-0.8, -0.2),
                                        armF=((40 + 30*math.sin(tq(t)*12), 150), -25), armB=((-40 - 30*math.sin(tq(t)*12), 150), 25))))

def sh_ncu(T, t):
    u = t - CUT['ncu']
    T.cx, T.cy, T.z = 760, 1110, 2.1 + 0.04*u
    sky(T, PAR, t); sea(T, PAR, t); shore(T, PAR, t)
    draw_nova(T, nova_talk(t, dict(x=780, y=1640, s=0.85, face=-1, look=(-0.2, 0.15), lid=0.42, brow=-0.3, sm=0.0,
                                    armF=((-40, -230), 10), armB=((40, 170), 18))))
    # raised finger
    hx, hy = 780 + 0.85*(72 + 40), 1640 + 0.85*(-385 - 230)

def microbe(T, x, y, s, t, i):
    w = 4*math.sin(tq(t)*8 + i)
    T.shape([(x + (34 + 5*math.sin(a*3 + tq(t)*6 + i))*s*math.cos(a), y + (26 + 4*math.cos(a*2 + tq(t)*5))*s*math.sin(a)) for a in np.linspace(0, 2*math.pi, 24)],
            ('#ff8fb8', '#ffb36b', '#c79bff')[i % 3], lw=5)
    for ex in (-9, 9):
        T.shape(ellipse_pts(x + ex*s, y - 4*s + w*0.2, 7*s, 8*s, 12), '#ffffff', lw=4)
        T.dot(x + ex*s + 2*s, y - 4*s, 2.6*s)
    for k in range(3):
        a = math.pi*(0.75 + k*0.25); T.stroke([(x + 34*s*math.cos(a), y + 26*s*math.sin(a)), (x + 50*s*math.cos(a) + w, y + 40*s*math.sin(a))], lw=4)

def ghost(T, kind, x, y, s, k, t, xk):
    """dashed outline of a creature that can't live here, with a red X"""
    if k <= 0: return
    if kind == 'fish':
        pts = [(x - 90*s, y), (x - 40*s, y - 45*s), (x + 40*s, y - 40*s), (x + 80*s, y), (x + 40*s, y + 40*s), (x - 40*s, y + 45*s), (x - 90*s, y),
               (x - 140*s, y - 40*s), (x - 140*s, y + 40*s), (x - 90*s, y)]
    elif kind == 'coral':
        pts = [(x - 20*s, y + 90*s), (x - 20*s, y), (x - 80*s, y - 60*s), (x - 60*s, y - 80*s), (x - 10*s, y - 30*s), (x, y - 110*s), (x + 25*s, y - 105*s), (x + 20*s, y - 30*s),
               (x + 70*s, y - 70*s), (x + 90*s, y - 50*s), (x + 25*s, y + 10*s), (x + 25*s, y + 90*s)]
    else:   # seaweed / plant
        pts = [(x - 15*s, y + 100*s), (x - 30*s, y + 30*s), (x - 5*s, y - 30*s), (x - 25*s, y - 100*s), (x + 5*s, y - 110*s), (x + 20*s, y - 30*s), (x, y + 30*s), (x + 15*s, y + 100*s)]
    T.shape(pts, '#ffffff', lw=0, line=False, alpha=0.25*k)
    c = T.c; c.save(); c.set_dash([18, 14]); T.shape(pts, None, lw=7, alpha=k); c.restore()
    if xk > 0:
        r = 95*s*back(xk, 1.6)
        T.stroke([(x - r, y - r), (x + r, y + r)], lw=16, col='#ff3b5c'); T.stroke([(x + r, y - r), (x - r, y + r)], lw=16, col='#ff3b5c')

def sh_under(T, t, pal=PAR):
    u = t - CUT['under']
    tilt = ease(u/0.6)
    T.cx, T.cy, T.z = 540, 380 + 580*tilt, 1.0
    # above the surface: the sky + Kiko floating (cut off at the waterline)
    sky(T, pal, t, moons=False)
    SURF = 700
    y = SURF + 0.6*235 + 5*math.sin(tq(t)*4)
    draw_kiko(T, dict(t=t, x=540, y=y, s=0.6, rot=-0.05, ring=True, closed=True, sm=0.8, brow=0.6, legL=(-10 + 12*math.sin(tq(t)*3), 0), legR=(10 - 12*math.sin(tq(t)*3), 0),
                      armF=((150, -170), -60), armB=((-150, -170), 60)))
    # water body (translucent bands over his legs)
    bands = ['#a6e8de', '#8fd8cf', '#77c6c2', '#62b3b5', '#4f9fa8']
    for i, col in enumerate(bands):
        T.flat(rect(-200, SURF + i*280, 1500, 284), col, alpha=0.82 if i == 0 else 1.0)
    T.stroke([(x, SURF + 6*math.sin(x/50 + tq(t)*5)) for x in range(-200, 1300, 30)], lw=8)
    # salt crystal floor
    for i in range(16):
        x = -60 + i*80; hh = 50 + (i*37 % 70)
        T.shape([(x - 40, 1720), (x - 30, 1720 - hh), (x + 10, 1720 - hh - 25), (x + 40, 1720 - hh + 10), (x + 45, 1720)], '#fbf8f0', shadow='#cfd9e6', shade_dir=(1, 0.1), shade_w=0.3, lw=6)
    T.shape(rect(-200, 1710, 1500, 700), '#e8e2f0', lw=7)
    # ghosts of what can't live here
    tf = at('n4', 0.33); tp = at('n4', 0.45)
    ghost(T, 'fish', 330, 1040, 1.2, clamp((t - tf + 0.3)/0.3), t, (t - tf)/0.25)
    ghost(T, 'coral', 800, 1520, 1.0, clamp((t - tp + 0.3)/0.3), t, (t - tp)/0.25)
    ghost(T, 'plant', 230, 1540, 0.95, clamp((t - tp + 0.2)/0.3), t, (t - tp - 0.15)/0.25)
    ghost(T, 'fish', 790, 1250, 0.8, clamp((t - tf)/0.3), t, (t - tf - 0.2)/0.25)
    # tiny microbes pop in
    tm = at('n4', 0.74)
    for i in range(9):
        t0 = tm + i*0.07
        if t > t0:
            k = back((t - t0)/0.25, 2.0)
            mx, my = ((180, 900), (520, 860), (860, 940), (300, 1180), (690, 1110), (950, 1300), (140, 1400), (480, 1380), (780, 1460))[i]
            microbe(T, mx + 20*math.sin(t*1.3 + i), my + 15*math.cos(t*1.1 + i), 1.25*k, t, i)

def sh_red(T, t):
    u = t - CUT['red']
    T.cx, T.cy, T.z = 540, 1010, 1.0 + 0.03*u
    k = ease((u - 0.3)/2.4)
    pal = dict(lerp_pal(PAR, RED, k), sea=PAR['sea'] if k < 1 else RED['sea'], sea2=PAR['sea2'] if k < 1 else RED['sea2'])
    sky(T, pal, t); sea(T, pal, t)
    if 0 < k < 1:
        r = 120 + 1500*k
        T.shape([(420 + r*(1 + 0.08*math.sin(5*a + t*3))*math.cos(a), 1150 + min(r*0.3, 280)*(1 + 0.08*math.sin(5*a + t*3))*math.sin(a)) for a in np.linspace(0, 2*math.pi, 50)], RED['sea'], lw=7)
    wl = 1215 - 0.62*235 + 5*math.sin(tq(t)*4)
    panic = k > 0.35
    draw_kiko(T, dict(t=t, x=400, y=1215 + 5*math.sin(tq(t)*4), s=0.62, rot=-0.05, ring=True, legs=False, er=50 if panic else 40, closed=not panic, sm=-0.6 if panic else 0.8,
                      o=0.55 if panic else 0, brow=-1.0 if panic else 0.6, sweat=panic, look=(0, 0.4), tremble=(math.sin(int(t*12)*78.2) % 1 - 0.5)*6 if panic else 0,
                      armF=((-60, -250), 20) if panic else ((150, -170), -60), armB=((60, -250), -20) if panic else ((-150, -170), 60)))
    water_front(T, pal if k >= 1 else dict(pal, sea=RED['sea'] if k > 0.15 else PAR['sea'], sea2=RED['sea2'] if k > 0.15 else PAR['sea2']), t, wl, x1=SHORE + 2000)
    front_shore(T, 700)
    draw_nova(T, nova_talk(t, dict(x=830, y=1640, s=0.85, face=1, look=(-0.8, 0.0), armF=((-140, 40), 40), lid=0.2, brow=0.3)))

def sh_card(T, t):
    u = t - CUT['card']
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.025*u
    T.flat(rect(-300, -300, 1700, 2600), '#2a1f4a')
    for k in range(-2, 16):
        T.flat(rect(-300, 200*k + (tq(t)*30 % 200), 1700, 3), '#3a2e63')
    c = T.c
    kc = back(u/0.35, 1.4)
    if kc > 0.01:
        # flat "photo" of the red Dead Sea: a postcard
        cx, cy = 540, 980
        c.save(); X, Y = T.xf((cx, cy)); c.translate(X, Y); c.rotate(-0.04); c.scale(kc, kc); c.translate(-X, -Y)
        T.shape(rect(cx - 400, cy - 330, 800, 660), '#fbf8f0', lw=9)
        T.flat(rect(cx - 360, cy - 290, 720, 300), '#ffa45c'); T.flat(rect(cx - 360, cy - 290, 720, 120), '#ea6a4a')
        T.shape([(cx - 360, cy - 40), (cx - 200, cy - 110), (cx - 60, cy - 70), (cx + 80, cy - 130), (cx + 360, cy - 60), (cx + 360, cy + 10), (cx - 360, cy + 10)], '#b77b55', lw=6)
        T.shape(rect(cx - 360, cy + 10, 720, 250), '#c8324a', lw=6)
        for j in range(4):
            T.stroke([(cx - 300 + j*170, cy + 80 + (j % 2)*70), (cx - 240 + j*170, cy + 70 + (j % 2)*70)], lw=7, col='#e2607a')
        c.restore()
        kinetic(c, t, 'DEAD SEA', CUT['card'] + 0.15, 540, 470, 110, '#ffffff', -0.03)
        kinetic(c, t, '1992', at('n5', 0.86), 540, 1480, 230, '#ff4fa3', 0.04)
        if t > at('n5', 0.92):
            kinetic(c, t, 'REAL!', at('n5', 0.92), 860, 1260, 90, '#7dff9a', 0.2)

def poll_chip(c, x, y, txt, col, k, icon):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(58)
    w = c.text_extents(txt).x_advance + 160; h = 116; r = 58
    c.new_path(); c.arc(-w/2 + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(w/2 - r, 0, r, -math.pi/2, math.pi/2); c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(8); c.stroke()
    icon(c, -w/2 + 66, 0)
    c.move_to(-w/2 + 122, 20); c.text_path(txt); c.set_source_rgb(*LINE); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill()
    c.restore()

def icon_ring(c, x, y):
    c.new_path(); c.arc(x, y, 30, 0, 2*math.pi); c.new_sub_path(); c.arc_negative(x, y, 13, 2*math.pi, 0)
    c.set_source_rgba(*hexc('#ff8a1f')); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(5); c.stroke()
def icon_fish(c, x, y):
    c.new_path(); c.move_to(x - 30, y); c.curve_to(x - 10, y - 26, x + 20, y - 22, x + 30, y); c.curve_to(x + 20, y + 22, x - 10, y + 26, x - 30, y)
    c.line_to(x - 44, y - 16); c.line_to(x - 44, y + 16); c.close_path()
    c.set_source_rgba(*hexc('#4fd8ff')); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(5); c.stroke()
    c.arc(x + 14, y - 5, 4, 0, 2*math.pi); c.fill()

def sh_end(T, t):
    u = t - CUT['end']
    k = 1.0 - ease((u - 0.5)/3.0)*0.0
    pal = RED
    T.cx, T.cy, T.z = 560, 1060 - 30*ease(u/3), 0.92 + 0.03*u
    sky(T, pal, t); sea(T, pal, t)
    wl = 1215 - 0.62*235 + 5*math.sin(tq(t)*4)
    draw_kiko(T, dict(t=t, x=330, y=1215 + 5*math.sin(tq(t)*4), s=0.62, rot=-0.15, ring=True, legs=False, closed=False, sm=0.2, brow=-0.2, look=(0.7, -0.2),
                      blink=blinkf(t, 2.6), armF=((-120, -40), 30), armB=((120, -40), -30)))
    water_front(T, pal, t, wl, x1=SHORE + 2000)
    front_shore(T, 560)
    portal(T, t, 650, 1240, 140, back(u/0.4, 1.0))
    draw_nova(T, nova_talk(t, dict(x=860, y=1620, s=0.85, face=-1, look=(0.0, 0.1), armF=((-80, -60), 30), armB=((60, 150), 15), brow=0.9)))
    c = T.c
    poll_chip(c, 540, 440, 'FLOAT FOREVER', '#ff4fa3', back((t - at('n6', 0.25))/0.3, 1.6), icon_ring)
    poll_chip(c, 540, 600, 'KEEP THE FISH', '#3a8fd8', back((t - at('n6', 0.55))/0.3, 1.6), icon_fish)

SHOTS = {'beach0': sh_beach0, 'arrive': sh_arrive, 'glass': sh_glass, 'kcu1': lambda T, t: sh_kcu(T, t, 'kcu1'), 'float': sh_float,
         'kcu2': lambda T, t: sh_kcu(T, t, 'kcu2'), 'ncu': sh_ncu, 'under': sh_under, 'kcu3': lambda T, t: sh_kcu(T, t, 'kcu3'),
         'red': sh_red, 'card': sh_card, 'end': sh_end}

def render(t, clean=False):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
    sh = shot_at(t)
    T = Toon(c, t)
    SHOTS[sh](T, t)
    if not clean:
        if sh in ('arrive', 'kcu1', 'float'): tag(c, t, 'WORLD #12 · OCEAN SALT 34%', CUT['arrive'] + 0.4)
        if sh in ('red',): tag(c, t, 'WARNING: MICROBE BLOOM', CUT['red'] + 0.9, '#ff6b7d')
        caption(c, t)
        brand(c, t)
        flash(c, t, CUT['glass'], 0.1, 0.35); flash(c, t, CUT['card'], 0.1, 0.35); flash(c, t, CUT['under'], 0.12, 0.3)
        swirl_wipe(c, t, CUT['arrive'])
        # fade out at the very end
        if t > TOTAL - 0.35:
            c.set_source_rgba(0, 0, 0, clamp((t - (TOTAL - 0.35))/0.35)); c.paint()
    return surf

def frame_bytes(i):
    s = render(i/FPS); return bytes(s.get_data())

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    os.makedirs('/home/claude/pw/out', exist_ok=True)
    if mode == 'stills':
        ts = [float(x) for x in sys.argv[2:]] or [CUT[k] + 0.6 for k in ORDER]
        for t in ts:
            render(t).write_to_png(f'/home/claude/pw/out/ep12_{t:05.2f}.png')
    elif mode == 'video':
        N = int(TOTAL*FPS)
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '/home/claude/pw/out/ep12_v.mp4'], stdin=subprocess.PIPE)
        with Pool(2) as pool:
            for i, b in enumerate(pool.imap(frame_bytes, range(N), chunksize=6)):
                p.stdin.write(b)
                if i % 120 == 0: print(i, '/', N, flush=True)
        p.stdin.close(); p.wait()
