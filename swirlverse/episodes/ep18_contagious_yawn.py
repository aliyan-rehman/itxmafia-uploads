"""EP18 - Why are YAWNS contagious? (Short, MIND HACK format with a parallel-world twist, built with shortkit)
Format: MIND HACK (psychology) + portal twist ("every yawn is 100% contagious" world). Topic family: brain / behaviour.
Gate score: curiosity 5, relatable 5, visual 4, fact certainty 4, freshness 3 (common question already covered by big
explainer channels; our angle = the dog study + a parallel world where every yawn spreads through the whole family) = 21/25.
Facts (checked, 2026-11-27):
- In controlled studies about 40-60% of typical volunteers yawned after watching someone yawn in a video
  (Live Science, "Why is yawning contagious?"); "about 45-60% of the time" (National Geographic, 2008). Said as "about half".
- People (and animals) are more likely to catch yawns from familiar individuals (family, friends) than from strangers:
  the "familiarity bias" (Live Science, quoting Andrew Gallup); Houston Methodist (2021) says the same.
- Dogs catch human yawns: 21 of 29 dogs (72%) yawned when an unfamiliar experimenter yawned, none when the person only
  opened their mouth (Joly-Mascheroni et al. 2008, Biology Letters, via National Geographic); a University of Tokyo PLOS ONE
  study found dogs catch their owner's yawns more than a stranger's (Smithsonian; Live Science).
- Why is still debated: one idea is that yawning helps cool the brain (Gallup et al. 2007, Evolutionary Psychology, via Live
  Science / Smithsonian); another is that contagious yawning keeps a group alert and in sync (Live Science). The empathy
  link is mixed, so the video does not claim it.
Sources: Live Science; National Geographic (Biology Letters 2008); Smithsonian Magazine; Houston Methodist.
No real people, no brands; the dog is a generic drawing."""
import math
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Nova... why are yawns so contagious?!", gap=0.3),
    dict(who=N, text="Ha! You just caught mine. About half of people yawn after watching someone yawn.", gap=0.3),
    dict(who=N, text="And you catch yawns more from family and friends than from strangers.", gap=0.3),
    dict(who=K_, text="Can animals catch them too?", gap=0.25),
    dict(who=N, text="Yes! In one study, twenty one out of twenty nine dogs caught a person's yawn.",
         cap="Yes! In one study, 21 out of 29 dogs caught a person's yawn.", gap=0.3),
    dict(who=N, text="Why? Scientists still debate it. Maybe yawns cool the brain, and keep a group alert together.", gap=0.3),
    dict(who=N, text="But in this parallel world, every single yawn is contagious.", gap=0.3),
    dict(who=K_, text="One yawn, and the whole family yawns!", gap=0.35),
    dict(who=N, text="Did you yawn while watching this? Yes, or no? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep18_contagious_yawn', our_set='room', par_set='room',
    title="Why Are YAWNS Contagious? \U0001F300 #Swirlverse",
    description=("Why are yawns contagious? About half of people yawn after watching someone else yawn, and we catch yawns "
                 "more from family and friends than from strangers. Even dogs can catch a person's yawn! "
                 "But in this parallel world, every single yawn is contagious... \U0001F971\n"
                 "Did you yawn while watching? Comment yes or no \U0001F447\n\n"
                 "Real science: in controlled studies about 40-60% of people yawned after seeing a yawn video. "
                 "In a 2008 study (Biology Letters), 21 of 29 dogs yawned after a person yawned, but not when the person only opened their mouth. "
                 "Why it spreads is still debated: one idea is that yawning helps cool the brain, another that it keeps a group alert together. "
                 "Sources: Live Science, National Geographic, Smithsonian.\n\n"
                 "#shorts #science #yawning #psychology #brain #swirlverse"),
    tags=['why are yawns contagious', 'contagious yawning', 'why do we yawn', 'yawning', 'dogs catch yawns',
          'brain cooling', 'psychology', 'brain science', 'mind hack', 'parallel world', 'science shorts', 'swirlverse', 'animation'],
    topic='why yawns are contagious / contagious yawning (40-60% of people, familiarity bias, 21 of 29 dogs, brain-cooling idea; every-yawn-contagious world)',
    category='brain / psychology',
    hook='kiko mid-yawn question cold open -> stats -> dogs -> portal twist (yawn wave)',
)
DROPS = []

# ---------------------------------------------------------------- helpers
def yawnk(u, d=1.6):
    """0 -> 1 -> 0 yawn curve over d seconds starting at u=0"""
    if u <= 0 or u >= d: return 0.0
    x = u/d
    return clamp(math.sin(math.pi*x)*1.25)

