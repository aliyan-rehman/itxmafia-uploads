"""LONG02 — What if you could remember being a baby? (16:9, sitcom-toon look, Kokoro voices)"""
import math, json, sys, os, re, subprocess, cairo, numpy as np
from multiprocessing import Pool
import toonline
toonline.W, toonline.H = 1920, 1080
from toonline import Toon, hexc, mixc, ellipse_pts, rect, star, LINE
from toonchars import draw_nova, draw_kiko, draw_baby, draw_adult, MOM, DAD, GRANDPA, walk_legs, land_sq, tq
from world import swirl
W, H = 1920, 1080
FPS = 24

TL = json.load(open('/home/claude/pw/long02/timeline.json'))
TOTAL = TL['total']; LINES = TL['lines']
def S(i): return LINES[i]['s']
def E(i): return LINES[i]['e']
def at(i, f): return S(i) + (E(i) - S(i))*f
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

CHAPTERS = {1: 'Kiko remembers?!', 2: 'Why we forget', 3: 'Babies DO make memories', 4: 'The parallel world', 5: 'The catch', 6: 'Why forgetting helps', 7: 'Your turn'}
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
        txt = l['text'].replace('twenty twenty-five', '2025').replace('six thousand', '6,000')
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

# ---------------------------------------------------------------- shots
def cam(T, cx, cy, z): T.cx, T.cy, T.z = cx, cy, z

def sh_hook(T, t):
    """Kiko bursts in, excited; Nova on the sofa side"""
    cam(T, 960, 560, 1.0 + 0.02*t)
    room(T, t)
    tr0, tr1 = 0.0, 1.1
    v = ease((t - tr0)/(tr1 - tr0)); running = t < tr1
    lL, lR, bob = walk_legs(t, running, 38, 22, 16)
    kx = 1950 + (1180 - 1950)*v
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.2 if t < 1.0 else 0.9, armF=((-30, 170), -18))))
    draw_kiko(T, kiko_talk(t, dict(x=kx, y=FLOOR + 150, s=0.95, face=-1, legL=lL, legR=lR, bob=bob, lean=0.1 if running else 0, sq=land_sq(t, tr1),
                                    look=(-0.8, -0.1), brow=0.9, sm=0.8, er=44, armF=((-120, -150), 30) if not running else ((40 + 40*math.sin(tq(t)*16), 150), -20),
                                    armB=((120, -150), -30) if not running else ((-40 - 40*math.sin(tq(t)*16), 150), 20))))

def sh_memory_birthday(T, t, t0, fake=False):
    """baby Kiko in a highchair with a blue cake, sneezing on it; inside a memory bubble"""
    u = t - t0
    cam(T, 960, 540, 1.0 + 0.02*u)
    T.flat(rect(-2000, -2000, 6000, 5000), '#ffe9c9')
    for i in range(-12, 30): T.flat(rect(i*120, -2000, 50, 5000), '#ffdcae')
    # party bunting
    for i in range(12):
        x = 100 + i*150; T.shape([(x, 90), (x + 120, 90), (x + 60, 180)], ('#ff4fa3', '#4fd8ff', '#ffd43b')[i % 3], lw=6)
    T.stroke([(40, 88), (1880, 88)], lw=6)
    highchair(T, 960, 1100, 1.1)
    sneeze_t = 1.2
    sn = clamp((u - sneeze_t)/0.4)
    pre = u > sneeze_t - 0.6 and u < sneeze_t
    draw_baby(T, dict(t=t, x=960, y=760, s=1.25, sq=1.0 - 0.06*math.sin(min(1, sn)*math.pi), closed=pre, o=0.8 if 0 < sn < 1 else 0.2, sm=0.8, brow=0.8 if pre else 0.3,
                      armF=((-60, -40), 20), armB=((60, -40), -20), legs=False, headtilt=-0.12 if pre else (0.1 if 0 < sn < 1 else 0)))
    cake(T, 960, 840, 1.2, sn, t)
    kin(T.c, t, 'ACHOO!', t0 + sneeze_t, 1400, 320, 110, '#ffffff', 0.12)

def sh_twoshot(T, t, t0, par=False, focus=None, kx=1180, nx=560, kp=None, np_=None, z0=1.0, push=0.02, fridge=True):
    u = t - t0
    if focus == 'nova': cam(T, nx + 120, 360, z0 + push*u)
    elif focus == 'kiko': cam(T, kx - 80, 380, z0 + push*u)
    else: cam(T, 960, 560, z0 + push*u)
    room(T, t, par, fridge)
    P1 = dict(x=nx, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.5); P1.update(np_ or {})
    P2 = dict(x=kx, y=FLOOR + 150, s=0.95, face=-1, look=(-0.8, 0), brow=-0.3); P2.update(kp or {})
    draw_nova(T, nova_talk(t, P1)); draw_kiko(T, kiko_talk(t, P2))

