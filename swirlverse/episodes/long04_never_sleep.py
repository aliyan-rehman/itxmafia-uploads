"""LONG04 - What if we never needed sleep? (WHAT IF, parallel world)
Research gate (2026-11-25): curiosity 5, relatable 5, visual 4, certainty 4, freshness 3 = 21/25.
Facts and sources:
- We spend about one third of our lives asleep (NIH NINDS "Brain Basics: Understanding Sleep"). 1/3 of 75 years = 25 years.
- Adults need 7 or more hours a night; about 1 in 3 US adults don't get enough (CDC FastStats Sleep in Adults; CDC/Scientific American report).
- Sleep helps the brain store memories (NINDS; Cleveland Clinic sleep basics).
- In mice, the space between brain cells grew about 60% during sleep, letting fluid clear waste faster (Xie et al. 2013, Science; NIH news release "Brain may flush out toxins during sleep"; URMC).
- A rare DEC2 gene change lets some people feel fine on about 6 hours (He, Fu et al. 2009, Science; UCSF news 2009/2018).
- 8 extra hours x 365 = 2,920 hours a year (arithmetic).
Original cast only. Parallel-world consequences are imagined and labelled as such."""
LINES = [
 {"who": "KIKO", "text": "Nova! Psst! Nova! It's three in the morning! Wake up!", "gap": 0.4, "ch": 1},
 {"who": "NOVA", "text": "Kiko... why are you awake?", "gap": 0.4, "ch": 1},
 {"who": "KIKO", "text": "I had a big idea. What if we just... never slept again?", "gap": 0.4, "ch": 1},
 {"who": "NOVA", "text": "Then I could finish this sentence without yawni... yaaawn.", "gap": 0.4, "ch": 1},
 {"who": "KIKO", "text": "Think of all the free time!", "gap": 0.9, "ch": 1},
 {"who": "NOVA", "text": "In our world, sleep is not optional. Scientists say we spend about one third of our lives asleep.", "gap": 0.35, "ch": 2},
 {"who": "KIKO", "text": "A third?! If you live to seventy five, that's twenty five years of sleeping!", "gap": 0.35, "ch": 2,
  "cap": "A third?! If you live to 75, that's 25 years of sleeping!"},
 {"who": "NOVA", "text": "Yep. Health experts say adults need at least seven hours a night.", "gap": 0.35, "ch": 2},
 {"who": "NOVA", "text": "But about one in three adults in the United States doesn't get enough.", "gap": 0.35, "ch": 2,
  "cap": "But about 1 in 3 adults in the United States doesn't get enough."},
 {"who": "KIKO", "text": "So everyone is tired. Even the grown ups.", "gap": 0.9, "ch": 2},
 {"who": "NOVA", "text": "And your brain is busy while you sleep. It sorts out your day, and helps save your memories.", "gap": 0.35, "ch": 3},
 {"who": "NOVA", "text": "In studies on mice, the spaces between brain cells grew by about sixty percent during sleep.", "gap": 0.35, "ch": 3,
  "cap": "In studies on mice, the spaces between brain cells grew by about 60% during sleep."},
 {"who": "NOVA", "text": "That lets fluid wash the waste away much faster. Like a cleaning crew that works at night.", "gap": 0.35, "ch": 3},
 {"who": "KIKO", "text": "My brain has a cleaning crew?! Do they want snacks?", "gap": 0.4, "ch": 3},
 {"who": "NOVA", "text": "And a few rare people feel fine on about six hours, thanks to a tiny change in one gene.", "gap": 0.35, "ch": 3},
 {"who": "KIKO", "text": "Lucky! I want that gene.", "gap": 0.9, "ch": 3},
 {"who": "NOVA", "text": "But in this parallel world... nobody ever needs to sleep. Not even a nap.", "gap": 0.4, "ch": 4},
 {"who": "NOVA", "text": "Every day gets about eight extra hours. That's almost three thousand hours a year!", "gap": 0.35, "ch": 4,
  "cap": "Every day gets about 8 extra hours. That's almost 3,000 hours a year!"},
 {"who": "KIKO", "text": "School at three A M? Nooo!", "gap": 0.4, "ch": 4, "cap": "School at 3 AM? Nooo!"},
 {"who": "NOVA", "text": "Bedrooms turn into game rooms. Beds? Nobody buys them.", "gap": 0.4, "ch": 4},
 {"who": "KIKO", "text": "And shops never close. Midnight pancakes for everyone!", "gap": 0.9, "ch": 4},
 {"who": "NOVA", "text": "But there's a catch. Our brains use sleep to clean up and save memories.", "gap": 0.35, "ch": 5},
 {"who": "NOVA", "text": "So in this world, brains would need a brand new trick to do that while we're awake.", "gap": 0.35, "ch": 5},
 {"who": "KIKO", "text": "Wait. No sleep means... no dreams?", "gap": 0.4, "ch": 5},
 {"who": "NOVA", "text": "No dreams. No cozy blankets. No big morning stretch.", "gap": 0.4, "ch": 5},
 {"who": "KIKO", "text": "Okay... that's a little sad.", "gap": 0.9, "ch": 5},
 {"who": "NOVA", "text": "But the good side is big. Doctors, pilots and night workers would never fight sleepiness.", "gap": 0.35, "ch": 6},
 {"who": "NOVA", "text": "And sleepy driving? Gone.", "gap": 0.35, "ch": 6},
 {"who": "KIKO", "text": "And I'd finally finish all my books. And all my snacks.", "gap": 0.35, "ch": 6},
 {"who": "NOVA", "text": "Mostly the snacks.", "gap": 0.9, "ch": 6},
 {"who": "NOVA", "text": "So... would you give up sleep for eight extra hours a day? Or keep your dreams?", "gap": 0.4, "ch": 7},
 {"who": "KIKO", "text": "Keep the dreams. Definitely. Good night, Nova.", "gap": 0.45, "ch": 7},
 {"who": "NOVA", "text": "Kiko... it's morning now.", "gap": 0.4, "ch": 7},
 {"who": "NOVA", "text": "What would you pick? Comment below. A new parallel world, every day.", "gap": 1.8, "ch": 7},
]
CHAPTERS = {1: 'The 3 AM idea', 2: 'How much we sleep', 3: 'Your brain at night', 4: 'The parallel world', 5: 'The catch', 6: 'The good side', 7: 'Your turn'}
META = dict(id='long04_never_sleep', title='What If We Never Needed SLEEP? \U0001F300 Swirlverse',
    description=("Kiko woke Nova at 3 AM with a big idea: what if nobody ever needed to sleep again?\n"
                 "Real science first: we spend about a third of our lives asleep, adults need 7+ hours, and in mouse studies the brain's "
                 "'night cleaning crew' clears waste much faster during sleep. Then we jump into a parallel world with 8 extra hours every day.\n\n"
                 "{CHAPTERS}\n\n"
                 "Sources: NIH NINDS (Brain Basics: Understanding Sleep), CDC (Sleep in Adults), Xie et al. 2013 in Science (NIH news release), "
                 "UCSF (DEC2 short-sleep gene, 2009).\n"
                 "This is a fun science video, not medical advice.\n\n"
                 "#whatif #parallelworld #sleep #brain #swirlverse"),
    tags=['what if', 'parallel world', 'what if we never slept', 'why do we sleep', 'sleep science', 'brain facts',
          'glymphatic system', 'short sleeper gene', 'science for everyone', 'swirlverse'])
