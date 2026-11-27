"""LONG05 - What if humans could eat sunlight (photosynthesize)? (WHAT IF, parallel world)
Research gate (2026-11-27): curiosity 5, relatable 4, visual 5, certainty 4, freshness 3 = 21/25.
Fresh angle: the 'one banana a day' number + real animals that already borrow photosynthesis.
Facts and sources:
- Photosynthesis: light + water + carbon dioxide -> sugar (+ oxygen). Chlorophyll absorbs mostly red and blue light and
  reflects green, so leaves look green (Britannica "Photosynthesis"; Wikipedia "Chlorophyll").
- Typical plants/crops store only about 1-2% of incoming sunlight as chemical energy (Britannica "Energy efficiency of
  photosynthesis"; Wikipedia "Photosynthetic efficiency"; Harvard BioNumbers).
- Green sea slug Elysia chlorotica keeps chloroplasts from the algae it eats and can live for months on sunlight
  (Smithsonian Magazine 2015; Yale e360; MBL news; Wikipedia "Elysia chlorotica").
- Spotted salamander embryos have algae living inside their cells, the first known case in a vertebrate
  (Kerney et al. 2011, PNAS, PMC3091133; Scienceline 2021).
- Adults: around 2,000 kcal/day is the reference used on US food labels (FDA); a medium banana is about 105 kcal (USDA).
- Rough estimate (labelled as 'roughly' in the video, arithmetic): a sunny day gives about 5-7 kWh per m2; if ~1 m2 of
  skin (about half of an adult's ~2 m2) faced the sun all day at 1-2% -> about 50-140 Wh = about 45-120 kcal, i.e. about
  one banana. To get ~2,000 kcal (2.3 kWh) at ~1.5% you would need ~25 m2: the floor of a big living room.
  Live Science ("What if humans had photosynthetic skin?") reaches the same conclusion: only a small fraction of needs.
Original cast only. Parallel-world consequences are imagined and labelled as such."""
LINES = [
 {"who": "KIKO", "text": "Nova! I'm starving, and lunch is still two hours away!", "gap": 0.4, "ch": 1},
 {"who": "NOVA", "text": "Plants never have that problem. They just stand in the sun and make their own food.", "gap": 0.4, "ch": 1},
 {"who": "KIKO", "text": "Wait. What if I could do that? Lunch... made of sunshine!", "gap": 0.4, "ch": 1},
 {"who": "NOVA", "text": "Solar powered Kiko. Let's find out if it works.", "gap": 0.9, "ch": 1},
 {"who": "NOVA", "text": "In our world, plants make food by photosynthesis. Light, water and air go in. Sugar comes out.", "gap": 0.35, "ch": 2},
 {"who": "KIKO", "text": "So every leaf is a tiny kitchen?", "gap": 0.35, "ch": 2},
 {"who": "NOVA", "text": "Kind of! And the cook is a green chemical called chlorophyll.", "gap": 0.35, "ch": 2},
 {"who": "NOVA", "text": "It soaks up red and blue light, and bounces green light back. That's why leaves look green.", "gap": 0.35, "ch": 2},
 {"who": "KIKO", "text": "So plants are green because they don't want green? Rude.", "gap": 0.9, "ch": 2},
 {"who": "NOVA", "text": "And some animals already borrow this trick.", "gap": 0.35, "ch": 3},
 {"who": "NOVA", "text": "A green sea slug eats algae, and keeps their tiny food factories inside its own body.", "gap": 0.35, "ch": 3},
 {"who": "NOVA", "text": "Then it can live for months, just soaking up sunlight.", "gap": 0.35, "ch": 3},
 {"who": "KIKO", "text": "A slug that eats sunshine?! Legend.", "gap": 0.4, "ch": 3},
 {"who": "NOVA", "text": "And baby spotted salamanders have algae living right inside their cells, while they grow in their eggs.", "gap": 0.35, "ch": 3},
 {"who": "KIKO", "text": "Okay. Nature is way weirder than me.", "gap": 0.9, "ch": 3},
 {"who": "NOVA", "text": "But in this parallel world... humans can photosynthesize. Our skin is full of chlorophyll.", "gap": 0.4, "ch": 4},
 {"who": "KIKO", "text": "Look at me! I'm a walking salad!", "gap": 0.4, "ch": 4},
 {"who": "NOVA", "text": "Lunch break means standing in the sun. And shady trees are suddenly not popular.", "gap": 0.4, "ch": 4},
 {"who": "KIKO", "text": "And cloudy days? Hungry days!", "gap": 0.9, "ch": 4},
 {"who": "NOVA", "text": "But here's the catch. Plants only turn about one or two percent of sunlight into food.", "gap": 0.35, "ch": 5,
  "cap": "But here's the catch. Plants only turn about 1-2% of sunlight into food."},
 {"who": "NOVA", "text": "If half your skin faced the sun all day, you'd make roughly the energy of one banana.", "gap": 0.4, "ch": 5},
 {"who": "KIKO", "text": "One banana?! That's just a snack!", "gap": 0.4, "ch": 5},
 {"who": "NOVA", "text": "Most adults need around two thousand calories a day. A banana has about one hundred.", "gap": 0.35, "ch": 5,
  "cap": "Most adults need around 2,000 calories a day. A banana has about 100."},
 {"who": "NOVA", "text": "To live on sunlight alone, you'd need skin as big as a living room floor.", "gap": 0.4, "ch": 5},
 {"who": "KIKO", "text": "So I'd be a giant, flat, green blanket. No thanks.", "gap": 0.9, "ch": 5},
 {"who": "NOVA", "text": "Still, there's a good side. Every sunny walk becomes a free little snack.", "gap": 0.35, "ch": 6},
 {"who": "NOVA", "text": "And a day at the beach counts as part of lunch.", "gap": 0.35, "ch": 6},
 {"who": "KIKO", "text": "And when Mom says go outside, I can say: I'm already charging!", "gap": 0.35, "ch": 6},
 {"who": "NOVA", "text": "Charging at one banana per day.", "gap": 0.9, "ch": 6},
 {"who": "NOVA", "text": "So... would you swap your skin for green, solar powered skin? Or keep your lunch?", "gap": 0.4, "ch": 7},
 {"who": "KIKO", "text": "Keep my lunch. Definitely. Can we eat now?", "gap": 0.45, "ch": 7},
 {"who": "NOVA", "text": "What would you pick? Comment below. A new parallel world, every day.", "gap": 1.8, "ch": 7},
]
CHAPTERS = {1: 'The lunch idea', 2: 'How plants eat light', 3: 'Animals that borrow it', 4: 'The parallel world',
            5: 'The banana catch', 6: 'The good side', 7: 'Your turn'}
