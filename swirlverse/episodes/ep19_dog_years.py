"""EP19 - Is 1 dog year REALLY 7 human years? (Short, IS IT TRUE? format with a parallel-world test, built with shortkit)
Format: IS IT TRUE? (verdict MYTH!) + portal test ("exactly-7 world"). Topic family: animals / pets
(today's 5 PM Short was brain / psychology, so this is a different family).
Gate score: curiosity 5, relatable 5 (almost everyone has heard the x7 rule), visual 4 (puppy vs teen, age chart),
fact certainty 4 (vet guideline is an estimate; breed size changes it), freshness 3 (popular question; our angle is the
age curve vs the straight x7 line and an exactly-7 parallel world where puppies stay little kids) = 21/25.
Facts (checked):
- The "1 dog year = 7 human years" rule is a myth / oversimplification (American Kennel Club "How to Calculate Dog Years
  to Human Years", citing the AVMA guideline; Smithsonian Magazine 2019 on the UC San Diego epigenetic study;
  NHGRI genome.gov 2019 news release reframing dog-to-human aging).
- Vet guideline (AVMA, via AKC): the first year of a medium-sized dog is about 15 human years, year two adds about 9
  (so ~24 at age 2), and each year after adds about 4-5 human years.
- Size matters: large dogs age faster and have shorter lives than small dogs (AKC; NHGRI notes breed size affects aging).
- The UC San Diego DNA-methylation study (Wang et al., Labradors) also found dogs age very fast at first and then slow
  down (Smithsonian, NHGRI). We don't quote its formula, to keep the numbers simple.
- Parallel-world part is labelled imaginary: if every year were exactly x7, a 1-year-old dog would be like a 7-year-old
  child (still a little kid), not a teenager. No other numbers claimed.
Sources: AKC (AVMA guideline); Smithsonian Magazine; NHGRI (genome.gov); UC Davis Vet Med health topics.
No real people, no brands. Generic cartoon dog (same design as ep18)."""
import math
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Is one dog year really seven human years?", gap=0.3),
    dict(who=N, text="Nope! A one year old dog is already like a fifteen year old teenager!",
         cap="Nope! A 1 year old dog is already like a 15 year old teenager!", gap=0.3),
    dict(who=N, text="By age two? About twenty four.", cap="By age 2? About 24.", gap=0.3),
    dict(who=K_, text="Whoa, puppies grow up super fast!", gap=0.3),
    dict(who=N, text="Then it slows down. About four or five human years for every dog year.",
         cap="Then it slows down. About 4 or 5 human years for every dog year.", gap=0.3),
    dict(who=N, text="And big dogs usually age faster than small dogs.", gap=0.3),
    dict(who=N, text="So, times seven? Myth!", cap="So, x7? MYTH!", gap=0.35),
    dict(who=N, text="But in this parallel world, every dog year is exactly seven human years.", gap=0.3),
    dict(who=K_, text="Huh? My one year old dog is still a clumsy little kid!", gap=0.35),
    dict(who=N, text="Real dogs grow up way faster than that.", gap=0.35),
    dict(who=N, text="Fast puppies, or slow puppies? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep19_dog_years', our_set='park', par_set='park',
    title="Is 1 Dog Year REALLY 7 Human Years? \U0001F300 #Swirlverse",
    description=("Is one dog year really seven human years? Myth! A 1-year-old dog is already about 15 in human years, "
                 "about 24 by age 2, and after that each dog year adds about 4 or 5 human years. Big dogs usually age faster than small dogs. "
                 "But in this parallel world, every dog year is exactly 7 human years... \U0001F436\n"
                 "Fast puppies or slow puppies? Comment below \U0001F447\n\n"
                 "Real science: vets use an age guideline (AVMA, shared by the American Kennel Club) instead of the old x7 rule, "
                 "and a DNA study of Labradors at UC San Diego also found that dogs age very fast at first and then slow down. "
                 "These are estimates: breed and size change them. "
                 "Sources: American Kennel Club (AVMA guideline), Smithsonian Magazine, NHGRI (genome.gov).\n\n"
                 "#shorts #science #dogs #dogyears #animals #swirlverse"),
    tags=['dog years', 'is a dog year 7 human years', 'dog years to human years', 'dog age', 'how old is my dog',
          'puppy', 'dogs', 'animal science', 'myth or fact', 'parallel world', 'science shorts', 'swirlverse', 'animation'],
    topic='is 1 dog year 7 human years / dog age in human years (1st year ~15, 2nd ~24, then 4-5 per year; big dogs age faster; exactly-7 world)',
    category='animals / pets',
    hook='kiko + dog question cold open -> 15 teen counter -> age curve vs x7 line -> MYTH verdict -> portal test',
)
DROPS = []

