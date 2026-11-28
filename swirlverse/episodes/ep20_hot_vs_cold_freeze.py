"""EP20 - Hot water vs cold water: which FREEZES first? (Short, VS format with an IT DEPENDS verdict and a parallel-world test)
Format: VS (first VS on the channel) + portal test ("hot-always-wins world"). Topic family: everyday physics / kitchen
(proven family; the last Shorts were brain/psychology and pets).
Gate score: curiosity 5 (classic 'people also ask' question, endless forum threads), relatable 4 (everyone has an ice tray),
visual 4 (two cups racing in a freezer), fact certainty 4 (the honest answer is that it is still debated), freshness 3
(many videos simply claim "hot freezes faster"; our angle is the VS race with an honest IT DEPENDS verdict plus a
parallel world where hot always wins) = 20/25. No score is 1.
Facts (checked, 2+ sources each):
- The claim that hot water can freeze before cold is called the Mpemba effect, after a student in Tanzania who noticed hot
  ice-cream mix freezing first in the 1960s (PBS NOVA "The ice cream that changed physics"; Wikipedia "Mpemba effect";
  Royal Society of Chemistry 2012 Mpemba competition press release). The video does not show or quote any real person.
- Results keep disagreeing: the Royal Society of Chemistry ran a 2012 competition to explain it; Quanta Magazine (2022)
  "Does hot water freeze faster than cold? Physicists keep asking"; Chemistry World on the dispute.
- Small details change the result: container, freezer, how 'freezing' is defined, and where the thermometer sits.
  Burridge & Linden 2016 (Scientific Reports, Imperial College / Cambridge; PMC5121640) found results are very sensitive
  to thermocouple position, and with careful measurement found no evidence that hot water cools faster ("Questioning the
  Mpemba effect: hot water does not cool more quickly than cold"). So "in one careful 2016 test, hot water did not win".
- Verdict "IT DEPENDS / still debated" is the honest summary (Quanta 2022; Chemistry World; Wikipedia).
- Parallel-world part is labelled imaginary (hot water always freezes first). No numbers are claimed for it.
Sources: PBS NOVA; Burridge & Linden 2016 Scientific Reports (Imperial, via PMC); Quanta Magazine 2022; Chemistry World;
Royal Society of Chemistry. No real people shown, no brands."""
import math
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Hot water versus cold water. Which one freezes first?",
         cap="Hot water vs cold water. Which one freezes first?", gap=0.3),
    dict(who=N, text="Some people say hot water wins! It's called the Mpemba effect.", gap=0.3),
    dict(who=N, text="A student in Tanzania spotted it in the nineteen sixties, making ice cream.",
         cap="A student in Tanzania spotted it in the 1960s, making ice cream.", gap=0.3),
    dict(who=K_, text="Wait, so hot water really is faster?!", gap=0.3),
    dict(who=N, text="Scientists have tested it for years, and the results keep changing.", gap=0.3),
    dict(who=N, text="Tiny details matter. The cup, the freezer, even the thermometer spot.", gap=0.3),
    dict(who=N, text="In one careful test in twenty sixteen, hot water did not win. So? It depends!",
         cap="In one careful test in 2016, hot water did NOT win. So? It depends!", gap=0.35),
    dict(who=N, text="But in this parallel world, hot water always freezes first.", gap=0.3),
    dict(who=K_, text="Whoa! My hot cocoa turned to ice before my cold juice!", gap=0.35),
    dict(who=N, text="Hot wins, or cold wins? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep20_hot_vs_cold_freeze', our_set='room', par_set='room',
    title="Hot vs Cold Water: Which FREEZES First? \U0001F300 #Swirlverse",
    description=("Hot water vs cold water: which one freezes first? Some people say hot water wins. It's called the Mpemba effect, "
                 "after a student in Tanzania who noticed hot ice-cream mix freezing first in the 1960s. "
                 "But scientists keep getting different results: the cup, the freezer and even where you put the thermometer change the answer. "
                 "In one careful 2016 study, hot water did NOT cool faster. So the honest verdict: it depends, and it's still debated! "
                 "And in this parallel world, hot water ALWAYS freezes first... \U0001F9CA\n"
                 "Hot wins or cold wins? Comment below \U0001F447\n\n"
                 "Sources: Burridge & Linden 2016 (Scientific Reports, Imperial College London), PBS NOVA, Quanta Magazine, "
                 "Chemistry World, Royal Society of Chemistry.\n\n"
                 "#shorts #science #physics #mpembaeffect #swirlverse"),
    tags=['mpemba effect', 'does hot water freeze faster', 'hot water vs cold water', 'hot water freezes faster',
          'which freezes first', 'freezing water', 'ice', 'physics', 'science experiment', 'myth or fact',
          'parallel world', 'science shorts', 'swirlverse', 'animation'],
    topic='hot vs cold water which freezes first / Mpemba effect (1960s Tanzania ice cream, results depend on cup/freezer/thermometer, 2016 careful test: hot did not win, still debated; hot-always-wins world)',
    category='everyday physics',
    hook='VS cold open (hot cup vs cold cup) -> Mpemba claim -> freezer race -> details matter -> IT DEPENDS verdict -> portal test',
)
DROPS = []

