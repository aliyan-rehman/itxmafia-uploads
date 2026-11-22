"""Swirlverse LONG kit (1920x1080). Episode files: see episodes/_template_long.py. Built by build_long.py. (16:9, sitcom-toon look, Kokoro voices)"""
import math, json, sys, os, re, subprocess, cairo, numpy as np
from multiprocessing import Pool
import toonline
from toonline import Toon, hexc, mixc, ellipse_pts, rect, star, LINE
import shortkit as _sk
toonline.W, toonline.H = 1920, 1080
from toonchars import draw_nova, draw_kiko, draw_baby, draw_adult, MOM, DAD, GRANDPA, walk_legs, land_sq, tq
from shortkit import swirl
W, H = 1920, 1080
FPS = 24

LONG_DIR = os.environ.get('SV_LONG_DIR', '/tmp/swirl/long')
TL = json.load(open(os.path.join(LONG_DIR, 'timeline.json')))
TOTAL = TL['total']; LINES = TL['lines']
def S(i): return LINES[i]['s']
def E(i): return LINES[i]['e']
def at(i, f): return S(i) + (E(i) - S(i))*f
def L(i): return S(i) - 0.12
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(u): u = clamp(u); return u*u*(3 - 2*u)
def back(u, k=1.3):
    u = clamp(u); return 1 + (k + 1)*(u - 1)**3 + k*(u - 1)**2
def lip(who, t):
    for l in LINES:
        if l['who'] == who and l['s'] <= t <= l['e']:
            i = int((tq(t) - l['s'])*24); return l['lip'][min(max(i, 0), len(l['lip']) - 1)]
    return 0.0
def blinkf(t, period, off=0.0): return ((t + off) % period) > period - 0.12
def jitter(t, a=5): return (math.sin(int(t*12)*12.9898)*43758.5 % 1 - 0.5)*a
def nova_talk(t, extra=None):
    o = lip('NOVA', t); P = dict(t=t, o=o*0.95, nod=o*7, blink=blinkf(t, 3.4), sm=0.45)
    if extra: P.update(extra)
    return P
def kiko_talk(t, extra=None):
    o = lip('KIKO', t); P = dict(t=t, o=o*1.1, nod=o*7, blink=blinkf(t, 2.9, 1.1))
    if extra: P.update(extra)
    return P

CHAPTERS = {}   # set by the episode: longkit.CHAPTERS.update({1: 'Title', ...})
CH_START = {}
for l in LINES: CH_START.setdefault(l['ch'], l['s'] - 0.3 if l['ch'] > 1 else 0.0)

# ---------------------------------------------------------------- sets
OUR_SKY = [mixc('#2f7fe0', '#bfe4ff', k/5) for k in range(6)]
PAR_SKY = [mixc('#3b1f8c', '#ff9fd1', k/5) for k in range(6)]
FLOOR = 840

