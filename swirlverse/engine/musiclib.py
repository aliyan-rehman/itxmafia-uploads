"""Synthesized Swirlverse score + soft tonal SFX (no samples, no Content ID risk)."""
import numpy as np, sound as S
from sound import SR, T as TT, mtof, filt, env, osc, norm, reverb

def place(buf, x, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf) or i + len(x) <= 0: return
    j = min(len(buf), i + len(x)); buf[max(i, 0):j] += g*x[max(0, -i): j - i]

def theremin(notes, d, vib=5.6):
    """notes: [(t, midi, dur)] -> legato sine lead with portamento, delayed vibrato, a little 2nd/3rd harmonic"""
    n = int(d*SR); f = np.zeros(n); a = np.zeros(n)
    for (t0, m, du) in notes:
        i0, i1 = int(t0*SR), min(n, int((t0 + du)*SR)); f[i0:i1] = mtof(m); a[i0:i1] = 1
    # portamento (~70 ms) on frequency, soft attack/release on amplitude
    k = np.exp(-1/(0.07*SR)); lf = np.copy(f); last = f[f > 0][0] if (f > 0).any() else 440
    for i in range(n):
        if f[i] > 0: last = last*k + f[i]*(1 - k)
        lf[i] = last
    a = np.convolve(a, np.ones(int(0.04*SR))/int(0.04*SR), 'same')
    vibd = np.zeros(n)
    for (t0, m, du) in notes:
        i0, i1 = int(t0*SR), min(n, int((t0 + du)*SR)); tt = np.arange(i1 - i0)/SR
        vibd[i0:i1] = np.clip((tt - 0.15)/0.25, 0, 1)*0.006
    tt = np.arange(n)/SR
    fr = lf*(1 + vibd*np.sin(2*np.pi*vib*tt))
    ph = 2*np.pi*np.cumsum(fr)/SR
    y = (np.sin(ph) + 0.25*np.sin(2*ph) + 0.12*np.sin(3*ph))*a
    return reverb(y*0.5, 1.2, 0.25)

def sq(m, d, v=0.5):
    t = TT(d); x = np.sign(np.sin(2*np.pi*mtof(m)*t))*0.5 + np.sin(2*np.pi*mtof(m)*t)*0.5
    return filt(x, 'lowpass', 1800)*env(len(t), 0.004, 0.06, d=d*0.7)*v

def anabass(m, d, v=0.8):
    t = TT(d); x = osc(mtof(m), d, 'saw') + 0.6*np.sin(2*np.pi*mtof(m)*t)
    return filt(x, 'lowpass', 520)*env(len(t), 0.006, 0.06, d=d*0.8)*v*0.5

def tick_hat(v=0.3): t = TT(0.04); return np.sin(2*np.pi*6200*t)*np.exp(-t*160)*v*0.5

PROG_D = [(50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67]), (45, [57, 61, 64])]   # Dm Bb C A

def groove(d, bpm=120, lead=True, seed=1, drums=True):
    b = 60/bpm; out = np.zeros(int(d*SR) + 2*SR); t = 0.0; bar = 0; notes = []
    motif = [(0, 62), (0.75, 65), (1.5, 69), (2, 67), (2.5, 65), (3, 64), (3.5, 61), (4, 62)]   # own motif: D F A G F E C# D
    while t < d:
        root, ch = PROG_D[bar % 4]
        place(out, anabass(root - 12, b*0.9), t); place(out, anabass(root - 12, b*0.45, 0.6), t + 1.5*b)
        place(out, anabass(root, b*0.45, 0.5), t + 2.5*b); place(out, anabass(root - 12, b*0.9), t + 3*b)
        for i in range(8):   # soft square arp on 8ths
            place(out, sq(ch[i % 3] + (12 if i % 4 == 3 else 0), b*0.45, 0.16), t + i*b/2)
        if drums:
            for i in range(4):
                if i % 2 == 0: place(out, S.kick(0.55), t + i*b)
                place(out, tick_hat(0.35), t + i*b + b/2)
            place(out, S.clap(0.25) if hasattr(S, 'clap') else S.snare(0.25), t + b); place(out, S.clap(0.25) if hasattr(S, 'clap') else S.snare(0.25), t + 3*b)
        if lead and bar % 2 == 0:
            for (bt, m) in motif:
                notes.append((t + bt*b, m + 12, 0.45*b if bt < 4 else b*1.6))
        t += 4*b; bar += 1
    y = out[:int(d*SR)]
    if notes: th = theremin(notes, d); y += 0.55*th[:len(y)]
    return y

