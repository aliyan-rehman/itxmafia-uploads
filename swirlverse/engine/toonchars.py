"""Nova + Kiko rig for the sitcom-toon look. Local coords: origin at the feet, y down (up is negative).
P keys: x, y, s, face (+1 faces screen-right, -1 mirrors), rot (lean whole body, radians, about the feet),
lean (upper-body shear), bob, sq (squash), legL/legR ((dx,dy) ankle offsets), armF/armB (hand pos relative
to shoulder, bend), look (pupils), lid, brow (-1 worried .. +1 excited), o (mouth open), sm (smile), blink,
closed (happy closed eyes), sweat, ring (swim ring), hold ('clicker'), press, legs (False: hide legs),
headtilt, jit (nervous jitter px)."""
import math
from toonline import ellipse_pts, rect, noodle_pts, star, hexc, LINE

INK = '#1b1422'
SKIN, SKIN_S = '#f7f5ef', '#d9d4c4'

def tq(t): return math.floor(t*12)/12          # 12 fps drawing time

def walk_legs(t, on=True, amp=26, lift=16, speed=12):
    if not on: return (0, 0), (0, 0), 0
    a = tq(t)*speed
    return ((math.sin(a)*amp, -max(0, math.cos(a))*lift), (-math.sin(a)*amp, -max(0, -math.cos(a))*lift), -abs(math.sin(a))*7)

def land_sq(t, tl):
    u = t - tl
    if u < 0 or u > 0.5: return 1.0
    return 1 - 0.22*math.exp(-u*9)*math.cos(u*30)

class Pose:
    def __init__(self, P):
        self.P = P; self.x = P.get('x', 0); self.y = P.get('y', 0); self.s = P.get('s', 1.0)
        self.f = P.get('face', 1); self.rot = P.get('rot', 0.0); self.lean = P.get('lean', 0.0)
        self.bob = P.get('bob', 0.0); self.sq = P.get('sq', 1.0); self.jit = P.get('jit', 0.0)
        self.cr, self.sr = math.cos(self.rot), math.sin(self.rot)
    def __call__(self, pts, upper=True):
        out = []
        for (x, y) in pts:
            if upper and y < -200: x += self.lean*(-y - 200)
            x *= self.f; y = y*self.sq + self.bob
            X = x*self.cr - y*self.sr; Y = x*self.sr + y*self.cr
            out.append((self.x + self.jit + X*self.s, self.y + Y*self.s))
        return out
    def p(self, x, y, upper=True): return self(((x, y),), upper)[0]

def _eye(T, Q, x, y, r, look=(0, 0), lid=0.0, blink=False, closed=False, skin=SKIN, tremble=0.0):
    if blink or closed:
        if closed:
            T.stroke(Q([(x - r*0.8 + 2*r*0.8*i/10, y + r*0.15 - math.sin(math.pi*i/10)*r*0.55) for i in range(11)]), lw=7)
        else:
            T.stroke(Q([(x - r, y), (x + r, y)]), lw=7)
        return
    T.shape(Q(ellipse_pts(x, y, r, r*1.08, 36)), '#ffffff', lw=7)
    lx = look[0]*Q.f   # look is in screen terms: +x = screen right
    px, py = x + lx*r*0.45 + tremble, y + look[1]*r*0.45
    X, Y = Q.p(px, py); T.dot(X, Y, r*0.14*Q.s)
    if lid > 0:
        yl = y - r*1.08 + lid*2*r
        T.shape(Q([(x - r*1.15, y - r*1.25), (x + r*1.15, y - r*1.25), (x + r*1.15, yl), (x - r*1.15, yl + r*0.08)]), skin, line=False)
        T.stroke(Q([(x - r*1.05, yl + r*0.08), (x + r*1.05, yl)]), lw=7)