def room(T, t, par=False, fridge=True, cam_extra=None):
    wall = '#fff0d6' if not par else '#efe0ff'; wall2 = '#ffe2b8' if not par else '#ddc8ff'
    T.flat(rect(-1500, -1500, 5000, FLOOR + 1500), wall)
    for i in range(-12, 40):   # wallpaper stripes
        T.flat(rect(i*90, -1500, 38, FLOOR + 1500), wall2)
    # window with the sky (our / parallel)
    wx, wy, ww, wh = 260, 140, 520, 360
    T.shape(rect(wx - 22, wy - 22, ww + 44, wh + 44), '#ffffff', lw=8)
    sky = PAR_SKY if par else OUR_SKY
    for i, col in enumerate(sky):
        T.shape(rect(wx, wy + i*wh/6, ww, wh/6 + 1), col, line=False, amp=0)
    if par:
        T.shape(ellipse_pts(wx + 380, wy + 110, 60, 60), '#fff2c8', shadow='#e7c98f', shade_dir=(1, 0.5), shade_w=0.25, lw=6)
        T.shape(ellipse_pts(wx + 250, wy + 70, 26, 26), '#c9f3ff', lw=5)
        bob = 5*math.sin(t*1.3)
        T.shape([(wx + 60, wy + 240 + bob), (wx + 170, wy + 232 + bob), (wx + 150, wy + 270 + bob), (wx + 110, wy + 300 + bob)], '#7a4a8a', lw=6)
    else:
        T.shape(ellipse_pts(wx + 400, wy + 100, 56, 56), '#ffe066', shadow='#ffc93c', shade_dir=(1, 0.5), shade_w=0.2, lw=6)
        for (cx, cy, s) in ((wx + 150, wy + 120, 0.8), (wx + 300, wy + 240, 0.6)):
            T.shape([(cx - 110*s, cy + 30*s), (cx - 80*s, cy - 20*s), (cx - 20*s, cy - 50*s), (cx + 50*s, cy - 30*s), (cx + 110*s, cy + 30*s)], '#ffffff', lw=6)
    T.stroke([(wx + ww/2, wy), (wx + ww/2, wy + wh)], lw=12, col='#ffffff'); T.stroke([(wx, wy + wh/2), (wx + ww, wy + wh/2)], lw=12, col='#ffffff')
    T.shape(rect(wx - 40, wy + wh + 18, ww + 80, 26), '#ffffff', lw=7)
    # picture frame + lamp
    T.shape(rect(980, 200, 200, 150), '#c98a4a', lw=7); T.shape(rect(1000, 220, 160, 110), '#9fe3d9', lw=5)
    T.shape([(1010, 320), (1060, 260), (1100, 300), (1130, 270), (1150, 320)], '#47c2a0', lw=5)
    # floor + skirting
    T.shape(rect(-1500, FLOOR, 5000, 1200), '#c98a5a' if not par else '#b07acb', lw=8)
    for i in range(-10, 30):
        T.stroke([(i*160, FLOOR + 10), (i*160 - 120, FLOOR + 300)], lw=5, col='#b5764a' if not par else '#9a64b5')
    T.shape(rect(-1500, FLOOR - 24, 5000, 26), '#ffffff', lw=6)
    # sofa
    T.shape([(-120, FLOOR - 10), (-120, FLOOR - 250), (180, FLOOR - 250), (180, FLOOR - 10)], '#4d7ff0', shadow='#3a63c7', shade_dir=(1, 0), shade_w=0.2, lw=8)
    T.shape([(-160, FLOOR - 10), (-160, FLOOR - 150), (220, FLOOR - 150), (220, FLOOR - 10)], '#5b8cff', lw=8)
    if fridge:   # fridge on the right with the cake photo magnet
        fx = 1500
        T.shape(rect(fx, FLOOR - 640, 300, 640), '#e8f4ff', shadow='#c7d8ea', shade_dir=(1, 0), shade_w=0.25, lw=8)
        T.stroke([(fx, FLOOR - 400), (fx + 300, FLOOR - 400)], lw=7)
        T.shape(rect(fx + 250, FLOOR - 560, 18, 120), '#9aa8b8', lw=5); T.shape(rect(fx + 250, FLOOR - 340, 18, 150), '#9aa8b8', lw=5)
        photo(T, fx + 70, FLOOR - 590, 150, -0.06)

def photo(T, x, y, w, rot=0.0):
    """the 'blue cake' photo: baby Kiko + blue cake, polaroid style"""
    h = w*1.15
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    cx, cy = x + w/2, y + h/2
    R = lambda p: (cx + (p[0] - cx)*math.cos(rot) - (p[1] - cy)*math.sin(rot), cy + (p[0] - cx)*math.sin(rot) + (p[1] - cy)*math.cos(rot))
    T.shape([R(p) for p in pts], '#ffffff', lw=6)
    T.shape([R(p) for p in [(x + w*0.08, y + w*0.08), (x + w*0.92, y + w*0.08), (x + w*0.92, y + w*0.85), (x + w*0.08, y + w*0.85)]], '#ffe9b8', lw=4)
    T.shape([R(p) for p in [(x + w*0.25, y + w*0.6), (x + w*0.75, y + w*0.6), (x + w*0.72, y + w*0.8), (x + w*0.28, y + w*0.8)]], '#4fa8ff', lw=4)
    T.shape([R(p) for p in ellipse_pts(x + w*0.5, y + w*0.38, w*0.17, w*0.16, 16)], '#f7f5ef', lw=4)
    T.shape([R(p) for p in ellipse_pts(x + w*0.5, y + w*0.27, w*0.16, w*0.07, 12, math.pi, 2*math.pi)], '#1e7a4c', lw=4)
    X, Y = R((x + w*0.5, y - 6)); T.shape(ellipse_pts(X, Y, 16, 16, 12), '#ff4fa3', lw=5)

