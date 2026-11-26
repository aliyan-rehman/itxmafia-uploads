"""EP17 - Is lightning HOTTER than the Sun? (Short, IS IT TRUE? format with a parallel-world test, built with shortkit)
Format: IS IT TRUE? (verdict IT DEPENDS) + portal test ("candle-flame lightning world"). Topic family: weather / space
(new family; today's 5 PM Short was food chemistry).
Gate score: curiosity 5, relatable 4 (everyone has seen a storm), visual 5, fact certainty 4 (sources give a range),
freshness 3 (the claim is well known; our angle is the two-part verdict: TRUE for the surface, but the core is ~500x
hotter than lightning, plus a cool-lightning parallel world) = 21/25.
Facts (checked):
- Lightning can heat the air it passes through to about 50,000 F (~27,700 C), about 5 times hotter than the surface of
  the Sun (NOAA National Weather Service, "How Hot Is Lightning?"). Other sources give ~30,000 K for the return stroke
  (AIP Inside Science; BBC Science Focus "5 times hotter than the Sun"). NOAA NSSL gives a lower ~18,000 F for the channel
  in general, so the video says "CAN heat the air to about 27,000 C" (the peak), not an average.
- The Sun's visible surface (photosphere) is about 5,500 C / 10,000 F (NASA Sun facts; Britannica "How Hot Is the Sun").
- The Sun's core is about 15 million C / 27 million F (NASA Sun facts; Britannica). 15,000,000 / 27,700 = ~540, so
  "over 500 times hotter than lightning" is honest.
- Thunder: the heat makes the air expand very rapidly, creating the sound wave we hear as thunder (NOAA NSSL Lightning Basics).
- Parallel-world physics (labelled as imaginary): a much cooler channel would heat and expand the air far less, so a weaker
  pressure wave (a soft puff instead of a boom), and a cooler gas glows dimmer. No numbers claimed for that world.
Sources: NOAA National Weather Service; NOAA NSSL; NASA; Britannica; BBC Science Focus. No real people, no brands."""
import math, numpy as np
from shortkit import *
from thumbkit import burst, big_text, arrow, emoji_burst

N, K_ = 'NOVA', 'KIKO'
LINES = [
    dict(who=K_, text="Is lightning really hotter than the Sun?", gap=0.3),
    dict(who=N, text="A lightning bolt can heat the air to about twenty seven thousand degrees Celsius!",
         cap="A lightning bolt can heat the air to about 27,000°C!", gap=0.3),
    dict(who=N, text="The Sun's glowing surface? Only about five thousand five hundred.",
         cap="The Sun's glowing surface? Only about 5,500°C.", gap=0.3),
    dict(who=K_, text="So lightning is five times hotter?!", gap=0.3),
    dict(who=N, text="Than the surface, yes! The hot air blasts outward. Boom, thunder!", gap=0.35),
    dict(who=N, text="But the Sun's core? About fifteen million degrees. Over five hundred times hotter!",
         cap="But the Sun's core? About 15 million °C. Over 500 times hotter!", gap=0.35),
    dict(who=N, text="So, true? Surface, yes. Core, no way!", gap=0.3),
    dict(who=N, text="In this parallel world, lightning is only as hot as a candle flame.", gap=0.3),
    dict(who=K_, text="Huh? It's so dim... and the thunder just goes poof!", gap=0.7),
    dict(who=N, text="Less heat, less blast. Thunder needs that super hot flash.", gap=0.35),
    dict(who=N, text="Hot lightning, or calm lightning? Comment below. A new parallel world, every day.", gap=1.6),
]
META = dict(
    id='ep17_lightning_sun', our_set='park', par_set='park',
    our_palette=palette(OUR, sky=bands('#141a36', '#56628f'), sun=False),
    title="Is Lightning HOTTER Than the Sun? \U0001F300 #Swirlverse",
    description=("Is lightning really hotter than the Sun? It depends! A lightning bolt can heat the air to about 27,000°C, "
                 "about 5 times hotter than the Sun's surface (about 5,500°C). But the Sun's core is about 15 million °C, over 500 times hotter than lightning. "
                 "And in this parallel world, lightning is only as hot as a candle flame... ⚡\n"
                 "Hot lightning or calm lightning? Comment below \U0001F447\n\n"
                 "Real science: lightning superheats a narrow channel of air so fast that it expands with a bang, and that sound wave is thunder. "
                 "The 27,000°C figure is a peak; parts of the channel are cooler. "
                 "Sources: NOAA National Weather Service, NOAA NSSL, NASA, Britannica.\n\n"
                 "#shorts #science #lightning #sun #weather #swirlverse"),
    tags=['is lightning hotter than the sun', 'how hot is lightning', 'lightning temperature', 'sun temperature', 'sun core',
          'thunder', 'weather science', 'space science', 'parallel world', 'what if', 'science shorts', 'swirlverse', 'animation'],
    topic='is lightning hotter than the sun / lightning temperature vs sun surface and core (thunder from rapid heating)',
    category='weather / space', hook='storm flash + kiko question cold open -> thermometers -> IT DEPENDS verdict -> portal test',
)
DROPS = []

