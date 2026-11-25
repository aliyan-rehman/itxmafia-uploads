"""EP14 - Why can't you TICKLE yourself? (Short, WHY format with a parallel-world twist, built with shortkit)
Format: WHY (everyday mystery) + portal twist. Gate score: curiosity 5, relatable 5, visual 4, fact certainty 5, freshness 3 = 22/25.
Facts (checked):
- When you move, your brain predicts the sensations the movement will cause and turns down (attenuates) the response to
  self-produced touch; the cerebellum is thought to make this prediction (Britannica; Scientific American Q&A by
  Sarah-Jayne Blakemore, UCL; Blakemore, Frith & Wolpert 1999).
- Blakemore, Frith & Wolpert (1999, J. Cognitive Neuroscience 11:551-559, UCL): people moved a robot arm with one hand and a
  second robot touched their other palm with soft foam. Adding a delay of 100-300 ms made the self-made touch feel more
  tickly; at 200 ms (and 300 ms) ratings were no longer significantly different from touch produced externally.
Sources: Britannica "Why can't you tickle yourself?"; Scientific American "Why can't a person tickle himself?";
Blakemore, Frith & Wolpert 1999 (J Cogn Neurosci); UCL news 2016 note on Blakemore's study."""
import math, numpy as np
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Why can't I tickle myself?", gap=0.3),
    dict(who=N, text="Your brain is a spoiler. When you move, it predicts what you'll feel.", gap=0.3),
    dict(who=N, text="That's thought to happen in the cerebellum, at the back.", gap=0.3),
    dict(who=N, text="So your own touch gets turned down. No surprise, no tickle.", gap=0.35),
    dict(who=N, text="In nineteen ninety nine, scientists tested it with a robot... and a tiny delay.", cap="In 1999, scientists tested it with a robot... and a tiny delay.", gap=0.35),
    dict(who=N, text="So in this parallel world, every touch arrives zero point two seconds late.", cap="So in this parallel world, every touch arrives 0.2 seconds late.", gap=0.3),
    dict(who=K_, text="Wait... hee hee! I'm tickling myself!", gap=0.35),
    dict(who=N, text="In the test, that delay made it feel about as tickly as someone else's touch.", gap=0.35),
    dict(who=K_, text="Best. World. Ever!", gap=0.35),
    dict(who=N, text="Our world, or the delay world? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep14_tickle_yourself', our_set='room', par_set='room',
    title="Why Can't You TICKLE Yourself? \U0001F300 #Swirlverse",
    description=("Why can't you tickle yourself? Your brain is a spoiler: it predicts the feeling of your own touch and turns it down. "
                 "But in this parallel world, every touch arrives 0.2 seconds late... \U0001F602\n"
                 "Our world or the delay world? Comment below \U0001F447\n\n"
                 "Real science: in a 1999 UCL study (Blakemore, Frith & Wolpert), people tickled their own palm through a robot. "
                 "Adding a delay of about 0.2 s made it feel about as tickly as a touch from someone else. "
                 "The prediction is thought to come from the cerebellum.\n\n"
                 "#shorts #science #brain #tickle #psychology #swirlverse"),
    tags=['why cant you tickle yourself', 'tickle yourself', 'tickling science', 'brain science', 'cerebellum', 'parallel world',
          'what if', 'science shorts', 'psychology', 'swirlverse', 'animation'],
    topic='why you cannot tickle yourself / sensory prediction', category='senses/body', hook='kiko question cold open -> explain -> portal twist',
)
DROPS = []

# ---------------------------------------------------------------- props
def tickle_pose(t, laugh=False):
    """Kiko with both hands on his belly, fingers wiggling"""
    w = math.sin(tq(t)*18)*14
    P = pose('happy' if laugh else 'deadpan', 'rest', armF=((75 + w, 75), -40), armB=((-60 - w, 80), 40))
    if laugh:
        P.update(closed=True, sm=1.0, jit=jitter(t, 10), o=0.7 + 0.3*math.sin(tq(t)*20))
    return P

