"""EP15 - Do cats ALWAYS land on their feet? (Short, IS IT TRUE? format with a parallel-world test, built with shortkit)
Format: IS IT TRUE? + portal test ("stiff-cat world"). Topic family: animals (new family; 5 PM Short was senses/body).
Gate score: curiosity 5, relatable 5, visual 5, fact certainty 4, freshness 3 (common question, but the stiff-cat
parallel-world test is our own angle) = 22/25.
Facts (checked):
- The cat righting reflex: a falling cat bends in the middle so its front and back halves turn about different axes; it
  tucks the front legs (less moment of inertia) and spins the front half a lot while the back half (legs out) turns a
  little the opposite way, then swaps; total angular momentum stays zero (Scientific American "Why Do Cats Land on Their
  Feet? Physics Explains"; Live Science "How do cats land on their feet?"; Wikipedia "Cat righting reflex", which gives
  front ~90 deg vs rear ~10 deg per step).
- It needs a very flexible spine (Scientific American; Live Science "flexible lumbar region"; Wikipedia).
- Not guaranteed: very short drops leave too little time to turn (Live Science, about 0.3-0.6 m, citing Annals of
  Improbable Research), and cats can still be hurt in falls (Wikipedia). So the honest verdict is "MOSTLY TRUE".
- Physics of the twist world: a rigid body that starts with zero angular momentum cannot rotate itself (conservation
  of angular momentum), so a cat that could not bend would stay upside down.
Sources: Scientific American (2023, physics of falling cats); Live Science; Wikipedia "Cat righting reflex" /
"Falling cat problem". No real people, no brands; the cat is a generic original toon cat."""
import math, numpy as np
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Do cats always land on their feet?", gap=0.3),
    dict(who=N, text="Almost always! Let's slow it way down.", gap=0.3),
    dict(who=N, text="First, the falling cat bends in the middle.", gap=0.3),
    dict(who=N, text="It tucks its front paws in, and spins its front half around.", gap=0.3),
    dict(who=N, text="The back half twists a little the other way. Then they swap. Feet down!", gap=0.35),
    dict(who=N, text="That trick needs a super bendy spine.", gap=0.3),
    dict(who=N, text="So, true? Mostly. A very short drop is too quick to turn.", gap=0.35),
    dict(who=N, text="But what if cats couldn't bend? Let's test it in a parallel world.", gap=0.3),
    dict(who=K_, text="Whoa! The stiff cat... stays upside down!", gap=0.35),
    dict(who=N, text="No bend, no twist. A stiff body that starts with no spin can't flip itself over.", gap=0.35),
    dict(who=N, text="Bendy cats, or stiff cats? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep15_cat_feet', our_set='room', par_set='room',
    title="Do Cats ALWAYS Land on Their Feet? \U0001F300 #Swirlverse",
    description=("Do cats always land on their feet? Almost! A falling cat bends in the middle, tucks its front paws, spins its front half, "
                 "then swaps and spins the back half. But in this parallel world, cats can't bend... \U0001F431\n"
                 "Bendy cats or stiff cats? Comment below \U0001F447\n\n"
                 "Real science: the cat righting reflex. The front and back halves turn in opposite directions, so the total spin "
                 "(angular momentum) stays zero. It needs a super flexible spine. It isn't guaranteed: a very short drop is too quick to turn. "
                 "Sources: Scientific American, Live Science.\n\n"
                 "#shorts #science #cats #physics #animals #swirlverse"),
    tags=['do cats always land on their feet', 'cat righting reflex', 'how cats land on their feet', 'cat physics', 'falling cat',
          'angular momentum', 'animal science', 'parallel world', 'what if', 'science shorts', 'swirlverse', 'animation'],
    topic='do cats always land on their feet / cat righting reflex', category='animals', hook='kiko question cold open -> slow-mo twist -> verdict -> portal test',
)
DROPS = []

ORANGE, ORANGE_SH, CREAM, STRIPE = '#ffa24a', '#e57d22', '#fff1dc', '#c8601a'