def sh_timeline(T, t, t0):
    """age 0 -> 7 years; most first memories start around age 3"""
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t)
    x0, x1, y = 260, 1660, 640
    k = ease(u/0.6)
    T.shape(rect(x0, y - 14, (x1 - x0)*k, 28), '#ffffff', lw=6)
    for a in range(8):
        x = x0 + (x1 - x0)*a/7
        if k >= a/7 - 1e-6:
            T.shape(ellipse_pts(x, y, 26, 26, 16), '#ffd43b' if a == 3 else '#ffffff', lw=6)
            label(c, f'{a}', x, y + 80, 46, '#ffffff')
    label(c, 'AGE (YEARS)', W/2, y + 160, 40, '#c9b8ff')
    # grey 'forgotten' zone 0..3 and the first-memory marker
    if u > 0.9:
        kz = ease((u - 0.9)/0.6)
        T.shape(rect(x0, y - 150, (x1 - x0)*3/7*kz, 110), '#6a5a8f', lw=6, alpha=0.9)
        if kz > 0.8: label(c, 'FORGOTTEN', x0 + (x1 - x0)*1.5/7, y - 95, 48, '#c9b8ff')
    mx = x0 + (x1 - x0)*3/7
    if u > 1.8:
        kk = back((u - 1.8)/0.3, 1.6)
        T.shape([(mx - 40, y - 260*kk), (mx + 40, y - 260*kk), (mx + 40, y - 190*kk), (mx + 12, y - 190*kk), (mx, y - 160*kk), (mx - 12, y - 190*kk), (mx - 40, y - 190*kk)], '#ff4fa3', lw=6)
        label(c, 'FIRST MEMORY: AGE 3', mx + 10, y - 320, 56, '#ff4fa3', -0.02, kk)
    kin(c, t, 'INFANTILE AMNESIA', S(5), W/2, 220, 120, '#ffd43b', -0.03)

def sh_superbaby(T, t, t0):
    u = t - t0
    cam(T, 1000, 440, 1.5); room(T, t)
    draw_kiko(T, kiko_talk(t, dict(x=1180, y=FLOOR + 150, s=0.95, face=-1, look=(-0.5, -0.6), brow=0.8, sm=0.6, closed=False)))
    # the 'baby superhero' he pictures flies across
    v = clamp((u - 0.4)/1.6)
    if 0 < v < 1:
        bx = 600 + 1000*v; by = 200 - 60*math.sin(v*math.pi)
        memory_bubble(T, 840, 240, 230, back((u - 0.2)/0.3, 1.2), t, lambda T: (T.flat(rect(0, -400, 3000, 1400), '#bfe4ff'),
                      draw_baby(T, dict(t=t, x=bx - 120, y=by + 150, s=0.75, rot=-1.2, cape=True, sm=0.9, brow=0.8, armF=((-90, -60), 10), armB=((60, 40), 10), look=(0.6, 0)))))
    elif u >= 0.2:
        memory_bubble(T, 840, 240, 230, back((u - 0.2)/0.3, 1.2) if v == 0 else 1 - ease((u - 2.0)/0.3), t, lambda T: T.flat(rect(0, -400, 3000, 1400), '#bfe4ff'))

def person_icon(T, x, y, s, col):
    T.shape(ellipse_pts(x, y - 34*s, 16*s, 16*s, 12), col, lw=4)
    T.shape([(x - 20*s, y + 20*s), (x - 16*s, y - 12*s), (x + 16*s, y - 12*s), (x + 20*s, y + 20*s)], col, lw=4)

def sh_study(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t)
    label(c, '6,641 PEOPLE', W/2, 120, 90, '#ffffff', 0, back(u/0.3, 1.5))
    n_hi = int(clamp((u - 1.2)/2.0)*39)
    for i in range(100):
        r, q = divmod(i, 20)
        x = 180 + q*64; y = 300 + r*125
        k = clamp((u - 0.2 - i*0.008)/0.2)
        if k <= 0: continue
        hi = i < n_hi
        person_icon(T, x, y + 30, 1.35*k, '#ff4fa3' if hi else '#8e84b8')
    if u > 1.2:
        pct = 38.6*clamp((u - 1.2)/2.0)
        label(c, f'{pct:.1f}%', 1700, 440, 120, '#ff4fa3', -0.04)
        label(c, '"I remember being', 1700, 590, 40, '#ffffff', 0, 1, FONT, 10)
        label(c, '2 or younger!"', 1700, 645, 40, '#ffffff', 0, 1, FONT, 10)

def sh_madeup(T, t, t0):
    """old photo + family story fly into a memory bubble and 'build' the fake memory"""
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0); board(T, t)
    v1 = ease((u - 0.3)/1.0); v2 = ease((u - 0.9)/1.0)
    memory_bubble(T, 1250, 470, 300, back((u - 0.1)/0.4, 1.2), t,
                  lambda T: (T.flat(rect(0, 0, 3000, 2000), '#ffe9c9'), draw_baby(T, dict(t=t, x=1250, y=520 + 60, s=0.7, sm=0.8, legs=False)), cake(T, 1250, 640, 0.6, 0, t)) if u > 1.9 else None)
    if v1 < 1: photo(T, 260 + (1150 - 260)*v1, 250 + (380 - 250)*v1, 220*(1 - 0.6*v1), -0.15 + 0.15*v1)
    if v2 < 1 and u > 0.6:   # speech bubble 'family story'
        x = 300 + (1150 - 300)*v2; y = 700 + (480 - 700)*v2; s = 1 - 0.6*v2
        T.shape([(x - 200*s, y - 80*s), (x + 200*s, y - 80*s), (x + 200*s, y + 60*s), (x - 60*s, y + 60*s), (x - 120*s, y + 120*s), (x - 100*s, y + 60*s), (x - 200*s, y + 60*s)], '#ffffff', lw=6)
        if s > 0.6: label(c, '"You loved that cake!"', x, y - 10, 30*s, '#3a3f8f', 0, 1, FONT, 6)
    if u > 2.6: kin(c, t, 'MADE UP?', t0 + 2.6, 1260, 860, 110, '#ff4fa3', -0.05)
    label(c, 'OLD PHOTOS', 330, 160, 50, '#ffd43b', -0.03, back((u - 0.05)/0.3, 1.5))
    label(c, 'FAMILY STORIES', 330, 900, 50, '#4fd8ff', 0.03, back((u - 0.6)/0.3, 1.5))