def yawn_pose(k, base='neutral'):
    """open mouth wide, eyes shut, arms stretching up while yawning"""
    if k < 0.08: return pose(base, 'rest')
    P = pose(base, 'rest', o=1.0 + 0.7*k, closed=k > 0.45, brow=0.9*k, sm=0.0)
    if k > 0.3:
        a = (k - 0.3)/0.7
        P.update(armF=((-40 - 80*a, 40 - 260*a), 25), armB=((40 + 80*a, 40 - 260*a), -25))
    return P

DOG, DOG_S, EAR = '#d9a066', '#b97f48', '#8a5a33'
def dog(T, x, y, s=1.0, k=0.0, t=0.0, body=True):
    """a generic friendly dog; (x, y) = paws on the floor; k = yawn amount"""
    if body:
        T.shape(ellipse_pts(x + 60*s, y - 120*s, 150*s, 85*s, 32), DOG, shadow=DOG_S, shade_dir=(1, 0.4), shade_w=0.3, lw=8)
        for lx in (-40, 20, 110, 170):
            T.shape(rect(x + lx*s, y - 80*s, 34*s, 80*s), DOG, lw=6)
        wag = math.sin(tq(t)*10)*0.4
        T.stroke([(x + 200*s, y - 150*s), (x + 250*s, y - (200 + 40*wag)*s), (x + 270*s, y - (250 + 20*wag)*s)], lw=12*s + 4, col=DOG_S)
    dog_head(T, x - 60*s, y - 230*s, s, k)

def dog_head(T, hx, hy, s=1.0, k=0.0, col=DOG, glow=False):
    if glow: T.glow(hx, hy, 120*s, '#ffe066', ((1.5, 0.18), (1.2, 0.3)))
    for sx in (-1, 1):   # floppy ears
        T.shape([(hx + sx*70*s, hy - 70*s), (hx + sx*125*s, hy - 40*s), (hx + sx*120*s, hy + 60*s), (hx + sx*80*s, hy + 50*s)], EAR, lw=6)
    T.shape(ellipse_pts(hx, hy, 100*s, 95*s, 36), col, shadow=mixc(col, '#000000', 0.18), shade_dir=(1, 0.4), shade_w=0.25, lw=7)
    T.shape(ellipse_pts(hx, hy + 50*s, 62*s, 45*s, 28), '#f6e2c4', lw=6)   # snout
    T.shape(ellipse_pts(hx, hy + 25*s, 20*s, 14*s, 16), '#2a1a14', lw=4)    # nose
    for ex in (-38, 38):
        if k > 0.45: T.stroke([(hx + (ex - 16)*s, hy - 22*s), (hx + ex*s, hy - 16*s), (hx + (ex + 16)*s, hy - 22*s)], lw=max(3, 6*s))
        else: T.dot(hx + ex*s, hy - 20*s, 13*s, '#2a1a14')
    if k > 0.08:
        mh = 70*s*k
        T.shape(ellipse_pts(hx, hy + 70*s + mh*0.5, 38*s, mh*0.6 + 6*s, 24), '#5a1630', lw=6)
        T.shape(ellipse_pts(hx, hy + 70*s + mh*0.9, 24*s, mh*0.25 + 3*s, 18), '#ff7a90', line=False, amp=0)
    else:
        T.stroke([(hx - 26*s, hy + 70*s), (hx, hy + 80*s), (hx + 26*s, hy + 70*s)], lw=max(3, 6*s))

def simple_brain(T, x, y, s=1.0, col='#ffb3c8', shade='#f08fae'):
    pts = []
    for i in range(48):
        a = 2*math.pi*i/48; r = 1 + 0.06*math.sin(9*a)
        pts.append((x + 300*s*r*math.cos(a), y + 200*s*r*math.sin(a)*(1 if math.sin(a) < 0 else 0.85)))
    T.shape(pts, col, shadow=shade, shade_dir=(1, 0.4), shade_w=0.2, lw=8)
    for k in range(5):
        cx = x - 220*s + k*110*s
        T.stroke([(cx, y - 120*s), (cx + 30*s, y - 60*s), (cx - 10*s, y), (cx + 30*s, y + 60*s)], lw=6, col=shade)
    T.shape([(x + 80*s, y + 130*s), (x + 140*s, y + 160*s), (x + 120*s, y + 260*s), (x + 80*s, y + 250*s)], col, lw=7)

