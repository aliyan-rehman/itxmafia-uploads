"""EP13 - What if ice SANK? (Short, built with shortkit)
Facts (checked): ice ~0.917 g/cm3, about 9% less dense than water; floating ice insulates lakes and the deep water
stays near 4 C so fish survive; if ice sank, lakes would freeze from the bottom up and shallow lakes freeze solid;
polar oceans would pile up ice on the seafloor that summer melt could not reach.
Sources: Britannica (why water freezes from the top down), WorldAtlas (why does ice float), LibreTexts Ocean Sciences 5.9."""
import math, numpy as np
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=N, text="In our world, ice floats. It's about nine percent lighter than water.", cap="In our world, ice floats. It's about 9% lighter than water.", gap=0.6),
    dict(who=N, text="But in this parallel world... ice sinks!", gap=0.35),
    dict(who=K_, text="So the ice in my drink is... at the bottom?", gap=0.3),
    dict(who=N, text="That's the small problem. In winter, lakes freeze from the bottom up. Layer by layer.", gap=0.35),
    dict(who=K_, text="And the fish?", gap=0.3),
    dict(who=N, text="Normally, floating ice is a blanket. The water under it stays around four degrees, so fish survive.", cap="Normally, floating ice is a blanket. The water under it stays around 4°C, so fish survive.", gap=0.35),
    dict(who=N, text="Here, there's no blanket. Shallow lakes freeze solid.", gap=0.3),
    dict(who=K_, text="Poor fish!", gap=0.35),
    dict(who=N, text="And the oceans pile up ice on the seafloor... that summer can never melt.", gap=0.4),
    dict(who=N, text="Floating ice, or sinking ice? Comment below. A new parallel world, every day.", gap=1.6),
]
WINTER = palette(PAR, ground='#e8f4ff', ground2='#cfe6f7')
META = dict(
    id='ep13_ice_sinks', our_set='park', par_set='park', par_palette=WINTER,
    title='What If ICE SANK? \U0001F300 #Swirlverse',
    description=("In our world, ice floats - it's about 9% lighter than water. But in this parallel world, ice SINKS... "
                 "and lakes freeze from the bottom up! \U0001F976\U0001F41F\nFloating ice or sinking ice? Comment below \U0001F447\n\n"
                 "Real science: floating ice insulates lakes so the water below stays near 4°C and fish survive the winter.\n\n"
                 "#shorts #whatif #ice #science #physics #swirlverse"),
    tags=['what if', 'parallel world', 'what if ice sank', 'why does ice float', 'ice density', 'lakes freeze', 'science shorts', 'physics', 'swirlverse', 'animation'],
    topic='ice sinks / density of ice', category='everyday physics', hook='our-world fact -> portal -> twist',
)
DROPS = []

# ---------------------------------------------------------------- props
def glass(T, x, y, s, ice_k, t):
    """drinking glass; ice_k 0 = cubes floating at the top, 1 = sunk to the bottom"""
    w, h = 220*s, 330*s
    T.shape([(x - w/2, y - h), (x + w/2, y - h), (x + w/2 - 18*s, y), (x - w/2 + 18*s, y)], '#e8fbff', lw=7, alpha=0.9)
    T.shape([(x - w/2 + 8*s, y - h*0.78), (x + w/2 - 8*s, y - h*0.78), (x + w/2 - 24*s, y - 6*s), (x - w/2 + 24*s, y - 6*s)], '#ffb36b', line=False)
    for i in range(3):
        top = y - h*0.78 + 4*s; bot = y - 60*s - (i % 2)*50*s
        cy = top + (bot - top)*ease(ice_k) + 6*math.sin(t*3 + i)*(1 - ice_k)
        cx = x - 60*s + i*60*s
        T.shape([(cx - 30*s, cy - 26*s), (cx + 28*s, cy - 30*s), (cx + 32*s, cy + 26*s), (cx - 26*s, cy + 30*s)], '#eaffff', shadow='#b9e6f5', shade_dir=(1, 0.3), shade_w=0.3, lw=5)
    T.stroke([(x - w/2 + 26*s, y - h + 30*s), (x - w/2 + 36*s, y - 60*s)], lw=8, col='#ffffff', alpha=0.8)