THINK = (5, 6)
# ===== SHOTS =====
from longkit import *

NIGHT = '#141a3d'

def moon(T, x, y, r=60):
    T.shape(ellipse_pts(x, y, r, r, 30), '#fff2c8', shadow='#e7c98f', shade_dir=(1, 0.5), shade_w=0.25, lw=6)

def night_window(T):
    """paint the room window as a night sky with a moon"""
    T.shape(rect(260, 140, 520, 360), NIGHT, line=False, amp=0)
    moon(T, 650, 250, 55)
    for (sx, sy) in ((330, 200), (420, 320), (540, 180), (360, 420), (700, 420)):
        T.shape(star(sx, sy, 12, 5, 5, 0), '#ffe066', lw=3)

def bed(T, x, y, s=1.0, col='#7b5cff'):
    T.shape(rect(x - 260*s, y - 120*s, 520*s, 120*s), '#c98a4a', lw=8)
    T.shape(rect(x - 280*s, y - 260*s, 40*s, 260*s), '#a86e34', lw=7)
    T.shape(rect(x - 240*s, y - 160*s, 480*s, 60*s), col, shadow=mixc(col, '#000000', 0.25), shade_dir=(0, 1), shade_w=0.3, lw=7)
    T.shape(ellipse_pts(x - 170*s, y - 175*s, 70*s, 32*s, 20), '#ffffff', lw=6)

def clock(T, c, x, y, r, hh, mm=0, col='#ffffff', label_txt=None):
    T.shape(ellipse_pts(x, y, r, r, 40), col, lw=8)
    for k in range(12):
        a = k*math.pi/6
        T.stroke([(x + 0.82*r*math.sin(a), y - 0.82*r*math.cos(a)), (x + 0.92*r*math.sin(a), y - 0.92*r*math.cos(a))], lw=6, col='#2a2140')
    ah = (hh % 12 + mm/60)*math.pi/6; am = mm*math.pi/30
    T.stroke([(x, y), (x + 0.5*r*math.sin(ah), y - 0.5*r*math.cos(ah))], lw=12, col='#2a2140')
    T.stroke([(x, y), (x + 0.75*r*math.sin(am), y - 0.75*r*math.cos(am))], lw=8, col='#2a2140')
    T.dot(x, y, 10)
    if label_txt: label(c, label_txt, x, y + r + 60, 54, '#ffd43b', 0, 1)

