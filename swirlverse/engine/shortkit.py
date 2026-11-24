"""Swirlverse SHORT kit (1080x1920, 24 fps, sitcom-toon look).
An episode is a python file that defines LINES, META and shots(K) (see episodes/_template_short.py).
The kit gives ready shots (hook, arrive, twoshot, kcu, ncu, stat, compare, words, end) and the sets
(beach, park, room, street, space), so a new episode only needs a script, a shot list and, when useful,
a few custom draw functions."""
import math, json, re, os, cairo, numpy as np
import toonline
toonline.W, toonline.H = 1080, 1920
from toonline import Toon, hexc, mixc, ellipse_pts, rect, star, noodle_pts, LINE
from toonchars import draw_nova, draw_kiko, draw_baby, draw_adult, MOM, DAD, GRANDPA, walk_legs, land_sq, tq, swim_ring
W, H, FPS = 1080, 1920, 24
FONT = 'Fredoka Light'
CAP_FACE = cairo.ToyFontFace(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(u): u = clamp(u); return u*u*(3 - 2*u)
def back(u, k=1.3):
    u = clamp(u); return 1 + (k + 1)*(u - 1)**3 + k*(u - 1)**2
def jitter(t, a=5): return (math.sin(int(t*12)*12.9898)*43758.5 % 1 - 0.5)*a
def blinkf(t, period, off=0.0): return ((t + off) % period) > period - 0.12

def swirl(c, x, y, r, a=1.0, t=0.0):
    c.new_path(); c.save(); c.translate(x, y); c.rotate(t*2)
    for i in range(3):
        c.arc(0, 0, r*(0.35 + i*0.3), i*2.1, i*2.1 + 4.2); c.set_source_rgba(*hexc(('#ff6bd6', '#7cf3ff', '#ffd43b')[i], a))
        c.set_line_width(r*0.22); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()

# ------------------------------------------------------------------ palettes (channel colours: keep these)
def bands(a, b): return [mixc(a, b, k/5) for k in range(6)]
OUR = dict(sky=bands('#2f7fe0', '#bfe4ff'), sea='#2f8fd8', sea2='#58aee6', ground='#5cc46b', ground2='#47a857', sand='#f6d48a', wall='#fff0d6', wall2='#ffe2b8', floor='#c98a5a', moons=False, sun=True)
PAR = dict(sky=bands('#3b1f8c', '#ff9fd1'), sea='#a6e8de', sea2='#d4f6ef', ground='#4fc59a', ground2='#3aa883', sand='#f2d6a8', wall='#efe0ff', wall2='#ddc8ff', floor='#b07acb', moons=True, sun=False)
def palette(base, **over): d = dict(base); d.update(over); return d

EMO = {
    'neutral': dict(brow=0.4, sm=0.4), 'happy': dict(brow=0.8, sm=0.9), 'excited': dict(brow=1.0, sm=0.9, er=46),
    'worried': dict(brow=-0.8, sm=-0.4, sweat=True), 'shock': dict(brow=-1.0, er=50, sm=-0.6, sweat=True),
    'deadpan': dict(lid=0.4, brow=0.0, sm=0.1), 'smug': dict(lid=0.3, brow=0.6, sm=0.8), 'sad': dict(brow=-0.6, lid=0.3, sm=-0.6),
    'proud': dict(brow=0.9, sm=0.9, closed=True), 'confused': dict(brow=-0.3, sm=-0.2, look=(0.3, -0.5)),
}
GEST = {
    'rest': {}, 'point': dict(armF=((-150, -40), 40)), 'arms_up': dict(armF=((-120, -200), 30), armB=((120, -200), -30)),
    'hands_head': dict(armF=((-20, -260), 20), armB=((20, -260), -20)), 'shrug': dict(armF=((-110, -40), 30), armB=((110, -40), -30)),
    'hips': dict(armF=((60, 120), -40), armB=((-60, 120), 40)), 'finger_up': dict(armF=((-40, -230), 10)), 'wave': dict(armF=((-130, -160), 30)),
    'present': dict(armF=((-150, -100), 40)), 'clicker': dict(armF=((-150, -40), 40), hold='clicker'),
}
def pose(emo='neutral', gest='rest', **kw):
    P = dict(EMO.get(emo, {})); P.update(GEST.get(gest, {})); P.update(kw); return P

# ------------------------------------------------------------------ sets (world coords = the 1080x1920 frame at zoom 1)
HZ, SHORE, FEET = 860, 1270, 1600

def sky(T, pal, t):
    edges = [-1500, 150, 300, 450, 600, 750, 1500]
    for i, col in enumerate(pal['sky']):
        T.flat(rect(-1500, edges[i], 4080, edges[i + 1] - edges[i] + 2), col)
    if pal.get('sun'):
        T.glow(820, 300, 90, '#fff6b0'); T.shape(ellipse_pts(820, 300, 90, 90), '#ffe066', shadow='#ffc93c', shade_dir=(1, 0.5), shade_w=0.2, lw=7)
        for (cx, cy, s) in ((230, 260, 1.0), (640, 470, 0.7)):
            T.shape([(cx - 110*s, cy + 30*s), (cx - 80*s, cy - 20*s), (cx - 20*s, cy - 50*s), (cx + 50*s, cy - 30*s), (cx + 110*s, cy + 30*s)], '#ffffff', lw=7)
    if pal.get('moons'):
        for (x, y, r, col, sh) in ((820, 260, 95, '#fff2c8', '#e7c98f'), (640, 170, 42, '#c9f3ff', '#9fd6ea')):
            T.glow(x, y, r, col); T.shape(ellipse_pts(x, y, r, r), col, shadow=sh, shade_dir=(1, 0.5), shade_w=0.25, lw=7)
        bob = 8*math.sin(t*1.3)
        T.shape([(120, 520 + bob), (330, 505 + bob), (300, 560 + bob), (240, 640 + bob), (200, 600 + bob), (150, 565 + bob)], '#7a4a8a', shadow='#5c3570', lw=7)
        T.shape([(110, 525 + bob), (340, 505 + bob), (332, 530 + bob), (118, 545 + bob)], '#47c2a0', lw=7)

def set_beach(T, pal, t):
    sky(T, pal, t)
    T.shape([(-1500, HZ), (2580, HZ), (2580, SHORE + 400), (-1500, SHORE + 400)], pal['sea'], lw=7)
    for k in range(4):
        y = HZ + 50 + k*95; ph = tq(t)*1.5 + k
        for j in range(5):
            x0 = -100 + j*280 + (k % 2)*140 + 25*math.sin(ph + j)
            T.stroke([(x0, y), (x0 + 60, y - 10), (x0 + 120, y)], lw=7, col=pal['sea2'])
    T.shape([(-1500, SHORE)] + [(x, SHORE + 14*math.sin(x/120)) for x in range(-1500, 2600, 60)] + [(2580, 3600), (-1500, 3600)], pal['sand'], lw=7)

def house(T, x, w, h, wall, roof, base=1180):
    T.shape(rect(x, base - h, w, h), wall, lw=7)
    T.flat(rect(x + w*0.72, base - h, w*0.28, h), '#000000', alpha=0.12)
    T.shape([(x - 20, base - h + 5), (x + w/2, base - h - 110), (x + w + 20, base - h + 5)], roof, lw=7)
    for wx in (x + 35, x + w - 95): T.shape(rect(wx, base - h + 60, 60, 70), '#fff6d8', lw=6)

def round_tree(T, x, y, r, col, sh):
    T.shape(rect(x - 14, y, 28, 120), '#8a5a3c', lw=6); T.shape(ellipse_pts(x, y - 30, r, r*0.9), col, shadow=sh, lw=7)

def set_park(T, pal, t):
    sky(T, pal, t)
    T.shape([(-1500, 1000)] + [(x, 960 - 40*math.sin(x/170)) for x in range(-1500, 2600, 40)] + [(2580, 1300), (-1500, 1300)], mixc(pal['ground'], '#6c5bb5', 0.45), lw=6)
    for (x, w, h, wall, roof) in ((40, 230, 260, '#ffd166', '#e4572e'), (720, 300, 330, '#7bdff2', '#3d5a80'), (470, 200, 220, '#f4a6c6', '#6a4c93')):
        house(T, x, w, h, wall, roof)
    T.shape([(-1500, 1160), (2580, 1140), (2580, 3600), (-1500, 3600)], pal['ground'], lw=7)
    T.shape([(430, 1160), (620, 1158), (900, 3000), (160, 3000)], '#f2d6a8', lw=7)
    round_tree(T, 980, 1110, 95, '#2fa36b', '#1f7a4f'); round_tree(T, 90, 1120, 80, '#ff7fb0', '#d9558b')

def set_room(T, pal, t):
    FL = 1350
    T.flat(rect(-1500, -1500, 4100, FL + 1500), pal['wall'])
    for i in range(-12, 30): T.flat(rect(i*90, -1500, 38, FL + 1500), pal['wall2'])
    wx, wy, ww, wh = 140, 360, 460, 380
    T.shape(rect(wx - 22, wy - 22, ww + 44, wh + 44), '#ffffff', lw=8)
    for i, col in enumerate(pal['sky']): T.shape(rect(wx, wy + i*wh/6, ww, wh/6 + 1), col, line=False, amp=0)
    if pal.get('moons'): T.shape(ellipse_pts(wx + 330, wy + 110, 56, 56), '#fff2c8', shadow='#e7c98f', shade_dir=(1, 0.5), shade_w=0.25, lw=6)
    else: T.shape(ellipse_pts(wx + 340, wy + 100, 50, 50), '#ffe066', lw=6)
    T.stroke([(wx + ww/2, wy), (wx + ww/2, wy + wh)], lw=12, col='#ffffff'); T.stroke([(wx, wy + wh/2), (wx + ww, wy + wh/2)], lw=12, col='#ffffff')
    T.shape(rect(720, 420, 220, 170), '#c98a4a', lw=7); T.shape(rect(742, 442, 176, 126), '#9fe3d9', lw=5)
    T.shape(rect(-1500, FL, 4100, 1200), pal['floor'], lw=8)
    T.shape(rect(-1500, FL - 24, 4100, 26), '#ffffff', lw=6)

def set_street(T, pal, t):
    sky(T, pal, t)
    for (x, w, h, col) in ((-60, 300, 560, '#7bdff2'), (260, 260, 420, '#ffd166'), (540, 260, 640, '#f4a6c6'), (820, 300, 480, '#9fe3d9')):
        T.shape(rect(x, 1250 - h, w, h), col, lw=7)
        for wy in range(1250 - h + 50, 1170, 110):
            for wx in (x + 40, x + w - 100): T.shape(rect(wx, wy, 60, 70), '#fff6d8', lw=5)
    T.shape(rect(-1500, 1250, 4100, 2400), '#8e8aa8', lw=8); T.shape(rect(-1500, 1250, 4100, 40), '#c9c3d9', lw=6)

def set_space(T, pal, t):
    T.flat(rect(-1500, -1500, 4100, 5000), '#120a2e')
    rng = np.random.default_rng(3)
    for i in range(120):
        x, y = rng.uniform(-200, 1300), rng.uniform(-200, 2100); T.dot(x, y, rng.uniform(1.5, 4), '#ffffff')
    T.shape(ellipse_pts(540, 2300, 1100, 700), '#3d7bfd', shadow='#2a56c0', shade_dir=(1, 0.3), shade_w=0.2, lw=8)
    T.shape([(200, 1700), (420, 1650), (520, 1760), (300, 1820)], '#47c2a0', lw=6); T.shape([(700, 1680), (900, 1720), (860, 1800), (680, 1790)], '#47c2a0', lw=6)

SETS = dict(beach=set_beach, park=set_park, room=set_room, street=set_street, space=set_space)

def portal(T, t, cx, cy, R, open_k=1.0):
    if open_k <= 0.01: return
    R = R*open_k
    T.glow(cx, cy, R, '#ffd84d', ((1.35, 0.10), (1.18, 0.16)), sy=1.25)
    rim = [(cx + R*(1 + 0.05*math.sin(5*a + t*2))*math.cos(a), cy + 1.25*R*(1 + 0.05*math.sin(5*a + t*2))*math.sin(a)) for a in np.linspace(0, 2*math.pi, 60)]
    T.shape(rim, '#ffd84d', lw=9, seed=11)
    inner = [(cx + 0.86*(x - cx), cy + 0.86*(y - cy)) for x, y in rim]
    T.shape(inner, '#7a2fbf', line=False, seed=12, amp=0)
    c = T.c; c.save(); T._path(T.X(inner)); c.clip()
    for arm, col in enumerate(['#ff4fa3', '#4fd8ff', '#ff4fa3', '#4fd8ff']):
        pts = [(cx + R*0.86*(i/49)*math.cos(arm*math.pi/2 + (i/49)*3.4 + t*2.2), cy + 1.25*R*0.86*(i/49)*math.sin(arm*math.pi/2 + (i/49)*3.4 + t*2.2)) for i in range(50)]
        c.set_source_rgba(*hexc(col)); c.set_line_width(46*R/230*T.z); c.set_line_cap(cairo.LINE_CAP_ROUND); T._path(T.X(pts), False); c.stroke()
    c.restore()
    T.shape(ellipse_pts(cx, cy, 62*R/230, 78*R/230), '#fff7e0', line=False, amp=0)

# ------------------------------------------------------------------ screen overlays
def label(c, txt, x, y, size, col='#ffffff', rot=0.0, k=1.0, font='Luckiest Guy', lw=None):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    if font == 'Luckiest Guy': c.select_font_face(font)
    else: c.set_font_face(CAP_FACE)
    c.set_font_size(size); e = c.text_extents(txt)
    c.move_to(-e.x_advance/2, size*0.36); c.text_path(txt)
    c.set_source_rgb(*LINE); c.set_line_width(lw if lw is not None else size*0.2); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*hexc(col)); c.fill(); c.restore()