# ---------------------------------------------------------------- shots
def sh_cold(K, T, t, u):
    """Kiko yawns huge while asking; the question pops at once"""
    T.cx, T.cy, T.z = 540, 980, 1.15 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    kk = yawnk(u + 0.35, 2.2)
    P = yawn_pose(kk, 'neutral')
    if kk < 0.08: P = pose('confused', 'shrug')
    K.kiko(T, t, **P) if kk < 0.08 else K.kiko(T, t, **dict(P, o=P['o']))
    nk = yawnk(u - 1.3, 1.8)   # Nova catches it
    K.nova(T, t, **(yawn_pose(nk, 'happy') if nk > 0.08 else pose('smug', 'rest')))
    label(T.c, 'WHY ARE YAWNS', 540, 330, 112, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'CONTAGIOUS?', 540, 480, 130, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_nova_caught(K, T, t, u):
    """Nova close-up mid-yawn: 'you just caught mine'"""
    T.cx, T.cy, T.z = 800, 1020, 2.0
    K.world(T, t, False)
    k = yawnk(u + 0.4, 1.4)
    K.nova(T, t, **(yawn_pose(k, 'happy') if k > 0.08 else pose('smug', 'finger_up')))
    kin(T.c, t, 'CAUGHT IT!', K.L(1) + 0.15, 540, 360, 140, '#ffd43b', -0.05)

def sh_family(K, T, t, u):
    """yawns spread more between family & friends than strangers (no invented numbers: MORE vs LESS)"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t)
    label(T.c, 'WHO DO YOU CATCH', 540, 300, 90, '#ffffff', -0.02, back(u/0.3, 1.4))
    label(T.c, 'YAWNS FROM?', 540, 420, 100, '#ffd43b', 0.02, back((u - 0.1)/0.3, 1.4))
    for i, (name, h, col, cfg) in enumerate((('FAMILY & FRIENDS', 540, '#7dff9a', MOM), ('STRANGERS', 260, '#c9b8ff', None))):
        k = ease((u - 0.4 - i*0.4)/0.8); x = 300 + i*480; hh = h*k
        T.shape(rect(x - 120, 1400 - hh, 240, max(hh, 2)), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=8)
        label(T.c, name, x, 1490, 54 if len(name) < 12 else 640/len(name)*1.6, '#ffffff', 0, 1, FONT, 10)
        if k > 0.6: label(T.c, 'MORE' if i == 0 else 'LESS', x, 1400 - hh/2 + 30, 70 if i == 0 else 60, '#ffffff', 0, back((k - 0.6)/0.4, 1.5))
    # tiny family heads yawning on top of the tall bar
    yk = yawnk(u - 1.2, 1.6)
    P = yawn_pose(yk, 'happy'); P.update(x=240, y=1400 - 540*ease((u - 0.4)/0.8) - 10, s=0.32, face=1)
    draw_adult(T, dict(P, t=t), MOM)
    P2 = yawn_pose(yawnk(u - 1.5, 1.6), 'happy'); P2.update(x=360, y=P['y'], s=0.32, face=-1)
    draw_adult(T, dict(P2, t=t), DAD)

def sh_dogs(K, T, t, u):
    """29 dog faces; 21 of them light up and yawn, counter runs to 21/29"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.01*u
    board(T, t, '#1f2a4a', '#2c3a63')
    label(T.c, 'DOGS vs A YAWN', 540, 300, 100, '#ffffff', -0.03, back(u/0.3, 1.4))
    order = [0, 7, 13, 2, 22, 9, 16, 27, 4, 11, 19, 25, 6, 14, 1, 21, 28, 8, 17, 24, 12]   # 21 yawners
    dur = 2.6; n = int(clamp((u - 0.5)/dur)*21 + 0.0001)
    on = set(order[:n])
    for idx in range(29):
        r, cidx = divmod(idx, 6)
        cols = 6 if r < 4 else 5
        x = 140 + cidx*160 + (80 if r == 4 else 0); y = 560 + r*190
        if idx in on:
            j = order.index(idx); kk = 0.6 + 0.4*math.sin(tq(t)*3 + j)
            dog_head(T, x, y, 0.62, kk, '#ffd27a', glow=True)
        else:
            dog_head(T, x, y, 0.62, 0.0, '#a89a8a')
    label(T.c, f'{n} / 29', 540, 1560, 150, '#ffd43b', -0.03, back((u - 0.5)/0.3, 1.5))
    label(T.c, 'caught the yawn (2008 study)', 540, 1680 - 40, 48, '#c9b8ff', 0, back((u - 0.8)/0.3, 1.3), FONT, 10)

def sh_dog_kiko(K, T, t, u):
    """Kiko asks; a dog in the room"""
    T.cx, T.cy, T.z = 420, 1060, 1.35
    K.world(T, t, False)
    K.kiko(T, t, **pose('confused', 'point', look=(0.8, 0.3)))
    dog(T, 640, FEET, 0.9, yawnk(u - 0.9, 1.6), t)
    kin(T.c, t, 'DOGS TOO?', K.L(3) + 0.3, 540, 380, 140, '#ffd43b', -0.04)

def sh_brain(K, T, t, u):
    """why? still debated: brain cooling idea + group alert idea"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t)
    simple_brain(T, 540, 900, 1.05)
    for i in range(5):   # cool air swooshes in
        ph = (u*0.8 + i/5) % 1
        y = 760 + i*60; x0 = 60 + ph*260
        T.stroke([(x0, y), (x0 + 80, y - 20), (x0 + 160, y)], lw=10, col='#7fd0ff', alpha=1 - ph*0.6)
    kin(T.c, t, 'COOL THE BRAIN?', K.S(5) + 0.9, 540, 380, 110, '#7fd0ff', -0.03)
    kin(T.c, t, 'KEEP THE GROUP ALERT?', K.at(5, 0.6), 540, 1300, 82, '#7dff9a', 0.02)
    if u > K.at(5, 0.25) - K.L(5):
        k = back((u - (K.at(5, 0.25) - K.L(5)))/0.25, 1.8)
        c = T.c; c.save(); c.translate(540, 1500); c.rotate(-0.1); c.scale(k, k)
        label(c, 'STILL DEBATED', 0, 0, 96, '#ff4fa3', 0, 1); c.restore()

FAM = [('g', GRANDPA, 150), ('m', MOM, 345), ('k', None, 540), ('d', DAD, 735), ('n', None, 930)]
def yawn_line(K, T, t, u, start=0.3, step=0.45, s=0.6):
    for i, (who, cfg, x) in enumerate(FAM):
        k = yawnk(u - start - i*step, 1.7)
        P = yawn_pose(k, 'happy'); P.update(x=x, y=FEET, s=s, face=1 if x < 540 else -1)
        if who == 'k': K.kiko(T, t, **P)
        elif who == 'n': K.nova(T, t, **P)
        else: draw_adult(T, dict(P, t=t, blink=False), cfg)
        if k > 0.5: lx, ly = T.xf((x, FEET - 560*s - 190*s)); label(T.c, 'YAWN!', lx, ly, 52, '#ffd43b', (-0.1, 0.1)[i % 2], back((k - 0.5)/0.3, 1.5))

def sh_wave(K, T, t, u):
    """parallel world: one yawn races down the whole family"""
    T.cx, T.cy, T.z = 540, 1290, 1.08 + 0.02*u
    K.world(T, t, True)
    yawn_line(K, T, t, u, 0.2, 0.42)
    kin(T.c, t, '100% CONTAGIOUS', K.S(6) + 0.6, 540, 420, 104, '#ff4fa3', -0.04)

def sh_wave2(K, T, t, u):
    """...and it keeps going around again (plus the dog)"""
    T.cx, T.cy, T.z = 540, 1290, 1.1 + 0.02*u
    K.world(T, t, True)
    yawn_line(K, T, t, u, 0.0, 0.32)
    dog(T, 830, FEET + 60, 0.42, yawnk(u - 1.7, 1.5), t)
    kin(T.c, t, 'NONSTOP YAWNS!', K.S(7) + 0.2, 540, 420, 120, '#ffd43b', -0.04)

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.custom(K.L(1), sh_nova_caught, sfx='swoop')
    K.stat(K.at(1, 0.4), '~50%', 'CATCH THE YAWN', 'about 40-60% in lab studies')
    K.custom(K.L(2), sh_family, sfx='pop')
    K.custom(K.L(3), sh_dog_kiko, sfx='boing')
    K.custom(K.L(4), sh_dogs, sfx='blip')
    K.custom(K.L(5), sh_brain, sfx='swoop')
    K.hook(K.at(5, 0.75), portal_line=5, portal_f=0.9)
    K.arrive(tag_text='WORLD #18 · EVERY YAWN SPREADS')
    K.custom(K.at(6, 0.35), sh_wave, sfx='pop')
    K.custom(K.L(7), sh_wave2, sfx='boing')
    K.end(K.L(8), poll=('YES, I YAWNED', 'NO YAWN'))

def thumbnail(c, K):
    """huge 'TRY NOT TO YAWN' challenge (the video really ends asking if you yawned), giant yawning Kiko, yawning dog"""
    burst(c, W, H, 540, 1150, '#ffe9a8', '#3b1f8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    P = yawn_pose(1.0, 'neutral'); P.update(x=330, y=2280, s=1.75, face=1, jit=0, blink=False)
    K.kiko(T, 1.0, **P)
    dog(T, 800, 1880, 0.95, 1.0, 0.0)
    big_text(c, 'TRY NOT TO', 540, 250, 140, max_w=980)
    big_text(c, 'YAWN!', 540, 470, 230, hl=0, hl_col='#ff4fa3', max_w=1010)
    emoji_burst(c, 820, 760, 150, 'DOGS TOO?!', '#ff2d55', 0.2)
    arrow(c, 860, 930, 760, 1470, '#ffd43b', 26)