HOT, COLD, ICE = '#ff6b4a', '#4fb8ff', '#d8f4ff'

def cup(T, t, x, y, s=1.0, liquid=HOT, steam=True, frozen=0.0, mug='#ffffff'):
    """a mug with liquid; frozen 0..1 turns the top into ice; steam puffs when hot. (x, y) = bottom centre"""
    w, h = 170*s, 200*s
    T.shape([(x - w/2, y - h), (x + w/2, y - h), (x + w/2*0.88, y), (x - w/2*0.88, y)], mug,
            shadow=mixc(mug, '#000000', 0.15), shade_dir=(1, 0), shade_w=0.2, lw=7)
    T.stroke([(x + w/2 - 4, y - h*0.75), (x + w/2 + 55*s, y - h*0.7), (x + w/2 + 55*s, y - h*0.3), (x + w/2*0.9, y - h*0.25)], lw=14*s + 3, col=mug)
    col = mixc(liquid, ICE, frozen)
    T.shape(ellipse_pts(x, y - h + 18*s, w/2 - 12*s, 22*s, 24), col, lw=5)
    if frozen > 0.4:
        for dx in (-30, 15):
            T.stroke([(x + dx*s, y - h + 10*s), (x + (dx + 20)*s, y - h + 26*s)], lw=4, col='#ffffff')
    if steam and frozen < 0.3:
        for i, dx in enumerate((-40, 0, 40)):
            ph = (tq(t)*0.8 + i*0.33) % 1
            yy = y - h - 40*s - ph*160*s; xx = x + dx*s + math.sin(ph*6 + i)*18*s
            T.stroke([(xx, yy + 40*s), (xx + 14*s, yy + 15*s), (xx - 8*s, yy - 10*s)], lw=10*s + 2, col='#ffffff', alpha=1 - ph)

def freezer(T, t, x, y, w, h, frost=0.0):
    """open freezer box seen from the front; (x, y) = top-left"""
    T.shape(rect(x - 30, y - 30, w + 60, h + 60), '#e8eef7', shadow='#b9c4d6', shade_dir=(1, 0), shade_w=0.15, lw=8)
    T.shape(rect(x, y, w, h), '#bfe6ff', lw=6)
    T.flat(rect(x, y, w, 40 + 60*frost), '#ffffff', alpha=0.6)
    for k in range(6):
        fx = x + 40 + k*(w - 80)/5
        T.stroke([(fx, y + 10), (fx + 8, y + 30 + 15*math.sin(k)), (fx - 4, y + 50)], lw=5, col='#ffffff')

def thermo(T, x, y, s, lvl, col):
    T.shape(rect(x - 18*s, y - 300*s, 36*s, 300*s), '#ffffff', lw=6)
    T.shape(rect(x - 9*s, y - 300*s*lvl, 18*s, 300*s*lvl), col, line=False, amp=0)
    T.shape(ellipse_pts(x, y + 20*s, 34*s, 34*s, 20), col, lw=6)