def wiggles(T, x, y, t, k=1.0):
    for i in range(3):
        a = -0.9 + i*0.9 + 0.2*math.sin(tq(t)*10 + i)
        r0, r1 = 70, 120
        T.stroke([(x + r0*math.cos(a)*k, y + r0*math.sin(a)*k), (x + r1*math.cos(a)*k, y + r1*math.sin(a)*k)], lw=8, col='#ffd43b')

def brain(T, x, y, s=1.0, glow=0.0, t=0.0, col='#ffb3c8', shade='#f08fae'):
    """side view of a brain; the front faces left, the cerebellum (striped, lower back) can glow"""
    pts = []
    for i in range(48):
        a = 2*math.pi*i/48; r = 1 + 0.06*math.sin(9*a)
        pts.append((x + 300*s*r*math.cos(a), y + 200*s*r*math.sin(a)*(1 if math.sin(a) < 0 else 0.8)))
    T.shape(pts, col, shadow=shade, shade_dir=(1, 0.4), shade_w=0.2, lw=8)
    for k in range(5):
        cx = x - 230*s + k*100*s
        T.stroke([(cx, y - 120*s), (cx + 30*s, y - 60*s), (cx - 10*s, y), (cx + 30*s, y + 60*s)], lw=6, col=shade)
    T.shape([(x + 60*s, y + 130*s), (x + 120*s, y + 140*s), (x + 100*s, y + 280*s), (x + 60*s, y + 270*s)], col, lw=7)
    cx, cy = x + 210*s, y + 150*s
    if glow > 0: T.glow(cx, cy, 110*s, '#ffe066', ((1.8, 0.18*glow), (1.3, 0.35*glow)))
    cc = mixc('#e98fb0', '#ffd43b', glow)
    T.shape(ellipse_pts(cx, cy, 120*s, 75*s, 30), cc, shadow=mixc(cc, '#000000', 0.15), shade_dir=(1, 0.5), shade_w=0.25, lw=7)
    for k in range(4):
        yy = cy - 45*s + k*30*s
        T.stroke([(cx - 95*s, yy), (cx - 30*s, yy + 8*s), (cx + 40*s, yy + 4*s), (cx + 100*s, yy - 6*s)], lw=5, col=mixc(cc, '#000000', 0.25))

def stopwatch(T, x, y, r, t, txt='0.2 s', col='#ff4fa3'):
    T.shape(rect(x - 22, y - r - 46, 44, 36), '#c9c9d6', lw=6)
    T.shape(ellipse_pts(x, y, r, r, 40), '#ffffff', shadow='#d9d9e6', shade_dir=(1, 0.4), shade_w=0.2, lw=9)
    a = -math.pi/2 + tq(t)*4
    T.stroke([(x, y), (x + r*0.75*math.cos(a), y + r*0.75*math.sin(a))], lw=8, col=col)
    label(T.c, txt, x, y + r + 90, 70, col, 0, 1)

def sh_cold(K, T, t, u):
    """Kiko tries to tickle himself, deadpan. Question on screen at once."""
    T.cx, T.cy, T.z = 540, 980, 1.15 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    K.kiko(T, t, **tickle_pose(t))
    wiggles(T, K.KIKO_X + 20, FEET - 0.92*290, t, 0.8)
    K.nova(T, t, **pose('excited', 'finger_up'))
    label(T.c, "WHY CAN'T YOU", 540, 330, 108, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'TICKLE YOURSELF?', 540, 480, 112, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))
    label(T.c, '...NOTHING', 300, 900, 60, '#ffffff', -0.05, back((u - 1.0)/0.3, 1.4))