def sh_fridge(T, t, t0):
    u = t - t0
    pan = ease((u - 0.25)/0.8)
    cam(T, 1180 + (1580 - 1180)*pan, 470 - 80*pan, 1.0 + 1.0*pan)
    room(T, t)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.9, -0.1), lid=0.35, armF=((-260, -60), 30) if u > 0.2 else ((-30, 170), -18), brow=0.0)))
    draw_kiko(T, kiko_talk(t, dict(x=1180, y=FLOOR + 150, s=0.95, face=1, look=(0.9, -0.3), brow=-0.8, er=46)))
    if u > 0.9:
        T.glow(1650, 350, 120, '#ffd43b', ((1.3, 0.18*min(1, (u - 0.9)*3)),))

def sh_oh(T, t, t0):
    u = t - t0
    cam(T, 1150, 470, 2.0 - 0.04*u)
    room(T, t)
    sag = ease(u/0.8)
    draw_kiko(T, kiko_talk(t, dict(x=1180, y=FLOOR + 150, s=0.95, face=-1, look=(0.2, 0.5), brow=-0.5, lid=0.35*sag, sm=-0.5, sweat=True, sq=1 - 0.05*sag,
                                    armF=((-10, 170), -10), armB=((10, 170), 10))))

def sh_cant_save(T, t, t0):
    """old belief: baby brain can't save — memory cards bounce off"""
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0); board(T, t)
    brain(T, 960, 500, 1.0, 0, t)
    for i in range(4):
        tt = u - 0.3 - i*0.45
        if 0 < tt < 1.2:
            if tt < 0.5: x = -100 + (700 + 100)*tt/0.5; y = 300 + i*60
            else: x = 700 - 500*(tt - 0.5); y = 300 + i*60 + 600*(tt - 0.5)**2
            T.shape(rect(x - 50, y - 36, 100, 72), ('#ffd43b', '#4fd8ff', '#ff4fa3', '#7dff9a')[i], lw=6)
            T.shape(rect(x - 30, y - 20, 60, 30), '#ffffff', lw=4)
    label(c, 'OLD IDEA: BABY BRAINS', W/2, 200, 64, '#c9b8ff', 0, back(u/0.3, 1.4))
    if u > 1.0: kin(c, t, "CAN'T SAVE!", t0 + 1.0, 1500, 800, 90, '#ff4fa3', 0.06)

def sh_scanner(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 900 + 40*u, 560, 0.95 + 0.02*u)
    T.flat(rect(-2000, -2000, 6000, 5000), '#dff3ff')
    T.shape(rect(-2000, 840, 6000, 1200), '#b8d6ea', lw=8)
    mri(T, 700, 880, 1.0, t)
    # baby on the bed with blanket + pacifier
    draw_baby(T, dict(t=t, x=1010, y=700, s=0.75, rot=-1.5708, paci=True, look=(0, -0.4), legs=False, armF=((-30, 40), -10), armB=((30, 40), 10)))
    T.shape([(880, 660), (1250, 660), (1270, 720), (870, 720)], '#ffb3c8', lw=7)
    # parent's hand/teddy for comfort
    T.shape(ellipse_pts(1300, 650, 50, 46, 20), '#c98a5a', lw=6); T.shape(ellipse_pts(1300, 590, 36, 34, 18), '#c98a5a', lw=6)
    for ex in (-14, 14): T.dot(1300 + ex, 585, 5)
    tag(c, t, 'YALE UNIVERSITY · 2025', t0 + 0.3, '#ffd43b')
    label(c, 'AWAKE BABIES · 4 MONTHS – 2 YEARS', 1350, 180, 44, '#ffffff', -0.02, back((u - 1.2)/0.3, 1.4), FONT, 10)

def sh_hippo(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.02*u); board(T, t, '#1f2a4a', '#2c3a63')
    hk = ease((u - 1.0)/0.8)
    brain(T, 900, 520, 1.25, hk, t)
    label(c, 'HIPPOCAMPUS', 1450, 200, 72, '#ffe066', 0.02, back((u - 1.3)/0.3, 1.5))
    label(c, "the brain's memory maker", 1450, 280, 40, '#ffffff', 0, back((u - 1.6)/0.3, 1.5), FONT, 10)
    if hk > 0.6: T.stroke([(1260, 300), (1050, 560)], lw=7, col='#ffe066')
    # little pictures fly into the hippocampus and get saved
    for i in range(4):
        tt = u - 2.4 - i*0.55
        if 0 < tt < 0.7:
            v = ease(tt/0.7); x = 1750 + (925 - 1750)*v; y = 760 + (607 - 760)*v - 120*math.sin(v*math.pi); s = 1 - 0.7*v
            T.shape(rect(x - 60*s, y - 45*s, 120*s, 90*s), '#ffffff', lw=5)
            T.shape(rect(x - 48*s, y - 34*s, 96*s, 60*s), ('#9fe3d9', '#ffb3c8', '#ffd43b', '#c9b8ff')[i], lw=3)
    if u > 2.9: saved_badge(c, t, t0 + 2.9, 'SAVED — AT ~1 YEAR OLD', W/2, 900)

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