def _mouth(T, Q, x, y, w, o=0.0, sm=0.0, lw=7):
    k = w*0.5
    if o < 0.07:
        T.stroke(Q([(x - w, y - sm*k), (x, y + sm*k*0.9), (x + w, y - sm*k)]), lw=lw); return
    h = o*w*1.25
    up = [(x - w + 2*w*i/10, y - sm*k*(1 - math.sin(math.pi*i/10)) - h*0.18*math.sin(math.pi*i/10)) for i in range(11)]
    dn = [(x + w - 2*w*i/12, y - sm*k*(1 - math.sin(math.pi*i/12)) + h*math.sin(math.pi*i/12)) for i in range(13)]
    pts = up + dn
    T.shape(Q(pts), '#5a1630', lw=lw)
    if o > 0.25:   # teeth + tongue (flat, drawn inside, no outline)
        T.shape(Q([(x - w*0.7, y - h*0.12), (x + w*0.7, y - h*0.12), (x + w*0.62, y + h*0.16), (x - w*0.62, y + h*0.16)]), '#ffffff', line=False, amp=0)
        T.shape(Q(ellipse_pts(x + w*0.12, y + h*0.78, w*0.5, h*0.25, 20)), '#ff7a90', line=False, amp=0)

def clicker(T, Q, hx, hy, press=0.0):
    T.shape(Q([(hx - 26, hy - 44), (hx + 26, hy - 44), (hx + 26, hy + 30), (hx - 26, hy + 30)]), '#8d96a3', shadow='#6c7482', shade_dir=(1, 0), shade_w=0.3, lw=6)
    T.shape(Q(ellipse_pts(hx, hy - 16 + press*4, 16, 14 - press*4, 20)), '#ff4fa3', lw=5)
    T.stroke(Q([(hx + 10, hy - 44), (hx + 16, hy - 70), (hx + 6, hy - 84)]), lw=5)
    X, Y = Q.p(hx + 6, hy - 88); T.dot(X, Y, 8*Q.s, '#4fd8ff')

def swim_ring(T, Q, y, front=True, rx=135, ry=40, thick=46):
    """front=False draws the back half (behind the body), True the front half"""
    a0, a1 = (math.pi, 2*math.pi) if not front else (0, math.pi)
    outer = ellipse_pts(0, y, rx + thick/2, ry + thick/2, 30, a0, a1)
    inner = ellipse_pts(0, y, rx - thick/2, ry - thick/2, 30, a1, a0)
    T.shape(Q(outer + inner), '#ff8a1f' if front else '#e06c0c', lw=7)
    if front:
        for a in (0.45, 1.55, 2.6):
            seg_o = ellipse_pts(0, y, rx + thick/2, ry + thick/2, 6, a, a + 0.35)
            seg_i = ellipse_pts(0, y, rx - thick/2, ry - thick/2, 6, a + 0.35, a)
            T.shape(Q(seg_o + seg_i), '#ffffff', lw=5)

def _arm(T, Q, sh, hand, bend, w, col, skin=SKIN, fist=False, hold=None, press=0.0):
    a = sh; b = (sh[0] + hand[0], sh[1] + hand[1])
    T.shape(Q(noodle_pts(a, b, bend, w, w*0.9)), col, lw=7)
    T.shape(Q(ellipse_pts(b[0], b[1] + 4, w*0.78, w*0.72, 20)), skin, lw=7)
    if hold == 'clicker': clicker(T, Q, b[0] + 4, b[1] - 18, press)

def _legs(T, Q, P, hipx, hipy, w, col, shoe, shoe_s):
    for sx, lg in ((-1, P.get('legL', (0, 0))), (1, P.get('legR', (0, 0)))):
        hip = (sx*hipx, hipy); ank = (sx*(hipx + 10) + lg[0], -22 + lg[1])
        T.shape(Q(noodle_pts(hip, ank, sx*-5, w, w*0.9), upper=False), col, lw=7)
        sh = [(ank[0] - 30, ank[1] + 24), (ank[0] - 28, ank[1] + 2), (ank[0] + 6, ank[1] - 4), (ank[0] + 44, ank[1] + 8), (ank[0] + 46, ank[1] + 24)]
        T.shape(Q(sh, upper=False), shoe, shadow=shoe_s, shade_dir=(0, 1), shade_w=0.4, lw=7)