DOG, DOG_S, EAR = '#d9a066', '#b97f48', '#8a5a33'
def dog(T, x, y, s=1.0, t=0.0, col=DOG, tilt=0.0, happy=True):
    """a generic friendly dog; (x, y) = paws on the floor"""
    sh = mixc(col, '#000000', 0.18)
    T.shape(ellipse_pts(x + 60*s, y - 120*s, 150*s, 85*s, 32), col, shadow=sh, shade_dir=(1, 0.4), shade_w=0.3, lw=8)
    for lx in (-40, 20, 110, 170):
        T.shape(rect(x + lx*s, y - 80*s, 34*s, 80*s), col, lw=6)
    wag = math.sin(tq(t)*10)*0.4
    T.stroke([(x + 200*s, y - 150*s), (x + 250*s, y - (200 + 40*wag)*s), (x + 270*s, y - (250 + 20*wag)*s)], lw=12*s + 4, col=sh)
    dog_head(T, x - 60*s, y - 230*s + tilt*20*s, s, col)

def dog_head(T, hx, hy, s=1.0, col=DOG, glow=False, happy=True):
    if glow: T.glow(hx, hy, 120*s, '#ffe066', ((1.5, 0.18), (1.2, 0.3)))
    for sx in (-1, 1):
        T.shape([(hx + sx*70*s, hy - 70*s), (hx + sx*125*s, hy - 40*s), (hx + sx*120*s, hy + 60*s), (hx + sx*80*s, hy + 50*s)], EAR, lw=6)
    T.shape(ellipse_pts(hx, hy, 100*s, 95*s, 36), col, shadow=mixc(col, '#000000', 0.18), shade_dir=(1, 0.4), shade_w=0.25, lw=7)
    T.shape(ellipse_pts(hx, hy + 50*s, 62*s, 45*s, 28), '#f6e2c4', lw=6)
    T.shape(ellipse_pts(hx, hy + 25*s, 20*s, 14*s, 16), '#2a1a14', lw=4)
    for ex in (-38, 38): T.dot(hx + ex*s, hy - 20*s, 13*s, '#2a1a14')
    if happy:
        T.shape(ellipse_pts(hx, hy + 82*s, 22*s, 20*s, 18), '#ff7a90', lw=5)   # tongue
    T.stroke([(hx - 26*s, hy + 70*s), (hx, hy + 80*s), (hx + 26*s, hy + 70*s)], lw=max(3, 6*s))

def puppy(T, x, y, s=0.5, t=0.0, roll=0.0):
    """tiny clumsy puppy: big head, small body; roll = tumble angle"""
    c = T.c
    dog(T, x, y, s, t, '#e6b47a')

def cake(T, x, y, s, n, col='#ff8fc0'):
    """birthday cake with n candles"""
    T.shape(rect(x - 120*s, y - 110*s, 240*s, 110*s), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.2, lw=7)
    T.shape(rect(x - 130*s, y - 130*s, 260*s, 30*s), '#ffffff', lw=6)
    for i in range(n):
        cx = x - 90*s + (180*s*i/(max(n - 1, 1)))
        T.shape(rect(cx - 8*s, y - 200*s, 16*s, 70*s), '#7fd0ff', lw=4)
        T.glow(cx, y - 215*s, 20*s, '#ffd43b', ((1.6, 0.2), (1.2, 0.4)))
        T.shape(ellipse_pts(cx, y - 215*s, 9*s, 15*s, 12), '#ffd43b', lw=3)

def teen(T, t, x, y, s, k):
    """a generic teen silhouette icon (tall, headphones) drawn from shapes"""
    if k <= 0.01: return
    col = '#7fd0ff'
    T.shape(ellipse_pts(x, y - 420*s, 70*s, 75*s, 28), '#f2c9a0', lw=7)
    T.stroke([(x - 75*s, y - 430*s), (x - 60*s, y - 510*s), (x + 60*s, y - 510*s), (x + 75*s, y - 430*s)], lw=10*s + 4, col='#3a2e63')
    T.shape(rect(x - 85*s, y - 340*s, 170*s, 220*s), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.2, lw=7)
    for lx in (-60, 20): T.shape(rect(x + lx*s, y - 125*s, 40*s, 125*s), '#3a2e63', lw=6)