def sh_mouse(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u); board(T, t, '#1f3a3a', '#2c5050')
    # calendar flips 'weeks later' then a light beam re-activates the memory
    flips = int(clamp((u - 0.6)/1.6)*8)
    T.shape(rect(1380, 180, 300, 300), '#ffffff', lw=7); T.shape(rect(1380, 180, 300, 70), '#ff4fa3', lw=7)
    label(c, f'DAY {1 + round(flips*89/8)}', 1530, 380, 56, '#3a3f8f', 0, 1, FONT, 8)
    lit = clamp((u - 2.6)/0.5)
    if u > 2.4:
        T.stroke([(960, -50), (800, 360)], lw=int(10 + 18*lit), col='#7dd8ff', alpha=0.6)
    mouse(T, 700, 640, 1.4, t, lit)
    label(c, 'IN MICE', 360, 140, 70, '#7dff9a', -0.04, back(u/0.3, 1.4))
    if lit > 0.5: kin(c, t, 'MEMORY IS BACK!', t0 + 3.0, 1450, 800, 80, '#ffe066', 0.03)

def sh_lock(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.03*u); board(T, t)
    # a chest of baby memories with a padlock
    x, y = 960, 640
    T.shape(rect(x - 300, y - 120, 600, 280), '#c98a4a', shadow='#a86e34', shade_dir=(1, 0), shade_w=0.2, lw=8)
    lid = 30*math.sin(tq(t)*6) if u > 0.3 else 0
    T.shape([(x - 320, y - 120), (x - 300, y - 230 - lid*0.2), (x + 300, y - 230 - lid*0.2), (x + 320, y - 120)], '#d99a5a', lw=8)
    for k in range(5):   # glowing memories peeking out
        T.glow(x - 200 + k*100, y - 140, 26, '#ffe066', ((1.6, 0.25),))
    T.shape(rect(x - 70, y - 40, 140, 120), '#ffd43b', lw=7)
    T.shape(ellipse_pts(x, y - 50, 50, 60, 20, math.pi, 2*math.pi), None, lw=14)
    T.shape(ellipse_pts(x, y + 10, 16, 16, 10), LINE and '#1b1422', lw=0, line=False)
    label(c, 'NOT DELETED', W/2, 170, 80, '#7dff9a', -0.03, back((u - 0.2)/0.3, 1.5))
    if u > 1.3: kin(c, t, 'JUST LOCKED', t0 + 1.3, W/2, 290, 80, '#ff4fa3', 0.03)

def sh_keyhunt(T, t, t0):
    """Kiko frantically searches the sofa for 'the key'; Nova deadpan"""
    u = t - t0
    cam(T, 760, 560, 1.15)
    room(T, t)
    hop = abs(math.sin(tq(t)*10))*30
    draw_kiko(T, kiko_talk(t, dict(x=200 + 60*math.sin(tq(t)*3), y=FLOOR + 150 - hop, s=0.95, face=1, look=(0.2, 0.6), brow=-0.9, sweat=True, er=48,
                                    armF=((-140, 60 + 40*math.sin(tq(t)*12)), 30), armB=((140, 60 - 40*math.sin(tq(t)*12)), -30), jit=jitter(t, 6))))
    for i in range(3):   # flying cushions
        tt = (u*1.2 + i*0.4) % 1.2
        T.shape(rect(150 + i*60 + 300*tt, FLOOR - 300 - 400*tt + 500*tt*tt, 90, 60), ('#ff8fb8', '#ffd43b', '#9fe3d9')[i], lw=6)
    draw_nova(T, nova_talk(t, dict(x=1150, y=FLOOR + 140, s=0.95, face=-1, look=(-0.6, 0), lid=0.4, brow=-0.1, sm=0.1)))

def sh_portal(T, t, t0):
    """end of 'our world': Nova clicks, the room swirls"""
    u = t - t0
    cam(T, 760, 450, 1.3 + 0.1*u)
    room(T, t)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.2, 0), armF=((-150, -40), 40), hold='clicker', press=1.0 if u > 0.15 else 0.0, brow=0.9)))

def sh_par_room(T, t, t0):
    u = t - t0
    cam(T, 960, 560, 1.05 - 0.02*u)
    room(T, t, par=True)
    draw_nova(T, nova_talk(t, dict(x=760, y=FLOOR + 140, s=0.95, face=1, look=(0.1, 0), armF=((-150, -100), 40), brow=0.9)))
    tag(T.c, t, 'WORLD #13 · MEMORY: ALWAYS ON', t0 + 0.6)