# ---------------------------------------------------------------- shots
def sh_cold(K, T, t, u):
    """VS cold open: Kiko holds the question, a hot cup and a cold cup between them"""
    T.cx, T.cy, T.z = 540, 1000, 1.14 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    K.kiko(T, t, **pose('confused', 'point', x=280, look=(0.8, 0.3)))
    K.nova(T, t, **pose('excited', 'finger_up', x=920))
    T.shape(rect(380, 1290, 340, 40), '#a8744a', lw=6)
    cup(T, t, 470, 1290, 0.7, HOT, True)
    cup(T, t, 640, 1290, 0.7, COLD, False)
    label(T.c, 'HOT  vs  COLD', 540, 330, 120, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'WHICH FREEZES FIRST?', 540, 480, 86, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_versus_hot(T, t, x, y):
    cup(T, t, x, y + 200, 1.25, HOT, True); thermo(T, x + 170, y + 150, 0.8, 0.9, HOT)

def sh_versus_cold(T, t, x, y):
    cup(T, t, x, y + 200, 1.25, COLD, False); thermo(T, x - 190, y + 150, 0.8, 0.3, COLD)

def sh_icecream(K, T, t, u):
    """a 1960s kitchen-class moment: two ice-cream bowls in a freezer, the hot one freezes first (the claim)"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    freezer(T, t, 140, 700, 800, 620, ease(u/2))
    k = ease((u - 0.8)/1.6)
    for (x, hot, lab) in ((350, True, 'HOT MIX'), (730, False, 'COLD MIX')):
        T.shape(ellipse_pts(x, 1180, 150, 40, 28), '#ffffff', lw=6)
        T.shape([(x - 150, 1180), (x + 150, 1180), (x + 100, 1290), (x - 100, 1290)], '#ffffff', shadow='#c9d4e6', shade_dir=(1, 0), shade_w=0.2, lw=7)
        T.shape(ellipse_pts(x, 1178, 128, 30, 24), mixc('#ffe0b8', ICE, k if hot else 0.25*k), lw=5)
        if hot and k < 0.4:
            for i in range(3):
                ph = (tq(t)*0.8 + i*0.33) % 1
                T.stroke([(x - 40 + i*40, 1130 - ph*120), (x - 26 + i*40, 1100 - ph*120)], lw=10, col='#ffffff', alpha=1 - ph)
        label(T.c, lab, x, 1380, 56, '#ffffff', 0, 1, FONT, 10)
    if k > 0.9: kin(T.c, t, 'FROZE FIRST?!', K.S(2) + 2.4, 350, 1000, 70, '#ff4fa3', -0.05)
    label(T.c, 'TANZANIA, 1960s', 540, 330, 100, '#ffd43b', -0.02, back(u/0.3, 1.4))
    label(T.c, 'the Mpemba effect', 540, 470, 60, '#ffffff', 0.02, back((u - 0.3)/0.3, 1.4), FONT, 10)

def sh_results(K, T, t, u):
    """lab results flip back and forth: HOT WINS / COLD WINS cards"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    flip = int(max(u - 0.3, 0)/0.55) % 2
    names = ('HOT WINS', 'COLD WINS')
    for i in range(min(int(max(u, 0)/0.55) + 1, 5)):
        y = 700 + i*170; w = names[i % 2]
        col = HOT if w.startswith('HOT') else COLD
        T.shape(rect(240, y - 70, 600, 130), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=7)
        label(T.c, f'TEST {i + 1}: {w}', 540, y, 62, '#ffffff', (-0.03, 0.03)[i % 2], back((u - i*0.55)/0.25, 1.5))
    label(T.c, 'RESULTS KEEP', 540, 330, 110, '#ffffff', -0.03, back(u/0.3, 1.4))
    label(T.c, 'CHANGING!', 540, 470, 120, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.4))