def board(T, t, col='#2a1f4a', grid='#3a2e63'):
    T.flat(rect(-2000, -2000, 6000, 5000), col)
    for k in range(-12, 30):
        T.flat(rect(-2000, 120*k + (tq(t)*24 % 120), 6000, 3), grid)
        T.flat(rect(120*k, -2000, 3, 5000), grid)

def cake(T, x, y, s=1.0, sneeze=0.0, t=0.0):
    T.shape([(x - 120*s, y), (x - 120*s, y - 110*s), (x + 120*s, y - 110*s), (x + 120*s, y)], '#4fa8ff', shadow='#2f86e0', shade_dir=(1, 0), shade_w=0.25, lw=7)
    T.shape([(x - 128*s, y - 100*s)] + [(x - 128*s + 256*s*i/10, y - 100*s + (14*s if i % 2 else 0)) for i in range(11)] + [(x + 128*s, y - 130*s), (x - 128*s, y - 130*s)], '#ffffff', lw=7)
    T.shape(rect(x - 8*s, y - 190*s, 16*s, 62*s), '#ff4fa3', lw=6)
    if sneeze < 0.5:
        T.shape([(x, y - 236*s), (x + 14*s, y - 205*s), (x, y - 192*s), (x - 14*s, y - 205*s)], '#ffd43b', lw=5)
    for i in range(int(sneeze*14)):   # frosting/sneeze specks
        a = -math.pi*(0.1 + i*0.06); r = (60 + 260*sneeze)*s
        T.shape(ellipse_pts(x + r*math.cos(a + i), y - 150*s + r*0.6*math.sin(a), 10*s, 8*s, 10), '#bfe9ff' if i % 2 else '#ffffff', lw=4)

def highchair(T, x, y, s=1.0):
    for sx in (-1, 1):
        T.stroke([(x + sx*90*s, y), (x + sx*60*s, y - 300*s)], lw=10, col='#ffcf8a'); T.stroke([(x + sx*90*s, y), (x + sx*60*s, y - 300*s)], lw=3)
    T.shape(rect(x - 150*s, y - 330*s, 300*s, 36*s), '#ffcf8a', lw=7)

def crib_bars(T, x0, x1, y0, y1, n=7):
    T.shape(rect(x0, y0 - 30, x1 - x0, 40), '#ffffff', lw=7)
    for i in range(n + 1):
        x = x0 + (x1 - x0)*i/n; T.shape(rect(x - 14, y0, 28, y1 - y0), '#ffffff', lw=6)

def mouse(T, x, y, s=1.0, t=0.0, glow=0.0):
    b = 4*math.sin(tq(t)*6)
    T.shape(ellipse_pts(x, y + b, 150*s, 95*s, 40), '#c9c3d9', shadow='#a7a0bd', shade_dir=(1, 0.3), shade_w=0.25, lw=8)
    T.stroke([(x - 150*s, y + 40*s), (x - 260*s, y + 10*s + 10*math.sin(tq(t)*5)), (x - 320*s, y + 60*s)], lw=8, col='#ff9fb8')
    T.shape(ellipse_pts(x + 150*s, y - 40*s + b, 95*s, 80*s, 36), '#d6d0e6', lw=8)
    for ex, ey in ((60, -130), (170, -125)):
        T.shape(ellipse_pts(x + ex*s, y + ey*s + b, 55*s, 55*s, 24), '#d6d0e6', lw=7); T.shape(ellipse_pts(x + ex*s, y + ey*s + b, 32*s, 32*s, 18), '#ffb3c8', lw=5)
    T.shape(ellipse_pts(x + 170*s, y - 50*s + b, 18*s, 20*s, 12), '#ffffff', lw=5); T.dot(x + 175*s, y - 48*s + b, 7*s)
    T.shape(ellipse_pts(x + 245*s, y - 20*s + b, 14*s, 12*s, 10), '#ff6f9a', lw=5)
    if glow > 0:   # glowing memory in the head
        T.glow(x + 120*s, y - 70*s + b, 55*s*glow, '#ffe066', ((2.0, 0.18), (1.4, 0.3)))
        T.shape(star(x + 120*s, y - 70*s + b, 40*s*glow, 16*s*glow, 5, t), '#ffe066', lw=5)