def sh_mom_pov(T, t, t0):
    """baby's view from the crib: Mom leans in for the first time"""
    u = t - t0; c = T.c
    lean = ease(u/1.4)
    cam(T, 960, 560 + 40*(1 - lean), 1.15 + 0.3*lean)
    T.flat(rect(-2000, -2000, 6000, 5000), '#ffe6f0')
    for i in range(-12, 30): T.flat(rect(i*120, -2000, 40, 5000), '#ffd6e6')
    # mobile toy
    T.stroke([(960, -400), (960, 80)], lw=6)
    T.stroke([(780, 80), (1140, 80)], lw=6)
    for i, col in enumerate(('#ffd43b', '#4fd8ff', '#ff4fa3')):
        x = 800 + i*160; yy = 160 + 12*math.sin(t*2 + i)
        T.stroke([(x, 80), (x, yy - 40)], lw=4); T.shape(star(x, yy, 40, 18, 5, t*0.5 + i), col, lw=5)
    draw_adult(T, dict(t=t, x=960, y=1060, s=1.0, look=(0, 0.5), sm=0.9, closed=blinkf(t, 3.1), brow=0.6, armF=((-90, 120), -30), armB=((90, 120), 30)), MOM)
    crib_bars(T, -200, 2120, 860, 1500, 14)
    if u > 0.9: c.save(); memory_look(c, 0.7); c.restore()
    saved_badge(c, t, t0 + 1.6, 'MEMORY #1 SAVED', W - 330, 160)

def sh_first_word(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.04*u)
    T.flat(rect(-2000, -2000, 6000, 5000), '#ffe9c9')
    for i in range(-12, 30): T.flat(rect(i*120, -2000, 50, 5000), '#ffdcae')
    T.shape(rect(-2000, 900, 6000, 1200), '#c98a5a', lw=8)
    highchair(T, 760, 1120, 1.1)
    said = u > 1.6
    draw_baby(T, dict(t=t, x=760, y=780, s=1.15, sm=0.9, o=0.9 if 1.6 < u < 2.3 else 0.1, er=36 if said else 30, look=(0.8, 0.1), brow=0.9 if said else 0.2,
                      armF=((-90, -150), 30) if said else ((-50, -30), 20), armB=((90, -150), -30) if said else ((50, -30), -20), legs=False))
    # cake on the counter, dad holding it
    draw_adult(T, dict(t=t, x=1420, y=1180, s=0.95, face=-1, look=(-0.6, 0.2), sm=0.7, armF=((-150, -40), 30)), DAD)
    cake(T, 1230, 760, 0.6, 0, t)
    if said:
        k = back((u - 1.6)/0.25, 2.0)
        T.shape([(820, 330), (1160, 330), (1160, 520), (980, 520), (900, 600), (920, 520), (820, 520)], '#ffffff', lw=7)
        label(c, 'CAKE!', 990, 425, 110*k, '#ff4fa3', -0.04)
    saved_badge(c, t, t0 + 2.2, 'FIRST WORD SAVED', W - 330, 160)

def sh_walk(T, t, t0):
    """baby wobbles toward clapping Mom & Dad, falls once, gets up"""
    u = t - t0; c = T.c
    cam(T, 960, 600, 1.0 + 0.03*u)
    room(T, t, par=True, fridge=False)
    fall_t = 1.9
    if u < fall_t: bx = 300 + 200*u; fall = 0
    elif u < fall_t + 0.9: bx = 300 + 200*fall_t; fall = 1
    else: bx = 300 + 200*fall_t + 220*(u - fall_t - 0.9); fall = 0
    lL, lR, bob = walk_legs(t, not fall, 18, 14, 10)
    rot = 0.18*math.sin(tq(t)*6) if not fall else 0
    draw_adult(T, dict(t=t, x=1300, y=FLOOR + 150, s=0.95, face=-1, look=(-0.7, 0.4), sm=0.9, armF=((-60 + 30*math.sin(tq(t)*14), -80), 30), armB=((60 - 30*math.sin(tq(t)*14), -80), -30)), MOM)
    draw_adult(T, dict(t=t, x=1650, y=FLOOR + 150, s=0.95, face=-1, look=(-0.8, 0.4), sm=0.9, armF=((-60 + 30*math.sin(tq(t)*14 + 1), -80), 30), armB=((60 - 30*math.sin(tq(t)*14 + 1), -80), -30), cfg_ph=1), DAD)
    if fall:
        draw_baby(T, dict(t=t, x=bx, y=FLOOR + 130, s=0.95, sq=land_sq(u, fall_t + 0.05), legs=False, look=(0.3, -0.3), er=36, brow=-0.6, armF=((-70, -40), 20), armB=((70, -40), -20)))
    else:
        draw_baby(T, dict(t=t, x=bx, y=FLOOR + 130, s=0.95, rot=rot, legL=lL, legR=lR, bob=bob, look=(0.8, 0), sm=0.8, brow=0.6,
                          armF=((-90, -100), 30), armB=((90, -100), -30)))
    if u > fall_t: kin(c, t, 'BUMP', t0 + fall_t, bx/1.0 * T.z - (T.cx - W/2)*T.z if False else W*0.33, 300, 80, '#ffffff', -0.1)
    counters = [('WOBBLES', int(u*9)), ('FALLS', 1 if u > fall_t else 0), ('CLAPS', int(u*14))]
    for i, (n, v) in enumerate(counters):
        if u > 0.3 + i*0.3: label(c, f'{n}: {v}', 260, 150 + i*70, 44, ('#ffd43b', '#ff4fa3', '#7dff9a')[i], 0, 1, FONT, 10)
    saved_badge(c, t, t0 + 3.2, 'ALL OF IT SAVED', W - 330, 160)