META = dict(id='long05_eat_sunlight', title='What If Humans Could Eat SUNLIGHT? \U0001F300 Swirlverse',
    description=("Kiko is starving and has a big idea: what if humans could make food from sunlight, like plants?\n"
                 "Real science first: how photosynthesis works, why chlorophyll makes leaves green, and the real animals that "
                 "already borrow it (a green sea slug and spotted salamander embryos). Then we jump into a parallel world with "
                 "green, solar powered skin... and do the maths. Plants store only about 1-2% of sunlight as food, so a whole "
                 "sunny day on half your skin gives roughly one banana of energy (a rough estimate).\n\n"
                 "{CHAPTERS}\n\n"
                 "Sources: Britannica (Photosynthesis; Energy efficiency of photosynthesis), Smithsonian Magazine (green sea slug), "
                 "Kerney et al. 2011 in PNAS (algae in spotted salamander cells), FDA (2,000-calorie reference), USDA (banana).\n\n"
                 "#whatif #parallelworld #photosynthesis #science #swirlverse"),
    tags=['what if', 'parallel world', 'what if humans could photosynthesize', 'photosynthesis', 'chlorophyll',
          'solar powered sea slug', 'spotted salamander algae', 'science for everyone', 'biology facts', 'swirlverse'])
THINK = (5, 6)
# ===== SHOTS =====
from longkit import *

LEAF = '#5fd068'; LEAF_S = '#3ea84a'

def sun(T, c, t, x, y, r=90):
    for k in range(12):
        a = k*math.pi/6 + t*0.4
        T.stroke([(x + (r + 20)*math.cos(a), y + (r + 20)*math.sin(a)), (x + (r + 70)*math.cos(a), y + (r + 70)*math.sin(a))], lw=12, col='#ffb627')
    T.shape(ellipse_pts(x, y, r, r, 30), '#ffd43b', shadow='#f2a541', shade_dir=(1, 0.6), shade_w=0.25, lw=7)

def leaf(T, x, y, s=1.0, rot=0.0, col=LEAF):
    pts = []
    for k in range(21):
        v = k/20; w = math.sin(v*math.pi)*60*s
        pts.append((v*200*s - 100*s, -w))
    for k in range(20, -1, -1):
        v = k/20; w = math.sin(v*math.pi)*60*s
        pts.append((v*200*s - 100*s, w))
    cs, sn = math.cos(rot), math.sin(rot)
    P = [(x + px*cs - py*sn, y + px*sn + py*cs) for px, py in pts]
    T.shape(P, col, shadow=LEAF_S, shade_dir=(0, 1), shade_w=0.3, lw=6)
    T.stroke([(x - 90*s*cs, y - 90*s*sn), (x + 90*s*cs, y + 90*s*sn)], lw=4, col=LEAF_S)

def sprout(T, x, y, s=1.0, t=0.0):
    T.stroke([(x, y), (x + 4*s*math.sin(t*2), y - 70*s)], lw=8, col=LEAF_S)
    leaf(T, x - 50*s, y - 80*s, 0.45*s, -0.5 + 0.08*math.sin(t*3))
    leaf(T, x + 50*s, y - 85*s, 0.45*s, 0.5 - 0.08*math.sin(t*3))