def sh_spoiler(K, T, t, u):
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t)
    brain(T, 540, 900, 1.2, 0, t)
    # a speech bubble from the brain: "you'll feel THIS"
    k = back((u - 0.4)/0.3, 1.5)
    T.shape(ellipse_pts(540, 470, 330*k + 1, 120*k + 1, 40), '#ffffff', lw=8)
    if k > 0.5: label(T.c, 'SPOILER ALERT!', 540, 500, 76, '#ff2d55', 0, 1)
    kin(T.c, t, 'PREDICTS IT', K.at(1, 0.55), 540, 1380, 110, '#ffd43b', -0.04)

def sh_cerebellum(K, T, t, u):
    T.cx, T.cy, T.z = 640, 1000, 1.0 + 0.1*ease(u/2)
    board(T, t)
    g = ease((u - 0.6)/0.6)*(0.8 + 0.2*math.sin(t*6))
    brain(T, 540, 900, 1.2, g, t)
    label(T.c, 'CEREBELLUM', 760, 1300, 90, '#ffd43b', -0.03, back((u - 0.9)/0.3, 1.5))
    arrow(T.c, 760, 1220, 790, 1130, '#ffd43b', 20) if u > 1.0 else None
    label(T.c, 'FRONT', 230, 560, 48, '#c9b8ff', 0, 1, FONT, 10)
    label(T.c, 'BACK', 900, 560, 48, '#c9b8ff', 0, 1, FONT, 10)

def sh_volume(K, T, t, u):
    """touch volume meter turning down for your own touch"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t, '#1f2a4a', '#2c3a63')
    label(T.c, 'TOUCH VOLUME', 540, 330, 100, '#ffffff', -0.02, back(u/0.3, 1.4))
    rows = (("SOMEONE ELSE", 1.0, '#ff4fa3'), ('YOUR OWN HAND', 1.0 - 0.75*ease((u - 0.6)/0.9), '#7fd0ff'))
    for i, (name, v, col) in enumerate(rows):
        y = 700 + i*420
        label(T.c, name, 540, y - 130, 60, col, 0, 1, FONT, 10)
        for j in range(10):
            on = j < round(v*10)
            T.shape(rect(120 + j*86, y + 40 - j*14, 66, 120 + j*14), col if on else '#3a4670', lw=6)
    if u > 1.6: kin(T.c, t, 'NO TICKLE', K.S(3) + 1.6, 540, 1560, 120, '#ffd43b', 0.04)

def hand(T, x, y, s=1.0, flip=1):
    T.shape(ellipse_pts(x, y, 70*s, 55*s, 24), '#ffd2b0', lw=7)
    for k in range(4):
        fx = x - 45*s + k*30*s
        T.shape(ellipse_pts(fx, y - 70*s*flip, 13*s, 34*s, 16), '#ffd2b0', lw=6)

def sh_robot(K, T, t, u):
    """1999 experiment diagram: your hand moves a robot, a 2nd robot strokes your palm with foam, through a delay box"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    label(T.c, 'THE 1999 TEST', 540, 300, 100, '#ffffff', -0.03, back(u/0.3, 1.4))
    m = 40*math.sin(tq(t)*5)
    # left: your hand on a robot stick
    T.shape(rect(120, 1120, 260, 120), '#7fd0ff', shadow='#5aa8d8', shade_dir=(1, 0), shade_w=0.2, lw=8)
    T.stroke([(250, 1120), (250 + m, 900)], lw=18, col='#c9c9d6')
    hand(T, 250 + m, 880, 0.9)
    label(T.c, 'YOU MOVE', 250, 1330, 52, '#7fd0ff', 0, 1, FONT, 10)
    # right: robot touches the other palm with foam
    T.shape(rect(700, 600, 260, 110), '#ff4fa3', shadow='#d93a86', shade_dir=(1, 0), shade_w=0.2, lw=8)
    lag = 40*math.sin(tq(t - (0.2 if u > 1.6 else 0.0))*5)
    T.stroke([(830, 710), (830 + lag, 900)], lw=18, col='#c9c9d6')
    T.shape(ellipse_pts(830 + lag, 925, 48, 30, 20), '#ffe066', lw=6)
    hand(T, 830, 1080, 1.0, flip=-1)
    label(T.c, 'ROBOT TOUCH', 830, 1330, 52, '#ff4fa3', 0, 1, FONT, 10)
    # cable via delay box
    T.stroke([(380, 1180), (540, 1180), (540, 650), (700, 650)], lw=10, col='#c9b8ff')
    if u > 1.4:
        k = back((u - 1.4)/0.3, 1.5)
        T.shape(rect(420, 840, 240, 120), '#ffd43b', lw=8)
        label(T.c, 'DELAY', 540, 922, 42*k + 1, '#ffffff', 0, 1)
    label(T.c, 'Blakemore et al., UCL', 540, 1480, 44, '#c9b8ff', 0, 1, FONT, 10)