def brain(T, x, y, s=1.0, hippo=0.0, t=0.0, col='#ffb3c8', shade='#f08fae'):
    """side view of a brain (flat, bumpy), with an optional glowing hippocampus (seahorse curl)"""
    pts = []
    for i in range(48):
        a = 2*math.pi*i/48; r = 1 + 0.06*math.sin(9*a)
        pts.append((x + 300*s*r*math.cos(a), y + 200*s*r*math.sin(a)*(1 if math.sin(a) < 0 else 0.85)))
    T.shape(pts, col, shadow=shade, shade_dir=(1, 0.4), shade_w=0.2, lw=8)
    for k in range(5):   # folds
        cx = x - 220*s + k*110*s
        T.stroke([(cx, y - 120*s), (cx + 30*s, y - 60*s), (cx - 10*s, y), (cx + 30*s, y + 60*s)], lw=6, col=shade)
    T.shape([(x + 80*s, y + 130*s), (x + 140*s, y + 160*s), (x + 120*s, y + 260*s), (x + 80*s, y + 250*s)], col, lw=7)   # brain stem
    if hippo > 0:
        hx, hy = x + 20*s, y + 70*s
        T.glow(hx, hy, 70*s, '#ffe066', ((1.8, 0.15*hippo), (1.3, 0.3*hippo)))
        sea = [(hx - 70*s, hy - 30*s), (hx - 20*s, hy - 50*s), (hx + 40*s, hy - 30*s), (hx + 60*s, hy + 10*s), (hx + 30*s, hy + 40*s), (hx, hy + 20*s), (hx + 20*s, hy), (hx - 10*s, hy - 15*s), (hx - 60*s, hy - 5*s)]
        T.shape(sea, mixc('#ffcf6b', '#ffe066', hippo), lw=6)

def mri(T, x, y, s=1.0, t=0.0, baby_p=None):
    T.shape(ellipse_pts(x, y - 280*s, 300*s, 300*s, 50), '#eef2f7', shadow='#c9d2de', shade_dir=(1, 0.3), shade_w=0.18, lw=9)
    T.shape(ellipse_pts(x, y - 280*s, 150*s, 150*s, 40), '#3a3f6b', lw=8)
    for k in range(3):   # psychedelic patterns inside (the real study kept babies engaged with patterns)
        T.shape(ellipse_pts(x, y - 280*s, (130 - k*40)*s, (130 - k*40)*s, 30), ('#ff4fa3', '#4fd8ff', '#ffd84d')[(k + int(t*3)) % 3], line=False)
    T.shape(rect(x - 60*s, y - 170*s, 620*s, 70*s), '#ffffff', lw=8)
    T.shape(rect(x + 420*s, y - 100*s, 60*s, 100*s), '#c9d2de', lw=7)

def memory_bubble(T, x, y, r, k, t, inner=None):
    """dream-like memory bubble (cloud outline) that grows with k; inner(T) draws inside (clipped)"""
    if k <= 0.01: return
    pts = []
    for i in range(60):
        a = 2*math.pi*i/60; rr = r*k*(1 + 0.06*abs(math.sin(4*a + t)))
        pts.append((x + rr*1.25*math.cos(a), y + rr*0.9*math.sin(a)))
    T.shape(pts, '#fff6e8', lw=9)
    if inner:
        c = T.c; c.save(); T._path(T.X(pts)); c.clip(); inner(T); c.restore()
        T.shape(pts, None, lw=9)
    for j, (dx, dy, rr) in enumerate(((-r*1.1, r*0.95, 26), (-r*1.35, r*1.2, 16))):
        T.shape(ellipse_pts(x + dx*k, y + dy*k, rr*k, rr*k, 14), '#fff6e8', lw=6)