def fish(T, x, y, s, col='#ff8a3d', frozen=False, happy=True, t=0.0):
    b = 0 if frozen else 6*math.sin(tq(t)*6 + x)
    pts = [(x - 70*s, y + b), (x - 30*s, y - 36*s + b), (x + 40*s, y - 30*s + b), (x + 70*s, y + b), (x + 40*s, y + 30*s + b), (x - 30*s, y + 36*s + b)]
    T.shape(pts, col, shadow=mixc(col, '#000000', 0.2), shade_dir=(0, 1), shade_w=0.3, lw=6)
    T.shape([(x - 66*s, y + b), (x - 110*s, y - 34*s + b), (x - 110*s, y + 34*s + b)], col, lw=6)
    if frozen:
        T.stroke([(x + 22*s, y - 10*s), (x + 40*s, y - 10*s)], lw=5)
        T.shape(rect(x - 130*s, y - 70*s, 230*s, 140*s), '#cfefff', lw=6, alpha=0.55)
    else:
        T.shape(ellipse_pts(x + 32*s, y - 8*s + b, 12*s, 13*s, 12), '#ffffff', lw=4); T.dot(x + 34*s, y - 7*s + b, 4*s)
        T.stroke([(x + 50*s, y + 12*s + b), (x + 58*s, y + (8 if happy else 18)*s + b)], lw=4)

def lake_section(T, t, mode, k, label_c=None):
    """cross-section of a lake. mode 'ours': ice lid on top + 4C water + happy fish.
    'up': ice layers grow from the bottom (k 0..1). 'solid': fully frozen."""
    T.flat(rect(-500, -500, 2100, 1100), '#bfe4ff')
    T.shape([(-500, 600), (1600, 600), (1600, 2400), (-500, 2400)], '#e8f4ff', lw=8)
    basin = [(-100, 700)] + [(540 + 640*math.cos(a), 700 + 900*math.sin(a)) for a in np.linspace(math.pi, 0, 40)][::-1][::-1] + [(1180, 700)]
    bowl = [(540 + 620*math.cos(a), 700 + 880*math.sin(a)) for a in np.linspace(0, math.pi, 50)]
    T.shape(bowl, '#4f9fd8', lw=8)
    c = T.c; c.save(); T._path(T.X(bowl)); c.clip()
    if mode == 'ours':
        T.flat(rect(-200, 690, 1500, 70), '#eaffff'); T.stroke([(-80, 760), (1160, 760)], lw=7)
        for i, (fx, fy) in enumerate(((330, 1000), (700, 1150), (520, 1330))): fish(T, fx, fy, 0.9, ('#ff8a3d', '#ffd43b', '#ff6fa8')[i], t=t)
    else:
        n = int(1 + k*6) if mode == 'up' else 7
        for j in range(n):
            y0 = 1600 - j*130 - (130*((k*6) % 1) if (mode == 'up' and j == n - 1) else 0)
            T.flat(rect(-200, y0 - 130, 1500, 134), '#eaffff' if j % 2 == 0 else '#d6f6ff')
            T.stroke([(-200, y0 - 130), (1300, y0 - 130)], lw=4, col='#9fd6ea')
        if mode == 'up':
            ytop = 1600 - n*130
            for i, fx in enumerate((350, 700)):
                fish(T, fx, max(780, ytop - 120 - i*60), 0.9, ('#ff8a3d', '#ffd43b')[i], t=t, happy=False)
        else:
            fish(T, 540, 1100, 1.0, '#ff8a3d', frozen=True)
    c.restore()
    T.shape(bowl, None, lw=8)

def sh_glass(K, T, t, u):
    T.cx, T.cy, T.z = 540, 980, 1.0 + 0.02*u
    board(T, t, '#1f2a4a', '#2c3a63')
    glass(T, 300, 1250, 1.0, 0.0, t); glass(T, 780, 1250, 1.0, clamp((u - 0.4)/0.8), t)
    label(T.c, 'OUR WORLD', 300, 1360, 50, '#7fd0ff', 0, 1, FONT, 10)
    label(T.c, 'PARALLEL', 780, 1360, 50, '#ff4fa3', 0, 1, FONT, 10)
    kin(T.c, t, 'ICE SINKS!', K.at(1, 0.55), 540, 560, 150, '#4fd8ff', -0.04)

def sh_kiko_drink(K, T, t, u):
    T.cx, T.cy, T.z = 330, 1090, 2.0 + 0.04*u
    K.world(T, t, True)
    K.kiko(T, t, **pose('confused', 'rest', armF=((-150, -60), 30), look=(-0.5, 0.4)))
    glass(T, 330 - 0.92*(66 + 150) + 230, 1600 - 0.92*(355 + 60) + 60, 0.55, 1.0, t)

def sh_layers(K, T, t, u):
    T.cx, T.cy, T.z = 540, 1000, 1.0
    lake_section(T, t, 'up', clamp(u/3.6))
    n = int(1 + clamp(u/3.6)*6)
    label(T.c, f'LAYER {n}', 820, 420, 80, '#ff4fa3', 0.05, 1)
    kin(T.c, t, 'BOTTOM UP!', K.at(3, 0.55), 540, 260, 120, '#ffd43b', -0.04)