def sh_diaper(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0); board(T, t, '#3a2a1f', '#4a3a2c')
    draw_baby(T, dict(t=t, x=960, y=780, s=1.1, diaper=True, look=(0, 0), brow=-0.4, sm=-0.3, er=36))
    n = int(1 + (u**2)*60)
    label(c, f'DIAPER #{n:,}', W/2, 170, 100, '#ffd43b', 0.02*math.sin(t*20))
    kin(c, t, 'EVERY.', S(28) + 0.0, 330, 560, 90, '#ffffff', -0.08)
    kin(c, t, 'SINGLE.', S(28) + (E(28) - S(28))*0.35, 1590, 560, 90, '#ffffff', 0.08)
    kin(c, t, 'DIAPER.', S(28) + (E(28) - S(28))*0.7, W/2, 920, 100, '#ff4fa3', -0.03)

def sh_grudge(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.04*u)
    room(T, t, par=True, fridge=False)
    # armchair + grandpa
    T.shape([(1250, FLOOR + 10), (1250, FLOOR - 330), (1700, FLOOR - 330), (1700, FLOOR + 10)], '#a85a5a', shadow='#8a4545', shade_dir=(1, 0), shade_w=0.2, lw=8)
    draw_adult(T, dict(t=t, x=1470, y=FLOOR + 120, s=0.9, face=-1, look=(-0.7, 0.3), lid=0.25, brow=-0.5 if u > 1.0 else 0.2, sm=-0.2 if u > 1.0 else 0.3, sweat=u > 1.0,
                       hold='rattle' if False else None, armF=((-60, 150), -10)), GRANDPA)
    # baby stands in the crib, pointing
    crib_floor = FLOOR + 80
    draw_baby(T, kiko_talk(t, dict(x=560, y=crib_floor - 120, s=1.05, face=1, angry=True, look=(0.9, 0), er=34, armF=((-160, -20), 20), armB=((60, 60), -10), legs=False,
                                   o=lip('KIKO', t)*0.9)))
    crib_bars(T, 340, 800, crib_floor - 280, crib_floor + 120, 6)
    # memory inset: grandpa taking the rattle
    if u > 0.8:
        memory_bubble(T, 900, 230, 170, back((u - 0.8)/0.3, 1.2), t, lambda T: (T.flat(rect(0, -400, 3000, 1400), '#ffe9c9'),
                      T.shape(rect(820, 160, 30, 140), '#ffd43b', lw=6), T.shape(ellipse_pts(835, 150, 40, 40, 16), '#ff4fa3', lw=6),
                      draw_adult(T, dict(t=t, x=1000, y=700, s=0.6, face=-1, look=(-0.8, 0), sm=0.6, armF=((-200, -150), 20)), GRANDPA)))
        label(c, '8 MONTHS OLD', 900, 420, 36, '#ffffff', 0, back((u - 1.0)/0.3, 1.5), FONT, 9)

def sh_scary(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.02*u); board(T, t)
    label(c, 'SCARY MEMORIES', W/2, 120, 80, '#ffffff', 0, back(u/0.3, 1.4))
    jars = [('THUNDER', '#4fd8ff'), ('NEEDLE', '#ff4fa3'), ('LOUD DOG', '#ffd43b'), ('BATH WATER', '#7dff9a'), ('DARK ROOM', '#c9b8ff')]
    for i, (n, col) in enumerate(jars):
        k = back((u - 0.4 - i*0.35)/0.3, 1.6)
        if k <= 0.01: continue
        x = 330 + i*315; y = 560
        T.shape([(x - 110*k, y - 150*k), (x + 110*k, y - 150*k), (x + 120*k, y + 160*k), (x - 120*k, y + 160*k)], '#e8fbff', lw=7, alpha=0.95)
        T.shape(rect(x - 120*k, y - 190*k, 240*k, 45*k), col, lw=6)
        T.glow(x, y + 20*k, 50*k, col, ((1.4, 0.35), (1.0, 0.5)))
        label(c, n, x, y + 230, 34, col, 0, k, FONT, 8)
    # a gentle lightning flash once (thunder)
    flash(c, t, t0 + 0.9, 0.1, 0.25)
    if u > 2.6: kin(c, t, 'FOREVER', t0 + 2.6, W/2, 900, 100, '#ff4fa3', -0.03)

