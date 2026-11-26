"""EP16 - Why do ONIONS make you cry? (Short, WHY format with a parallel-world twist, built with shortkit)
Format: WHY (everyday mystery) + portal twist ("no-tear-enzyme world"). Topic family: food chemistry / senses (new family).
Gate score: curiosity 5, relatable 5, visual 5, fact certainty 4, freshness 3 (common question; our own angle is the
parallel world with the tear enzyme removed, which scientists really did in a lab) = 22/25.
Facts (checked):
- Cutting an onion breaks its cells; enzymes turn its sulfur amino-acid sulfoxides into sulfenic acid, and a second enzyme,
  lachrymatory-factor synthase (LFS), turns that into syn-propanethial-S-oxide, an airborne chemical similar to tear gas
  (Library of Congress "Everyday Mysteries: Why does chopping an onion make you cry?"; RSC Education "Magnificent molecules:
  propanethial-S-oxide").
- On the surface of the eye it reacts with water to make an acid that triggers a nerve response, and tears wash it away
  (RSC Education); the lachrymal glands become irritated and produce tears (Library of Congress).
- The LFS enzyme was discovered by scientists in Japan: Imai et al. 2002, Nature 419:685 ("An onion enzyme that makes the
  eyes water"); before that, alliinase alone was blamed (Library of Congress, RSC).
- A genetically modified onion with the LFS enzyme switched off was developed in New Zealand (RSC Education); a very sharp
  knife minimises cell damage (RSC Education). A 2025 Cornell preprint (PopSci) also found dull blades spray far more
  droplets; not used as a number because it was not yet peer reviewed.
Sources: Library of Congress Everyday Mysteries; RSC Education (Royal Society of Chemistry); Imai et al. 2002 (Nature).
No real people, no brands; onions and knife are generic drawings."""
import math, numpy as np
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Why do onions make me cry?!", gap=0.3),
    dict(who=N, text="It's a chemical trap! Cutting breaks its cells, and chemicals kept apart, mix.", gap=0.3),
    dict(who=N, text="Enzymes turn them into a stingy chemical that floats up.", gap=0.3),
    dict(who=N, text="In your eyes, it mixes with water and makes a tiny bit of acid.", gap=0.3),
    dict(who=N, text="Your nerves sound the alarm, and tears rush out to wash it away.", gap=0.35),
    dict(who=N, text="In two thousand two, scientists in Japan found the enzyme behind it.", cap="In 2002, scientists in Japan found the enzyme behind it.", gap=0.3),
    dict(who=N, text="So in this parallel world, onions have no tear enzyme at all.", gap=0.3),
    dict(who=K_, text="Chop chop chop... zero tears!", gap=0.35),
    dict(who=N, text="Scientists really made onions like that! Back home, a sharp knife helps.", gap=0.35),
    dict(who=N, text="Tear onions, or no tear onions? Comment below. A new parallel world, every day.", cap="Tear onions, or no-tear onions? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep16_onion_tears', our_set='room', par_set='room',
    title="Why Do ONIONS Make You Cry? \U0001F300 #Swirlverse",
    description=("Why do onions make you cry? It's a chemical trap! Cutting breaks the onion's cells, enzymes make a stingy chemical "
                 "that floats into your eyes, and your tears rush out to wash it away. But in this parallel world, onions have no tear enzyme... \U0001F9C5\n"
                 "Tear onions or no-tear onions? Comment below \U0001F447\n\n"
                 "Real science: an enzyme called lachrymatory-factor synthase makes syn-propanethial-S-oxide. On your eye it reacts with water "
                 "to make a little acid, which sets off the nerves and the tears. Scientists in Japan discovered the enzyme in 2002 (Imai et al., Nature), "
                 "and researchers in New Zealand later made an onion with it switched off. A very sharp knife breaks fewer cells. "
                 "Sources: Library of Congress, Royal Society of Chemistry.\n\n"
                 "#shorts #science #onions #chemistry #kitchen #swirlverse"),
    tags=['why do onions make you cry', 'onion tears', 'cutting onions', 'onion chemistry', 'syn-propanethial-S-oxide',
          'lachrymatory factor', 'kitchen science', 'chemistry', 'parallel world', 'what if', 'science shorts', 'swirlverse', 'animation'],
    topic='why onions make you cry / onion tear enzyme (lachrymatory-factor synthase, syn-propanethial-S-oxide)', category='food chemistry / senses',
    hook='kiko crying question cold open -> chemistry chain -> portal twist',
)
DROPS = []