BOLT, BOLT_HOT, CANDLE = '#fff27a', '#ffffff', '#ffae4a'
SUN, SUN_SH, CORE = '#ffcf3a', '#ff9a1f', '#fff8d0'

# ---------------------------------------------------------------- props
def bolt_pts(x, y, s, seed=0):
    """zigzag lightning bolt polygon, top at (x, y), length ~ 900*s"""
    zz = [(0, 0), (-70, 260), (20, 250), (-60, 560), (40, 540), (-30, 900)]
    left = [(x + (px - 22)*s, y + py*s) for (px, py) in zz]
    right = [(x + (px + 22)*s, y + py*s) for (px, py) in reversed(zz)]
    return left[:-1] + [(x + zz[-1][0]*s, y + zz[-1][1]*s)] + right[1:]

def bolt(T, x, y, s, col=BOLT, k=1.0, glow=True):
    if k <= 0.01: return
    if glow:
        for (fy, r) in ((0.15, 260), (0.45, 300), (0.8, 260)):
            T.glow(x, y + 900*s*fy, r*s*k, col, ((2.2, 0.10*k), (1.5, 0.18*k)))
    T.shape(bolt_pts(x, y, s), col, lw=8, alpha=min(1, k))

def thermo(T, t, x, y, h, frac, col, txt, u):
    """vertical thermometer: tube + bulb, filled to frac, label above"""
    T.shape(rect(x - 45, y - h, 90, h), '#ffffff', lw=8)
    f = ease(u/1.0)*frac
    T.shape(rect(x - 26, y - h*f, 52, h*f + 10), col, lw=0, line=False)
    T.shape(ellipse_pts(x, y + 40, 80, 80), col, shadow=mixc(col, '#000000', 0.25), shade_dir=(1, 0.4), shade_w=0.25, lw=8)
    for i in range(1, 6): T.stroke([(x + 45, y - h*i/6), (x + 75, y - h*i/6)], lw=6, col='#ffffff')

def sun(T, t, x, y, r, face='happy', core=0.0):
    rot = tq(t)*0.6
    for i in range(14):
        a = rot + 2*math.pi*i/14
        T.shape([(x + math.cos(a - 0.12)*r*1.08, y + math.sin(a - 0.12)*r*1.08), (x + math.cos(a)*r*1.42, y + math.sin(a)*r*1.42),
                 (x + math.cos(a + 0.12)*r*1.08, y + math.sin(a + 0.12)*r*1.08)], SUN_SH, lw=6)
    T.glow(x, y, r, '#fff0a0')
    T.shape(ellipse_pts(x, y, r, r), SUN, shadow=SUN_SH, shade_dir=(1, 0.5), shade_w=0.22, lw=9)
    if core > 0.01:   # cut-away: layers down to the white-hot core
        T.shape(ellipse_pts(x, y, r*0.72*core, r*0.72*core), '#ff8a2a', lw=6)
        T.shape(ellipse_pts(x, y, r*0.45*core, r*0.45*core), '#ffd35a', lw=6)
        T.glow(x, y, r*0.3*core, CORE, ((2.0, 0.3), (1.4, 0.45)))
        T.shape(ellipse_pts(x, y, r*0.25*core, r*0.25*core), CORE, lw=6)
    else:
        ex = r*0.32; ey = y - r*0.12
        for e in (-1, 1):
            T.shape(ellipse_pts(x + e*ex, ey, r*0.09, r*0.12), '#2b2b3a', lw=0, line=False)
        if face == 'happy':
            T.stroke([(x - r*0.3, y + r*0.25), (x, y + r*0.42), (x + r*0.3, y + r*0.25)], lw=9, col='#2b2b3a')
        else:
            T.shape(ellipse_pts(x, y + r*0.32, r*0.12, r*0.15), '#2b2b3a', lw=0, line=False)