def kin(c, t, txt, t0, x, y, size, col='#ffd43b', rot=0.0):
    if t >= t0: label(c, txt, x, y, size, col, rot, back((t - t0)/0.25, 2.0))

def flash(c, t, t0, d=0.1, a=0.3):
    if t0 <= t < t0 + d: c.set_source_rgba(1, 1, 1, a*(1 - (t - t0)/d)); c.paint()

def swirl_wipe(c, t, tc, d=0.32):
    u = (t - (tc - d))/(2*d)
    if u <= 0 or u >= 1: return
    R = math.hypot(W, H)*0.62
    r_out, r_in = (R*ease(u*2), 0) if u < 0.5 else (R, R*ease((u - 0.5)*2))
    c.save(); c.translate(W/2, H/2); c.new_path(); c.arc(0, 0, r_out, 0, 2*math.pi)
    if r_in > 0: c.new_sub_path(); c.arc_negative(0, 0, r_in, 2*math.pi, 0)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_source_rgba(*hexc('#5a1f9a')); c.paint()
    for arm, col in enumerate(['#ff4fa3', '#4fd8ff', '#ffd84d', '#ff4fa3', '#4fd8ff', '#ffd84d']):
        c.new_path()
        for i in range(60):
            v = i/59; a = arm*math.pi/3 + v*4.2 + t*9; r = R*1.1*v
            (c.move_to if i == 0 else c.line_to)(r*math.cos(a), r*math.sin(a))
        c.set_source_rgba(*hexc(col)); c.set_line_width(70); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.arc(0, 0, 70, 0, 2*math.pi); c.set_source_rgb(1, 0.97, 0.88); c.fill(); c.restore()

