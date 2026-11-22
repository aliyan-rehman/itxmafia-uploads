"""Generic Swirlverse mix: our-world cue -> parallel-world groove after the swirl wipe, optional silent beats,
soft tonal SFX gated to half while anyone speaks and capped below the voice. Loudness is normalised at mux (-14 LUFS)."""
import numpy as np, sound as S
from sound import SR
import musiclib as M

SFX = {
    'blip': lambda: M.blip(900, 600), 'click': lambda: M.blip(1200, 900), 'pop': lambda: S.pop(),
    'pop2': lambda: S.pop(0.09, 1100, 500), 'boing': lambda: S.boing(0.5), 'chime': lambda: M.chime(1046, 1318, 1568),
    'chime4': lambda: M.chime(1046, 1318, 1568, 2093), 'portal': M.portal_open, 'swoop': lambda: M.glide(400, 1600, 0.5, 0.5),
    'nope': M.soft_x, 'bloop': M.bloop, 'squeak': M.squeak, 'tick': lambda: S.tick(), 'whistle_up': lambda: S.slide_whistle(0.55, True),
    'whistle_down': lambda: S.slide_whistle(0.55, False), 'fwump': M.fwump, 'bubble': lambda: M.bubble(900),
}

def build_mix(total, vo_path, lines, sfx, out_path, wipe_t=None, drops=(), long_form=False, think=None):
    m = S.Mix(total)
    m.voice(vo_path, 0, 1.0)
    mus = np.zeros(int(total*SR) + SR)
    w = wipe_t if wipe_t else 0.0
    if w > 0.5:
        a = M.bright_intro(w + 0.2); fo = int(0.5*SR); a[-fo:] *= np.linspace(1, 0, fo); M.place(mus, a, 0, 0.8)
    end_g = total if not think else think[0]
    g = M.groove(end_g - w + 0.4, 120, seed=3); fo = int(0.4*SR); g[-fo:] *= np.linspace(1, 0, fo); M.place(mus, g, w, 1.0)
    if think:
        tc = M.think_cue(think[1] - think[0] + 0.3); fi = int(0.4*SR); tc[:fi] *= np.linspace(0, 1, fi); tc[-fi:] *= np.linspace(1, 0, fi); M.place(mus, tc, think[0], 1.1)
        g2 = M.groove(total - think[1] + 0.5, 120, seed=5)[:int((total - think[1])*SR)]; M.place(mus, g2, think[1], 0.9)
    fo = int(1.2*SR); mus[int(total*SR) - fo:int(total*SR)] *= np.linspace(1, 0, fo)
    for (a, b) in drops:   # hard musical silence for a punchline
        mus[int(a*SR):int(b*SR)] *= 0.08
    m.music(mus[:m.n], 0, 0.55, 0.05, 0.4)
    m.duck([(l['s'] - 0.06, l['e'] + 0.06) for l in lines], 0.45, 0.12)
    for (t0, name, gain) in sfx:
        snd = SFX[name]() if isinstance(name, str) else name
        m.sfx(snd, max(0, t0), gain)
    m.sfx(M.chime(1046, 1318, 1568, 2093), max(0, total - 1.4), 0.18)
    gate = np.ones(m.n)
    for l in lines:
        a_, b_ = int((l['s'] - 0.05)*SR), int((l['e'] + 0.05)*SR); gate[max(0, a_):b_] = 0.5
    m.fx *= np.convolve(gate, np.ones(2400)/2400, mode='same')
    nz = np.abs(m.vo[0][m.vo[0] != 0]); vp = np.percentile(nz, 99.5); fp = np.abs(m.fx).max()
    if fp > 0.55*vp: m.fx *= 0.55*vp/fp
    m.write(out_path)