def zzz(T, c, t, x, y, s=1.0):
    for j in range(3):
        v = ((t*0.5 + j/3) % 1)
        label(c, 'z', x + 60*v*s, y - 120*v*s, (34 + 30*v)*s, '#c9b8ff', 0.1, 1 - v*0.6)

# ---------- chapter 1: the 3 AM idea
def sh_wake(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.025*u); room(T, t)
    night_window(T)
    bed(T, 640, FLOOR + 40, 1.0)
    clock(T, c, 1500, 260, 90, 3, 0)
    draw_nova(T, nova_talk(t, dict(x=600, y=FLOOR + 140, s=0.95, face=1, look=(0.6, 0.3), lid=0.75, brow=-0.3, sm=-0.2, armF=((-60, -60), 30))))
    draw_kiko(T, kiko_talk(t, dict(x=1250, y=FLOOR + 150, s=0.95, face=-1, look=(-0.8, -0.1), brow=0.9, sm=0.9, er=46,
                                    armF=((-230, -40), 30), armB=((60, -150), 15), jit=jitter(t, 3))))
    if u > 0.6: kin(c, t, '3:00 AM', t0 + 0.6, 1500, 430, 70, '#ffd43b', 0.04)

def sh_sleepy_nova(T, t, t0, yawn=False):
    u = t - t0
    cam(T, 640, 450, 1.85 + 0.03*u); room(T, t); night_window(T)
    o = 0.9 if (yawn and u > 1.6) else None
    P = dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.4, 0.2), lid=0.6, brow=-0.4, sm=-0.1)
    if o: P.update(o=o, lid=0.95, armF=((-40, -200), 10))
    draw_nova(T, nova_talk(t, P))
    if yawn and u > 1.6: kin(T.c, t, 'YAAAWN', t0 + 1.6, 1300, 300, 100, '#c9b8ff', 0.06)

def sh_kiko_idea(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, extra=dict(brow=0.9, sm=0.9, er=48, look=(-0.6, -0.4), armF=((-60, -260), 10)))
    night_window(T)
    k = back((u - 0.8)/0.3, 1.6)
    if k > 0.01:
        T.shape(ellipse_pts(1500, 230, 90*k, 90*k, 24), '#ffe066', lw=7)
        T.shape(rect(1470, 320, 60*k, 50), '#c9d2de', lw=5)
        label(c, 'NEVER SLEEP?!', 1250, 120, 70, '#ffd43b', -0.03, k)

def sh_freetime(T, t, t0):
    def extra(T, t, u):
        for i in range(5):
            v = ((u*0.35 + i/5) % 1)
            x = 960 + 360*math.sin(i*1.9 + u*0.6); y = 640 - 420*v
            clock(T, T.c, x, y, 40*(1 - 0.4*v), (i*3) % 12, 0)
        kin(T.c, t, 'FREE TIME!', t0 + 0.5, 1300, 170, 90, '#7dff9a', 0.04)
    sh_twoshot(T, t, t0, np_=dict(lid=0.6, brow=-0.2, sm=0.1), kp=dict(brow=0.9, sm=1.0, er=48, armF=((-200, -200), 30), armB=((200, -200), -30)), extra_draw=extra)

# ---------- chapter 2: how much we sleep
def sh_third(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t)
    label(c, 'A LIFETIME', W/2, 170, 70, '#ffffff', 0, back(u/0.3, 1.4))
    x0, x1, y = 260, 1660, 520
    T.shape(rect(x0, y - 70, x1 - x0, 140), '#4fd8ff', lw=8)
    k = ease((u - 0.8)/1.2)
    if k > 0:
        T.shape(rect(x1 - (x1 - x0)/3*k, y - 70, (x1 - x0)/3*k, 140), '#3b1f8c', lw=8)
        if k > 0.9: zzz(T, c, t, x1 - 300, y - 20, 1.2)
    label(c, 'AWAKE', (x0 + x1 - (x1 - x0)/3)/2, y + 10, 64, '#1b1422', 0, 1, FONT, 0.1)
    if u > 2.0:
        label(c, '1/3 ASLEEP', x1 - (x1 - x0)/6, y + 160, 64, '#c9b8ff', 0.02, back((u - 2.0)/0.3, 1.5))