def banana(T, x, y, s=1.0, rot=0.0):
    out = ellipse_pts(0, 0, 170*s, 110*s, 24, 0.15*math.pi, 0.85*math.pi)
    inn = ellipse_pts(0, -40*s, 140*s, 80*s, 24, 0.85*math.pi, 0.15*math.pi - 0.0001) if False else list(reversed(ellipse_pts(0, -45*s, 150*s, 85*s, 24, 0.12*math.pi, 0.88*math.pi)))
    cs, sn = math.cos(rot), math.sin(rot)
    P = [(x + px*cs - py*sn, y + px*sn + py*cs) for px, py in out + inn]
    T.shape(P, '#ffe066', shadow='#f2c230', shade_dir=(0, 1), shade_w=0.35, lw=7)
    ex, ey = P[0]; T.dot(ex, ey, 9*s, '#6b4a2a')

def plate(T, x, y, s=1.0):
    T.shape(ellipse_pts(x, y, 220*s, 60*s, 30), '#ffffff', shadow='#d9d4c4', shade_dir=(0, 1), shade_w=0.3, lw=7)

def chloroplast(T, x, y, s=1.0, t=0.0):
    T.shape(ellipse_pts(x, y, 120*s, 70*s, 30), '#7ee07a', shadow='#4cb85a', shade_dir=(1, 0.6), shade_w=0.3, lw=6)
    for k in range(4):
        sx = x - 75*s + k*50*s
        for j in range(3): T.shape(ellipse_pts(sx, y - 24*s + j*20*s, 18*s, 8*s, 12), '#2f8f45', lw=3)

def slug(T, x, y, s=1.0, t=0.0):
    pts = []
    for k in range(41):
        v = k/40; w = math.sin(v*math.pi)**0.8*90*s*(1 + 0.08*math.sin(v*12 + t*3))
        pts.append((x - 230*s + v*460*s, y - w))
    for k in range(40, -1, -1):
        v = k/40; w = math.sin(v*math.pi)**0.8*40*s
        pts.append((x - 230*s + v*460*s, y + w))
    T.shape(pts, '#47c46b', shadow='#2f9a50', shade_dir=(0, 1), shade_w=0.35, lw=7)
    for k in range(6): T.stroke([(x - 160*s + k*60*s, y - 10*s), (x - 130*s + k*60*s, y - 60*s)], lw=4, col='#2f9a50')
    hx = x - 230*s
    T.stroke([(hx + 20*s, y - 10*s), (hx - 20*s, y - 70*s)], lw=7, col='#2f9a50'); T.stroke([(hx + 30*s, y - 10*s), (hx + 10*s, y - 80*s)], lw=7, col='#2f9a50')
    T.dot(hx + 30*s, y + 2*s, 8*s)

def egg(T, x, y, r, t=0.0, k=1.0):
    T.shape(ellipse_pts(x, y, r*k, r*k, 30), '#d8f3ff', lw=6, alpha=0.85)
    # curled embryo
    T.stroke([(x + 0.45*r*k*math.cos(a), y + 0.45*r*k*math.sin(a)) for a in [i*0.3 for i in range(18)]], lw=int(22*k) + 1, col='#e6c79a')
    T.dot(x + 0.45*r*k, y, 12*k, '#e6c79a')
    for i in range(9):
        a = i*0.7 + t*0.5
        T.dot(x + 0.75*r*k*math.cos(a), y + 0.75*r*k*math.sin(a), 8*k, '#3fbf5f')

def living_room(T, x, y, w, h, k=1.0):
    T.shape(rect(x, y, w*k, h*k), '#c98a5a', lw=7)
    for i in range(1, 6): T.stroke([(x + w*k*i/6, y), (x + w*k*i/6, y + h*k)], lw=4, col='#a86e34')

def tint(c, col, a):
    c.save(); r, g, b = int(col[1:3], 16)/255, int(col[3:5], 16)/255, int(col[5:7], 16)/255
    c.set_source_rgba(r, g, b, a); c.paint(); c.restore()

# ---------- chapter 1: the lunch idea
def sh_starving(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.025*u); room(T, t)
    plate(T, 960, FLOOR - 20, 0.9)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0.1), brow=0.3, sm=0.3)))
    draw_kiko(T, kiko_talk(t, dict(x=1320, y=FLOOR + 150, s=0.95, face=-1, look=(-0.6, 0.3), brow=-0.7, sm=-0.6, er=46, sweat=True,
                                    armF=((-60, -60), 30), armB=((60, -60), -30), jit=jitter(t, 3))))
    if u > 0.6: kin(c, t, 'GRRRUMBLE', t0 + 0.6, 1380, 250, 80, '#ffd43b', 0.05)
    if u > 1.4: kin(c, t, 'LUNCH IN 2 HOURS', t0 + 1.4, 960, 120, 60, '#ff4fa3', -0.02)