ONION, ONION_SH, ONION_IN, ONION_RING = '#c9a0dc', '#a678c2', '#f5ecff', '#dcc4ee'
GAS = '#c8f56a'

# ---------------------------------------------------------------- props
def tears(T, x, y, s, t, k=1.0):
    """streams of tears from Kiko's eyes. (x, y) = Kiko's feet, s = his scale"""
    if k <= 0: return
    for ex in (-38, 38):
        X, Y = x + ex*s, y - 470*s
        T.shape([(X - 9*s, Y), (X + 9*s, Y), (X + 7*s, Y + 120*s*k), (X - 7*s, Y + 120*s*k)], '#8fd8ff', lw=5, alpha=0.9)
        for i in range(3):
            ph = (tq(t)*1.6 + i/3) % 1
            dy = Y + (60 + ph*190)*s*k; dx = X + (ex/38)*ph*40*s
            r = 11*s
            T.shape([(dx, dy - 2*r), (dx + r, dy), (dx, dy + r), (dx - r, dy)], '#bfe9ff', lw=5)

def onion(T, x, y, r, t=0.0, cut=False):
    """whole onion bulb, or a cut half showing rings"""
    if not cut:
        pts = []
        for i in range(48):
            a = 2*math.pi*i/48
            rr = r*(1 + 0.08*math.cos(a))
            yy = y + rr*math.sin(a)*(1.0 if math.sin(a) > 0 else 0.95)
            pts.append((x + rr*math.cos(a)*0.95, yy))
        T.shape(pts, ONION, shadow=ONION_SH, shade_dir=(1, 0.4), shade_w=0.3, lw=8)
        T.shape([(x - r*0.18, y - r*0.88), (x, y - r*1.45), (x + r*0.18, y - r*0.88)], ONION_SH, lw=7)
        for dx in (-0.45, 0.0, 0.45):
            T.stroke([(x + dx*r*0.4, y - r*0.8), (x + dx*r, y), (x + dx*r*0.5, y + r*0.85)], lw=4, col=ONION_SH)
        for k in range(4):
            T.stroke([(x - 15 + k*10, y + r*0.95), (x - 25 + k*16, y + r*1.15)], lw=4, col='#d9c28a')
    else:
        T.shape(ellipse_pts(x, y, r, r*0.85, 40, math.pi, 2*math.pi) + [(x + r, y), (x - r, y)], ONION, lw=8)
        for i, f in enumerate((0.82, 0.62, 0.42, 0.22)):
            T.shape(ellipse_pts(x, y, r*f, r*0.85*f, 30, math.pi, 2*math.pi) + [(x + r*f, y), (x - r*f, y)], ONION_IN if i % 2 == 0 else ONION_RING, lw=5)

def knife(T, x, y, a=0.0, s=1.0):
    ca, sa = math.cos(a), math.sin(a)
    def R(pts): return [(x + (px*ca - py*sa)*s, y + (px*sa + py*ca)*s) for px, py in pts]
    T.shape(R([(-70, -16), (0, -16), (0, 16), (-70, 16)]), '#3a2a2a', lw=6)
    T.shape(R([(0, -20), (190, -20), (220, 10), (0, 22)]), '#e9eef5', shadow='#b9c3cf', shade_dir=(0, 1), shade_w=0.35, lw=6)