def tag(c, t, text, t0, col='#4fd8ff', y=150):
    n = int(clamp((t - t0)/0.9)*len(text))
    if n <= 0: return
    s = text[:n] + ('_' if (t*4) % 1 < 0.5 and n < len(text) else '')
    c.select_font_face('DejaVu Sans Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(36)
    w = c.text_extents(text).x_advance
    c.set_source_rgba(0.06, 0.04, 0.12, 0.8); c.rectangle((W - w)/2 - 22, y - 44, w + 44, 62); c.fill()
    c.move_to((W - w)/2, y); c.set_source_rgba(*hexc(col)); c.show_text(s); c.new_path()

def poll_chip(c, x, y, txt, col, k):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.set_font_face(CAP_FACE); c.set_font_size(58)
    w = c.text_extents(txt).x_advance + 90; r = 58
    c.new_path(); c.arc(-w/2 + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(w/2 - r, 0, r, -math.pi/2, math.pi/2); c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(8); c.stroke()
    c.move_to(-w/2 + 45, 20); c.text_path(txt); c.set_source_rgb(*LINE); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill(); c.restore()

def board(T, t, col='#2a1f4a', grid='#3a2e63'):
    T.flat(rect(-2000, -2000, 6000, 6000), col)
    for k in range(-12, 30): T.flat(rect(-2000, 200*k + (tq(t)*30 % 200), 6000, 3), grid)

# ------------------------------------------------------------------ the kit
class Kit:
    def __init__(self, ep_dir, meta):
        self.dir = ep_dir; self.meta = meta
        self.TL = json.load(open(os.path.join(ep_dir, 'timeline.json')))
        self.TOTAL = self.TL['total']; self.LINES = self.TL['lines']
        self.our = meta.get('our_palette', OUR); self.par = meta.get('par_palette', PAR)
        self.our_set = meta.get('our_set', 'park'); self.par_set = meta.get('par_set', self.our_set)
        self.wipe_t = None; self.edl = []; self.sfx = []; self.drops = []
        self.caps = self._caps()
        self.NOVA_X, self.KIKO_X = 800, 270
    # timing helpers
    def S(self, i): return self.LINES[i]['s']
    def E(self, i): return self.LINES[i]['e']
    def at(self, i, f): return self.S(i) + (self.E(i) - self.S(i))*f
    def L(self, i): return self.S(i) - 0.12
    def lip(self, who, t):
        for l in self.LINES:
            if l['who'] == who and l['s'] <= t <= l['e']:
                i = int((tq(t) - l['s'])*24); return l['lip'][min(max(i, 0), len(l['lip']) - 1)]
        return 0.0
    def nova(self, T, t, **P):
        o = self.lip('NOVA', t); D = dict(t=t, x=self.NOVA_X, y=FEET, s=0.92, o=o*0.95, nod=o*7, blink=blinkf(t, 3.4), sm=0.45, face=-1, look=(-0.6, 0)); D.update(P)
        draw_nova(T, D)
    def kiko(self, T, t, **P):
        o = self.lip('KIKO', t); D = dict(t=t, x=self.KIKO_X, y=FEET, s=0.92, o=o*1.1, nod=o*7, blink=blinkf(t, 2.9, 1.1), face=1, look=(0.6, 0)); D.update(P)
        draw_kiko(T, D)
    def world(self, T, t, par):
        (SETS[self.par_set if par else self.our_set])(T, self.par if par else self.our, t)
    # ----- captions
    def _caps(self):
        out = []
        for l in self.LINES:
            txt = l.get('cap', l['text'])
            parts = [p.strip() for p in re.split(r'(?<=[.?!,])\s+', txt) if p.strip()]
            merged = []
            for p in parts:
                if merged and len(merged[-1]) + len(p) < 24 and not merged[-1].endswith(('.', '?', '!')): merged[-1] += ' ' + p
                else: merged.append(p)
            fin = []
            for p in merged:
                while len(p) > 30:
                    w = p.split(); half = len(w)//2; fin.append(' '.join(w[:half])); p = ' '.join(w[half:])
                fin.append(p)
            tot = sum(len(p) for p in fin); t0 = l['s']
            for p in fin:
                d = (l['e'] - l['s'])*len(p)/tot; out.append((t0, t0 + d + 0.12, p, l['who'])); t0 += d
        return out
    def caption(self, c, t):
        for (a, b, txt, who) in self.caps:
            if a <= t < b:
                col = '#3a3f8f' if who == 'NOVA' else '#1e7a4c'
                c.set_font_face(CAP_FACE); c.set_font_size(66)
                words = txt.split(); sp = c.text_extents('  ').x_advance*0.75
                wid = sum(c.text_extents(w).x_advance for w in words) + sp*(len(words) - 1)
                fs = 66
                if wid > 980: fs = 66*980/wid; c.set_font_size(fs); sp *= 980/wid; wid = 980
                x = (W - wid)/2; y = 1790
                pop = 1 + 0.08*math.exp(-(t - a)*18)
                c.save(); c.translate(W/2, y - 20); c.scale(pop, pop); c.translate(-W/2, -(y - 20))
                c.new_path()
                for w in words:
                    c.move_to(x, y); c.text_path(w); x += c.text_extents(w).x_advance + sp
                c.set_source_rgb(*LINE); c.set_line_width(20); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill()
                c.set_font_size(32); e2 = c.text_extents(who); px = (W - wid)/2; py = y - 120; w2 = e2.x_advance + 40; r = 24
                c.new_path(); c.arc(px + r, py + r, r, math.pi/2, 3*math.pi/2); c.arc(px + w2 - r, py + r, r, -math.pi/2, math.pi/2); c.close_path()
                c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(6); c.stroke()
                c.move_to(px + 20, py + 36); c.set_source_rgb(1, 1, 1); c.show_text(who); c.new_path(); c.restore(); return
    # ----- shot builders: each returns (t0, draw(T, t)) and may register sfx
    def add(self, t0, fn, sfx='blip'):
        self.edl.append((t0, fn))
        if sfx: self.sfx.append((t0, sfx, 0.12))
        return self
    def hook(self, t0=0.0, portal_line=0, portal_f=0.8, nova=None, kiko=None, z0=1.12):
        """our world two-shot; Nova clicks, a portal opens near the end of `portal_line`, rush zoom + swirl wipe into the parallel world at the start of the next line."""
        po = self.at(portal_line, portal_f); self.wipe_t = self.S(portal_line + 1)
        self.sfx += [(po - 0.25, 'click', 0.22), (po, 'portal', 0.32), (self.wipe_t - 0.35, 'swoop', 0.2)]
        PX, PY = 540, 1080
        def f(T, t):
            u = t - t0; rush = clamp((t - (self.wipe_t - 0.6))/0.55)
            T.cx = 540 + (PX - 540)*ease(rush); T.cy = 960 + (PY - 960)*ease(rush)
            T.z = 1.0 + (z0 - 1.0)*(1 - ease(u/1.4)) + 0.03*u/4 + 2.2*ease(rush)**2
            self.world(T, t, False)
            portal(T, t, PX, PY, 200, back((t - po)/0.35, 1.0) if t > po else 0)
            P = pose('worried' if t > po else 'neutral', 'rest', look=(0.6, -0.1) if t < po else (0.9, -0.2)); P.update(kiko or {})
            if t > po: P['jit'] = jitter(t)
            self.kiko(T, t, **P)
            g = math.sin(tq(t)*2.2)
            P = pose('excited', 'present', armF=((-150 - 20*g, -120 + 30*g), 50)) if t < po - 0.6 else pose('excited', 'clicker', press=1.0 if po - 0.25 < t < po + 0.1 else 0.0)
            P.update(nova or {}); self.nova(T, t, **P)
        return self.add(t0, f, None)
    def arrive(self, t0=None, tag_text=None, hold=2.0):
        """both hop out of the portal into the parallel world, tag types in"""
        t0 = self.wipe_t if t0 is None else t0
        self.sfx += [(t0 + 0.5, 'boing', 0.14), (t0 + 0.35, 'pop', 0.2)]
        self.tag_text = tag_text; self.tag_t = t0 + 0.4
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 980 - 20*ease(u/2.0), 1.0 + 0.03*u
            self.world(T, t, True)
            portal(T, t, 540, 1080, 200, 1 - clamp((u - 1.2)/0.4))
            for who in ('kiko', 'nova'):
                a0 = 0.05 if who == 'nova' else 0.25; a1 = a0 + 0.45
                a = (540, 1080); b = (self.NOVA_X, FEET) if who == 'nova' else (self.KIKO_X, FEET)
                v = clamp((u - a0)/(a1 - a0))
                if u <= a0: continue
                x = a[0] + (b[0] - a[0])*v; y = a[1] + (b[1] - a[1])*v - math.sin(v*math.pi)*260
                P = dict(x=x, y=y, s=0.92*(0.4 + 0.6*v), sq=land_sq(u, a1))
                if who == 'nova': P.update(pose('excited', 'present' if v >= 1 else 'arms_up')); self.nova(T, t, **P)
                else: P.update(pose('shock' if v < 1 else 'worried', 'arms_up' if v < 1 else 'rest')); self.kiko(T, t, **P)
        return self.add(t0, f, None)
    def twoshot(self, t0, par=True, nova=None, kiko=None, push=0.02, z=1.0, extra=None):
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, z + push*u
            self.world(T, t, par)
            self.kiko(T, t, **(kiko or pose('neutral')))
            self.nova(T, t, **(nova or pose('neutral', 'present')))
            if extra: extra(T, t, u)
        return self.add(t0, f)
    def kcu(self, t0, par=True, emo='neutral', gest='rest', z=2.05, extra=None, **kw):
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = self.KIKO_X + 30, 1090, z + 0.05*u
            self.world(T, t, par)
            P = pose(emo, gest, **kw)
            if emo in ('worried', 'shock'): P.setdefault('jit', jitter(t, 6)); P.setdefault('tremble', (math.sin(int(t*12)*78.2) % 1 - 0.5)*5)
            self.kiko(T, t, **P)
            if extra: extra(T, t, u)
        return self.add(t0, f)
    def ncu(self, t0, par=True, emo='neutral', gest='rest', z=2.0, extra=None, **kw):
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = self.NOVA_X - 30, 1110, z + 0.04*u
            self.world(T, t, par)
            self.nova(T, t, **pose(emo, gest, **kw))
            if extra: extra(T, t, u)
        return self.add(t0, f)
    def stat(self, t0, big, label_txt='', sub='', col='#ffd43b', count=None, icon=None, bg=('#2a1f4a', '#3a2e63')):
        """insert board: a huge number/word (optionally counting up), a label and a sub line. count=(from, to, fmt)"""
        self.sfx += [(t0 + 0.05, 'pop', 0.2), (t0 + 0.9, 'chime', 0.2)]
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u; board(T, t, *bg); c = T.c
            if icon: icon(T, t, u)
            txt = big
            if count:
                v = count[0] + (count[1] - count[0])*ease((u - 0.2)/1.0); txt = count[2].format(v)
            label(c, txt, 540, 760, 260 if len(txt) <= 5 else 1300/len(txt), col, -0.04, back((u - 0.1)/0.35, 1.6))
            if label_txt: label(c, label_txt, 540, 1010, 90 if len(label_txt) < 14 else 1200/len(label_txt), '#ffffff', 0.02, back((u - 0.5)/0.3, 1.5))
            if sub: label(c, sub, 540, 1140, 50, '#c9b8ff', 0, back((u - 0.9)/0.3, 1.4), FONT, 10)
        return self.add(t0, f, None)
    def compare(self, t0, left, right, lval, rval, lcol='#7fd0ff', rcol='#ff4fa3', title=None, unit=''):
        """two bars: our world vs the parallel world"""
        self.sfx += [(t0 + 0.05, 'pop', 0.2), (t0 + 1.2, 'chime', 0.2)]
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, 1.0; board(T, t); c = T.c
            mx = max(lval, rval) or 1
            for i, (name, v, col) in enumerate(((left, lval, lcol), (right, rval, rcol))):
                k = ease((u - 0.3 - i*0.5)/0.8); x = 300 + i*480; h = 820*v/mx*k
                T.shape(rect(x - 130, 1350 - h, 260, max(h, 2)), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=8)
                label(c, name, x, 1440, 54, '#ffffff', 0, 1, FONT, 10)
                if k > 0.05: label(c, f'{v*k:g}{unit}' if isinstance(v, int) else f'{v*k:.1f}{unit}', x, 1350 - h - 70, 80, col, 0, 1)
            if title: label(c, title, 540, 330, 90 if len(title) < 16 else 1400/len(title), '#ffffff', -0.02, back(u/0.3, 1.4))
        return self.add(t0, f, None)
    def words(self, t0, items, par=True, over='board', times=None):
        """kinetic words popping in (e.g. ['BEST.', 'OCEAN.', 'EVER!']); over='board' or 'world'"""
        times = times or [t0 + 0.1 + i*0.45 for i in range(len(items))]
        for tt in times: self.sfx.append((tt, 'pop', 0.2))
        cols = ('#ffd43b', '#4fd8ff', '#ff4fa3', '#7dff9a')
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
            if over == 'board': board(T, t)
            else: self.world(T, t, par)
            for i, (w, tt) in enumerate(zip(items, times)):
                kin(T.c, t, w, tt, 540, 520 + i*220, 170 if len(w) < 8 else 1100/len(w), cols[i % 4], (-0.05, 0.04, -0.03, 0.05)[i % 4])
        return self.add(t0, f, None)
    def custom(self, t0, fn, sfx='blip'):
        """fn(K, T, t, u): draw anything (use K.world, K.nova, K.kiko, props, label...)"""
        return self.add(t0, lambda T, t: fn(self, T, t, t - t0), sfx)
    def end(self, t0, poll=('OPTION A', 'OPTION B'), par=True, nova=None, kiko=None):
        self.sfx += [(t0 + 1.0, 'pop', 0.22), (t0 + 1.6, 'pop', 0.22)]
        self.end_t = t0
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 560, 1060 - 30*ease(u/3), 0.92 + 0.03*u
            self.world(T, t, par)
            portal(T, t, 830, 640, 110, back(u/0.4, 1.0))
            self.kiko(T, t, **(kiko or pose('happy', 'rest')))
            self.nova(T, t, **(nova or pose('excited', 'present', look=(0, 0.1))))
            poll_chip(T.c, 540, 440, poll[0], '#ff4fa3', back((u - 1.0)/0.3, 1.6))
            poll_chip(T.c, 540, 600, poll[1], '#3a8fd8', back((u - 1.6)/0.3, 1.6))
        return self.add(t0, f, None)

    # ----- non-"what if" formats (why / myth-or-true / versus / mind hacks)
    def cold_open(self, t0, question, par=False, nova=None, kiko=None, z0=1.15, q_col='#ffd43b'):
        """no portal: both in our world, the big question pops on screen at once (for WHY / IS IT TRUE / VS videos)"""
        self.sfx += [(t0 + 0.15, 'pop', 0.22)]
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 980, z0 - 0.1*ease(u/2.5)
            self.world(T, t, par)
            self.kiko(T, t, **(kiko or pose('confused', 'shrug')))
            self.nova(T, t, **(nova or pose('excited', 'finger_up')))
            words = question.split(); half = (len(words) + 1)//2
            for i, line in enumerate((' '.join(words[:half]), ' '.join(words[half:]))):
                if line: label(T.c, line, 540, 330 + i*150, 120 if len(line) < 12 else 1300/len(line), '#ffffff' if i == 0 else q_col, (-0.04, 0.03)[i], back((u - 0.1 - i*0.15)/0.3, 1.6))
        return self.add(t0, f, None)
    def verdict(self, t0, word='MYTH!', col='#ff2d55', sub='', over='board', par=False):
        """big rubber-stamp verdict: MYTH! / TRUE! / BOTH WRONG! / IT DEPENDS"""
        self.sfx += [(t0 + 0.12, 'pop2', 0.26), (t0 + 0.2, 'nope' if col == '#ff2d55' else 'chime', 0.2)]
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
            if over == 'board': board(T, t)
            else: self.world(T, t, par)
            c = T.c; k = 1 + 1.6*(1 - ease(u/0.18)) if u < 0.18 else 1 + 0.04*math.exp(-(u - 0.18)*10)*math.sin((u - 0.18)*40)
            c.save(); c.translate(540, 820); c.rotate(-0.12); c.scale(k, k)
            c.select_font_face('Luckiest Guy'); fs = 230 if len(word) <= 6 else 1500/len(word); c.set_font_size(fs)
            e = c.text_extents(word); pad = 40
            c.rectangle(-e.x_advance/2 - pad, -fs*0.75 - pad, e.x_advance + 2*pad, fs*0.85 + 2*pad)
            c.set_source_rgba(*hexc(col)); c.set_line_width(22); c.stroke()
            c.move_to(-e.x_advance/2, 0); c.text_path(word); c.set_source_rgb(*LINE); c.set_line_width(fs*0.12); c.stroke_preserve(); c.set_source_rgba(*hexc(col)); c.fill()
            c.restore()
            if sub: label(c, sub, 540, 1120, 56 if len(sub) < 26 else 1400/len(sub), '#ffffff', 0, back((u - 0.5)/0.3, 1.4), FONT, 10)
        return self.add(t0, f, None)
    def versus(self, t0, left, right, lcol='#4fd8ff', rcol='#ff4fa3', title='VS', draw_left=None, draw_right=None):
        """split screen A vs B (two hero objects drawn by callbacks fn(T, t, x, y))"""
        self.sfx += [(t0 + 0.1, 'swoop', 0.16), (t0 + 0.5, 'pop', 0.2)]
        def f(T, t):
            u = t - t0; T.cx, T.cy, T.z = 540, 960, 1.0
            T.flat(rect(-500, -500, 1040, 3000), mixc(lcol, '#1b1422', 0.55)); T.flat(rect(540, -500, 1100, 3000), mixc(rcol, '#1b1422', 0.55))
            sl = ease(u/0.35)
            if draw_left: draw_left(T, t, 270 - 400*(1 - sl), 1000)
            if draw_right: draw_right(T, t, 810 + 400*(1 - sl), 1000)
            label(T.c, left, 270, 560, 80 if len(left) < 9 else 700/len(left), lcol, -0.04, back((u - 0.2)/0.3, 1.5))
            label(T.c, right, 810, 560, 80 if len(right) < 9 else 700/len(right), rcol, 0.04, back((u - 0.35)/0.3, 1.5))
            label(T.c, title, 540, 960, 150, '#ffffff', 0, back((u - 0.5)/0.3, 2.0))
        return self.add(t0, f, None)
    # ----- render
    def finalize(self):
        self.edl.sort(key=lambda e: e[0])
    def render(self, t, clean=False):
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
        i = 0
        for k, (t0, f) in enumerate(self.edl):
            if t >= t0: i = k
        T = Toon(c, t); self.edl[i][1](T, t)
        if not clean:
            if getattr(self, 'tag_text', None) and self.wipe_t and self.wipe_t <= t < self.wipe_t + 6 and self.edl[i][0] <= self.wipe_t + 3:
                tag(c, t, self.tag_text, self.tag_t)
            self.caption(c, t)
            swirl(c, W/2, 70, 34, 0.95, t)
            if i > 0 and abs(self.edl[i][0] - (self.wipe_t or -9)) > 0.05: flash(c, t, self.edl[i][0], 0.08, 0.22)
            if self.wipe_t: swirl_wipe(c, t, self.wipe_t)
            if t > self.TOTAL - 0.35: c.set_source_rgba(0, 0, 0, clamp((t - (self.TOTAL - 0.35))/0.35)); c.paint()
        return surf