def sh_plant_sun(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); street(T, t, par=False)
    sun(T, c, t, 1600, 190, 90)
    T.shape(rect(860, FLOOR - 160, 200, 160), '#e07a4a', lw=7)
    T.stroke([(960, FLOOR - 160), (960, FLOOR - 420)], lw=12, col=LEAF_S)
    for j, (dx, dy, r) in enumerate(((-90, -260, -0.6), (90, -320, 0.6), (-80, -380, -0.4), (80, -430, 0.4))):
        leaf(T, 960 + dx, FLOOR + dy, 0.8, r + 0.06*math.sin(t*2 + j))
    for i in range(4):   # light beams
        v = ((u*0.7 + i/4) % 1)
        T.stroke([(1550 - 590*v, 240 + 360*v - 30), (1530 - 590*v, 260 + 360*v - 30)], lw=14, col='#ffe066', alpha=0.9)
    label(c, 'FREE FOOD?', 480, 200, 90, '#ffffff', -0.03, back((u - 0.6)/0.3, 1.5))

def sh_kiko_idea(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, extra=dict(brow=0.9, sm=0.9, er=48, look=(-0.6, -0.4), armF=((-60, -260), 10)))
    k = back((u - 0.8)/0.3, 1.6)
    if k > 0.01:
        sun(T, c, t, 1520, 230, 70*k)
        label(c, 'SUNSHINE LUNCH?!', 1150, 120, 70, '#ffd43b', -0.03, k)

def sh_solar(T, t, t0):
    def extra(T, t, u):
        sun(T, T.c, t, 1650, 180, 60)
        kin(T.c, t, 'SOLAR KIKO?', t0 + 0.4, 1300, 330, 70, '#7dff9a', 0.04)
    sh_twoshot(T, t, t0, np_=dict(brow=0.8, sm=0.7, armF=((-200, -60), 30)), kp=dict(brow=0.9, sm=1.0, er=48, armF=((-200, -220), 30), armB=((200, -220), -30)), extra_draw=extra)