def draw_nova(T, P):
    Q = Pose(P); t = P.get('t', 0)
    br = 1 + 0.01*math.sin(t*2.5)
    HY = -560*br + P.get('nod', 0)
    armB = P.get('armB', ((40, 170), 18)); armF = P.get('armF', ((-30, 170), -18))
    # back arm
    _arm(T, Q, (70, -380), armB[0], armB[1], 32, '#ececf4')
    if P.get('legs', True): _legs(T, Q, P, 34, -215, 36, '#3d7bfd', '#2a2140', '#14101f')
    # body: white lab shirt + belt
    T.shape(Q([(-95, -200), (-80, -410), (80, -410), (95, -200)]), '#ffffff', shadow='#d6d3e6', shade_dir=(1, 0), shade_w=0.3, lw=8)
    T.shape(Q(rect(-93, -262, 186, 30)), '#6b4a2f', lw=7)
    T.shape(Q(rect(-18, -264, 36, 34)), '#ffd166', lw=6)
    if P.get('ring'): swim_ring(T, Q, -250, True)
    # front arm
    _arm(T, Q, (-72, -385), armF[0], armF[1], 32, '#ffffff', hold=P.get('hold'), press=P.get('press', 0))
    # head
    tilt = P.get('headtilt', 0.0)
    hq = lambda pts: Q([(x + (y - HY)*tilt, y) for x, y in pts])
    hq.f, hq.s, hq.p = Q.f, Q.s, (lambda x, y: hq([(x, y)])[0])
    T.shape(hq(ellipse_pts(0, HY, 150, 145, 56)), SKIN, shadow=SKIN_S, shade_dir=(1, 0.3), shade_w=0.22, lw=8)
    spikes = []
    for i in range(9):
        a = math.pi*(1.05 + i*0.11)
        spikes += [(150*math.cos(a), HY - 10 + 145*math.sin(a)), (225*math.cos(a + 0.055), HY - 30 + 215*math.sin(a + 0.055))]
    spikes += [(150*math.cos(math.pi*2.04), HY - 10 + 145*math.sin(math.pi*2.04)), (120, HY - 40), (-120, HY - 40)]
    T.shape(hq(spikes), '#3a3f8f', shadow='#2a2d6b', shade_dir=(1, 0.2), shade_w=0.18, lw=8)
    look = P.get('look', (0, 0)); bl = P.get('blink', False)
    for ex in (-58, 52):
        _eye(T, hq, ex, HY + 25, 42, look, P.get('lid', 0), bl, P.get('closed', False))
        T.shape(hq(ellipse_pts(ex, HY + 25, 57, 59, 40)), None, lw=7)
    T.stroke(hq([(-1, HY + 25), (-6, HY + 20)]), lw=7)
    b = P.get('brow', 0.5)
    T.stroke(hq([(-102, HY - 52 + b*6), (-28, HY - 58 - b*10)]), lw=9)
    T.stroke(hq([(20, HY - 60 - b*10), (100, HY - 52 + b*6)]), lw=9)
    _mouth(T, hq, -8, HY + 96, 38, P.get('o', 0), P.get('sm', 0.4))
    if P.get('sweat'):
        T.shape(hq([(-150, HY - 70), (-138, HY - 44), (-150, HY - 34), (-162, HY - 44)]), '#bfe9ff', lw=6)