# ---------------------------------------------------------------- the cat
def cat(T, x, y, s=1.0, rf=0.0, rb=0.0, tuckF=0.0, tuckB=0.0, bend=0.0, t=0.0, face='calm', tail=True):
    """side view toon cat facing left. rf / rb = roll of the front / back half (0 = feet down, pi = upside down),
    tuck = 0 legs out .. 1 legs tucked, bend = angle (rad) of the V at the waist."""
    mx, my = x, y
    def tr(pts, sgn):
        a = bend*sgn; ca, sa = math.cos(a), math.sin(a)
        return [(mx + (px - mx)*ca - (py - my)*sa, my + (px - mx)*sa + (py - my)*ca) for (px, py) in pts]
    def half(front):
        r = rf if front else rb; k = math.cos(r); tuck = tuckF if front else tuckB
        sgn = 1 if front else -1
        hx = x - 85*s if front else x + 85*s
        # legs (drawn first when they are on the far side, i.e. pointing "up" behind the body)
        L = (85 - 60*tuck)*s
        legs = []
        for dx in ((-45, -10) if front else (10, 45)):
            lx = hx + dx*s
            y0 = y + k*35*s; y1 = y + k*(35*s + L)
            legs.append([(lx - 13*s, y0), (lx + 13*s, y0), (lx + 13*s, y1), (lx - 13*s, y1)])
            legs.append(ellipse_pts(lx, y1, 18*s, 13*s, 16))
        for p in legs: T.shape(tr(p, sgn), ORANGE, lw=6)
        # body half
        T.shape(tr(ellipse_pts(hx, y, 105*s, 62*s, 30), sgn), ORANGE, shadow=ORANGE_SH, shade_dir=(0, -k if abs(k) > 0.1 else 1), shade_w=0.25, lw=8)
        if abs(k) > 0.05:
            T.shape(tr(ellipse_pts(hx, y + k*30*s, 70*s, 26*s*abs(k), 20), sgn), CREAM, lw=0, line=False)
            for j in range(3):
                sx = hx + (-50 + j*40)*s
                T.stroke(tr([(sx, y - k*58*s), (sx + 8*s, y - k*30*s)], sgn), lw=7*s + 1, col=STRIPE)
        if front:
            hxh, hy = x - 200*s, y - k*30*s
            for e in (-1, 1):   # ears point to the "top" side
                ex = hxh + e*28*s
                T.shape(tr([(ex - 20*s, hy - k*35*s), (ex + 20*s, hy - k*35*s), (ex, hy - k*95*s)], sgn), ORANGE, lw=6)
            T.shape(tr(ellipse_pts(hxh, hy, 66*s, 58*s, 30), sgn), ORANGE, shadow=ORANGE_SH, shade_dir=(1, 0.3), shade_w=0.2, lw=8)
            T.shape(tr(ellipse_pts(hxh - 22*s, hy + k*20*s, 34*s, 22*s, 20), sgn), CREAM, lw=0, line=False)
            if face == 'shock':
                for e in (-1, 1): T.shape(tr(ellipse_pts(hxh + e*22*s, hy - k*8*s, 15*s, 18*s, 16), sgn), '#ffffff', lw=5)
                for e in (-1, 1): T.shape(tr(ellipse_pts(hxh + e*22*s, hy - k*8*s, 6*s, 7*s, 10), sgn), '#2b2b3a', lw=0, line=False)
            else:
                for e in (-1, 1): T.stroke(tr([(hxh + e*22*s - 10*s, hy - k*10*s), (hxh + e*22*s, hy - k*16*s), (hxh + e*22*s + 10*s, hy - k*10*s)], sgn), lw=6, col='#2b2b3a')
            T.shape(tr(ellipse_pts(hxh - 30*s, hy + k*14*s, 9*s, 7*s, 10), sgn), '#ff7aa8', lw=4)
            for e in (-1, 1):
                T.stroke(tr([(hxh - 40*s, hy + k*20*s), (hxh - 105*s, hy + k*(20 + e*14)*s)], sgn), lw=4, col='#2b2b3a')
        elif tail:
            w = math.sin(tq(t)*5)*0.25
            pts = [(x + 185*s + i*22*s, y - k*(i*i*7*s) + w*i*10*s) for i in range(7)]
            T.stroke(tr(pts, sgn), lw=26*s + 2, col=LINE_HEX)
            T.stroke(tr(pts, sgn), lw=16*s + 1, col=ORANGE)
    # draw the half that is further "back" first: just back half then front half
    half(False); half(True)

LINE_HEX = '#2b2b3a'

def speedlines(T, x, y, t, n=5, w=260):
    for i in range(n):
        yy = y - 200 + i*90 + (tq(t)*400 % 90)
        T.stroke([(x - w, yy - 160), (x - w, yy - 40)], lw=6, col='#ffffff', alpha=0.5)
        T.stroke([(x + w, yy - 140), (x + w, yy - 20)], lw=6, col='#ffffff', alpha=0.5)

def pillow(T, x, y, w=420):
    T.shape([(x - w/2, y), (x - w/2 + 20, y - 110), (x + w/2 - 20, y - 110), (x + w/2, y), (x + w/2 - 30, y + 50), (x - w/2 + 30, y + 50)],
            '#8fd3ff', shadow='#5fb0e8', shade_dir=(0, 1), shade_w=0.3, lw=8)

def slowmo_tag(c, t):
    label(c, 'SLOW-MO', 900, 210, 54, '#ff4fa3', 0.06, 1)
    if int(t*3) % 2 == 0:
        c.new_path(); c.arc(780, 192, 14, 0, 2*math.pi); c.set_source_rgb(1, 0.18, 0.33); c.fill()