# ---------- chapter 2: how plants eat light
def sh_recipe(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f3a2a', '#2c5040')
    label(c, 'PHOTOSYNTHESIS', W/2, 150, 90, '#7dff9a', 0, back(u/0.3, 1.4))
    items = [('LIGHT', '#ffd43b'), ('WATER', '#4fd8ff'), ('AIR (CO2)', '#c9d2de')]
    for i, (txt, col) in enumerate(items):
        k = back((u - 0.8 - i*0.45)/0.3, 1.6)
        if k <= 0.01: continue
        y = 360 + i*170
        T.shape(ellipse_pts(330, y, 60*k, 60*k, 24), col, lw=6)
        label(c, txt, 620, y, 60, col, 0, k)
    leaf(T, 1100, 530, 1.3*back((u - 0.4)/0.4, 1.3) + 0.01, -0.2)
    if u > 3.2:
        T.stroke([(1280, 530), (1440, 530)], lw=14, col='#ffffff')
        T.shape([(1440, 500), (1490, 530), (1440, 560)], '#ffffff', lw=5)
        kin(c, t, 'SUGAR!', t0 + 3.2, 1660, 530, 90, '#ff8fb8', -0.04)

def sh_kitchen(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, extra=dict(brow=0.8, sm=0.6, er=46, look=(-0.7, -0.3), armF=((-120, -200), 20)))
    k = back((u - 0.3)/0.3, 1.5)
    if k > 0.01:
        leaf(T, 1560, 260, 1.0*k, -0.15)
        T.shape(rect(1510, 150, 100*k, 40*k), '#ffffff', lw=5)   # tiny chef hat
        T.shape(ellipse_pts(1560, 140, 60*k, 40*k, 20), '#ffffff', lw=5)
        label(c, 'LEAF KITCHEN', 1560, 420, 54, '#3ea84a', 0.03, k)

def sh_chlorophyll(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.015*u); board(T, t, '#1f3a2a', '#2c5040')
    for i in range(3):
        k = back((u - 0.2 - i*0.2)/0.3, 1.6)
        chloroplast(T, 600 + i*360, 560 + 60*math.sin(i*2.0), 1.1*k + 0.01, t)
    label(c, 'CHLOROPHYLL', W/2, 200, 100, '#7dff9a', -0.02, back((u - 0.7)/0.3, 1.5))
    label(c, 'the green cook', W/2, 300, 50, '#ffffff', 0, back((u - 1.0)/0.3, 1.5), FONT, 10)

def sh_colors(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f2a4a', '#2c3a63')
    leaf(T, 960, 600, 1.6, 0.0)
    for i, (col, ok) in enumerate((('#ff3b5c', True), ('#7dff9a', False), ('#4f7dff', True))):
        k = clamp((u - 0.4 - i*0.5)/0.6)
        if k <= 0: continue
        y0 = 260 + i*60; x0 = 200
        xe = x0 + (760 - x0)*min(1, k*1.2)
        T.stroke([(x0, y0 + 200), (xe, y0 + 200 + (600 - y0 - 200)*min(1, k*1.2)*0.4)], lw=16, col=col)
        if not ok and k > 0.85:
            T.stroke([(800, 560), (1500, 220)], lw=16, col=col)
    if u > 1.6: label(c, 'RED + BLUE: EATEN', 1350, 760, 56, '#ffffff', 0, back((u - 1.6)/0.3, 1.5))
    if u > 2.6: label(c, 'GREEN: BOUNCED BACK', 1350, 860, 56, '#7dff9a', 0, back((u - 2.6)/0.3, 1.5))

def sh_rude(T, t, t0):
    sh_kcu(T, t, t0, extra=dict(brow=-0.7, sm=-0.3, er=44, look=(-0.4, 0.1), armF=((-150, -80), 40)))
    leaf(T, 1500, 330, 0.8, 0.3)
    kin(T.c, t, 'RUDE!', t0 + 1.8, 1500, 180, 90, '#ff4fa3', 0.05)

# ---------- chapter 3: animals that borrow it
def sh_borrow(T, t, t0):
    u = t - t0
    sh_ncu(T, t, t0, extra=dict(brow=0.8, sm=0.6, armF=((-150, -100), 40), look=(0.8, -0.1)))
    kin(T.c, t, 'BORROWED POWER', t0 + 0.5, 1300, 200, 70, '#7dff9a', -0.03)

def sh_slug(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u)
    for i in range(6): T.flat(rect(-2000, -2000 + i*560, 6000, 562), mixc('#2fa3c9', '#0f3c5a', i/5))
    for i in range(8):   # algae strands
        x = 200 + i*230; T.stroke([(x + 20*math.sin(t*1.5 + i + k*0.6), 1000 - k*60) for k in range(7)], lw=12, col='#3fbf5f')
    sx = 1250 - 120*ease(u/3)
    slug(T, sx, 640, 1.2, t)
    for i in range(5):   # chloroplasts flowing into the slug
        v = clamp((u - 0.5 - i*0.35)/0.8)
        if 0 < v < 1:
            x = 500 + (sx - 500)*ease(v); y = 820 - 180*ease(v)
            T.shape(ellipse_pts(x, y, 26, 16, 14), '#7ee07a', lw=4)
    label(c, 'GREEN SEA SLUG', W/2, 140, 90, '#ffffff', 0, back((u - 0.3)/0.3, 1.5))
    if u > 2.0: label(c, 'keeps the algae\'s food factories', W/2, 240, 46, '#d8f3ff', 0, back((u - 2.0)/0.3, 1.5), FONT, 10)

def sh_slug_months(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u)
    for i in range(6): T.flat(rect(-2000, -2000 + i*560, 6000, 562), mixc('#5fd0f0', '#1f6a8a', i/5))
    sun(T, c, t, 1600, 200, 80)
    for i in range(3):
        T.stroke([(1500 - i*60, 290), (1100 - i*60, 560)], lw=12, col='#ffe066', alpha=0.7)
    slug(T, 900, 640, 1.3, t)
    label(c, 'MONTHS', 600, 260, 130, '#ffd43b', -0.04, back((u - 0.4)/0.3, 1.6))
    label(c, 'on sunlight', 600, 370, 50, '#ffffff', 0, back((u - 0.7)/0.3, 1.5), FONT, 10)

def sh_legend(T, t, t0):
    u = t - t0
    sh_kcu(T, t, t0, extra=dict(brow=0.9, sm=1.0, er=48, look=(-0.6, -0.3), armF=((-60, -260), 10), armB=((60, -260), -10)))
    slug(T, 1560, 380, 0.5, t)
    kin(T.c, t, 'LEGEND!', t0 + 1.0, 1560, 200, 90, '#ffd43b', -0.05)

def sh_salamander(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f3a3a', '#2c5050')
    for i in range(5):
        k = back((u - 0.2 - i*0.15)/0.3, 1.5)
        if k > 0.01: egg(T, 330 + i*320, 600 + 40*math.sin(i*1.7), 120, t, k)
    label(c, 'SPOTTED SALAMANDER EGGS', W/2, 170, 76, '#ffffff', 0, back((u - 0.4)/0.3, 1.5))
    if u > 2.2: label(c, 'algae INSIDE their cells', W/2, 290, 56, '#7dff9a', 0, back((u - 2.2)/0.3, 1.5), FONT, 10)

def sh_weird(T, t, t0):
    sh_twoshot(T, t, t0, np_=dict(brow=0.6, sm=0.6), kp=dict(brow=-0.4, sm=0.3, er=44, armF=((-120, -160), 30)),
               extra_draw=lambda T, t, u: kin(T.c, t, 'WEIRD NATURE', t0 + 0.6, 960, 170, 80, '#7b5cff', -0.02))

# ---------- chapter 4: the parallel world
def sh_green_skin(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#3b1f8c', '#4c2fa0')
    k = ease((u - 0.6)/1.2)
    for i in range(5):
        col = mixc('#f7d9c4', '#5fd068', k)
        person_icon(T, 360 + i*300, 700, 7.0, col)
        if k > 0.7: sprout(T, 360 + i*300, 420, 0.8, t + i)
    label(c, 'GREEN SKIN', W/2, 170, 110, '#7dff9a', -0.02, back((u - 1.2)/0.3, 1.5))
    label(c, 'full of chlorophyll', W/2, 280, 50, '#ffffff', 0, back((u - 1.6)/0.3, 1.5), FONT, 10)

def sh_salad(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, par=True, extra=dict(brow=0.9, sm=1.0, er=48, look=(-0.6, -0.2), armF=((-200, -200), 30), armB=((200, -200), -30)))
    tint(c, '#5fd068', 0.18)
    for i in range(6):
        a = i*1.05 + t*0.7
        leaf(T, 1150 + 420*math.cos(a), 450 + 260*math.sin(a), 0.4, a)
    kin(c, t, 'WALKING SALAD!', t0 + 0.6, 1300, 150, 80, '#7dff9a', 0.03)

def sh_lunchbreak(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    sun(T, c, t, 1650, 170, 70)
    for i in range(4):
        x = 260 + i*190
        person_icon(T, x, FLOOR - 10, 5.0, '#5fd068')
        T.stroke([(x - 70, FLOOR - 250), (x - 110, FLOOR - 330)], lw=6, col='#ffe066')
    # lonely shady tree
    T.shape(rect(1330, FLOOR - 300, 50, 300), '#a86e34', lw=6)
    T.shape(ellipse_pts(1355, FLOOR - 380, 190, 150, 30), '#3ea84a', lw=7)
    label(c, 'LUNCH BREAK', 620, 300, 80, '#ffd43b', -0.03, back((u - 0.3)/0.3, 1.5))
    if u > 2.4: kin(c, t, 'NOBODY?', t0 + 2.4, 1355, 470, 64, '#ff4fa3', 0.05)

def sh_cloudy(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    cx = 1900 - 400*ease(u/1.2)
    for dx, dy, r in ((0, 0, 140), (-150, 30, 110), (150, 30, 110)):
        T.shape(ellipse_pts(cx + dx - 250, 180 + dy, r, r*0.75, 24), '#8e8aa8', lw=7)
    draw_kiko(T, kiko_talk(t, dict(x=960, y=FLOOR + 150, s=0.95, face=1, look=(0.6, -0.5), brow=-0.8, sm=-0.8, er=46, sweat=True,
                                    armF=((-60, -60), 30), armB=((60, -60), -30))))
    tint(c, '#5fd068', 0.12)
    if u > 0.9: kin(c, t, 'HUNGRY DAY!', t0 + 0.9, 1400, 480, 90, '#ff4fa3', -0.05)

# ---------- chapter 5: the banana catch
def sh_percent(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#3a1f2e', '#4c2a3c')
    for i in range(100):
        r, q = divmod(i, 20)
        x, y = 290 + q*70, 420 + r*80
        k = back((u - 0.2 - i*0.01)/0.2, 1.4)
        if k <= 0.01: continue
        col = '#7dff9a' if (i < 2 and u > 2.4) else '#ffd43b'
        T.shape(ellipse_pts(x, y, 24*k, 24*k, 14), col, lw=3)
    label(c, '100 SUN UNITS', W/2, 170, 80, '#ffd43b', 0, back((u - 0.2)/0.3, 1.5))
    if u > 2.4: label(c, 'ONLY 1-2 BECOME FOOD', W/2, 290, 66, '#7dff9a', 0, back((u - 2.4)/0.3, 1.5))

def sh_one_banana(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f2a4a', '#2c3a63')
    sun(T, c, t, 360, 300, 90)
    person_icon(T, 560, 760, 6.0, '#5fd068')
    k = clamp((u - 0.4)/2.4)
    x = 760 + 700*k   # the sun moves across: a whole day
    label(c, 'A WHOLE SUNNY DAY', 1180, 170, 66, '#ffffff', 0, back((u - 0.2)/0.3, 1.5))
    T.stroke([(760, 560), (760 + 640*k, 560)], lw=10, col='#ffe066')
    if u > 3.0:
        plate(T, 1460, 720, 0.9); banana(T, 1460, 650, 1.0*back((u - 3.0)/0.3, 1.5) + 0.01, 0.2)
        kin(c, t, '= 1 BANANA', t0 + 3.2, 1460, 440, 90, '#ffd43b', -0.04)
        label(c, '(roughly)', 1460, 520, 40, '#ffffff', 0, back((u - 3.4)/0.3, 1.5), FONT, 9)

def sh_snack(T, t, t0):
    u = t - t0; c = T.c
    sh_kcu(T, t, t0, par=True, extra=dict(brow=0.9, sm=-0.6, er=50, o=0.7, look=(-0.6, 0.2), armF=((-150, -120), 30)))
    tint(c, '#5fd068', 0.15)
    banana(T, 1450, 470, 0.55, -0.3)
    kin(c, t, 'JUST A SNACK?!', t0 + 0.6, 1350, 150, 80, '#ff4fa3', 0.04)

def sh_calories(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#3a1f2e', '#4c2a3c')
    x0, x1 = 260, 1660
    T.shape(rect(x0, 470, x1 - x0, 110), '#2a2140', lw=7)
    k = ease((u - 0.4)/1.2)
    T.shape(rect(x0, 470, (x1 - x0)*k + 1, 110), '#ff8fb8', lw=7)
    label(c, '~2,000 CALORIES A DAY', W/2, 330, 80, '#ffffff', 0, back((u - 0.4)/0.3, 1.5))
    if u > 2.6:
        T.shape(rect(x0, 640, (x1 - x0)*0.05, 110), '#ffe066', lw=7)
        banana(T, x0 + 230, 820, 0.45, 0.1)
        label(c, 'BANANA: ~100', 1150, 700, 76, '#ffd43b', -0.02, back((u - 2.6)/0.3, 1.5))

def sh_living_room(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); board(T, t, '#1f3a2a', '#2c5040')
    person_icon(T, 360, 760, 6.0, '#5fd068')
    k = ease((u - 0.6)/1.6)
    living_room(T, 620, 330, 1100, 560, max(0.02, k))
    if k > 0.95:
        T.shape(rect(700, 700, 300, 120), '#7b5cff', lw=6)    # sofa
        T.shape(rect(1400, 400, 200, 140), '#ffffff', lw=6)   # rug-ish
    label(c, 'SKIN THIS BIG', 1170, 220, 86, '#7dff9a', -0.02, back((u - 1.0)/0.3, 1.5))

def sh_blanket(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u); street(T, t, par=True)
    k = ease((u - 0.3)/1.2)
    T.shape([(960 - 700*k, FLOOR - 30), (960 - 600*k, FLOOR - 110), (960 + 600*k, FLOOR - 110), (960 + 700*k, FLOOR - 30)], '#5fd068', shadow=LEAF_S, shade_dir=(0, 1), shade_w=0.3, lw=7)
    T.shape(ellipse_pts(960, FLOOR - 170, 70, 60, 24), '#5fd068', lw=6)
    T.dot(940, FLOOR - 180, 8); T.dot(985, FLOOR - 180, 8)
    label(c, 'FLAT GREEN BLANKET', W/2, 250, 80, '#ffffff', 0, back((u - 0.6)/0.3, 1.5))
    if u > 2.2: kin(c, t, 'NO THANKS!', t0 + 2.2, W/2, 380, 90, '#ff4fa3', -0.04)

# ---------- chapter 6: the good side
def sh_walk(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    sun(T, c, t, 1650, 170, 70)
    x = 300 + 260*u
    draw_nova(T, nova_talk(t, dict(x=x, y=FLOOR + 140, s=0.9, face=1, look=(0.8, -0.3), brow=0.8, sm=0.8)))
    tint(c, '#5fd068', 0.1)
    if u > 1.2: kin(c, t, '+ FREE SNACK', t0 + 1.2, 1300, 380, 80, '#7dff9a', 0.04)

def sh_beach(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 540, 1.0 + 0.012*u)
    for i, col in enumerate(PAR_SKY): T.flat(rect(-2000, -2000 + (i > 0)*(2000 + i*110), 6000, 2110 if i == 0 else 112), col)
    T.flat(rect(-2000, 640, 6000, 200), '#4fd8ff')
    for k in range(5): T.stroke([(-200 + j*120, 680 + k*30 + 8*math.sin(j + t*3)) for j in range(20)], lw=5, col='#bfe4ff')
    T.shape(rect(-2000, 820, 6000, 600), '#ffe0a3', lw=7)
    sun(T, c, t, 1600, 170, 80)
    T.shape(rect(700, 860, 420, 60), '#ff4fa3', lw=6)  # towel
    person_icon(T, 900, 820, 4.5, '#5fd068')
    label(c, 'BEACH = LUNCH', 700, 220, 100, '#ffd43b', -0.03, back((u - 0.3)/0.3, 1.5))
    label(c, '(part of it)', 700, 330, 46, '#ffffff', 0, back((u - 0.7)/0.3, 1.5), FONT, 10)

def sh_charging(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 520, 1.0 + 0.02*u); street(T, t, par=True)
    sun(T, c, t, 1650, 170, 70)
    draw_kiko(T, kiko_talk(t, dict(x=900, y=FLOOR + 150, s=0.95, face=1, look=(0.6, -0.5), brow=0.9, sm=1.0, er=48,
                                    armF=((-200, -250), 20), armB=((200, -250), -20))))
    tint(c, '#5fd068', 0.12)
    # battery
    bx, by = 1380, 520; k = clamp(u/3.0)
    T.shape(rect(bx, by, 260, 130), '#ffffff', lw=8); T.shape(rect(bx + 260, by + 40, 24, 50), '#ffffff', lw=6)
    T.shape(rect(bx + 14, by + 14, 232*k + 1, 102), '#7dff9a', line=False)
    kin(c, t, 'CHARGING...', t0 + 1.0, 1500, 420, 66, '#7dff9a', 0.03)

def sh_one_per_day(T, t, t0):
    u = t - t0; c = T.c
    sh_ncu(T, t, t0, par=True, extra=dict(brow=0.4, sm=0.6, lid=0.3, look=(0.9, 0)))
    tint(c, '#5fd068', 0.1)
    banana(T, 1150, 300, 0.6, 0.2)
    kin(c, t, '1 BANANA / DAY', t0 + 0.5, 1150, 150, 70, '#ffd43b', -0.03)

# ---------- chapter 7: your turn
def sh_poll(T, t, t0):
    sh_end(T, t, t0, poll=('GREEN SKIN', 'KEEP LUNCH'), poll_t=(1.2, 2.4))

def sh_eat_now(T, t, t0):
    u = t - t0; c = T.c
    cam(T, 960, 560, 1.0 + 0.02*u); room(T, t)
    plate(T, 960, FLOOR - 20, 0.9)
    for k in range(3): T.shape(ellipse_pts(900 + k*60, FLOOR - 60 - (k % 2)*20, 50, 30, 16), ('#f2a541', '#7ac74f', '#ff8fb8')[k], lw=5)
    draw_nova(T, nova_talk(t, dict(x=560, y=FLOOR + 140, s=0.95, face=1, look=(0.8, 0.1), brow=0.6, sm=0.7)))
    draw_kiko(T, kiko_talk(t, dict(x=1320, y=FLOOR + 150, s=0.95, face=-1, look=(-0.6, 0.3), brow=0.9, sm=1.0, er=48,
                                    armF=((-200, -120), 30))))
    if u > 1.0: kin(c, t, 'LUNCH!', t0 + 1.0, 960, 170, 100, '#ffd43b', -0.03)


def shots(LK):
    EDL = [
        (0.0, lambda T, t: sh_starving(T, t, 0.0)),
        (L(1), lambda T, t: sh_plant_sun(T, t, L(1))),
        (L(2), lambda T, t: sh_kiko_idea(T, t, L(2))),
        (L(3), lambda T, t: sh_solar(T, t, L(3))),
        (L(4), lambda T, t: sh_recipe(T, t, L(4))),
        (L(5), lambda T, t: sh_kitchen(T, t, L(5))),
        (L(6), lambda T, t: sh_chlorophyll(T, t, L(6))),
        (L(7), lambda T, t: sh_colors(T, t, L(7))),
        (L(8), lambda T, t: sh_rude(T, t, L(8))),
        (L(9), lambda T, t: sh_borrow(T, t, L(9))),
        (L(10), lambda T, t: sh_slug(T, t, L(10))),
        (L(11), lambda T, t: sh_slug_months(T, t, L(11))),
        (L(12), lambda T, t: sh_legend(T, t, L(12))),
        (L(13), lambda T, t: sh_salamander(T, t, L(13))),
        (L(14), lambda T, t: sh_weird(T, t, L(14))),
        (E(14) - 0.1, lambda T, t: sh_portal(T, t, E(14) - 0.1)),
        (L(15) + 0.3, lambda T, t: sh_par_room(T, t, L(15) + 0.3, 'WORLD #16 · HUMANS: SOLAR POWERED')),
        (at(15, 0.5), lambda T, t: sh_green_skin(T, t, at(15, 0.5))),
        (L(16), lambda T, t: sh_salad(T, t, L(16))),
        (L(17), lambda T, t: sh_lunchbreak(T, t, L(17))),
        (L(18), lambda T, t: sh_cloudy(T, t, L(18))),
        (L(19), lambda T, t: sh_percent(T, t, L(19))),
        (L(20), lambda T, t: sh_one_banana(T, t, L(20))),
        (L(21), lambda T, t: sh_snack(T, t, L(21))),
        (L(22), lambda T, t: sh_calories(T, t, L(22))),
        (L(23), lambda T, t: sh_living_room(T, t, L(23))),
        (L(24), lambda T, t: sh_blanket(T, t, L(24))),
        (L(25), lambda T, t: sh_walk(T, t, L(25))),
        (L(26), lambda T, t: sh_beach(T, t, L(26))),
        (L(27), lambda T, t: sh_charging(T, t, L(27))),
        (L(28), lambda T, t: sh_one_per_day(T, t, L(28))),
        (L(29), lambda T, t: sh_poll(T, t, L(29))),
        (L(30), lambda T, t: sh_eat_now(T, t, L(30))),
        (L(31), lambda T, t: sh_poll(T, t, L(31) - 3.0)),
    ]
    return EDL, S(15), set()

def thumbnail(c, LK):
    from thumbkit import burst, big_text, emoji_burst, arrow
    burst(c, 1920, 1080, 1300, 600, '#b8ffb0', '#1f6a3a')
    T = Toon(c, 3.0); T.cx, T.cy, T.z = 960, 540, 1.0
    sun(T, c, 3.0, 1000, 230, 110)
    draw_kiko(T, dict(t=3.0, x=520, y=1500, s=1.45, face=1, look=(0.7, -0.4), brow=0.9, sm=-0.4, o=0.8, er=50, armF=((-170, -80), 30)))
    plate(T, 1000, 900, 1.0); banana(T, 1000, 830, 1.1, 0.2)
    big_text(c, 'SUN', 1500, 210, 190); big_text(c, 'LUNCH?!', 1500, 420, 180, hl=1, hl_col='#ffffff', hl_box='#2fa84a')
    emoji_burst(c, 1500, 680, 130, '= 1 BANANA', '#ffd43b', -0.12)
    arrow(c, 1330, 760, 1160, 820, '#ff2d55', 26)