def table(T, x0, x1, top):
    T.shape(rect(x0 + 20, top + 40, 26, 400), '#8a5a33', lw=6); T.shape(rect(x1 - 46, top + 40, 26, 400), '#8a5a33', lw=6)
    T.shape(rect(x0, top, x1 - x0, 50), '#c98a4a', shadow='#a66c35', shade_dir=(0, 1), shade_w=0.35, lw=8)

def kitchen(K, T, t, par, kiko_pose, kx=360, chop=True, cry=0.0, nova=None):
    K.world(T, t, par)
    if nova is not False: K.nova(T, t, **(nova or pose('excited', 'finger_up')))
    table(T, 520, 960, 1300)
    T.shape(rect(560, 1268, 330, 36), '#f2d6a8', lw=6)   # cutting board
    onion(T, 800, 1205, 62, t)
    onion(T, 660, 1268, 60, t, cut=True)
    m = abs(math.sin(tq(t)*7))*40 if chop else 0
    P = dict(kiko_pose); P.update(x=kx, armF=((283 - (kx - 360)/0.92, -4 - m), -30), armB=((150, 40), 20))
    K.kiko(T, t, **P)
    hx = kx + (-66 + 283 - (kx - 360)/0.92)*0.92; hy = FEET + (-355 - 4 - m)*0.92
    knife(T, hx, hy, 0.35, 0.8)
    if cry: tears(T, kx, FEET, 0.92, t, cry)

def molecule(T, x, y, s=1.0, col=GAS):
    """a little stingy 'S=O' blob with a grumpy face"""
    T.shape(ellipse_pts(x, y, 34*s, 30*s, 20), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0.4), shade_w=0.25, lw=5)
    T.shape(ellipse_pts(x + 34*s, y - 22*s, 16*s, 16*s, 14), '#ffd43b', lw=4)
    T.stroke([(x - 14*s, y - 10*s), (x - 4*s, y - 6*s)], lw=4); T.stroke([(x + 4*s, y - 6*s), (x + 14*s, y - 10*s)], lw=4)
    T.stroke([(x - 10*s, y + 10*s), (x, y + 6*s), (x + 10*s, y + 10*s)], lw=4)