def sh_newcells(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0); board(T, t, '#1f3a3a', '#2c5050')
    brain(T, 960, 520, 1.25, 0.6, t)
    label(c, 'IN BABY MICE', 360, 120, 64, '#7dff9a', -0.04, back(u/0.3, 1.4))
    # many new cells pop in and old memory notes get scrambled away
    for i in range(18):
        tt = u - 0.6 - i*0.12
        if tt > 0:
            k = back(tt/0.25, 2.0); a = i*2.4; r = 120 + (i*37 % 160)
            x = 960 + r*math.cos(a)*1.3; y = 520 + r*math.sin(a)*0.8
            T.shape(ellipse_pts(x, y, 26*k, 24*k, 14), '#7dff9a', lw=5)
            T.dot(x - 8*k, y - 4*k, 4*k); T.dot(x + 8*k, y - 4*k, 4*k)
    for i in range(5):
        tt = u - 1.4 - i*0.3
        if tt > 0:
            x = 960 + (i - 2)*90 + 500*tt*(1 if i % 2 else -1); y = 520 - 60*i + 300*tt*tt; r = tt*6
            T.shape([(x - 50*math.cos(r) + 40*math.sin(r), y - 50*math.sin(r) - 40*math.cos(r)), (x + 50*math.cos(r) + 40*math.sin(r), y + 50*math.sin(r) - 40*math.cos(r)),
                     (x + 50*math.cos(r) - 40*math.sin(r), y + 50*math.sin(r) + 40*math.cos(r)), (x - 50*math.cos(r) - 40*math.sin(r), y - 50*math.sin(r) + 40*math.cos(r))], '#fff6d8', lw=5)
    label(c, 'NEW BRAIN CELLS', 1540, 860, 54, '#7dff9a', 0.03, back((u - 0.8)/0.3, 1.4))
    label(c, '= OLD MEMORIES SCRAMBLED', 1540, 930, 40, '#ffffff', 0, back((u - 1.6)/0.3, 1.4), FONT, 10)

def sh_blocks(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.02*u); board(T, t)
    blocks = [('LANGUAGE', '#ff4fa3'), ('FACES', '#4fd8ff'), ('HOW THE WORLD WORKS', '#ffd43b')]
    for i, (n, col) in enumerate(blocks):
        t_i = 0.5 + i*0.9
        if u < t_i: continue
        v = clamp((u - t_i)/0.35); y_t = 860 - i*190
        y = -200 + (y_t + 200)*ease(v); sq = land_sq(u, t_i + 0.35)
        w = 700 - i*60
        T.shape(rect(960 - w/2, y - 160*sq, w, 160*sq), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=8)
        label(c, n, 960, y - 80*sq, 64, '#ffffff', 0, 1)

def sh_desk(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u)
    room(T, t, par=True, fridge=False)
    # a desk: papers get swept, then a little tower grows
    T.shape(rect(1050, 560, 620, 40), '#c98a4a', lw=8); T.shape(rect(1080, 600, 30, 240), '#a86e34', lw=6); T.shape(rect(1610, 600, 30, 240), '#a86e34', lw=6)
    sweep = ease((u - 1.2)/0.6)
    for i in range(6):
        x = 1120 + i*85 + 900*sweep*(1 + i*0.1); y = 540 - (i % 2)*10 + 400*sweep*sweep
        T.shape(rect(x - 34, y - 20, 68, 20), '#ffffff', lw=5)
    if u > 2.0:
        hgt = ease((u - 2.0)/1.2)
        for j in range(int(1 + hgt*6)):
            T.shape(rect(1310 - 40 + (j % 2)*10, 540 - (j + 1)*52, 90, 52), ('#ff4fa3', '#4fd8ff', '#ffd43b')[j % 3], lw=6)
    draw_nova(T, nova_talk(t, dict(x=700, y=FLOOR + 140, s=0.95, face=1, look=(0.7, 0.1), armF=((-160, -60), 40), brow=0.7)))

def poll_chip(c, x, y, txt, col, k):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(52)
    w = c.text_extents(txt).x_advance + 90; r = 52
    c.new_path(); c.arc(-w/2 + r, 0, r, math.pi/2, 3*math.pi/2); c.arc(w/2 - r, 0, r, -math.pi/2, math.pi/2); c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(8); c.stroke()
    c.move_to(-w/2 + 45, 18); c.text_path(txt); c.set_source_rgb(*LINE); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill(); c.restore()

def sh_end(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.015*u)
    room(T, t, par=True, fridge=True)
    k_kiko = S(37)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.1, 0.1), armF=((-150, -80), 40), brow=0.8)))
    has_cake = t > k_kiko - 0.3
    draw_kiko(T, kiko_talk(t, dict(x=1180, y=FLOOR + 150, s=0.95, face=-1, look=(-0.3, 0), brow=0.6, sm=0.9, closed=has_cake and lip('KIKO', t) < 0.2,
                                    armF=((-120, 40), 30) if has_cake else ((-30, 160), -18))))
    if has_cake:   # Kiko holds a slice of blue cake
        T.shape([(990, 600), (1090, 560), (1090, 640), (990, 680)], '#4fa8ff', lw=6); T.shape([(990, 600), (1090, 560), (1095, 545), (995, 585)], '#ffffff', lw=5)
    poll_chip(c, 560, 170, 'REMEMBER IT ALL', '#ff4fa3', back((t - at(36, 0.3))/0.3, 1.6))
    poll_chip(c, 1360, 170, 'BETTER TO FORGET', '#3a8fd8', back((t - at(36, 0.7))/0.3, 1.6))