def rain(T, t, a=0.45):
    rng = np.random.default_rng(7)
    for i in range(60):
        x0, y0 = rng.uniform(-100, 1180), rng.uniform(0, 1900)
        yy = (y0 + tq(t)*1400) % 2000 - 60
        T.stroke([(x0 + yy*0.08, yy), (x0 + yy*0.08 + 10, yy + 50)], lw=4, col='#bcd2ff', alpha=a)

def cloud(T, x, y, s, col='#3a4166'):
    for (dx, dy, r) in ((-160, 20, 110), (-40, -40, 150), (110, -10, 130), (220, 40, 90)):
        T.shape(ellipse_pts(x + dx*s, y + dy*s, r*s, r*s*0.8), col, shadow=mixc(col, '#000000', 0.3), shade_dir=(0, 1), shade_w=0.25, lw=7)

def rings(T, x, y, u, strength=1.0, col='#ffffff'):
    for i in range(4):
        p = (u*1.4 - i*0.22)
        if 0 < p < 1:
            c = T.c; c.new_path(); c.arc(x, y, 60 + p*520*strength, 0, 2*math.pi)
            c.set_source_rgba(*hexc(col, (1 - p)*0.8)); c.set_line_width(18*strength + 4); c.stroke()

# ---------------------------------------------------------------- shots
def sh_cold(K, T, t, u):
    """stormy park at night, a bolt cracks behind the pair; the question pops at once"""
    T.cx, T.cy, T.z = 540, 980, 1.14 - 0.1*ease(u/2.5)
    K.world(T, t, False)
    cloud(T, 560, 760, 1.0)
    fl = 1.0 if (0.25 < u < 0.6 or 1.4 < u < 1.6) else 0.0
    if fl: T.flat(rect(-500, -500, 2200, 3200), '#ffffff', alpha=0.18); bolt(T, 600, 700, 0.62, k=1.0)
    rain(T, t)
    K.kiko(T, t, **pose('shock' if u < 1.2 else 'confused', 'hands_head' if u < 1.2 else 'point', look=(0.8, -0.5), jit=jitter(t) if u < 0.8 else 0))
    K.nova(T, t, **pose('excited', 'finger_up'))
    label(T.c, 'IS LIGHTNING', 540, 330, 120, '#ffffff', -0.04, back((u - 0.05)/0.3, 1.6))
    label(T.c, 'HOTTER THAN THE SUN?', 540, 480, 92, '#ffd43b', 0.03, back((u - 0.2)/0.3, 1.6))