# ---------------------------------------------------------------- screen overlays
FONT = 'Fredoka Light'
CAP_FACE = cairo.ToyFontFace('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
def cap_lines():
    out = []
    for l in LINES:
        txt = l.get('cap', l['text'])
        parts = [p.strip() for p in re.split(r'(?<=[.?!,])\s+', txt) if p.strip()]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) + len(p) < 40 and not merged[-1].endswith(('.', '?', '!')): merged[-1] += ' ' + p
            else: merged.append(p)
        fin = []
        for p in merged:
            while len(p) > 52:
                w = p.split(); half = len(w)//2; fin.append(' '.join(w[:half])); p = ' '.join(w[half:])
            fin.append(p)
        tot = sum(len(p) for p in fin); t0 = l['s']
        for p in fin:
            d = (l['e'] - l['s'])*len(p)/tot; out.append((t0, t0 + d + 0.12, p, l['who'])); t0 += d
    return out
CAPS = cap_lines()

def caption(c, t):
    for (a, b, txt, who) in CAPS:
        if a <= t < b:
            col = '#3a3f8f' if who == 'NOVA' else '#1e7a4c'
            c.set_font_face(CAP_FACE); c.set_font_size(54)
            words = txt.split(); sp = c.text_extents('  ').x_advance*0.75
            wid = sum(c.text_extents(w).x_advance for w in words) + sp*(len(words) - 1)
            if wid > 1600:
                c.set_font_size(54*1600/wid); sp = c.text_extents('  ').x_advance*0.75
                wid = sum(c.text_extents(w).x_advance for w in words) + sp*(len(words) - 1)
            c.set_font_size(32); e2 = c.text_extents(who); pw = e2.x_advance + 40
            c.set_font_size(54 if wid <= 1600 else 54*1600/wid)
            x0 = (W - wid - pw - 24)/2; y = 1020
            # pill to the left of the line
            r = 24; px, py = x0, y - 42
            c.new_path(); c.arc(px + r, py + r, r, math.pi/2, 3*math.pi/2); c.arc(px + pw - r, py + r, r, -math.pi/2, math.pi/2); c.close_path()
            c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(6); c.stroke()
            fs = c.get_font_matrix().xx
            c.set_font_size(32); c.move_to(px + 20, py + 35); c.set_source_rgb(1, 1, 1); c.show_text(who); c.new_path()
            c.set_font_face(CAP_FACE); c.set_font_size(fs); x = x0 + pw + 24
            for w in words:
                c.move_to(x, y); c.text_path(w); x += c.text_extents(w).x_advance + sp
            c.set_source_rgb(*LINE); c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
            c.set_source_rgb(1, 1, 1); c.fill(); return

def label(c, txt, x, y, size, col='#ffffff', rot=0.0, k=1.0, font='Luckiest Guy', lw=None):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL if font == 'Luckiest Guy' else cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    e = c.text_extents(txt); c.move_to(-e.x_advance/2, e.height/2 if font == 'Luckiest Guy' else size*0.35); c.text_path(txt)
    c.set_source_rgb(*LINE); c.set_line_width(lw or size*0.2); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*hexc(col)); c.fill(); c.restore()

def kin(c, t, txt, t0, x, y, size, col='#ffd43b', rot=0.0):
    if t >= t0: label(c, txt, x, y, size, col, rot, back((t - t0)/0.25, 2.0))