# ---------------------------------------------------------------- edit decision list
def L(i): return S(i) - 0.12
EDL = [
    (0.0, lambda T, t: sh_hook(T, t)),
    (at(0, 0.40), lambda T, t: sh_memory_birthday(T, t, at(0, 0.40))),
    (L(1), lambda T, t: sh_twoshot(T, t, L(1), kp=dict(brow=0.8, sm=0.7, look=(-0.8, -0.1)), np_=dict(lid=0.3, brow=0.0))),
    (L(2), lambda T, t: sh_kcu(T, t, L(2), extra=dict(brow=1.0, sm=0.9, armF=((-60, -40), 30), armB=((60, -40), -30)))),
    (L(3), lambda T, t: sh_ncu(T, t, L(3), extra=dict(lid=0.2, brow=0.8, look=(0.4, -0.3), armF=((-60, -120), 40)))),
    (L(4), lambda T, t: sh_timeline(T, t, L(4))),
    (L(6), lambda T, t: sh_superbaby(T, t, L(6))),
    (L(7), lambda T, t: sh_study(T, t, L(7))),
    (L(8), lambda T, t: sh_madeup(T, t, L(8))),
    (L(9), lambda T, t: sh_kcu(T, t, L(9), extra=dict(brow=-0.2, sm=-0.2, look=(-0.8, 0), armF=((-80, -60), 30), armB=((80, -60), -30)))),
    (L(10), lambda T, t: sh_fridge(T, t, L(10))),
    (L(11), lambda T, t: sh_oh(T, t, L(11))),
    (L(12), lambda T, t: sh_cant_save(T, t, L(12))),
    (L(13), lambda T, t: sh_scanner(T, t, L(13))),
    (L(14), lambda T, t: sh_hippo(T, t, L(14))),
    (L(15), lambda T, t: sh_kcu(T, t, L(15), extra=dict(brow=0.9, er=46, look=(-0.6, -0.2), sm=0.4))),
    (L(16), lambda T, t: sh_mouse(T, t, L(16))),
    (L(17), lambda T, t: sh_lock(T, t, L(17))),
    (L(18), lambda T, t: sh_keyhunt(T, t, L(18))),
    (at(19, 0.55), lambda T, t: sh_portal(T, t, at(19, 0.55))),
    (L(20) + 0.3, lambda T, t: sh_par_room(T, t, L(20) + 0.3)),
    (L(21), lambda T, t: sh_mom_pov(T, t, L(21))),
    (L(22), lambda T, t: sh_first_word(T, t, L(22))),
    (L(23), lambda T, t: sh_twoshot(T, t, L(23), par=True, kp=dict(brow=0.9, sm=0.9, look=(-0.8, 0)))),
    (L(24), lambda T, t: sh_ncu(T, t, L(24), par=True, extra=dict(lid=0.45, brow=-0.1, sm=0.2, look=(0.9, 0)))),
    (L(25), lambda T, t: sh_walk(T, t, L(25))),
    (L(26), lambda T, t: sh_ncu(T, t, L(26), par=True, extra=dict(brow=0.2, lid=0.15, armF=((-40, -230), 10)))),
    (L(27), lambda T, t: sh_kcu(T, t, L(27), par=True, z=2.5, extra=dict(brow=-1.0, er=50, sweat=True, sm=-0.6, look=(-0.4, 0), jit=jitter(t)))),
    (L(28), lambda T, t: sh_diaper(T, t, L(28))),
    (L(29), lambda T, t: sh_grudge(T, t, L(29))),
    (L(31), lambda T, t: sh_scary(T, t, L(31))),
    (L(32), lambda T, t: sh_newcells(T, t, L(32))),
    (L(33), lambda T, t: sh_blocks(T, t, L(33))),
    (L(34), lambda T, t: sh_kcu(T, t, L(34), par=True, extra=dict(brow=0.7, look=(-0.6, -0.3), sm=0.3, armF=((-60, -200), 20)))),
    (L(35), lambda T, t: sh_desk(T, t, L(35))),
    (L(36), lambda T, t: sh_end(T, t, L(36))),
]
EDL.sort(key=lambda e: e[0])
CUTS = [e[0] for e in EDL]

def shot_index(t):
    i = 0
    for k, (t0, f) in enumerate(EDL):
        if t >= t0: i = k
    return i

WIPE_T = S(20)
def render(t, clean=False):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
    i = shot_index(t)
    T = Toon(c, t)
    EDL[i][1](T, t)
    if not clean:
        if EDL[i][0] == at(0, 0.40): memory_look(c, 1.0)
        caption(c, t); chapter_card(c, t); brand(c, t)
        if i > 0 and t - EDL[i][0] < 0.1 and EDL[i][0] not in (WIPE_T,): flash(c, t, EDL[i][0], 0.08, 0.18)
        swirl_wipe(c, t, WIPE_T)
        if t > TOTAL - 0.4: c.set_source_rgba(0, 0, 0, clamp((t - (TOTAL - 0.4))/0.4)); c.paint()
    return surf

def frame_bytes(i): return bytes(render(i/FPS).get_data())

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'
    os.makedirs('/home/claude/pw/out', exist_ok=True)
    if mode == 'stills':
        ts = [float(x) for x in sys.argv[2:]] or [e[0] + 1.0 for e in EDL]
        for t in ts: render(t).write_to_png(f'/home/claude/pw/out/l2_{t:06.2f}.png')
    elif mode == 'video':
        a = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0; b = float(sys.argv[3]) if len(sys.argv) > 3 else TOTAL
        out = sys.argv[4] if len(sys.argv) > 4 else '/home/claude/pw/out/long02_v.mp4'
        N0, N1 = int(a*FPS), int(b*FPS)
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        with Pool(2) as pool:
            for i, bts in enumerate(pool.imap(frame_bytes, range(N0, N1), chunksize=6)):
                p.stdin.write(bts)
                if i % 240 == 0: print(i, '/', N1 - N0, flush=True)
        p.stdin.close(); p.wait()