def sh_late(K, T, t, u):
    """parallel world: a stopwatch shows the 0.2 s lag on every touch"""
    T.cx, T.cy, T.z = 540, 980, 1.0 + 0.02*u
    K.world(T, t, True)
    stopwatch(T, 540, 640, 170, t)
    K.kiko(T, t, **pose('confused', 'rest', look=(0.6, -0.6)))
    K.nova(T, t, **pose('excited', 'present'))
    kin(T.c, t, 'EVERY TOUCH: LATE', K.at(5, 0.5), 540, 300, 90, '#ffd43b', -0.03)

def sh_laugh(K, T, t, u):
    T.cx, T.cy, T.z = K.KIKO_X + 30, 1090, 2.05 + 0.05*u
    K.world(T, t, True)
    K.kiko(T, t, **tickle_pose(t, laugh=u > 0.7))
    if u > 0.7:
        wiggles(T, K.KIKO_X + 20, FEET - 0.92*290, t, 1.0)
        kin(T.c, t, 'HA HA HA!', K.S(6) + 0.8, 540, 560, 150, '#ff4fa3', -0.05)

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.custom(K.L(1), sh_spoiler, sfx='pop')
    K.ncu(K.at(1, 0.6), par=False, emo='smug', gest='finger_up')
    K.custom(K.L(2), sh_cerebellum, sfx='chime')
    K.custom(K.L(3), sh_volume, sfx='blip')
    K.custom(K.L(4), sh_robot, sfx='pop')
    K.hook(K.at(4, 0.72), portal_line=4, portal_f=0.86)
    K.arrive(tag_text='WORLD #14 · TOUCH: 0.2 s LATE')
    K.custom(K.at(5, 0.55), sh_late, sfx='blip')
    K.custom(K.L(6), sh_laugh, sfx='boing')
    K.stat(K.L(7), '0.2 s', 'DELAY', "felt like someone else's tickle")
    K.twoshot(K.L(8), par=True, nova=pose('happy', 'present'), kiko=tickle_pose(K.S(8), laugh=True))
    K.end(K.L(9), poll=('OUR WORLD', 'DELAY WORLD'))

def thumbnail(c, K):
    """huge text, big laughing Kiko tickling himself, a big stopwatch hero object, arrow"""
    burst(c, W, H, 620, 1200, '#ffd6f0', '#3b1f8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    stopwatch(T, 820, 900, 180, 0.6, txt='')
    label(c, '0.2 s', 820, 1010, 110, '#ff4fa3', -0.05, 1)
    P = tickle_pose(0.3, laugh=True); P.update(x=330, y=2380, s=2.15, face=1, o=0.9, jit=0)
    K.kiko(T, 1.0, **P)
    big_text(c, "WHY CAN'T YOU", 540, 250, 130, max_w=950)
    big_text(c, 'TICKLE YOURSELF?', 540, 460, 150, hl=0, hl_col='#ff4fa3', max_w=1010)
    emoji_burst(c, 230, 720, 105, 'HA HA', '#ff2d55', -0.2)
    arrow(c, 900, 1150, 640, 1650, '#ffd43b', 26)