def sh_years(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#1f2a4a', '#2c3a63')
    for i in range(25):
        k = back((u - 0.3 - i*0.06)/0.25, 1.5)
        if k <= 0.01: continue
        r, q = divmod(i, 5)
        x, y = 330 + q*150, 300 + r*130
        T.shape(ellipse_pts(x, y, 55*k, 40*k, 18), '#ffffff', lw=5)
        T.shape(ellipse_pts(x - 25*k, y - 8*k, 20*k, 14*k, 12), '#c9d2de', lw=3)
    label(c, '25 YEARS', 1450, 450, 150, '#ffd43b', -0.04, back((u - 1.4)/0.3, 1.6))
    label(c, 'of sleeping (75-year life)', 1450, 580, 44, '#ffffff', 0, back((u - 1.7)/0.3, 1.5), FONT, 10)

def sh_seven(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t)
    clock(T, c, 620, 540, 260, 7, 0)
    k = ease((u - 0.4)/1.2)
    # 7-hour wedge
    T.shape([(620, 540)] + ellipse_pts(620, 540, 230, 230, 30, -math.pi/2, -math.pi/2 + 7/12*2*math.pi*k), '#7dff9a', line=False, alpha=0.55)
    label(c, '7+ HOURS', 1400, 450, 140, '#7dff9a', -0.03, back((u - 1.0)/0.3, 1.5))
    label(c, 'every night (adults)', 1400, 570, 46, '#ffffff', 0, back((u - 1.3)/0.3, 1.5), FONT, 10)

def sh_onein3(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#3a1f2e', '#4c2a3c')
    for i in range(3):
        k = back((u - 0.2 - i*0.15)/0.3, 1.6)
        if k <= 0.01: continue
        x = 520 + i*440; tired = i == 2 and u > 1.2
        person_icon(T, x, 640, 6.0*k, '#ff8fa3' if tired else '#9fe3d9')
        if tired: zzz(T, c, t, x + 80, 330, 1.3)
    label(c, '1 IN 3 ADULTS', W/2, 170, 100, '#ffd43b', 0, back((u - 0.9)/0.3, 1.5))
    label(c, 'in the US don\'t get enough sleep', W/2, 270, 46, '#ffffff', 0, back((u - 1.2)/0.3, 1.5), FONT, 10)

def sh_grownups(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u); room(T, t)
    for j, (x, cfg) in enumerate(((520, MOM), (900, DAD), (1280, GRANDPA))):
        draw_adult(T, dict(t=t, x=x, y=FLOOR + 140, s=0.85, face=1 if x < 960 else -1, look=(0, 0.3), lid=0.7, brow=-0.4, sm=-0.2), cfg)
        zzz(T, c, t + j*0.4, x + 40, 260, 1.0)
    T.shape(ellipse_pts(1600, FLOOR - 20, 80, 40, 20), '#8e84b8', lw=6)
    mouse(T, 1640, FLOOR - 40, 0.6, t)
    label(c, 'EVERYONE IS TIRED', W/2, 150, 80, '#3a3f8f', -0.02, back((u - 0.5)/0.3, 1.5), 'Luckiest Guy', 14)

# ---------- chapter 3: your brain at night
def sh_sorting(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#1f2a4a', '#2c3a63')
    brain(T, 960, 560, 1.1, 0.4 + 0.6*ease((u - 1.5)/1.0), t)
    for i in range(8):   # memory cards flying into the brain
        v = clamp((u - 0.3 - i*0.25)/0.9)
        if v <= 0 or v >= 1: continue
        sx = 200 if i % 2 == 0 else 1720; sy = 260 + (i*97 % 500)
        x = sx + (960 - sx)*ease(v); y = sy + (560 - sy)*ease(v)
        T.shape(rect(x - 50, y - 36, 100, 72), ('#ffd43b', '#4fd8ff', '#ff8fb8')[i % 3], lw=5, alpha=1 - 0.6*v)
        T.shape(star(x, y, 18, 8, 5, 0), '#ffffff', lw=3, alpha=1 - 0.6*v)
    label(c, 'SAVING MEMORIES', W/2, 150, 80, '#ffe066', 0, back((u - 0.6)/0.3, 1.5))

def sh_gaps(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1a2440', '#26335a')
    g = 1.0 + 0.6*ease((u - 1.2)/1.4)
    for r in range(4):
        for q in range(6):
            x = 960 + (q - 2.5)*170*g; y = 560 + (r - 1.5)*150*g
            T.shape(ellipse_pts(x, y, 70, 60, 20), '#ffb3c8', shadow='#f08fae', shade_dir=(1, 0.4), shade_w=0.3, lw=6)
    label(c, 'AWAKE' if u < 1.2 else 'ASLEEP', 300, 140, 70, '#ffffff', 0, 1)
    if u > 2.0:
        label(c, '+60% SPACE', 1450, 150, 100, '#4fd8ff', -0.03, back((u - 2.0)/0.3, 1.6))
    label(c, 'brain cells · studies in MICE', 420, 230, 40, '#c9b8ff', 0, back((u - 0.4)/0.3, 1.4), FONT, 9)

def sh_wash(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#1f2a4a', '#2c3a63')
    brain(T, 760, 560, 1.0, 0.5, t)
    front = -300 + 1300*ease((u - 0.6)/2.2)
    for i in range(18):   # waste dots get swept away by the blue wave
        x = 520 + (i*137 % 480); y = 420 + (i*71 % 300)
        if x > 760 - 400 + front: T.shape(ellipse_pts(x, y, 14, 14, 10), '#9b8a5a', lw=4)
    for j in range(4):
        xs = 760 - 420 + front - j*30
        T.stroke([(xs + 20*math.sin(k*0.8 + t*6), 330 + k*50) for k in range(10)], lw=10, col='#4fd8ff', alpha=0.8 - j*0.18)
    # tiny mop crew
    mx = 1450
    T.stroke([(mx, 460), (mx - 120, 760)], lw=12, col='#a86e34')
    T.shape(rect(mx - 190, 740, 150, 60), '#7dff9a', lw=6)
    label(c, 'NIGHT CLEANING CREW', 1300, 180, 64, '#7dff9a', 0.02, back((u - 0.4)/0.3, 1.5))

def sh_gene(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t)
    for k in range(24):   # DNA helix
        y = 140 + k*34; ph = k*0.5 + t*1.5
        x1 = 560 + 150*math.sin(ph); x2 = 560 - 150*math.sin(ph)
        hl = k == 12 and u > 1.0
        T.stroke([(x1, y), (x2, y)], lw=6, col='#ffd43b' if hl else '#c9d2de')
        T.shape(ellipse_pts(x1, y, 14, 14, 10), '#4fd8ff', lw=3); T.shape(ellipse_pts(x2, y, 14, 14, 10), '#ff4fa3', lw=3)
    if u > 1.0: kin(c, t, 'TINY CHANGE', t0 + 1.0, 880, 560, 54, '#ffd43b', 0.05)
    clock(T, c, 1400, 470, 170, 6, 0)
    T.shape([(1400, 470)] + ellipse_pts(1400, 470, 150, 150, 24, -math.pi/2, -math.pi/2 + math.pi*ease((u - 1.4)/1.0)), '#7dff9a', line=False, alpha=0.55)
    label(c, '~6 HOURS', 1400, 740, 90, '#7dff9a', 0, back((u - 1.8)/0.3, 1.5))
    label(c, 'RARE!', 1400, 850, 50, '#ffffff', 0, back((u - 2.2)/0.3, 1.5), FONT, 10)

# ---------- chapter 4: the parallel world
def sh_clock24(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#3b1f8c', '#4c2fa0')
    cx, cy, R = 620, 540, 280
    T.shape(ellipse_pts(cx, cy, R, R, 40), '#4fd8ff', lw=8)
    k = ease((u - 0.5)/1.0)
    T.shape([(cx, cy)] + ellipse_pts(cx, cy, R - 12, R - 12, 30, -math.pi/2, -math.pi/2 + 2*math.pi/3*max(0.01, k)), '#ffd43b', line=False)
    label(c, '24 h', cx, cy - R - 50, 50, '#ffffff', 0, 1, FONT, 9)
    label(c, '+8 HOURS', 1380, 390, 130, '#ffd43b', -0.03, back((u - 1.0)/0.3, 1.5))
    label(c, 'every day', 1380, 490, 46, '#ffffff', 0, back((u - 1.2)/0.3, 1.5), FONT, 10)
    if u > 2.6:
        label(c, '≈ 2,920 h / YEAR', 1380, 660, 80, '#7dff9a', 0.02, back((u - 2.6)/0.3, 1.5))

def sh_school(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u)
    T.flat(rect(-2000, -2000, 6000, 5000), '#efe0ff')
    T.shape(rect(260, 120, 900, 420), '#2f5a46', lw=9); T.shape(rect(240, 540, 940, 24), '#c98a4a', lw=6)
    label(c, 'CLASS STARTS: 3:00 AM', 710, 250, 50, '#ffffff', 0, 1, FONT, 0.1)
    T.shape(rect(1300, 140, 360, 260), NIGHT, lw=8); moon(T, 1560, 220, 45)
    clock(T, c, 1480, 520, 70, 3, 0)
    T.shape(rect(-2000, FLOOR, 6000, 1200), '#c98a5a', lw=8)
    draw_kiko(T, kiko_talk(t, dict(x=860, y=FLOOR + 150, s=0.95, face=1, look=(0.6, -0.4), brow=-0.8, sm=-0.8, er=46, sweat=True,
                                    armF=((-60, -250), 10), armB=((60, -250), -10))))
    if u > 0.9: kin(c, t, 'NOOO!', t0 + 0.9, 1300, 700, 110, '#ff4fa3', -0.06)

def sh_gameroom(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u); room(T, t, par=True)
    bed(T, 1350, FLOOR + 40, 0.8, '#8e84b8')
    if u > 1.6:
        T.stroke([(1100, 620), (1600, 880)], lw=22, col='#ff3b5c'); T.stroke([(1600, 620), (1100, 880)], lw=22, col='#ff3b5c')
        kin(c, t, 'BEDS?', t0 + 1.6, 1350, 520, 80, '#ff3b5c', 0.05)
    # game corner: ball, blocks
    T.shape(ellipse_pts(960, FLOOR - 50, 60, 60, 24), '#ffd43b', lw=7)
    for k in range(3): T.shape(rect(1040 + k*70, FLOOR - 70 - (k == 1)*70, 66, 66), ('#4fd8ff', '#ff4fa3', '#7dff9a')[k], lw=6)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.8, sm=0.6, armF=((-200, -40), 30))))
    label(c, 'GAME ROOM', 960, 150, 80, '#7b5cff', -0.03, back((u - 0.3)/0.3, 1.5), 'Luckiest Guy', 14)

def sh_pancakes(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    T.shape(rect(-1500, -1500, 5000, 1700), NIGHT, line=False, alpha=0.45, amp=0)
    T.shape(rect(620, 300, 680, 120), '#ff4fa3', lw=8)
    label(c, 'OPEN 24/7', 960, 365, 70, '#ffffff', 0, 1)
    for k in range(5):   # pancake stack
        T.shape(ellipse_pts(960, 700 - k*36, 170, 34, 24), '#f2a541', shadow='#d98a2b', shade_dir=(0, 1), shade_w=0.3, lw=6)
    T.shape(ellipse_pts(960, 540, 60, 20, 16), '#fff6d8', lw=5)
    clock(T, c, 400, 520, 70, 0, 0)
    label(c, 'MIDNIGHT', 400, 640, 44, '#ffd43b', 0, 1, FONT, 9)
    draw_kiko(T, kiko_talk(t, dict(x=1560, y=FLOOR + 150, s=0.9, face=-1, look=(-0.7, -0.2), brow=0.9, sm=1.0, er=46, armF=((-200, -200), 30))))

# ---------- chapter 5: the catch
def sh_catch(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#3a1f2e', '#4c2a3c')
    brain(T, 760, 560, 1.1, 0.5, t)
    for i in range(14):   # waste piling up
        x = 560 + (i*131 % 420); y = 450 + (i*67 % 260)
        T.shape(ellipse_pts(x, y, 15, 15, 10), '#9b8a5a', lw=4, alpha=clamp((u - 0.5 - i*0.08)/0.3))
    label(c, 'WHO CLEANS UP?', 1400, 330, 80, '#ff8fa3', 0.02, back((u - 0.8)/0.3, 1.5))
    if u > 1.8: kin(c, t, '?!', t0 + 1.8, 1400, 560, 200, '#ffd43b', -0.05)

def sh_newtrick(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#3b1f8c', '#4c2fa0')
    brain(T, 760, 560, 1.1, 0.7, t)
    for i in range(8):
        a = i*math.pi/4 + t*0.8; k = back((u - 0.6 - i*0.08)/0.25, 1.8)
        T.shape(star(760 + 380*math.cos(a), 560 + 270*math.sin(a), 26*k, 10*k, 5, t), '#7dff9a', lw=4)
    label(c, 'A NEW BRAIN TRICK', 1420, 330, 70, '#7dff9a', 0.02, back((u - 0.8)/0.3, 1.5))
    label(c, '(imagined)', 1420, 430, 44, '#ffffff', 0, back((u - 1.1)/0.3, 1.5), FONT, 9)

def sh_nodreams(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f2a4a', '#2c3a63')
    pop = u > 2.2
    if not pop:
        k = back((u - 0.2)/0.4, 1.4)
        T.shape(ellipse_pts(960, 480, 420*k, 280*k, 40), '#ffffff', lw=8)
        for j, (dx, dy, r) in enumerate(((-320, 330, 50), (-400, 420, 30))): T.shape(ellipse_pts(960 + dx, 480 + dy, r*k, r*k, 16), '#ffffff', lw=6)
        moon(T, 860, 440, 80*k); T.shape(star(1080, 400, 50*k, 20*k, 5, 0), '#ffe066', lw=5)
        mouse(T, 1060, 560, 0.7*k, t)
        label(c, 'DREAMS', 960, 160, 80, '#c9b8ff', 0, 1)
    else:
        kin(c, t, 'POP!', t0 + 2.2, 960, 480, 200, '#ff4fa3', 0.04)
        label(c, 'NO DREAMS', 960, 160, 80, '#ff8fa3', 0, 1)

def sh_blanket(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u); room(T, t, par=True)
    bed(T, 1300, FLOOR + 40, 0.9, '#ffb3c8')
    draw_nova(T, nova_talk(t, dict(x=600, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0.1), brow=-0.2, sm=-0.2, armF=((-120, -260), 10), armB=((120, -260), -10))))
    if u > 0.3:
        c.save(); c.set_source_rgba(0.1, 0.08, 0.2, 0.78); c.rectangle(1040, 130, 520, 360); c.fill(); c.restore()
    for i, txt in enumerate(('NO DREAMS', 'NO BLANKETS', 'NO STRETCH')):
        if u > 0.3 + i*0.9:
            label(c, txt, 1300, 200 + i*110, 60, '#ffffff', 0.02*(i - 1), back((u - 0.3 - i*0.9)/0.3, 1.5))
            T.stroke([(1080, 200 + i*110), (1520, 210 + i*110)], lw=12, col='#ff3b5c', screen=True)

# ---------- chapter 6: the good side
def sh_workers(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f3a3a', '#2c5050')
    icons = [('DOCTORS', '#ffffff'), ('PILOTS', '#4fd8ff'), ('NIGHT WORKERS', '#ffd43b')]
    for i, (txt, col) in enumerate(icons):
        k = back((u - 0.2 - i*0.4)/0.3, 1.6)
        if k <= 0.01: continue
        x = 420 + i*540
        T.shape(ellipse_pts(x, 470, 150*k, 150*k, 30), col, lw=8)
        if i == 0:
            T.shape(rect(x - 25*k, 390, 50*k, 160*k), '#ff3b5c', line=False); T.shape(rect(x - 80*k, 445, 160*k, 50*k), '#ff3b5c', line=False)
        elif i == 1:
            T.shape([(x - 100*k, 480), (x + 110*k, 460), (x + 100*k, 490), (x - 100*k, 500)], '#ffffff', lw=5)
            T.shape([(x - 10*k, 470), (x + 40*k, 400), (x + 60*k, 400), (x + 30*k, 475)], '#ffffff', lw=5)
        else:
            moon(T, x, 470, 70*k)
        label(c, txt, x, 700, 54, '#ffffff', 0, k)
    if u > 1.8: label(c, 'NEVER SLEEPY', W/2, 170, 90, '#7dff9a', -0.02, back((u - 1.8)/0.3, 1.5))

def sh_driving(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    x = 300 + 300*u
    T.shape(rect(x - 180, FLOOR - 150, 360, 110), '#4fd8ff', lw=8)
    T.shape([(x - 110, FLOOR - 150), (x - 70, FLOOR - 230), (x + 80, FLOOR - 230), (x + 120, FLOOR - 150)], '#bfe4ff', lw=7)
    for wx in (x - 110, x + 110): T.shape(ellipse_pts(wx, FLOOR - 40, 44, 44, 20), '#2a2140', lw=6)
    label(c, 'SLEEPY DRIVING', 1300, 200, 70, '#ffffff', 0, back((u - 0.2)/0.3, 1.5))
    if u > 1.0:
        T.stroke([(1000, 200), (1600, 220)], lw=16, col='#ff3b5c', screen=True)
        kin(c, t, 'GONE!', t0 + 1.0, 1300, 330, 100, '#ff3b5c', -0.05)

def sh_books(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, par=True, extra=dict(brow=0.9, sm=1.0, er=46, look=(-0.6, 0.2), armF=((-120, -60), 30)))
    for k in range(int(clamp(u/1.2)*7)):
        T.shape(rect(820 + (k % 2)*12, FLOOR - 40 - k*46, 220, 44), ('#ff4fa3', '#4fd8ff', '#ffd43b', '#7dff9a')[k % 4], lw=6)
    if u > 1.8:
        for k in range(4): T.shape(ellipse_pts(1460 + k*40, FLOOR - 30 - (k % 2)*30, 40, 40, 16), '#c98a4a', lw=5)
        kin(c, t, '+ SNACKS', t0 + 1.8, 1500, 420, 70, '#ffd43b', 0.05)

# ---------- chapter 7: your turn
def sh_poll(T, t, t0):
    sh_end(T, t, t0, poll=('KEEP SLEEP', 'NEVER SLEEP'), poll_t=(1.2, 2.4))

def sh_goodnight(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.012*u); room(T, t, par=True)
    bed(T, 1300, FLOOR + 40, 0.95, '#7b5cff')
    draw_kiko(T, kiko_talk(t, dict(x=1300, y=FLOOR + 60, s=0.8, face=-1, look=(-0.3, 0.2), lid=0.8 if u > 2.0 else 0.2, brow=0.5, sm=0.7)))
    T.shape(rect(1060, FLOOR - 100, 480, 70), '#7b5cff', shadow='#5f43d6', shade_dir=(0, 1), shade_w=0.3, lw=7)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.6, sm=0.4)))
    if u > 2.0: zzz(T, c, t, 1340, 520, 1.2)

def sh_morning(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.012*u); room(T, t, par=True)
    T.shape(ellipse_pts(520, 420, 70, 70, 24), '#ffd43b', lw=6)   # sun rising in the window
    bed(T, 1300, FLOOR + 40, 0.95, '#7b5cff')
    draw_kiko(T, kiko_talk(t, dict(x=1300, y=FLOOR + 60, s=0.8, face=-1, look=(-0.6, -0.2), lid=0.0, brow=-0.6, sm=-0.4, er=46, sweat=True)))
    T.shape(rect(1060, FLOOR - 100, 480, 70), '#7b5cff', shadow='#5f43d6', shade_dir=(0, 1), shade_w=0.3, lw=7)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0), brow=0.9, sm=0.7, armF=((-150, -100), 40))))
    if u > 0.8: kin(c, t, 'GOOD MORNING!', t0 + 0.8, 960, 170, 80, '#ffd43b', -0.03)


def shots(LK):
    EDL = [
        (0.0, lambda T, t: sh_wake(T, t, 0.0)),
        (L(1), lambda T, t: sh_sleepy_nova(T, t, L(1))),
        (L(2), lambda T, t: sh_kiko_idea(T, t, L(2))),
        (L(3), lambda T, t: sh_sleepy_nova(T, t, L(3), yawn=True)),
        (L(4), lambda T, t: sh_freetime(T, t, L(4))),
        (L(5), lambda T, t: sh_third(T, t, L(5))),
        (L(6), lambda T, t: sh_years(T, t, L(6))),
        (L(7), lambda T, t: sh_seven(T, t, L(7))),
        (L(8), lambda T, t: sh_onein3(T, t, L(8))),
        (L(9), lambda T, t: sh_grownups(T, t, L(9))),
        (L(10), lambda T, t: sh_sorting(T, t, L(10))),
        (L(11), lambda T, t: sh_gaps(T, t, L(11))),
        (L(12), lambda T, t: sh_wash(T, t, L(12))),
        (L(13), lambda T, t: sh_kcu(T, t, L(13), extra=dict(brow=0.9, er=48, sm=0.8, look=(-0.6, -0.3), armF=((-60, -40), 30), armB=((60, -40), -30)))),
        (L(14), lambda T, t: sh_gene(T, t, L(14))),
        (L(15), lambda T, t: sh_kcu(T, t, L(15), extra=dict(brow=0.7, sm=0.9, armF=((-60, -250), 10)))),
        (E(15) - 0.1, lambda T, t: sh_portal(T, t, E(15) - 0.1)),
        (L(16) + 0.3, lambda T, t: sh_par_room(T, t, L(16) + 0.3, 'WORLD #15 · SLEEP: NOT NEEDED')),
        (L(17), lambda T, t: sh_clock24(T, t, L(17))),
        (L(18), lambda T, t: sh_school(T, t, L(18))),
        (L(19), lambda T, t: sh_gameroom(T, t, L(19))),
        (L(20), lambda T, t: sh_pancakes(T, t, L(20))),
        (L(21), lambda T, t: sh_catch(T, t, L(21))),
        (L(22), lambda T, t: sh_newtrick(T, t, L(22))),
        (L(23), lambda T, t: sh_nodreams(T, t, L(23))),
        (L(24), lambda T, t: sh_blanket(T, t, L(24))),
        (L(25), lambda T, t: sh_kcu(T, t, L(25), par=True, extra=dict(brow=-0.6, sm=-0.5, lid=0.3, look=(-0.6, 0.2)))),
        (L(26), lambda T, t: sh_workers(T, t, L(26))),
        (L(27), lambda T, t: sh_driving(T, t, L(27))),
        (L(28), lambda T, t: sh_books(T, t, L(28))),
        (L(29), lambda T, t: sh_ncu(T, t, L(29), par=True, extra=dict(lid=0.4, brow=0.1, sm=0.4, look=(0.9, 0)))),
        (L(30), lambda T, t: sh_poll(T, t, L(30))),
        (L(31), lambda T, t: sh_goodnight(T, t, L(31))),
        (L(32), lambda T, t: sh_morning(T, t, L(32))),
        (L(33), lambda T, t: sh_poll(T, t, L(33) - 3.0)),
    ]
    return EDL, S(16), set()

def thumbnail(c, LK):
    from thumbkit import burst, big_text, emoji_burst, arrow
    burst(c, 1920, 1080, 1300, 600, '#ff9fd1', '#3b1f8c')
    T = Toon(c, 3.0); T.cx, T.cy, T.z = 960, 540, 1.0
    draw_nova(T, dict(t=3.0, x=480, y=1480, s=1.5, face=1, look=(0.5, -0.1), lid=0.7, brow=-0.5, sm=-0.3, o=0.6, armF=((-40, -260), 10)))
    draw_kiko(T, dict(t=3.0, x=1480, y=1500, s=1.4, face=-1, look=(-0.8, -0.1), brow=0.9, sm=0.9, o=0.45, er=48, armF=((170, -60), -30)))
    clock(T, c, 980, 760, 130, 3, 0)
    big_text(c, 'NEVER', 1350, 200, 170); big_text(c, 'SLEEP?!', 1350, 400, 190, hl=1, hl_col='#ffffff', hl_box='#ff2d55')
    emoji_burst(c, 760, 330, 120, '+8 HRS', '#7dff9a', -0.15)
    arrow(c, 820, 450, 920, 600, '#ffd43b', 26)