def draw_kiko(T, P):
    Q = Pose(P); t = P.get('t', 0)
    br = 1 + 0.012*math.sin(t*3)
    HY = -520*br + P.get('nod', 0)
    armB = P.get('armB', ((40, 160), 18)); armF = P.get('armF', ((-30, 160), -18))
    _arm(T, Q, (66, -350), armB[0], armB[1], 30, '#e0700f')
    if P.get('ring'): swim_ring(T, Q, -235, False, 125, 36, 42)
    if P.get('legs', True): _legs(T, Q, P, 30, -200, 34, '#2b4c7e', '#ffffff', '#d0d0dc')
    T.shape(Q([(-90, -190), (-72, -380), (72, -380), (90, -190)]), '#ff8a1f', shadow='#d96a0c', shade_dir=(1, 0), shade_w=0.3, lw=8)
    T.shape(Q([(-70, -372), (-45, -382), (92, -212), (80, -186)]), '#2b3f8f', lw=7)
    if P.get('ring'): swim_ring(T, Q, -235, True, 125, 36, 42)
    _arm(T, Q, (-66, -355), armF[0], armF[1], 30, '#ff8a1f')
    tilt = P.get('headtilt', 0.0)
    hq = lambda pts: Q([(x + (y - HY)*tilt, y) for x, y in pts])
    hq.f, hq.s, hq.p = Q.f, Q.s, (lambda x, y: hq([(x, y)])[0])
    T.shape(hq(ellipse_pts(0, HY, 140, 135, 56)), SKIN, shadow=SKIN_S, shade_dir=(1, 0.3), shade_w=0.22, lw=8)
    cap = ellipse_pts(0, HY - 30, 145, 120, 30, math.pi*1.02, math.pi*1.98)
    T.shape(hq(cap + [(140, HY - 20), (-140, HY - 20)]), '#1e7a4c', shadow='#145a37', shade_dir=(1, 0.2), shade_w=0.2, lw=8)
    T.shape(hq([(60, HY - 40), (230, HY - 30), (225, HY - 8), (70, HY - 14)]), '#1e7a4c', lw=8)
    X, Y = hq.p(0, HY - 150); T.dot(X, Y, 14*Q.s, '#ffffff')
    look = P.get('look', (0, 0)); tr = P.get('tremble', 0.0)
    for ex in (-38, 38):
        _eye(T, hq, ex, HY + 35, P.get('er', 40), look, P.get('lid', 0), P.get('blink', False), P.get('closed', False), tremble=tr)
    b = P.get('brow', -0.6)   # worried by default
    T.stroke(hq([(-82, HY - 10 + b*8), (-22, HY - 16 - b*4)]), lw=8)
    T.stroke(hq([(22, HY - 16 - b*4), (82, HY - 10 + b*8)]), lw=8)
    _mouth(T, hq, 5, HY + 100, 26 if P.get('o', 0) < 0.3 else 30, P.get('o', 0), P.get('sm', -0.4))
    if P.get('sweat'):
        k = (t*1.5) % 1
        for (dx, dy) in ((-150, -40), (150, -10)):
            T.shape(hq([(dx, HY + dy - 26 + k*30), (dx + 13, HY + dy + k*30), (dx, HY + dy + 12 + k*30), (dx - 13, HY + dy + k*30)]), '#bfe9ff', lw=6)