# ---------------------------------------------------------------- shots
def sh_cold(K, T, t, u):
    T.cx, T.cy, T.z = 540, 1000, 1.14 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    K.kiko(T, t, **pose('confused', 'point', x=330, look=(0.8, 0.3)))
    K.nova(T, t, **pose('excited', 'finger_up', x=900))
    dog(T, 560, FEET, 0.8, t)
    label(T.c, 'IS 1 DOG YEAR', 540, 330, 116, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'REALLY 7 HUMAN YEARS?', 540, 480, 84, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_fifteen(K, T, t, u):
    """1-candle cake + dog on the left, teen icon on the right, counter to 15"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    cake(T, 290, 1520, 1.0, 1)
    dog(T, 260, 1250, 0.8, t)
    teen(T, t, 800, 1560, 1.25, ease((u - 0.6)/0.3))
    v = 15*ease((u - 0.4)/1.3)
    label(T.c, '1 DOG YEAR =', 540, 330, 100, '#ffffff', -0.03, back((u - 0.05)/0.3, 1.5))
    label(T.c, f'{int(v)} HUMAN YEARS', 540, 480, 110, '#ffd43b', 0.02, back((u - 0.3)/0.3, 1.5))
    if u > 1.6: kin(T.c, t, 'A TEEN!', K.S(1) + 1.6, 800, 790, 100, '#ff4fa3', 0.05)

def chart(T, t, u, x7=True):
    """dog age 1..8 on x; vet guideline curve vs straight x7 line"""
    c = T.c
    X0, Y0, WX, HY = 170, 1500, 800, 900
    T.stroke([(X0, Y0 - HY), (X0, Y0), (X0 + WX, Y0)], lw=8, col='#ffffff')
    real = [0, 15, 24, 28, 32, 36, 40, 44, 48]
    def P(a, h): return (X0 + WX*a/8, Y0 - HY*h/56)
    k = ease((u - 0.2)/1.4)
    n = 1 + int(k*8*4)
    pts = []
    for i in range(n + 1):
        a = 8*i/(8*4)
        lo = int(min(a, 7.999)); f = a - lo
        pts.append(P(a, real[lo] + (real[lo + 1] - real[lo])*f))
    if len(pts) > 1: T.stroke(pts, lw=16, col='#ffd43b')
    if x7:
        k2 = ease((u - 0.9)/1.2)
        if k2 > 0.01: T.stroke([P(0, 0), P(8*k2, 56*k2)], lw=10, col='#ff4fa3', alpha=0.9)
        if k2 > 0.6: label(c, 'x7 RULE', X0 + WX - 120, Y0 - HY + 40, 60, '#ff4fa3', 0, back((k2 - 0.6)/0.3, 1.4))
    for a in (1, 2):
        if k*8 >= a:
            x, y = P(a, real[a]); T.dot(x, y, 18, '#ffffff')
            label(c, str(real[a]), x + 20, y - 60, 70, '#ffffff', 0, 1)
    label(c, 'DOG AGE', X0 + WX/2, Y0 + 80, 52, '#c9b8ff', 0, 1, FONT, 10)

def sh_chart(K, T, t, u):
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    chart(T, t, u)
    label(T.c, 'FAST, THEN SLOW', 540, 330, 100, '#ffd43b', -0.02, back(u/0.3, 1.4))
    if u > 1.8: label(T.c, '+4 to 5 a year', 660, 1180, 64, '#ffffff', 0.03, back((u - 1.8)/0.3, 1.4))

def sh_size(K, T, t, u):
    """big dog vs small dog; big dog's clock spins faster"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t, '#2a1f4a', '#3a2e63')
    sl = ease(u/0.35)
    dog(T, 270 - 300*(1 - sl), 1330, 1.15, t, '#a8784a')
    dog(T, 760 + 300*(1 - sl), 1330, 0.55, t, '#f0d0a0')
    for (x, sp, r) in ((300, 3.0, 110), (800, 1.2, 80)):
        T.shape(ellipse_pts(x, 820, r, r, 32), '#ffffff', lw=7)
        a = tq(t)*sp
        T.stroke([(x, 820), (x + math.sin(a)*r*0.8, 820 - math.cos(a)*r*0.8)], lw=8)
    label(T.c, 'BIG DOGS', 300, 1440, 70, '#ffd43b', -0.03, back((u - 0.3)/0.3, 1.5))
    label(T.c, 'SMALL DOGS', 800, 1440, 70, '#7fd0ff', 0.03, back((u - 0.4)/0.3, 1.5))
    label(T.c, 'AGE FASTER', 300, 1530, 64, '#ffffff', -0.03, back((u - 0.6)/0.3, 1.5))
    label(T.c, 'SIZE MATTERS', 540, 330, 110, '#ffffff', -0.02, back(u/0.3, 1.4))

def sh_slowpup(K, T, t, u):
    """parallel park: 1-year-old dog is still a tumbling puppy with a 1-candle cake; Kiko confused"""
    T.cx, T.cy, T.z = 540, 980, 1.05 + 0.03*ease(u/2)
    K.world(T, t, True)
    K.kiko(T, t, **pose('confused', 'hands_head' if u < 1.2 else 'shrug', x=300, look=(0.8, 0.4)))
    K.nova(T, t, **pose('smug', 'present', x=920))
    hop = abs(math.sin(tq(t)*5))*40
    puppy(T, 560, FEET - hop, 0.48, t)
    cake(T, 760, FEET + 150, 0.7, 1)
    label(T.c, '1 YEAR = 7', 540, 340, 130, '#ffd43b', -0.03, back((u - 0.1)/0.3, 1.5))
    if u > 0.8: kin(T.c, t, 'STILL A KID!', K.S(8) + 0.8, 600, 520, 100, '#ffffff', 0.04)

def sh_vs(K, T, t, u):
    """age 1: real world 15 vs parallel 7"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    for i, (name, v, col) in enumerate((('REAL DOGS', 15, '#ffd43b'), ('x7 WORLD', 7, '#ff4fa3'))):
        k = ease((u - 0.2 - i*0.4)/0.7); x = 300 + i*480; h = 820*v/15*k
        T.shape(rect(x - 130, 1400 - h, 260, max(h, 2)), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=8)
        label(T.c, name, x, 1490, 60, '#ffffff', 0, 1, FONT, 10)
        if k > 0.05: label(T.c, str(int(round(v*k))), x, 1400 - h - 80, 100, col, 0, 1)
    label(T.c, 'AT AGE 1', 540, 330, 110, '#ffffff', -0.02, back(u/0.3, 1.4))

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.custom(K.at(1, 0.12), sh_fifteen, sfx='swoop')
    K.stat(K.L(2), '24', 'AT AGE 2', 'in human years (vet guideline)')
    K.kcu(K.L(3), par=False, emo='shock', gest='hands_head')
    K.custom(K.L(4), sh_chart, sfx='swoop')
    K.custom(K.L(5), sh_size, sfx='boing')
    K.verdict(K.L(6), 'MYTH!', sub='year 1 = ~15  ·  then +4-5 a year')
    K.hook(K.L(7), portal_line=7, portal_f=0.45)
    K.arrive(tag_text='WORLD #19 · EXACTLY x7 DOG YEARS')
    K.custom(K.S(8) + 0.7, sh_slowpup, sfx='boing')
    K.custom(K.L(9), sh_vs, sfx='blip')
    K.end(K.L(10), poll=('FAST PUPPIES', 'SLOW PUPPIES'))

def thumbnail(c, K):
    """huge 'x7? NOPE', big shocked Kiko, dog with a 1-candle cake, '= 15!' sticker (all shown in the video)"""
    burst(c, W, H, 560, 1150, '#ffe9a8', '#1f4a8c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    dog(T, 760, 1700, 1.05, 0.0)
    cake(T, 820, 1900, 0.9, 1)
    P = pose('shock', 'hands_head'); P.update(x=260, y=2300, s=1.75, face=1, look=(0.8, -0.4), jit=0)
    K.kiko(T, 1.0, **P)
    big_text(c, 'x7 DOG YEARS?', 540, 250, 140, max_w=1000)
    big_text(c, 'NOPE!', 540, 470, 230, hl=0, hl_col='#ff4fa3', max_w=1010)
    emoji_burst(c, 800, 780, 130, 'AGE 1 = 15!', '#ff2d55', 0.15)
    arrow(c, 820, 930, 720, 1290, '#ffd43b', 26)