def sh_bolt(K, T, t, u):
    """board: giant bolt + thermometer shooting up, counter to 27,000 C"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#141a36', '#232c55')
    bolt(T, 330, 560, 1.0, k=ease(u/0.25))
    thermo(T, t, 790, 1450, 760, 1.0, '#ff4f4f', '', u - 0.3)
    v = 27000*ease((u - 0.3)/1.2)
    label(T.c, f'{int(round(v, -2)):,}°C', 540, 400, 150, '#ffd43b', -0.03, back((u - 0.2)/0.3, 1.5))
    label(T.c, 'LIGHTNING (PEAK)', 540, 540, 66, '#ffffff', 0, back((u - 0.6)/0.3, 1.4))

def sh_sun(K, T, t, u):
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*u
    board(T, t, '#3b1f4a', '#53306a')
    sun(T, t, 330, 1000, 210, 'happy')
    thermo(T, t, 790, 1450, 760, 0.2, '#ffa42b', '', u - 0.3)
    v = 5500*ease((u - 0.3)/1.0)
    label(T.c, f'{int(round(v, -2)):,}°C', 540, 400, 150, '#ffd43b', -0.03, back((u - 0.2)/0.3, 1.5))
    label(T.c, "SUN'S SURFACE", 540, 540, 70, '#ffffff', 0, back((u - 0.6)/0.3, 1.4))

def sh_vs(K, T, t, u):
    """two bars: lightning 27,000 vs sun surface 5,500, then a 5X stamp"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    for i, (name, v, col) in enumerate((('LIGHTNING', 27000, '#fff27a'), ('SUN SURFACE', 5500, '#ffa42b'))):
        k = ease((u - 0.1 - i*0.3)/0.7); x = 300 + i*480; h = 900*v/27000*k
        T.shape(rect(x - 130, 1450 - h, 260, max(h, 2)), col, shadow=mixc(col, '#000000', 0.2), shade_dir=(1, 0), shade_w=0.15, lw=8)
        label(T.c, name, x, 1540, 56, '#ffffff', 0, 1, FONT, 10)
        if k > 0.05: label(T.c, f'{int(round(v*k, -2)):,}°C', x, 1450 - h - 70, 70, col, 0, 1)
    if u > 0.2: bolt(T, 300, 560 + 900*(1 - ease((u - 0.1)/0.7)) - 380, 0.33, k=1.0, glow=False)
    k = back((u - 1.0)/0.25, 1.8)
    if k > 0.01: label(T.c, '5X HOTTER!', 640, 330, 140, '#ff4fa3', -0.06, k)