# ------------------------------------------------------------------ extra cast (same rig rules)
def draw_baby(T, P):
    """Baby Kiko: huge head, tiny body, orange onesie, mini green cap (his silhouette cue)."""
    Q = Pose(P); t = P.get('t', 0)
    br = 1 + 0.015*math.sin(t*3.2)
    HY = -250*br + P.get('nod', 0)
    armB = P.get('armB', ((26, 60), 10)); armF = P.get('armF', ((-26, 60), -10))
    _arm(T, Q, (34, -150), armB[0], armB[1], 22, '#e0700f')
    if P.get('legs', True):
        for sx, lg in ((-1, P.get('legL', (0, 0))), (1, P.get('legR', (0, 0)))):
            hip = (sx*22, -80); ank = (sx*28 + lg[0], -14 + lg[1])
            T.shape(Q(noodle_pts(hip, ank, sx*-4, 26, 24), upper=False), '#ff8a1f', lw=7)
            T.shape(Q(ellipse_pts(ank[0] + sx*4, ank[1] + 6, 18, 12, 14), upper=False), SKIN, lw=6)
    T.shape(Q(ellipse_pts(0, -110, 62, 62, 30)), '#ff8a1f', shadow='#d96a0c', shade_dir=(1, 0), shade_w=0.3, lw=8)
    if P.get('diaper'):
        T.shape(Q([(-58, -95), (58, -95), (40, -48), (0, -40), (-40, -48)]), '#ffffff', lw=7)
    else:
        T.shape(Q(ellipse_pts(0, -112, 18, 18, 14)), '#2b3f8f', lw=5)   # onesie badge
    _arm(T, Q, (-34, -152), armF[0], armF[1], 22, '#ff8a1f', hold=P.get('hold'))
    if P.get('hold') == 'rattle':
        hx, hy = -34 + armF[0][0], -152 + armF[0][1]
        T.stroke(Q([(hx, hy), (hx - 6, hy - 40)]), lw=9, col='#ffd43b')
        T.shape(Q(ellipse_pts(hx - 8, hy - 58, 22, 22, 16)), '#ff4fa3', lw=6)
    hq = lambda pts: Q(pts); hq.f, hq.s, hq.p = Q.f, Q.s, Q.p
    T.shape(hq(ellipse_pts(0, HY, 130, 122, 56)), SKIN, shadow=SKIN_S, shade_dir=(1, 0.3), shade_w=0.22, lw=8)
    if P.get('cap', True):
        cap = ellipse_pts(0, HY - 40, 112, 88, 24, math.pi*1.05, math.pi*1.95)
        T.shape(hq(cap + [(108, HY - 34), (-108, HY - 34)]), '#1e7a4c', shadow='#145a37', shade_dir=(1, 0.2), shade_w=0.2, lw=7)
        T.shape(hq([(50, HY - 48), (170, HY - 40), (166, HY - 24), (56, HY - 30)]), '#1e7a4c', lw=7)
    else:   # single curl of hair
        T.stroke(hq([(0, HY - 122), (12, HY - 150), (-8, HY - 160), (-14, HY - 140)]), lw=7)
    look = P.get('look', (0, 0))
    for ex in (-36, 36):
        _eye(T, hq, ex, HY + 28, P.get('er', 32), look, P.get('lid', 0), P.get('blink', False), P.get('closed', False), tremble=P.get('tremble', 0))
    b = P.get('brow', 0.0)
    if P.get('angry'):
        T.stroke(hq([(-72, HY - 18), (-14, HY - 2)]), lw=8); T.stroke(hq([(14, HY - 2), (72, HY - 18)]), lw=8)
    else:
        T.stroke(hq([(-66, HY - 8 + b*6), (-18, HY - 14 - b*4)]), lw=7); T.stroke(hq([(18, HY - 14 - b*4), (66, HY - 8 + b*6)]), lw=7)
    if P.get('paci'):
        T.shape(hq(ellipse_pts(0, HY + 84, 30, 20, 18)), '#4fd8ff', lw=6); T.shape(hq(ellipse_pts(0, HY + 84, 10, 10, 10)), '#ffffff', lw=5)
    else:
        _mouth(T, hq, 0, HY + 80, 22, P.get('o', 0), P.get('sm', 0.5), lw=6)
    for cx in (-80, 80):   # rosy cheeks (flat)
        X, Y = hq.p(cx, HY + 62); T.dot(X, Y, 14*Q.s, '#ffb3c1')
    if P.get('cape'):
        T.shape(Q([(-40, -165), (40, -165), (150, -60 + 15*math.sin(tq(t)*10)), (-10, -30)]), '#ff3b5c', lw=7)