def bright_intro(d, bpm=110):
    """our-world cue: sunny marimba arp in C"""
    b = 60/bpm; out = np.zeros(int(d*SR) + SR); t = 0.0; bar = 0
    prog = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
    while t < d:
        ch = prog[bar % 4]
        for i in range(8): place(out, S.marimba(ch[(i*2 + bar) % 4], 0.5, 0.5), t + i*b/2)
        place(out, S.bass(ch[0] - 24, b*1.5, 0.5), t); place(out, S.bass(ch[0] - 24, b, 0.4), t + 2*b)
        t += 4*b; bar += 1
    return out[:int(d*SR)]

def tension(d):
    """red-sea cue: tremolo low strings (filtered saws) + a slow theremin wobble"""
    t = TT(d); out = np.zeros(len(t))
    for m in (38, 45, 50, 53):
        x = filt(osc(mtof(m), d, 'saw'), 'lowpass', 900)*(0.6 + 0.4*np.sin(2*np.pi*11*t))*0.12
        out += x
    out *= np.clip(t/0.4, 0, 1)
    notes = [(0.3, 74, 1.4), (1.8, 73, 1.4), (3.3, 72, 1.4), (4.8, 71, 2.0)]
    th = theremin(notes, d); out += 0.45*th[:len(out)]
    return out

# ------------------------------------------------------------------ soft effects
def chime(*fs, gap=0.09, d=1.0):
    out = np.zeros(int((len(fs)*gap + d)*SR))
    for i, f in enumerate(fs):
        x = S.ding(f, d); a = int(i*gap*SR); out[a:a + len(x)] += x[:len(out) - a]
    return norm(out, 0.6)
def blip(f0=700, f1=520): return S.pop(0.06, f0, f1)
def glide(f0, f1, d, v=0.5):
    t = TT(d); f = f0*(f1/f0)**(t/d); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d)**1.5*v
def fwump(d=0.55):
    t = TT(d); f = 110*np.exp(-t*4) + 40; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5)*0.9
def portal_open():
    x = np.zeros(int(1.2*SR)); a = fwump(); x[:len(a)] += a
    g = glide(300, 1100, 0.9, 0.35)*(0.75 + 0.25*np.sin(2*np.pi*14*TT(0.9))); x[int(0.05*SR):int(0.05*SR) + len(g)] += g
    return norm(x, 0.7)
def bloop():   # tonal 'water landing', no noise
    x = glide(520, 140, 0.32, 0.8); x2 = S.pop(0.07, 1100, 600)*0.5; y = np.zeros(int(0.5*SR)); y[:len(x)] += x; y[int(0.12*SR):int(0.12*SR) + len(x2)] += x2
    return y
def squeak():
    a = glide(1500, 2300, 0.12, 0.45); b = glide(2100, 1500, 0.14, 0.4); return np.concatenate([a, np.zeros(int(0.03*SR)), b])
def bubble(f=900): return S.pop(0.07, f, f*0.6)*0.6
def soft_x():   # gentle "nope": two descending marimba notes
    y = np.zeros(int(0.7*SR)); a = S.marimba(64, 0.4, 0.7); b = S.marimba(60, 0.5, 0.7)
    y[:len(a)] += a; y[int(0.12*SR):int(0.12*SR) + len(b)] += b; return y


def think_cue(d):
    """chapter 6: soft marimba + low pad, no drums"""
    b = 60/100; out = np.zeros(int(d*SR) + SR); t = 0.0; bar = 0
    prog = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]
    while t < d:
        ch = prog[bar % 4]
        for i in range(6): place(out, S.marimba(ch[i % 3] + 12, 0.6, 0.35), t + i*b*0.66)
        place(out, S.bass(ch[0] - 24, b*3, 0.4), t)
        t += 4*b; bar += 1
    return out[:int(d*SR)]