def tag(c, t, text, t0, col='#4fd8ff', y=78):
    n = int(clamp((t - t0)/0.9)*len(text))
    if n <= 0: return
    s = text[:n] + ('_' if (t*4) % 1 < 0.5 and n < len(text) else '')
    c.select_font_face('DejaVu Sans Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(32)
    w = c.text_extents(text).x_advance
    c.set_source_rgba(0.06, 0.04, 0.12, 0.8); c.rectangle(40, y - 40, w + 44, 56); c.fill()
    c.move_to(62, y); c.set_source_rgba(*hexc(col)); c.show_text(s)

def chapter_card(c, t):
    for ch, t0 in CH_START.items():
        if ch == 1: continue
        u = t - t0
        if 0 <= u < 2.6:
            k = back(u/0.3, 1.4) if u < 2.2 else 1 - ease((u - 2.2)/0.4)
            txt = CHAPTERS[ch]
            c.save(); c.translate(W - 60, 70); c.scale(k, k)
            c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(40)
            w = c.text_extents(txt).x_advance + 150; r = 34
            c.new_path(); c.arc(-w + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(-r, 0, r, -math.pi/2, math.pi/2); c.close_path()
            c.set_source_rgba(*hexc('#ffd43b')); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(6); c.stroke()
            c.arc(-w + 40, 0, 26, 0, 2*math.pi); c.set_source_rgba(*hexc('#ff4fa3')); c.fill_preserve(); c.set_source_rgb(*LINE); c.stroke()
            c.select_font_face('Luckiest Guy'); c.set_font_size(32); e = c.text_extents(str(ch)); c.move_to(-w + 40 - e.x_advance/2, 12); c.set_source_rgb(1, 1, 1); c.show_text(str(ch))
            c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(40)
            c.move_to(-w + 84, 14); c.set_source_rgb(*LINE); c.show_text(txt)
            c.restore()

def brand(c, t):
    c.new_path(); swirl(c, W/2, 52, 30, 0.95, t)

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
        c.set_source_rgba(*hexc(col)); c.set_line_width(80); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.arc(0, 0, 80, 0, 2*math.pi); c.set_source_rgb(1, 0.97, 0.88); c.fill(); c.restore()

def memory_look(c, k=1.0):
    """warm, soft 'memory' grade: cream tint + vignette"""
    if k <= 0: return
    c.set_source_rgba(1.0, 0.86, 0.62, 0.22*k); c.paint()
    g = cairo.RadialGradient(W/2, H/2, H*0.35, W/2, H/2, H*0.95)
    g.add_color_stop_rgba(0, 1, 0.95, 0.85, 0); g.add_color_stop_rgba(1, 1, 0.95, 0.85, 0.85*k)
    c.set_source(g); c.paint()

def flash(c, t, t0, d=0.12, a=0.4):
    if t0 <= t < t0 + d: c.set_source_rgba(1, 1, 1, a*(1 - (t - t0)/d)); c.paint()

def saved_badge(c, t, t0, txt='MEMORY SAVED', x=W - 260, y=200):
    if t < t0 or t > t0 + 2.2: return
    k = back((t - t0)/0.25, 1.8) if t < t0 + 1.9 else 1 - ease((t - t0 - 1.9)/0.3)
    c.save(); c.translate(x, y); c.scale(k, k)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(36)
    w = c.text_extents(txt).x_advance + 110; r = 32
    c.new_path(); c.arc(-w/2 + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(w/2 - r, 0, r, -math.pi/2, math.pi/2); c.close_path()
    c.set_source_rgba(*hexc('#7dff9a')); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(6); c.stroke()
    c.set_line_width(7); c.move_to(-w/2 + 30, 0); c.line_to(-w/2 + 42, 12); c.line_to(-w/2 + 62, -12); c.stroke()
    c.move_to(-w/2 + 80, 13); c.show_text(txt); c.restore()

EDL = []; WIPE_T = None; MEMORY_T = set()
def set_edl(edl, wipe_t=None, memory_t=()):
    global EDL, WIPE_T, MEMORY_T
    EDL[:] = sorted(edl, key=lambda e: e[0]); WIPE_T = wipe_t; MEMORY_T = set(memory_t)

def shot_index(t):
    i = 0
    for k, (t0, f) in enumerate(EDL):
        if t >= t0: i = k
    return i

def render(t, clean=False):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
    i = shot_index(t)
    T = Toon(c, t)
    EDL[i][1](T, t)
    if not clean:
        if EDL[i][0] in MEMORY_T: memory_look(c, 1.0)
        caption(c, t); chapter_card(c, t); brand(c, t)
        if i > 0 and t - EDL[i][0] < 0.1 and EDL[i][0] != WIPE_T: flash(c, t, EDL[i][0], 0.08, 0.18)
        if WIPE_T: swirl_wipe(c, t, WIPE_T)
        if t > TOTAL - 0.4: c.set_source_rgba(0, 0, 0, clamp((t - (TOTAL - 0.4))/0.4)); c.paint()
    return surf


# ---------------------------------------------------------------- generic shots & props (from LONG03)
def cam(T, cx, cy, z): T.cx, T.cy, T.z = cx, cy, z

def table_soup(T, t, x=960, y=FLOOR + 40, steam=True, soup='#9bd16a'):
    T.shape(rect(x - 260, y - 190, 520, 36), '#c98a4a', shadow='#a86e34', shade_dir=(0, 1), shade_w=0.3, lw=8)
    for sx in (-1, 1): T.shape(rect(x + sx*220 - 14, y - 154, 28, 154), '#a86e34', lw=6)
    bx, by = x, y - 190
    T.shape(ellipse_pts(bx, by - 40, 110, 70, 30, 0, math.pi) + [(bx - 110, by - 40)], '#ffffff', shadow='#d6d3e6', shade_dir=(1, 0), shade_w=0.25, lw=7)
    T.shape(ellipse_pts(bx, by - 40, 110, 24, 30), soup, lw=6)
    for k in range(3):
        T.shape(ellipse_pts(bx - 40 + k*40, by - 42 + (k % 2)*6, 12, 6, 10), mixc(soup, '#3a6b1f', 0.4), line=False)
    if steam:
        for k in range(3):
            x0 = bx - 50 + k*50; ph = tq(t)*4 + k
            T.stroke([(x0 + 14*math.sin(ph + j*0.9), by - 80 - j*28) for j in range(5)], lw=6, col='#ffffff', alpha=0.8)

def spoon(T, x, y, rot=0.0):
    c, s_ = math.cos(rot), math.sin(rot)
    P = lambda px, py: (x + px*c - py*s_, y + px*s_ + py*c)
    T.shape([P(-4, 0), P(4, 0), P(5, 90), P(-5, 90)], '#c9d2de', lw=5)
    T.shape([P(*p) for p in ellipse_pts(0, -26, 22, 30, 16)], '#c9d2de', lw=5)

def sh_kcu(T, t, t0, par=False, extra=None, z=1.9):
    u = t - t0
    cam(T, 1150, 470, z + 0.03*u); room(T, t, par)
    P = dict(x=1180, y=FLOOR + 150, s=0.95, face=-1, look=(-0.6, -0.1), brow=0.4, er=42)
    if extra: P.update(extra)
    draw_kiko(T, kiko_talk(t, P))

def sh_ncu(T, t, t0, par=False, extra=None, z=1.85):
    u = t - t0
    cam(T, 640, 450, z + 0.03*u); room(T, t, par)
    P = dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.3, 0.1), brow=0.5)
    if extra: P.update(extra)
    draw_nova(T, nova_talk(t, P))

def person_icon(T, x, y, s, col):
    T.shape(ellipse_pts(x, y - 34*s, 16*s, 16*s, 12), col, lw=4)
    T.shape([(x - 20*s, y + 20*s), (x - 16*s, y - 12*s), (x + 16*s, y - 12*s), (x + 20*s, y + 20*s)], col, lw=4)

def sh_portal(T, t, t0):
    u = t - t0
    cam(T, 760, 450, 1.3 + 0.1*u)
    room(T, t)
    draw_nova(T, nova_talk(t, dict(x=600, y=FLOOR + 140, s=0.95, face=1, look=(0.2, 0), armF=((-150, -40), 40), hold='clicker', press=1.0 if u > 0.15 else 0.0, brow=0.9)))

def street(T, t, par=True):
    sky = PAR_SKY if par else OUR_SKY
    for i, col in enumerate(sky):
        T.flat(rect(-1500, -1500 + (i > 0)*(1500 + i*120), 5000, (1500 + 120) if i == 0 else 122), col)
    T.flat(rect(-1500, 720, 5000, 200), sky[-1])
    if par:
        T.shape(ellipse_pts(1650, 170, 70, 70), '#fff2c8', shadow='#e7c98f', shade_dir=(1, 0.5), shade_w=0.25, lw=6)
        T.shape(ellipse_pts(1500, 110, 30, 30), '#c9f3ff', lw=5)
    for (x, w, h, col) in ((-60, 300, 480, '#7bdff2'), (280, 260, 380, '#ffd166'), (1300, 320, 520, '#f4a6c6'), (1660, 300, 420, '#9fe3d9')):
        T.shape(rect(x, FLOOR - h, w, h), col, lw=7)
        for wy in range(FLOOR - h + 50, FLOOR - 80, 110):
            for wx in (x + 40, x + w - 100): T.shape(rect(wx, wy, 60, 70), '#fff6d8', lw=5)
    T.shape(rect(-1500, FLOOR, 5000, 1200), '#8e8aa8', lw=8)
    T.shape(rect(-1500, FLOOR, 5000, 40), '#c9c3d9', lw=6)

def burger(T, x, y, s=1.0):
    T.shape(ellipse_pts(x, y - 60*s, 150*s, 80*s, 30, math.pi, 2*math.pi) + [(x + 150*s, y - 50*s), (x - 150*s, y - 50*s)], '#f2a541', lw=7)
    for k in range(5): T.dot(x - 80*s + k*40*s, y - 100*s + (k % 2)*12*s, 5*s, '#fff6d8')
    T.shape(rect(x - 160*s, y - 52*s, 320*s, 22*s), '#7ac74f', lw=5)
    T.shape(rect(x - 150*s, y - 30*s, 300*s, 36*s), '#7a3b2e', lw=6)
    T.shape(rect(x - 140*s, y + 6*s, 280*s, 40*s), '#f2a541', lw=6)

def office(T, t):
    T.flat(rect(-2000, -2000, 6000, 5000), '#dfe8f2')
    for i in range(-12, 30): T.flat(rect(i*200, -2000, 6, 5000), '#cdd9e6')
    T.shape(rect(1250, 160, 360, 240), '#ffffff', lw=7); T.stroke([(1290, 350), (1360, 280), (1420, 320), (1500, 220), (1570, 250)], lw=7, col='#3fbf9f')
    T.shape(rect(-2000, FLOOR, 6000, 1200), '#8a9bb5', lw=8)

def comfy_chair(T, x, y, s=1.0):
    T.shape([(x - 120*s, y), (x - 120*s, y - 300*s), (x + 120*s, y - 300*s), (x + 120*s, y)], '#ff6f9a', shadow='#e0507c', shade_dir=(1, 0), shade_w=0.2, lw=8)
    T.shape(rect(x - 150*s, y - 140*s, 300*s, 70*s), '#ff8fb8', lw=7)

def poll_chip(c, x, y, txt, col, k):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(52)
    w = c.text_extents(txt).x_advance + 90; r = 52
    c.new_path(); c.arc(-w/2 + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(w/2 - r, 0, r, -math.pi/2, math.pi/2); c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(8); c.stroke()
    c.move_to(-w/2 + 45, 18); c.text_path(txt); c.set_source_rgb(*LINE); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill(); c.restore()

def sh_twoshot(T, t, t0, par=False, kp=None, np_=None, extra_draw=None, z=1.0, prop=None):
    u = t - t0
    cam(T, 960, 560, z + 0.02*u)
    room(T, t, par)
    P1 = dict(x=600, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.5); P1.update(np_ or {})
    P2 = dict(x=1300, y=FLOOR + 150, s=0.95, face=-1, look=(-0.8, 0), brow=-0.3); P2.update(kp or {})
    draw_nova(T, nova_talk(t, P1)); draw_kiko(T, kiko_talk(t, P2))
    if prop: prop(T, t, u)
    if extra_draw: extra_draw(T, t, u)

def sh_par_room(T, t, t0, tag_text='WORLD #?'):
    u = t - t0
    cam(T, 960, 560, 1.05 - 0.02*u)
    room(T, t, par=True)
    draw_nova(T, nova_talk(t, dict(x=760, y=FLOOR + 140, s=0.95, face=1, look=(0.1, 0), armF=((-150, -100), 40), brow=0.9)))
    tag(T.c, t, tag_text, t0 + 0.6)

def sh_end(T, t, t0, poll=('OPTION A', 'OPTION B'), poll_t=(0.6, 1.4), prop=None):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.012*u)
    room(T, t, par=True)
    draw_nova(T, nova_talk(t, dict(x=600, y=FLOOR + 140, s=0.95, face=1, look=(0.1, 0.1), brow=0.8, armF=((-150, -80), 40))))
    draw_kiko(T, kiko_talk(t, dict(x=1300, y=FLOOR + 150, s=0.95, face=-1, look=(-0.8, 0), brow=0.7, sm=0.8)))
    if prop: prop(T, t, u)
    poll_chip(c, 560, 170, poll[0], '#ff4fa3', back((u - poll_t[0])/0.3, 1.6))
    poll_chip(c, 1360, 170, poll[1], '#3a8fd8', back((u - poll_t[1])/0.3, 1.6))