def sh_cold(K, T, t, u):
    T.cx, T.cy, T.z = 560, 1050, 1.12 - 0.08*ease(u/2.5)
    kitchen(K, T, t, False, pose('sad', 'rest', sm=-0.8, brow=-1.0, jit=jitter(t, 4)), cry=ease(u/0.4))
    label(T.c, 'WHY DO ONIONS', 540, 330, 112, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'MAKE YOU CRY?', 540, 480, 120, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_cells(K, T, t, u):
    """onion cells: chemical A sits inside, enzyme B kept apart; a knife slices and they mix"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t)
    label(T.c, 'ONION CELLS', 540, 330, 100, '#ffffff', -0.03, back(u/0.3, 1.4))
    cut = ease((u - 1.0)/0.4)
    for i in range(3):
        for j in range(2):
            cx, cy = 260 + i*280, 760 + j*360
            T.shape(rect(cx - 125, cy - 160, 250, 320), '#f5ecff', shadow='#dcc4ee', shade_dir=(1, 0.3), shade_w=0.2, lw=7)
            T.shape(ellipse_pts(cx + 40, cy + 40, 70, 90, 24), '#ffe066' if cut < 0.5 else '#f5ecff', lw=5)
            for k in range(4):
                ang = k*1.7 + t*0.6
                if cut < 0.5:
                    T.dot(cx + 40 + 30*math.cos(ang), cy + 40 + 40*math.sin(ang), 12, '#ff9f1c')
                    T.dot(cx - 70 + 15*math.sin(ang), cy - 100 + k*45, 13, '#4fd8ff')
                else:
                    mx = cx + 60*math.cos(ang*1.3 + i); my = cy + 90*math.sin(ang + j)
                    T.dot(mx, my, 12, '#ff9f1c'); T.dot(mx + 24, my - 10, 13, '#4fd8ff')
    # the knife sweeps down through the cells
    ky = 420 + 1100*ease((u - 0.7)/0.6)
    if 0.6 < u < 1.5: knife(T, 540, ky, 0.0, 2.2)
    if cut > 0.5:
        T.stroke([(540, 560), (548, 900), (532, 1300)], lw=10, col='#ff2d55')
        kin(T.c, t, 'CUT = MIX!', K.at(1, 0.75), 540, 1500, 130, '#ffd43b', -0.04)
    label(T.c, 'KEPT APART', 540, 1500, 70, '#c9b8ff', 0, 1 - cut, FONT, 10) if cut < 0.95 else None

def sh_gas(K, T, t, u):
    """the stingy chemical floats up out of the chopped onion"""
    T.cx, T.cy, T.z = 540, 980, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    onion(T, 540, 1480, 190, t, cut=True)
    for i in range(9):
        ph = (u*0.35 + i/9) % 1
        x = 540 + 260*math.sin(i*2.1 + u*1.5)*(0.3 + ph*0.7); y = 1380 - ph*900
        molecule(T, x, y, 1.0 + 0.4*ph)
    kin(T.c, t, 'IT FLOATS UP!', K.at(2, 0.45), 540, 330, 112, GAS, -0.03)
    label(T.c, 'syn-propanethial-S-oxide', 540, 470, 52, '#c9b8ff', 0, back((u - 0.5)/0.3, 1.3), FONT, 10)

def eye(T, x, y, r, t, irritate=0.0):
    T.shape(ellipse_pts(x, y, r*1.5, r, 48), mixc('#ffffff', '#ffc2c2', irritate), lw=10)
    T.shape(ellipse_pts(x, y, r*0.6, r*0.6, 36), '#5a3a22', lw=7)
    T.shape(ellipse_pts(x, y, r*0.28, r*0.28, 24), '#1b1422', lw=4)
    T.dot(x - r*0.18, y - r*0.2, r*0.1, '#ffffff')
    if irritate > 0.3:
        for k in range(5):
            a = 0.4 + k*0.55
            T.stroke([(x + r*1.25*math.cos(a)*1.2, y + r*0.8*math.sin(a)), (x + r*0.85*math.cos(a)*1.2, y + r*0.55*math.sin(a))], lw=5, col='#ff4f6a')

def sh_eye(K, T, t, u):
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.03*u
    board(T, t)
    irr = ease((u - 1.2)/0.6)
    eye(T, 540, 980, 260, t, irr)
    for i in range(6):
        ph = clamp((u - 0.1 - i*0.15)/0.9)
        x = 220 + i*130; y = 360 + ph*480
        if ph < 1: molecule(T, x, y, 1.1)
        else:
            k = back((u - 1.0 - i*0.15)/0.25, 1.4)
            label(T.c, 'ACID', x, 860, 44*k + 1, '#ff2d55', 0, 1)
    label(T.c, '+ WATER = ACID', 540, 1450, 110, '#ffd43b', -0.03, back((u - 1.1)/0.3, 1.5))

def tears_extra(T, t, u):
    tears(T, 270, FEET, 0.92, t, ease(u/0.35)*1.2)
    kin(T.c, t, 'WASH IT AWAY!', 0, 540, 520, 110, '#4fd8ff', -0.04)

def sh_chop(K, T, t, u):
    """parallel world: Kiko chops happily, no tears"""
    T.cx, T.cy, T.z = 560, 1050, 1.08 + 0.02*u
    kitchen(K, T, t, True, pose('happy', 'rest', sm=1.0), cry=0.0, nova=pose('happy', 'present'))
    kin(T.c, t, '0 TEARS!', K.S(7) + 1.0, 540, 360, 160, '#7dff9a', -0.05)

def sh_lab(K, T, t, u):
    """an onion with its tear enzyme switched off"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t)
    onion(T, 540, 980, 230, t)
    k = back((u - 0.4)/0.3, 1.5)
    T.shape(rect(240, 520, 600, 130), '#2a1f4a', lw=7)
    label(T.c, 'TEAR ENZYME', 540, 610, 76, '#ffffff', 0, 1)
    if u > 0.9:
        T.shape(rect(330, 1310, 420, 150), '#ff2d55', lw=8)
        label(T.c, 'OFF', 540, 1420, 120*back((u - 0.9)/0.3, 1.6) + 1, '#ffffff', 0, 1)
    label(T.c, 'made in a lab, New Zealand', 540, 1580, 50, '#c9b8ff', 0, back((u - 1.2)/0.3, 1.3), FONT, 10)

def sh_knife(K, T, t, u):
    """our world tip: a sharp knife breaks fewer cells"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t, '#1f2a4a', '#2c3a63')
    label(T.c, 'OUR WORLD TIP', 540, 330, 96, '#ffffff', -0.03, back(u/0.3, 1.4))
    knife(T, 330, 900, -0.5, 2.4)
    T.shape(star(820, 760, 70, 30, 4, 0.3), '#ffffff', lw=5) if int(t*6) % 2 == 0 else None
    kin(T.c, t, 'SHARP KNIFE', K.at(8, 0.5) + 0.2, 540, 1250, 130, '#ffd43b', -0.04)
    kin(T.c, t, '= FEWER BROKEN CELLS', K.at(8, 0.5) + 0.6, 540, 1420, 72, '#7dff9a', 0.02)

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.ncu(K.L(1), par=False, emo='smug', gest='finger_up')
    K.custom(K.at(1, 0.35), sh_cells, sfx='swoop')
    K.custom(K.L(2), sh_gas, sfx='pop')
    K.custom(K.L(3), sh_eye, sfx='blip')
    K.kcu(K.L(4), par=False, emo='shock', gest='hands_head', extra=tears_extra)
    K.stat(K.L(5), '2002', 'TEAR ENZYME', 'found in Japan (Imai et al., Nature)')
    K.hook(K.at(5, 0.6), portal_line=5, portal_f=0.86)
    K.arrive(tag_text='WORLD #16 · ONIONS: NO TEAR ENZYME')
    K.custom(K.L(7), sh_chop, sfx='boing')
    K.custom(K.L(8), sh_lab, sfx='blip')
    K.custom(K.at(8, 0.5), sh_knife, sfx='swoop')
    K.end(K.L(9), poll=('TEAR ONIONS', 'NO-TEAR ONIONS'))

def thumbnail(c, K):
    """huge text, big crying Kiko, a giant cut onion hero object with stingy molecules rising, arrow"""
    burst(c, W, H, 560, 1150, '#e8d6ff', '#3b1f8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    P = pose('sad', 'rest', sm=-0.9, brow=-1.0, er=46); P.update(x=300, y=2380, s=2.15, face=1, o=0.7, jit=0)
    K.kiko(T, 1.0, **P)
    tears(T, 300, 2380, 2.15, 0.25, 0.9)
    onion(T, 820, 1800, 240, 0.3, cut=True)
    for (x, y, s) in ((860, 1450, 1.5), (720, 1250, 1.8), (880, 1050, 1.6), (700, 900, 1.3)):
        molecule(T, x, y, s)
    big_text(c, "IT'S A", 540, 250, 140, max_w=950)
    big_text(c, 'TRAP!', 540, 460, 210, hl=0, hl_col='#ff4fa3', max_w=1010)
    emoji_burst(c, 860, 700, 105, 'WHY?!', '#ff2d55', 0.2)
    arrow(c, 900, 1250, 600, 1320, '#ffd43b', 26)