def sh_details(K, T, t, u):
    """three icons pop in: CUP, FREEZER, THERMOMETER spot"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.015*u
    board(T, t, '#2a1f4a', '#3a2e63')
    ts = (0.2, 1.2, 2.3)
    k = [ease((u - a)/0.35) for a in ts]
    if k[0] > 0.01:
        cup(T, t, 230, 1150, 0.9*k[0] + 0.01, COLD, False, mug='#ffd166')
        label(T.c, 'CUP', 230, 1260, 60, '#ffffff', 0, k[0], FONT, 10)
    if k[1] > 0.01:
        T.shape(rect(450, 860, 180, 300), '#e8eef7', shadow='#b9c4d6', shade_dir=(1, 0), shade_w=0.15, lw=7)
        T.stroke([(450, 960), (630, 960)], lw=6); T.stroke([(600, 900), (600, 940)], lw=8)
        label(T.c, 'FREEZER', 540, 1260, 60, '#ffffff', 0, k[1], FONT, 10)
    if k[2] > 0.01:
        thermo(T, 850, 1110, 0.8, 0.5, '#ff4fa3')
        label(T.c, 'THERMOMETER', 850, 1330, 50, '#ffffff', 0, k[2], FONT, 10)
        a = math.sin(tq(t)*6)*30
        arrow(T.c, 850 + a, 700, 850, 840, '#ffd43b', 18)
    label(T.c, 'TINY DETAILS', 540, 330, 110, '#ffd43b', -0.02, back(u/0.3, 1.4))
    label(T.c, 'CHANGE THE WINNER', 540, 470, 80, '#ffffff', 0.02, back((u - 0.2)/0.3, 1.4))

def sh_race(K, T, t, u):
    """parallel kitchen: freezer race, steaming cocoa ices over first while the juice is still liquid; Kiko amazed"""
    T.cx, T.cy, T.z = 540, 980, 1.0 + 0.02*ease(u/2)
    K.world(T, t, True)
    K.kiko(T, t, **pose('shock' if u < 1.4 else 'excited', 'hands_head' if u < 1.4 else 'arms_up', x=250, look=(0.8, 0.2)))
    K.nova(T, t, **pose('smug', 'present', x=930))
    freezer(T, t, 380, 1000, 360, 280, ease(u/1.5))
    fk = ease((u - 0.2)/0.8)
    cup(T, t, 470, 1270, 0.55, '#a0623a', True, frozen=fk)
    cup(T, t, 640, 1270, 0.55, '#ffa94d', False, frozen=0.0)
    label(T.c, 'HOT ALWAYS', 540, 340, 120, '#ffd43b', -0.03, back((u - 0.1)/0.3, 1.5))
    label(T.c, 'FREEZES FIRST', 540, 490, 100, '#ffffff', 0.03, back((u - 0.25)/0.3, 1.5))
    if fk > 0.9: kin(T.c, t, 'ICE COCOA!', K.S(8) + 2.1, 470, 900, 70, '#7fd0ff', -0.05)

def sh_icecube(K, T, t, u):
    """Nova pours hot water into an ice tray; it freezes into cubes in a flash (parallel world)"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t, '#1f3a5a', '#2c4a73')
    k = ease((u - 0.5)/0.8)
    T.shape(rect(240, 1050, 600, 160), '#7fd0ff', shadow='#4f9fd0', shade_dir=(1, 0), shade_w=0.15, lw=8)
    for i in range(4):
        x = 270 + i*145
        T.shape(rect(x, 1070, 120, 110), mixc(HOT, ICE, k), lw=5)
        if k > 0.6: T.stroke([(x + 20, 1090), (x + 50, 1110)], lw=5, col='#ffffff')
    if k < 0.3:
        for i in range(4):
            ph = (tq(t)*0.8 + i*0.25) % 1
            T.stroke([(300 + i*145, 1020 - ph*150), (320 + i*145, 990 - ph*150)], lw=12, col='#ffffff', alpha=1 - ph)
    label(T.c, 'START HOT', 540, 360, 130, HOT, -0.03, back(u/0.3, 1.4))
    if k > 0.5: label(T.c, '= ICE FAST!', 540, 560, 110, '#7fd0ff', 0.03, back((k - 0.5)/0.3, 1.5))

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.versus(K.at(0, 0.55), 'HOT', 'COLD', lcol=HOT, rcol=COLD, draw_left=sh_versus_hot, draw_right=sh_versus_cold)
    K.ncu(K.L(1), par=False, emo='excited', gest='finger_up')
    K.custom(K.L(2), sh_icecream, sfx='swoop')
    K.kcu(K.L(3), par=False, emo='shock', gest='hands_head')
    K.custom(K.L(4), sh_results, sfx='blip')
    K.custom(K.L(5), sh_details, sfx='pop')
    K.verdict(K.at(6, 0.62), 'IT DEPENDS!', col='#ffd43b', sub='careful 2016 test: hot did NOT win')
    K.twoshot(K.L(6), par=False, nova=pose('neutral', 'present'), kiko=pose('confused', 'shrug'))
    K.hook(K.L(7), portal_line=7, portal_f=0.45)
    K.arrive(tag_text='WORLD #20 · HOT ALWAYS FREEZES FIRST')
    K.custom(K.S(8) + 1.0, sh_race, sfx='boing')
    K.end(K.L(9), poll=('HOT WINS', 'COLD WINS'))

def thumbnail(c, K):
    """huge 'HOT or COLD?', big shocked Kiko, hot steaming cup vs icy cup, 'IT DEPENDS?!' sticker (all shown in the video)"""
    burst(c, W, H, 560, 1150, '#ffe9a8', '#1f4a8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    cup(T, 0.3, 560, 1500, 1.5, HOT, True)
    cup(T, 0.3, 860, 1720, 1.15, COLD, False, frozen=0.8)
    P = pose('shock', 'hands_head'); P.update(x=230, y=2300, s=1.75, face=1, look=(0.8, -0.4), jit=0)
    K.kiko(T, 1.0, **P)
    big_text(c, 'HOT WATER', 540, 250, 160, max_w=1000)
    big_text(c, 'WINS?!', 540, 470, 230, hl=0, hl_col='#ff6b4a', max_w=1010)
    emoji_burst(c, 820, 760, 130, 'IT DEPENDS?!', '#ff2d55', 0.15)
    arrow(c, 820, 900, 640, 1180, '#ffd43b', 26)