# ---------------------------------------------------------------- shots
def sh_cold(K, T, t, u):
    """our room: a cat drops off the shelf; the question pops at once"""
    T.cx, T.cy, T.z = 540, 980, 1.12 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    T.shape(rect(380, 780, 330, 26), '#9a6a3a', lw=7)  # shelf
    fall = ease((u - 0.9)/0.9)
    roll = math.pi*(1 - ease((u - 1.3)/0.6)) if u > 0.9 else 0
    cat(T, 560, 720 + fall*560, 0.6, rf=roll, rb=roll*0.9, bend=0.25*math.sin(math.pi*clamp((u - 1.2)/0.7)), t=t,
        face='shock' if 0.9 < u < 1.9 else 'calm', tuckF=0.5 if 1.0 < u < 1.8 else 0)
    K.kiko(T, t, **pose('confused', 'point', look=(0.8, -0.5)))
    K.nova(T, t, **pose('excited', 'finger_up'))
    label(T.c, 'DO CATS ALWAYS', 540, 330, 108, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'LAND ON THEIR FEET?', 540, 480, 96, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_slow(K, T, t, u):
    """slow-mo board: cat falling upside down, front half starts to bend"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    speedlines(T, 540, 1000, t)
    cat(T, 540, 900 + 30*u, 1.45, rf=math.pi, rb=math.pi, bend=0, t=t, face='shock')
    slowmo_tag(T.c, t)
    kin(T.c, t, 'UPSIDE DOWN...', K.S(1) + 0.3, 540, 420, 100, '#ffd43b', -0.03)

def sh_bend(K, T, t, u):
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    speedlines(T, 540, 1000, t)
    b = 0.45*ease((u - 0.3)/0.8)
    cat(T, 540, 950, 1.45, rf=math.pi, rb=math.pi, bend=b, t=t, face='shock')
    slowmo_tag(T.c, t)
    label(T.c, 'STEP 1: BEND', 540, 400, 110, '#ffd43b', -0.03, back((u - 0.1)/0.3, 1.5))
    if u > 0.9: arrow(T.c, 540, 1350, 540, 1150, '#ff4fa3', 22)

def sh_front(K, T, t, u):
    """front paws tucked, front half rolls round fast; back half turns a little the other way"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    speedlines(T, 540, 1000, t)
    v = ease((u - 0.8)/1.8)
    cat(T, 540, 950, 1.45, rf=math.pi*(1 - v), rb=math.pi + 0.35*v, tuckF=ease((u - 0.2)/0.5), bend=0.45, t=t, face='shock')
    slowmo_tag(T.c, t)
    label(T.c, 'STEP 2: TUCK + SPIN', 540, 400, 92, '#ffd43b', -0.03, back((u - 0.1)/0.3, 1.5))
    if u > 0.9: label(T.c, 'FRONT: SPINS A LOT', 300, 1420, 54, '#7dff9a', 0, back((u - 0.9)/0.3, 1.4), FONT, 10)

def sh_swap(K, T, t, u):
    """back half rolls the other... then both halves feet down, landing"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    v = ease((u - 0.2)/1.6); land = ease((u - 2.4)/0.5)
    if land < 0.99: speedlines(T, 540, 1000, t)
    T.shape(rect(-200, 1420, 1500, 600), '#3a4670', lw=8)
    cat(T, 540, 950 + 300*land, 1.45, rf=0, rb=(math.pi + 0.35)*(1 - v), tuckB=0.7*(1 - v), tuckF=0.5*(1 - v), bend=0.45*(1 - ease((u - 1.6)/0.6)), t=t,
        face='calm' if land > 0.5 else 'shock')
    if land < 0.5: slowmo_tag(T.c, t)
    label(T.c, 'STEP 3: SWAP', 540, 400, 110, '#ffd43b', -0.03, back((u - 0.1)/0.3, 1.5))
    label(T.c, 'BACK: A LITTLE THE OTHER WAY', 540, 1560, 50, '#c9b8ff', 0, back((u - 0.4)/0.3, 1.4), FONT, 10)
    if land > 0.3: kin(T.c, t, 'FEET DOWN!', K.at(4, 0.8), 540, 600, 140, '#7dff9a', 0.04)

def sh_spine(K, T, t, u):
    """the bendy spine glows: a wobbly chain of vertebrae over the cat"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    b = 0.3*math.sin(tq(t)*4)
    cat(T, 540, 1000, 1.25, bend=b, t=t)
    g = ease((u - 0.3)/0.5)
    for i in range(9):
        a = b*(1 if i < 4.5 else -1)
        px = 540 + (i - 4)*48*1.25
        py = 1000 - 62*1.25 + abs(i - 4)*math.sin(abs(a))*40*(1 if a > 0 else 1)
        T.glow(px, py, 26, '#ffe066', ((1.8, 0.2*g), (1.3, 0.35*g)))
        T.shape(ellipse_pts(px, py, 22, 16, 14), mixc('#ffffff', '#ffd43b', g), lw=5)
    kin(T.c, t, 'SUPER BENDY SPINE', K.S(5) + 0.3, 540, 420, 100, '#ffd43b', -0.03)

def sh_stiff(K, T, t, u):
    """parallel room: a stiff cat falls upside down onto a big pillow between Kiko and Nova"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    K.world(T, t, True)
    K.kiko(T, t, **pose('shock', 'hands_head', x=150, jit=jitter(t)))
    K.nova(T, t, **pose('excited', 'present', x=950))
    pillow(T, 560, 1560, 520)
    fall = ease(u/1.1)
    bounce = 30*abs(math.sin((u - 1.1)*9))*math.exp(-(u - 1.1)*3) if u > 1.1 else 0
    cat(T, 560, 300 + fall*1100 - bounce, 0.75, rf=math.pi, rb=math.pi, bend=0, t=t, face='shock')
    if u > 1.1: kin(T.c, t, 'PHEW, PILLOW!', K.S(8) + 1.0, 540, 420, 100, '#ffd43b', 0.04)

def cat_on_pillow(T, t, u):
    pillow(T, 560, 1560, 520)
    cat(T, 560, 1400, 0.75, rf=math.pi, rb=math.pi, t=t, face='calm')

def sh_plank(K, T, t, u):
    """diagram: a rigid cat-plank with a crossed-out spin arrow"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    cat(T, 540, 900, 1.2, rf=math.pi, rb=math.pi, bend=0, t=t, face='shock')
    label(T.c, 'NO BEND', 540, 330, 120, '#ffffff', -0.03, back(u/0.3, 1.5))
    label(T.c, '= NO TWIST', 540, 480, 110, '#ffd43b', 0.03, back((u - 0.3)/0.3, 1.5))
    k = back((u - 1.2)/0.3, 1.4)
    if k > 0.01:
        c = T.c; c.new_path(); c.arc(540, 1260, 150*k, 0.3, 5.6); c.set_source_rgb(0.5, 0.9, 1); c.set_line_width(18); c.stroke()
        T.stroke([(380, 1100), (700, 1420)], lw=26, col='#ff2d55'); T.stroke([(700, 1100), (380, 1420)], lw=26, col='#ff2d55')
    label(T.c, 'no spin at the start = no flip', 540, 1560, 50, '#c9b8ff', 0, back((u - 1.6)/0.3, 1.4), FONT, 10)

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.ncu(K.L(1), par=False, emo='excited', gest='finger_up')
    K.custom(K.at(1, 0.55), sh_slow, sfx='swoop')
    K.custom(K.L(2), sh_bend, sfx='pop')
    K.custom(K.L(3), sh_front, sfx='blip')
    K.custom(K.L(4), sh_swap, sfx='boing')
    K.custom(K.L(5), sh_spine, sfx='chime')
    K.verdict(K.L(6), 'MOSTLY TRUE!', col='#7dff9a', sub='tiny drops: too quick to turn')
    K.kcu(K.at(6, 0.62), par=False, emo='confused', gest='shrug')
    K.hook(K.L(7), portal_line=7, portal_f=0.72)
    K.arrive(tag_text='WORLD #15 · CATS CAN\'T BEND')
    K.custom(K.at(8, 0.12), sh_stiff, sfx='swoop')
    K.custom(K.L(9), sh_plank, sfx='nope')
    K.twoshot(K.at(9, 0.7), par=True, nova=pose('smug', 'present', x=950), kiko=pose('happy', 'rest', x=150), extra=cat_on_pillow)
    K.end(K.L(10), poll=('BENDY CATS', 'STIFF CATS'))

def thumbnail(c, K):
    """huge text, big mid-twist cat (front half already feet-down, back half still upside down: really in the video), shocked Kiko, arrow"""
    burst(c, W, H, 560, 1150, '#ffe3c2', '#3b1f8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    P = pose('shock', 'hands_head'); P.update(x=230, y=2250, s=1.7, face=1, look=(0.8, -0.6), jit=0)
    K.kiko(T, 1.0, **P)
    cat(T, 600, 1080, 1.55, rf=0.0, rb=math.pi + 0.3, tuckB=0.6, bend=0.4, t=0.4, face='shock')
    big_text(c, 'DO CATS ALWAYS', 540, 250, 120, max_w=950)
    big_text(c, 'LAND ON FEET?', 540, 450, 150, hl=0, hl_col='#ff4fa3', max_w=1010)
    emoji_burst(c, 870, 720, 100, 'TWIST!', '#ff2d55', 0.2)
    arrow(c, 900, 1600, 760, 1260, '#ffd43b', 26)