def sh_thunder(K, T, t, u):
    """the bolt heats the air, rings blast outward: BOOM"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.03*u
    board(T, t, '#141a36', '#232c55')
    cloud(T, 540, 450, 1.1)
    bolt(T, 540, 520, 1.05, k=1.0 if (u % 0.9) < 0.6 else 0.6)
    rings(T, 540, 1000, u % 1.4, 1.0, '#c9d8ff')
    for (dx, dy) in ((-260, 0), (260, 60), (-200, 380), (230, 420)):
        T.glow(540 + dx, 1000 + dy, 40, '#ff8a4a', ((1.6, 0.2), (1.2, 0.3)))
    kin(T.c, t, 'HOT AIR BLASTS OUT', K.S(4) + 0.4, 540, 1580, 74, '#ffd43b', 0.02)
    if u > 1.6: kin(T.c, t, 'BOOM!', K.at(4, 0.65), 540, 300, 220, '#ffffff', -0.05)

def sh_core(K, T, t, u):
    """sun cut-away: the core glows white-hot; counter to 15 million"""
    T.cx, T.cy, T.z = 540, 980, 1.0 + 0.03*u
    board(T, t, '#2a1030', '#3e1a48')
    sun(T, t, 540, 1020, 300, core=ease((u - 0.2)/0.6))
    if u > 0.7: arrow(T.c, 880, 1500, 600, 1130, '#7dff9a', 22)
    v = 15*ease((u - 0.6)/1.2)
    label(T.c, 'SUN CORE', 540, 320, 110, '#ffffff', -0.03, back((u - 0.1)/0.3, 1.5))
    label(T.c, f'{v:.0f} MILLION °C' if v >= 1 else '...', 540, 470, 96, '#ffd43b', 0.02, back((u - 0.5)/0.3, 1.5))
    if u > K.at(5, 0.55) - K.L(5): kin(T.c, t, '500X+ LIGHTNING!', K.at(5, 0.55), 540, 1610, 90, '#ff4fa3', 0.03)

def sh_dim(K, T, t, u):
    """parallel park: a dim orange candle-flame bolt, a tiny 'poof' ring; Kiko unimpressed"""
    T.cx, T.cy, T.z = 540, 960, 1.0 + 0.02*ease(u/2)
    K.world(T, t, True)
    cloud(T, 560, 560, 1.1, '#6b5a9a')
    fl = 0.6 if (u < 1.4 and int(u*6) % 3 != 0) else 0.0
    if fl: bolt(T, 600, 620, 0.6, col=CANDLE, k=fl)
    if 0.5 < u < 2.0: rings(T, 600, 1040, (u - 0.5)*1.2, 0.25, '#ffd9a8')
    K.kiko(T, t, **pose('deadpan', 'shrug', look=(0.8, -0.6)))
    K.nova(T, t, **pose('smug', 'present', x=900))
    if u > 0.6: kin(T.c, t, 'poof.', K.S(8) + 1.6, 600, 470, 130, '#ffd9a8', 0.05)

def sh_blast(K, T, t, u):
    """side by side: super hot bolt = big blast rings; cool bolt = tiny ring"""
    T.cx, T.cy, T.z = 540, 960, 1.0
    board(T, t)
    bolt(T, 290, 520, 0.62, k=1.0)
    bolt(T, 800, 520, 0.62, col=CANDLE, k=0.55, glow=False)
    rings(T, 290, 900, u % 1.3, 0.55, '#c9d8ff')
    rings(T, 800, 900, u % 1.3, 0.12, '#ffd9a8')
    label(T.c, 'SUPER HOT', 290, 1380, 70, '#fff27a', -0.03, back((u - 0.1)/0.3, 1.5))
    label(T.c, '= BOOM', 290, 1480, 80, '#ffffff', -0.03, back((u - 0.3)/0.3, 1.5))
    label(T.c, 'CANDLE HOT', 800, 1380, 70, CANDLE, 0.03, back((u - 0.6)/0.3, 1.5))
    label(T.c, '= poof', 800, 1480, 80, '#ffffff', 0.03, back((u - 0.8)/0.3, 1.5))
    label(T.c, 'LESS HEAT = LESS BLAST', 540, 330, 80, '#ffd43b', -0.02, back(u/0.3, 1.4))

def storm_extra(T, t, u):
    rain(T, t, 0.35)

def shots(K):
    K.custom(0.0, sh_cold, sfx='pop')
    K.custom(K.at(1, 0.15), sh_bolt, sfx='swoop')
    K.custom(K.L(2), sh_sun, sfx='pop')
    K.kcu(K.L(3), par=False, emo='shock', gest='hands_head', extra=storm_extra)
    K.custom(K.at(3, 0.6), sh_vs, sfx='blip')
    K.custom(K.at(4, 0.3), sh_thunder, sfx='boing')
    K.custom(K.L(5), sh_core, sfx='swoop')
    K.verdict(K.L(6), 'IT DEPENDS!', col='#ffd43b', sub='surface: TRUE  ·  core: NO WAY')
    K.hook(K.L(7), portal_line=7, portal_f=0.45)
    K.arrive(tag_text='WORLD #17 · CANDLE-FLAME LIGHTNING')
    K.custom(K.S(8) + 1.0, sh_dim, sfx='swoop')
    K.custom(K.L(9), sh_blast, sfx='blip')
    K.end(K.L(10), poll=('HOT LIGHTNING', 'CALM LIGHTNING'))

def thumbnail(c, K):
    """huge text, big shocked Kiko, a giant bolt beside a small sun (bolt really is ~5x the sun's surface temp), arrow"""
    burst(c, W, H, 560, 1150, '#c9d4ff', '#141a5c', spin=0.15)
    T = Toon(c, 1.0, cam=(540, 960, 1.0))
    bolt(T, 760, 700, 1.05, k=1.0)
    sun(T, 0.3, 860, 1650, 140, 'shock')
    P = pose('shock', 'hands_head'); P.update(x=270, y=2300, s=1.8, face=1, look=(0.8, -0.6), jit=0)
    K.kiko(T, 1.0, **P)
    big_text(c, '5X HOTTER', 540, 250, 150, hl=0, hl_col='#ff4fa3', max_w=980)
    big_text(c, 'OR NOT?!', 540, 450, 170, max_w=1010)
    emoji_burst(c, 300, 760, 110, 'CORE?!', '#ff2d55', -0.15)
    arrow(c, 520, 1000, 700, 1150, '#ffd43b', 26)