def draw_adult(T, P, cfg):
    """generic adult in the same style. cfg: shirt, pants, skirt, hair ('bun','bald','curly'), hair_col, mustache, glasses, h (height scale)"""
    Q = Pose(P); t = P.get('t', 0)
    br = 1 + 0.01*math.sin(t*2.3 + cfg.get('ph', 0))
    HY = -560*br + P.get('nod', 0)
    armB = P.get('armB', ((40, 170), 18)); armF = P.get('armF', ((-30, 170), -18))
    sh, sh_s = cfg['shirt'], cfg.get('shirt_s', '#00000000')
    _arm(T, Q, (70, -380), armB[0], armB[1], 32, cfg.get('sleeve_b', sh))
    if P.get('legs', True):
        _legs(T, Q, P, 34, -215, 36, cfg.get('pants', '#555577'), cfg.get('shoe', '#2a2140'), '#14101f')
    if cfg.get('skirt'):
        T.shape(Q([(-95, -200), (-80, -410), (80, -410), (95, -200)]), sh, lw=8)
        T.shape(Q([(-90, -300), (90, -300), (135, -150), (-135, -150)]), cfg['skirt'], shadow=cfg.get('skirt_s'), shade_dir=(1, 0), shade_w=0.3, lw=8)
    else:
        T.shape(Q([(-95, -200), (-80, -410), (80, -410), (95, -200)]), sh, shadow=cfg.get('shirt_s'), shade_dir=(1, 0), shade_w=0.3, lw=8)
    if cfg.get('cardigan'):
        T.shape(Q([(-20, -410), (20, -410), (6, -205), (-6, -205)]), cfg['cardigan'], lw=6)
    _arm(T, Q, (-72, -385), armF[0], armF[1], 32, sh, hold=P.get('hold'))
    hq = lambda pts: Q(pts); hq.f, hq.s, hq.p = Q.f, Q.s, Q.p
    hair = cfg.get('hair'); hc = cfg.get('hair_col', '#5a3a2a')
    if hair == 'bun':
        T.shape(hq(ellipse_pts(0, HY - 165, 62, 55, 30)), hc, lw=8)
    T.shape(hq(ellipse_pts(0, HY, 148, 143, 56)), SKIN, shadow=SKIN_S, shade_dir=(1, 0.3), shade_w=0.22, lw=8)
    if hair == 'bun':
        T.shape(hq(ellipse_pts(0, HY - 50, 152, 100, 30, math.pi*1.0, math.pi*2.0) + [(140, HY - 30), (60, HY - 70), (-60, HY - 70), (-140, HY - 30)]), hc, shadow=cfg.get('hair_s'), shade_dir=(1, 0.2), shade_w=0.2, lw=8)
    elif hair == 'curly':
        bumps = []
        for i in range(11):
            a = math.pi*(1.0 + i*0.1); bumps.append((165*math.cos(a), HY - 20 + 150*math.sin(a)))
        T.shape(hq(bumps + [(130, HY - 40), (-130, HY - 40)]), hc, lw=8)
        for i in range(10):
            a = math.pi*(1.05 + i*0.1); X, Y = hq.p(165*math.cos(a), HY - 20 + 150*math.sin(a))
            T.shape(ellipse_pts(X, Y, 30*Q.s, 30*Q.s, 14), hc, lw=7)
    elif hair == 'bald':
        for sx in (-1, 1):
            T.shape(hq([(sx*140, HY - 10), (sx*160, HY - 40), (sx*165, HY + 20), (sx*145, HY + 40)]), '#e8e8ef', lw=6)
    look = P.get('look', (0, 0))
    for ex in (-52, 52):
        _eye(T, hq, ex, HY + 22, 38, look, P.get('lid', cfg.get('lid', 0)), P.get('blink', False), P.get('closed', False))
        if cfg.get('glasses'): T.shape(hq(ellipse_pts(ex, HY + 22, 50, 48, 30)), None, lw=6)
    b = P.get('brow', 0.3)
    T.stroke(hq([(-92, HY - 46 + b*6), (-24, HY - 52 - b*10)]), lw=8); T.stroke(hq([(24, HY - 52 - b*10), (92, HY - 46 + b*6)]), lw=8)
    if cfg.get('lashes'):
        for ex in (-52, 52):
            T.stroke(hq([(ex + 30, HY - 10), (ex + 44, HY - 22)]), lw=6)
    if cfg.get('mustache'):
        T.shape(hq([(-70, HY + 70), (-20, HY + 56), (0, HY + 66), (20, HY + 56), (70, HY + 70), (40, HY + 86), (0, HY + 78), (-40, HY + 86)]), '#e8e8ef', lw=7)
        _mouth(T, hq, 0, HY + 104, 30, P.get('o', 0), P.get('sm', 0.3))
    else:
        _mouth(T, hq, 0, HY + 92, 34, P.get('o', 0), P.get('sm', 0.5))

MOM = dict(shirt='#ff6fa8', shirt_s='#e0508c', skirt='#7b5cff', skirt_s='#5f43d6', pants='#f7f5ef', hair='bun', hair_col='#7a3b2e', hair_s='#5c2a20', lashes=True, shoe='#ff4f7a')
DAD = dict(shirt='#3fbf9f', shirt_s='#2a9a7e', pants='#3b4a7a', hair='curly', hair_col='#2a1f2e', glasses=False)
GRANDPA = dict(shirt='#c9a27a', shirt_s='#a8835e', cardigan='#8a5a3c', pants='#6b6b80', hair='bald', mustache=True, glasses=True, lid=0.25)