def sh_blanket(K, T, t, u):
    T.cx, T.cy, T.z = 540, 1000, 1.0 + 0.015*u
    lake_section(T, t, 'ours', 1)
    label(T.c, 'OUR WORLD', 540, 260, 90, '#7fd0ff', -0.03, back(u/0.3, 1.4))
    kin(T.c, t, 'ICE = BLANKET', K.at(5, 0.15), 540, 520, 90, '#ffffff', 0.03)
    kin(T.c, t, '~4°C', K.at(5, 0.55), 870, 1250, 110, '#ffd43b', 0.06)

def sh_solid(K, T, t, u):
    T.cx, T.cy, T.z = 540, 1000, 1.0 + 0.02*u
    lake_section(T, t, 'solid', 1)
    kin(T.c, t, 'FROZEN SOLID', K.S(6) + 0.6, 540, 300, 110, '#4fd8ff', -0.04)

def sh_ocean(K, T, t, u):
    T.cx, T.cy, T.z = 540, 980, 1.0
    T.flat(rect(-500, -500, 2100, 900), K.par['sky'][3])
    T.shape(ellipse_pts(860, 220, 80, 80), '#ffe066', shadow='#ffc93c', lw=7)
    for i, col in enumerate(('#3d7bd8', '#2f68c0', '#2456a8', '#1b4790')):
        T.flat(rect(-500, 420 + i*330, 2100, 334), col)
    T.stroke([(x, 420 + 8*math.sin(x/60 + t*3)) for x in range(-200, 1300, 30)], lw=8)
    grow = clamp(u/3.0)
    for j in range(int(2 + grow*6)):
        y = 1720 - j*90
        T.shape([(-200, y), (1300, y - 20), (1300, y + 92), (-200, y + 92)], '#eaffff' if j % 2 == 0 else '#d6f6ff', lw=5)
    T.shape(rect(-200, 1810, 1500, 400), '#8a7a6a', lw=7)
    label(T.c, 'SEAFLOOR ICE', 540, 1560 - grow*400, 70, '#ffffff', 0, 1)
    if u > 1.2:
        # summer melt only reaches the top
        T.shape([(780, 300), (700, 520), (760, 520), (720, 700)], '#ffd43b', lw=6)
        label(T.c, "SUMMER CAN'T REACH IT", 540, 820, 54, '#ffd43b', 0.02, back((u - 1.2)/0.3, 1.4))

def shots(K):
    K.hook(0.0, portal_line=0, portal_f=0.82)
    K.arrive(tag_text='WORLD #13 · ICE: SINKS')
    K.custom(K.at(1, 0.45), sh_glass, sfx='pop')
    K.custom(K.L(2), sh_kiko_drink)
    K.custom(K.L(3) + 1.2, sh_layers, sfx='nope')
    K.twoshot(K.L(3), par=True, nova=pose('deadpan', 'finger_up'), kiko=pose('confused'))
    K.kcu(K.L(4), emo='worried', gest='hands_head')
    K.custom(K.L(5), sh_blanket, sfx='chime')
    K.custom(K.L(6), sh_solid, sfx='nope')
    K.kcu(K.L(7), emo='sad', gest='hands_head')
    K.custom(K.L(8), sh_ocean, sfx='fwump')
    K.end(K.L(9), poll=('FLOATING ICE', 'SINKING ICE'))

def ice_block(T, x, y, s, t=0.0):
    """big solid ice cube with a frozen fish inside"""
    fish(T, x, y, s, '#ff8a3d', frozen=False, happy=False, t=0)
    T.shape([(x - 150*s, y - 120*s), (x + 140*s, y - 135*s), (x + 155*s, y + 115*s), (x - 140*s, y + 125*s)], '#bff0ff', lw=10, alpha=0.42)
    T.shape([(x - 150*s, y - 120*s), (x + 140*s, y - 135*s), (x + 175*s, y - 160*s), (x - 120*s, y - 150*s)], '#eaffff', lw=8)
    T.stroke([(x - 115*s, y - 80*s), (x - 60*s, y - 95*s)], lw=12, col='#ffffff'); T.stroke([(x - 120*s, y - 40*s), (x - 100*s, y - 45*s)], lw=12, col='#ffffff')

def thumbnail(c, K):
    """pro thumbnail: huge text, big shocked Kiko, a big frozen-fish ice block, arrow"""
    burst(c, W, H, 700, 1150, '#9fe8ff', '#14246b', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    ice_block(T, 790, 1080, 1.4)
    K.kiko(T, 1.0, **dict(pose('shock', 'hands_head'), x=330, y=2380, s=2.15, face=-1, look=(0.8, -0.5), o=0.95, jit=0, tremble=0))
    big_text(c, 'WHAT IF', 540, 250, 150, max_w=900)
    big_text(c, 'ICE SANK?!', 540, 470, 215, hl=0, hl_col='#7fd8ff', max_w=1010)
    emoji_burst(c, 230, 1000, 105, 'BRRR', '#ff2d55', -0.2)
    arrow(c, 330, 980, 560, 1040, '#ffd43b', 26)
