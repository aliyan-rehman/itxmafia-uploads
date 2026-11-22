"""sound.py - synthesized SFX + music + mixer (numpy/scipy). 100% original audio, no samples needed."""
import numpy as np, subprocess, random
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
def T(d): return np.arange(int(d * SR)) / SR
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a=0.005, r=None, d=None):
    e = np.ones(n); ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai)
    if d is not None: e *= np.exp(-np.arange(n) / SR / d)
    if r: ri = min(n, int(r * SR)); e[-ri:] *= np.linspace(1, 0, ri)
    return e
def filt(x, kind, f, order=2):
    f = np.clip(np.atleast_1d(f), 20, SR / 2 - 100)
    return sosfilt(butter(order, f if len(f) > 1 else f[0], kind, fs=SR, output='sos'), x)
def sweep_lp(x, f0, f1, block=256):
    """Lowpass with a cutoff that moves from f0 to f1 (one-pole, per block)."""
    y = np.zeros_like(x); s = 0.0; n = len(x)
    for i in range(0, n, block):
        f = f0 + (f1 - f0) * (i / n); a = np.exp(-2 * np.pi * f / SR)
        seg = x[i:i + block]; out = np.empty_like(seg)
        for j, v in enumerate(seg): s = (1 - a) * v + a * s; out[j] = s
        y[i:i + block] = out
    return y
def reverb(x, t60=1.6, mix=0.25, seed=1):
    rng = np.random.default_rng(seed); n = int(t60 * SR)
    ir = rng.standard_normal(n) * np.exp(-6.9 * np.arange(n) / n); ir = filt(ir, 'lowpass', 6000)
    wet = np.pad(fftconvolve(x, ir), (0, 1))[:len(x) + n]; wet /= (np.max(np.abs(wet)) + 1e-9) / (np.max(np.abs(x)) + 1e-9)
    out = np.zeros(len(x) + n); out[:len(x)] += x * (1 - mix); out += wet * mix; return out
def norm(x, peak=0.9): return x / (np.max(np.abs(x)) + 1e-9) * peak
def osc(f, d, kind='sine', phase=0):
    f = np.broadcast_to(np.asarray(f, float), (int(d * SR),)); ph = 2 * np.pi * np.cumsum(f) / SR + phase
    if kind == 'sine': return np.sin(ph)
    if kind == 'saw': return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if kind == 'square': return np.sign(np.sin(ph))
    if kind == 'tri': return 2 * np.abs(2 * ((ph / (2 * np.pi)) % 1) - 1) - 1
def noise(d, seed=None): return np.random.default_rng(seed).standard_normal(int(d * SR))

# ---------- SFX ----------
def whoosh(d=0.7, f0=300, f1=4000, seed=0):
    n = noise(d, seed); x = sweep_lp(n, f0, f1) * np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2
    return norm(reverb(x, 0.6, 0.2), 0.8)
def swish(d=0.25): return whoosh(d, 800, 7000, 3) * 0.8
def riser(d=2.5, seed=1):
    t = T(d); k = t / d
    x = sweep_lp(noise(d, seed), 300, 9000) * k ** 2 + 0.25 * osc(200 + 900 * k ** 2, d, 'saw') * k ** 3
    return norm(filt(x, 'highpass', 150), 0.8)
def impact(d=2.2):
    t = T(d); sub = np.sin(2 * np.pi * np.cumsum(30 + 50 * np.exp(-t * 6)) / SR) * np.exp(-t * 1.8)
    hit = filt(noise(d, 4), 'lowpass', 2500) * np.exp(-t * 14)
    return norm(reverb(sub + 0.7 * hit, 2.2, 0.3), 0.95)
def swell_hit(d=1.6):
    """Cinematic swell-in whoosh that lands on a title (softer than a boom)."""
    a = whoosh(d * 0.75, 200, 3000, 9); a = a * np.linspace(0.3, 1, len(a)) ** 2; land = int(d * 0.75 * SR)
    b = impact(1.8) * 0.6; out = np.zeros(max(len(a), land + len(b))); out[:len(a)] += a; out[land:land + len(b)] += b; return norm(out, 0.9)
def pop(d=0.09, f0=900, f1=320):
    t = T(d); return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR) * np.exp(-t * 40)
def boing(d=0.6):
    t = T(d); f = 180 + 120 * t / d + 60 * np.sin(2 * np.pi * 16 * t) * np.exp(-t * 4)
    return osc(f, d) * np.exp(-t * 5) * 0.9
def ding(f=1318.5, d=1.6):
    t = T(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * dc) for m, a, dc in ((1, 1, 2.5), (2.76, 0.4, 5), (5.4, 0.2, 9), (8.93, 0.1, 14)))
    return norm(x * env(len(t), 0.002), 0.6)
def success(): out = np.zeros(int(1.8 * SR)); a = ding(1046.5); b = ding(1568); out[:len(a)] += a; out[int(0.11 * SR):int(0.11 * SR) + len(b)] += b; return norm(out, 0.6)
def wrong():
    t = T(0.5); x = osc(np.where(t < 0.22, 220, 185), 0.5, 'square') * env(len(t), 0.005, 0.05); return filt(x, 'lowpass', 1800) * 0.35
def thud(d=0.4):
    t = T(d); return norm(np.sin(2 * np.pi * np.cumsum(45 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 9) + 0.3 * filt(noise(d, 5), 'lowpass', 400) * np.exp(-t * 25), 0.9)
def step(seed=0): return filt(noise(0.12, seed), 'bandpass', [120, 900]) * np.exp(-T(0.12) * 35) * 0.8
def click(): return filt(noise(0.02, 2), 'highpass', 2000) * np.exp(-T(0.02) * 300) * 0.6
def slide_whistle(d=0.7, up=True):
    t = T(d); f = np.linspace(500, 1400, len(t)) if up else np.linspace(1400, 450, len(t)); return osc(f + 6 * np.sin(2 * np.pi * 6 * t), d) * env(len(t), 0.02, 0.1) * 0.5
def scratch():
    t = T(0.45); f = 300 + 1600 * np.abs(np.sin(2 * np.pi * 3.2 * t)); return filt(osc(f, 0.45, 'saw') + 0.4 * noise(0.45, 6), 'bandpass', [300, 4000]) * env(len(t), 0.005, 0.1) * 0.5
def tick(): t = T(0.03); return np.sin(2 * np.pi * 3000 * t) * np.exp(-t * 200) * 0.4
def typing(d=1.5, seed=0):
    out = np.zeros(int(d * SR)); rng = random.Random(seed); x = 0.0
    while x < d - 0.05: c = click() * rng.uniform(0.5, 1); i = int(x * SR); out[i:i + len(c)] += c; x += rng.uniform(0.06, 0.16)
    return out
def page_flip(seed=0):
    d = 0.35; t = T(d); x = filt(noise(d, seed), 'bandpass', [1500, 7000]) * (np.exp(-t * 18) + 0.5 * np.exp(-((t - 0.12) ** 2) / 0.002)); return norm(x, 0.5)
def pencil(d=1.0, seed=0):
    t = T(d); x = filt(noise(d, seed), 'bandpass', [1500, 4500]) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 5 * t))) ** 2; return x * 0.12
def notif(): out = np.zeros(int(0.9 * SR)); a = ding(1760, 0.6); b = ding(2349, 0.7); out[:len(a)] += a; out[int(0.09 * SR):int(0.09 * SR) + len(b)] += b; return out * 0.7
def drum_roll(d=1.2): t = T(d); return filt(noise(d, 8), 'bandpass', [150, 3000]) * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * t)) * np.linspace(0.3, 1, len(t)) * 0.5

# ---------- instruments ----------
def piano(m, d=1.5, v=0.8):
    f = mtof(m); t = T(d); x = sum((1 / k ** 1.4) * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k)) for k in range(1, 7))
    return x * env(len(t), 0.004, 0.08) * v * 0.5
def rhodes(m, d=1.5, v=0.7):
    f = mtof(m); t = T(d); x = np.sin(2 * np.pi * f * t + 0.8 * np.exp(-t * 3) * np.sin(2 * np.pi * f * t)) * np.exp(-t * 1.0)
    return x * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * t)) * env(len(t), 0.004, 0.1) * v * 0.4
def pluck(m, d=0.35, v=0.7):
    f = mtof(m); t = T(d); x = sum((1 / k ** 1.2) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (8 + 6 * k)) for k in range(1, 6)); return x * env(len(t), 0.002) * v * 0.5
def marimba(m, d=0.6, v=0.7):
    f = mtof(m); t = T(d); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 25) + 0.1 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 60)
    return x * env(len(t), 0.002) * v * 0.5
def pad(ms, d=4.0, v=0.5, bright=1800):
    t = T(d); x = np.zeros(len(t))
    for m in ms:
        for det in (-0.12, 0, 0.11): x += sum(np.sin(2 * np.pi * mtof(m + det) * k * t + k) / k for k in range(1, 8))
    x = filt(x, 'lowpass', bright); return x / (len(ms) * 3) * env(len(t), min(0.8, d / 3), min(1.0, d / 3)) * v
def bass(m, d=0.5, v=0.8): t = T(d); return filt(osc(mtof(m), d, 'saw'), 'lowpass', 400) * env(len(t), 0.005, 0.05, d=0.4) * v * 0.6
def kick(v=1): t = T(0.35); return np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t * 35)) / SR) * np.exp(-t * 9) * v
def snare(v=1): t = T(0.22); return (filt(noise(0.22, 3), 'bandpass', [1200, 6000]) * np.exp(-t * 22) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)) * v * 0.6
def clap(v=1):
    t = T(0.25); e = sum(np.exp(-np.clip(t - o, 0, None) * 60) * (t >= o) for o in (0, 0.01, 0.02)); return filt(noise(0.25, 4), 'bandpass', [900, 4000]) * e * v * 0.4
def hat(v=1, d=0.05): t = T(d); return filt(noise(d, 5), 'highpass', 7000) * np.exp(-t * 70) * v * 0.35
def taiko(v=1): t = T(0.9); return norm(np.sin(2 * np.pi * np.cumsum(55 + 50 * np.exp(-t * 20)) / SR) * np.exp(-t * 4) + 0.3 * filt(noise(0.9, 7), 'lowpass', 300) * np.exp(-t * 12), 0.9) * v

def _place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf): return
    n = min(len(x), len(buf) - i); buf[i:i + n] += x[:n]

# ---------- music beds (seeded, loopable, any length) ----------
CHORDS = {  # midi roots-based voicings
    'C': [60, 64, 67], 'Am': [57, 60, 64], 'F': [53, 57, 60], 'G': [55, 59, 62], 'Em': [52, 55, 59], 'Dm': [50, 53, 57],
    'Fmaj7': [53, 57, 60, 64], 'Em7': [52, 55, 59, 62], 'Dm7': [50, 53, 57, 60], 'Cmaj7': [48, 52, 55, 59], 'Bb': [58, 62, 65],
    'D': [50, 54, 57], 'A': [57, 61, 64], 'Bm': [59, 62, 66], 'Gm': [55, 58, 62], 'Eb': [51, 55, 58],
}
def music_explainer(d, bpm=112, prog=('C', 'Am', 'F', 'G'), seed=1):
    """Curious, bouncy bed for fact/history Shorts: pizzicato arps + marimba hook + light groove."""
    out = np.zeros(int(d * SR) + SR); b = 60 / bpm; rng = random.Random(seed); pent = [0, 2, 4, 7, 9]
    bar = 0; t = 0.0
    while t < d:
        ch = CHORDS[prog[bar % len(prog)]]
        for i in range(8):
            _place(out, pluck(ch[i % 3] + (12 if i % 4 == 3 else 0), 0.3, 0.55), t + i * b / 2)
            _place(out, hat(0.5 if i % 2 else 0.8), t + i * b / 2)
        for i in (0, 2): _place(out, kick(0.7), t + i * b)
        for i in (1, 3): _place(out, clap(0.6), t + i * b)
        _place(out, bass(ch[0] - 24, b * 1.8), t); _place(out, bass(ch[0] - 24, b * 1.8), t + 2 * b)
        if bar % 2 == 1 or rng.random() < 0.5:
            for i in range(4):
                if rng.random() < 0.7: _place(out, marimba(72 + rng.choice(pent) + (12 if rng.random() < 0.2 else 0), 0.5, 0.5), t + i * b + rng.choice((0, b / 2)))
        t += 4 * b; bar += 1
    return norm(out[:int(d * SR)], 0.7)
def music_storytime(d, bpm=84, prog=('Fmaj7', 'Em7', 'Dm7', 'Cmaj7'), seed=2):
    """Warm lo-fi bed for funny personal stories (no crackle)."""
    out = np.zeros(int(d * SR) + SR); b = 60 / bpm; t = 0.0; bar = 0; rng = random.Random(seed)
    while t < d:
        ch = CHORDS[prog[bar % len(prog)]]
        for m in ch: _place(out, rhodes(m, 4 * b, 0.5), t + rng.uniform(0, 0.03))
        _place(out, bass(ch[0] - 12, 1.5 * b, 0.7), t); _place(out, bass(ch[0] - 12, b, 0.6), t + 2.5 * b)
        for i in range(8):
            sw = b / 2 * (0.62 if i % 2 else 0); _place(out, hat(0.35 + 0.2 * (i % 2 == 0)), t + (i // 2) * b + sw)
        _place(out, kick(0.6), t); _place(out, kick(0.45), t + 2.5 * b); _place(out, snare(0.45), t + b); _place(out, snare(0.45), t + 3 * b)
        t += 4 * b; bar += 1
    return norm(filt(out[:int(d * SR)], 'lowpass', 6500), 0.65)
def music_cinematic(d, mood='hope', bpm=72, seed=3):
    """mood: 'dark' (drone + sparse low piano), 'hope' (piano arps + strings), 'build' (ostinato + strings + taiko, rising)."""
    out = np.zeros(int(d * SR) + 4 * SR); b = 60 / bpm; t = 0.0; bar = 0
    prog = {'dark': ('Dm', 'Bb', 'Dm', 'A'), 'hope': ('D', 'A', 'Bm', 'G'), 'build': ('Dm', 'Bb', 'F', 'A')}[mood]
    if mood == 'dark':
        dr = pad([38, 45], d + 1, 0.6, 500); _place(out, dr, 0)
    while t < d:
        ch = CHORDS[prog[bar % len(prog)]]; k = t / max(d, 1e-6)
        _place(out, pad([m - 12 for m in ch] + [ch[0]], 4 * b + 1, 0.35 + (0.25 * k if mood != 'dark' else 0), 1400 if mood != 'dark' else 700), t)
        if mood == 'hope':
            for i in range(8): _place(out, piano(ch[i % 3] + 12 * (i // 3 % 2), 1.6, 0.55), t + i * b / 2)
        elif mood == 'dark':
            _place(out, piano(ch[0] - 12, 3, 0.5), t); _place(out, piano(ch[1], 2, 0.3), t + 2 * b)
        else:
            for i in range(16): _place(out, piano(ch[i % 3] + (12 if i % 4 == 0 else 0), 0.5, 0.35 + 0.35 * k), t + i * b / 4)
            _place(out, taiko(0.5 + 0.5 * k), t); _place(out, taiko(0.4 + 0.5 * k), t + 2 * b)
            if k > 0.5: _place(out, taiko(0.6 * k), t + 3 * b); _place(out, taiko(0.6 * k), t + 3.5 * b)
        t += 4 * b; bar += 1
    return norm(reverb(out[:int(d * SR)], 2.4, 0.3)[:int(d * SR)], 0.7)

# ---------- mixer ----------
class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR); self.fx = np.zeros((2, self.n)); self.mus = np.zeros((2, self.n)); self.vo = np.zeros((2, self.n)); self.dur = dur
    def _add(self, bus, x, at, gain, pan):
        x = np.asarray(x) * gain; l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        i = int(at * SR); n = min(len(x), self.n - i)
        if n > 0 and i >= 0: bus[0, i:i + n] += x[:n] * l * 1.41; bus[1, i:i + n] += x[:n] * r * 1.41
    def sfx(self, x, at, gain=0.8, pan=0.0): self._add(self.fx, x, at, gain, pan)
    def music(self, x, at=0, gain=0.35, fade_in=0.5, fade_out=1.0):
        x = np.array(x, float); fi, fo = int(fade_in * SR), int(fade_out * SR)
        if fi: x[:fi] *= np.linspace(0, 1, fi)
        if fo: x[-fo:] *= np.linspace(1, 0, fo)
        self._add(self.mus, x, at, gain, -0.0); d = int(0.012 * SR); self.mus[1, d:] = self.mus[1, d:] * 0.7 + self.mus[1, :-d] * 0.3
    def voice(self, path_or_arr, at=0, gain=1.0):
        x = load(path_or_arr) if isinstance(path_or_arr, str) else path_or_arr; self._add(self.vo, x, at, gain, 0)
    def duck(self, spans, amount=0.35, ramp=0.15):
        """Lower music under voice/key moments: spans=[(start,end),...]."""
        g = np.ones(self.n)
        for a, b in spans:
            i0, i1, r = int(a * SR), int(b * SR), int(ramp * SR); g[max(0, i0):i1] = np.minimum(g[max(0, i0):i1], amount)
            if i0 - r > 0: g[i0 - r:i0] = np.minimum(g[i0 - r:i0], np.linspace(1, amount, r))
            if i1 + r < self.n: g[i1:i1 + r] = np.minimum(g[i1:i1 + r], np.linspace(amount, 1, r))
        self.mus *= g
    def write(self, path):
        x = self.mus + self.fx + self.vo; x = np.tanh(x * 0.9) / np.tanh(0.9) * 0.9
        pcm = (np.clip(x.T, -1, 1) * 32767).astype(np.int16)
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', path], stdin=subprocess.PIPE)
        p.stdin.write(pcm.tobytes()); p.stdin.close(); p.wait(); return path
def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32767

# ---------- desi instruments ----------
def tabla(bol='na', v=1.0):
    """Synth tabla strokes: 'na','tin','ta' (dayan), 'ge','ka' (bayan), 'dha'=na+ge, 'dhin'=tin+ge."""
    if bol == 'dha': return _mixs(tabla('na', v), tabla('ge', v * 0.9))
    if bol == 'dhin': return _mixs(tabla('tin', v), tabla('ge', v * 0.8))
    if bol in ('na', 'ta', 'tin'):
        d = 0.5 if bol == 'tin' else 0.35; t = T(d); f = {'na': 660, 'ta': 640, 'tin': 700}[bol]
        x = np.sin(2 * np.pi * f * t) * np.exp(-t * (9 if bol == 'tin' else 14)) + 0.5 * np.sin(2 * np.pi * f * 2.05 * t) * np.exp(-t * 18) + 0.25 * np.sin(2 * np.pi * f * 3.1 * t) * np.exp(-t * 25)
        x += filt(noise(d, 11), 'bandpass', [2000, 7000]) * np.exp(-t * 120) * 0.6
        return x * v * 0.5
    if bol == 'ge':
        d = 0.7; t = T(d); f = 85 + 60 * (1 - np.exp(-t * 6))   # bayan pitch glide (meend)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5) * v * 0.8
    if bol == 'ka':
        d = 0.12; t = T(d); return filt(noise(d, 12), 'bandpass', [200, 1200]) * np.exp(-t * 60) * v * 0.6
def _mixs(a, b):
    n = max(len(a), len(b)); o = np.zeros(n); o[:len(a)] += a; o[:len(b)] += b; return o
def sitar(m, d=1.4, v=0.7, bend=0.0):
    f = mtof(m); t = T(d); fm = f * (1 + bend * (1 - np.exp(-t * 8)) * 0.06)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    x = sum((1 / k ** 0.8) * np.sin(k * ph) * np.exp(-t * (1.6 + 0.35 * k)) for k in range(1, 14))   # bright 'jawari' buzz
    x += 0.08 * filt(noise(d, int(m)), 'bandpass', [3000, 6000]) * np.exp(-t * 30)
    return x * env(len(t), 0.002, 0.1) * v * 0.22
def harmonium(ms, d=2.0, v=0.5):
    t = T(d); x = np.zeros(len(t))
    for m in ms:
        f = mtof(m); x += sum(((1 / k) if k % 2 else (0.6 / k)) * np.sin(2 * np.pi * f * k * t + 0.3 * k) for k in range(1, 9))
    x *= (1 + 0.06 * np.sin(2 * np.pi * 5 * t)); return filt(x, 'lowpass', 2800) / max(1, len(ms)) * env(len(t), 0.08, 0.25) * v * 0.35
def tanpura(root=50, d=4.0, v=0.4):
    out = np.zeros(int(d * SR)); seq = [root + 7, root + 12, root + 12, root]
    t0 = 0.0
    while t0 < d:
        for i, m in enumerate(seq): _place(out, sitar(m, 2.4, 0.35), t0 + i * 0.55)
        t0 += 2.2
    return out * v
RAAG = {'fun': [0, 2, 3, 5, 7, 9, 10, 12], 'mystery': [0, 1, 4, 5, 7, 8, 11, 12], 'warm': [0, 2, 4, 6, 7, 9, 11, 12]}
def music_desi(d, bpm=100, mood='fun', root=62, seed=5, sitar_on=True):
    """Desi bed: tabla theka + harmonium drone + sitar phrases in a raag-ish scale (Kafi=fun, Bhairav=mystery, Yaman=warm)."""
    out = np.zeros(int(d * SR) + 2 * SR); b = 60 / bpm / 2; rng = random.Random(seed); sc = RAAG[mood]
    theka = ['dha', 'dhin', 'na', 'dha', 'dha', 'dhin', 'na', 'ka', 'ta', 'tin', 'na', 'ta', 'dha', 'dhin', 'na', 'dha']
    t, i = 0.0, 0
    while t < d:
        bol = theka[i % 16]; _place(out, tabla(bol, 0.9 if i % 4 == 0 else 0.65), t)
        if i % 16 == 0: _place(out, harmonium([root - 12, root - 5, root], 16 * b + 0.3, 0.55), t)
        if sitar_on and i % 2 == 0 and rng.random() < 0.55:
            deg = rng.choice(sc[:7]); _place(out, sitar(root + 12 + deg - 12 * (rng.random() < 0.3), 1.2, 0.6, bend=rng.choice([0, 0, 1])), t)
        t += b; i += 1
    return norm(reverb(out[:int(d * SR)], 1.2, 0.18)[:int(d * SR)], 0.7)

# ---------- desi + editing SFX ----------
def spit(seed=2):
    d = 0.45; t = T(d); x = filt(noise(d, seed), 'bandpass', [600, 3500]) * np.exp(-t * 14) + 0.6 * np.sin(2 * np.pi * np.cumsum(420 - 300 * t) / SR) * np.exp(-t * 18)
    return norm(x, 0.7)
def splat(seed=4):
    d = 0.3; t = T(d); return norm(filt(noise(d, seed), 'lowpass', 1500) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 30), 0.6)
def hiccup():
    d = 0.22; t = T(d); f = 300 + 900 * t / d; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t - 0.05) ** 2) / 0.002) + 0.3 * filt(noise(d, 3), 'bandpass', [800, 3000]) * np.exp(-t * 40)
    return norm(x, 0.6)
def dhol(v=1.0):
    d = 0.8; t = T(d); x = np.sin(2 * np.pi * np.cumsum(70 + 80 * np.exp(-t * 25)) / SR) * np.exp(-t * 5) + 0.4 * filt(noise(d, 9), 'bandpass', [1500, 5000]) * np.exp(-t * 50)
    return norm(x, 0.9) * v
def pour(d=1.5, seed=6):
    t = T(d); x = filt(noise(d, seed), 'bandpass', [400, 2500]) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t) * np.sin(2 * np.pi * 2.3 * t))
    return x * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.2) * 0.35
def steam_hiss(d=1.5): t = T(d); return filt(noise(d, 7), 'highpass', 3000) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.5) * 0.25
def train_whistle(d=1.3):
    t = T(d); x = (np.sin(2 * np.pi * 523 * t) + 0.8 * np.sin(2 * np.pi * 659 * t) + 0.5 * np.sin(2 * np.pi * 784 * t)) / 2.3
    x = x * (1 + 0.3 * filt(noise(d, 8), 'lowpass', 30)) + 0.2 * filt(noise(d, 9), 'bandpass', [1500, 4000])
    return norm(reverb(x * env(len(t), 0.08, 0.3), 1.5, 0.3), 0.6)
def clock_tick(): t = T(0.05); return np.sin(2 * np.pi * 2500 * t) * np.exp(-t * 150) * 0.5
def time_stop():
    """Freeze hit: reversed swell into a glassy bell + pitch-dropping drone."""
    a = impact(1.2)[::-1][-int(0.7 * SR):] * 0.6; b = ding(1975, 1.8); t = T(1.8); drone = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 1.2) + 40) / SR) * np.exp(-t * 1.5) * 0.3
    out = np.zeros(len(a) + len(b)); out[:len(a)] += a; out[len(a):len(a) + len(b)] += b + drone; return norm(out, 0.8)
def time_resume(): return norm(np.concatenate([np.zeros(10), whoosh(0.6, 300, 6000, 4)]), 0.7)
def rewind(d=0.8):
    t = T(d); f = 600 + 2400 * (t / d) ** 2; x = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.3 * np.sign(np.sin(2 * np.pi * 18 * t)))) / SR)
    return filt(x, 'bandpass', [400, 5000]) * env(len(t), 0.02, 0.1) * 0.4
def stamp_sfx(): return norm(_mixs(thud(0.3), filt(noise(0.15, 10), 'bandpass', [1000, 5000]) * np.exp(-T(0.15) * 40) * 0.6), 0.85)
def chatter(d=3.0, seed=1):
    out = np.zeros(int(d * SR)); rng = random.Random(seed); x = 0.0
    while x < d - 0.3:
        L = rng.uniform(0.15, 0.4); t = T(L); f0 = rng.uniform(140, 260)
        v = osc(f0 * (1 + 0.1 * np.sin(2 * np.pi * 4 * t)), L, 'saw'); v = filt(v, 'bandpass', [rng.uniform(400, 900), rng.uniform(1400, 2600)])
        _place(out, v * np.sin(np.pi * t / L) * 0.25, x); x += rng.uniform(0.05, 0.3)
    return filt(out, 'lowpass', 2500) * 0.6
def bubble_pop(): return pop(0.07, 1200, 700) * 0.6

# ---------- emotional film scoring ----------
def music_piano(d, mood='sad', bpm=66, seed=9, strings=True):
    """Felt-piano film score: slow broken chords + sparse melody + soft string pad. mood: 'sad' | 'warm' | 'rise'."""
    prog = {'sad': ('Am', 'F', 'C', 'G'), 'warm': ('F', 'C', 'G', 'Am'), 'rise': ('Am', 'F', 'C', 'G')}[mood]
    out = np.zeros(int(d * SR) + 4 * SR); b = 60 / bpm; rng = random.Random(seed); t = 0.0; bar = 0; scale = [0, 2, 4, 5, 7, 9, 11]
    while t < d:
        ch = CHORDS[prog[bar % 4]]; k = t / max(d, 1e-6); vel = 0.35 + (0.3 * k if mood == 'rise' else 0)
        for i, m in enumerate([ch[0] - 12, ch[1], ch[2], ch[1] + 12, ch[2], ch[1]]):
            _place(out, filt(piano(m, 2.6, vel * (0.8 if i else 1.0)), 'lowpass', 2600), t + i * b * 0.66)
        if rng.random() < 0.7: _place(out, filt(piano(72 + rng.choice(scale), 2.4, vel * 0.9), 'lowpass', 3500), t + b * rng.choice((0, 1, 2)))
        if strings: _place(out, pad([m - 12 for m in ch] + [ch[0]], 4 * b + 1.5, 0.22 + (0.3 * k if mood == 'rise' else 0.08), 1100), t)
        t += 4 * b; bar += 1
    return norm(reverb(out[:int(d * SR)], 3.0, 0.35)[:int(d * SR)], 0.7)
def wind(d, seed=3, gust=0.3):
    t = T(d); x = sweep_lp(noise(d, seed), 300, 700) * (0.6 + gust * np.sin(2 * np.pi * 0.15 * t + seed)) ; return norm(x, 0.5)
def birdsong(d, seed=4, n=6):
    out = np.zeros(int(d * SR)); rng = random.Random(seed)
    for i in range(n):
        at = rng.uniform(0, d - 0.6); L = rng.uniform(0.08, 0.18); tt = T(L); f0 = rng.uniform(2500, 4200)
        ch = np.sin(2 * np.pi * np.cumsum(f0 + 900 * np.sin(2 * np.pi * rng.uniform(15, 30) * tt)) / SR) * np.sin(np.pi * tt / L) * 0.25
        for r in range(rng.randint(1, 3)): _place(out, ch, at + r * (L + 0.05))
    return out
def heartbeat(n=2, bpm=60, v=0.6):
    out = np.zeros(int((n * 60 / bpm + 0.5) * SR))
    for i in range(n):
        for off, g in ((0, 1.0), (0.22, 0.7)):
            t = T(0.25); _place(out, np.sin(2 * np.pi * np.cumsum(60 + 30 * np.exp(-t * 20)) / SR) * np.exp(-t * 18) * g * v, i * 60 / bpm + off)
    return out
def grass_step(seed=0): return filt(noise(0.14, seed), 'bandpass', [300, 3000]) * np.exp(-T(0.14) * 28) * 0.5


# ---------- kids lesson scoring ----------
def music_box(d, bpm=72, seed=11, prog=('Am', 'F', 'C', 'G')):
    """Soft music-box loop (night, 'something is not right' but never scary)."""
    out = np.zeros(int(d * SR) + 2 * SR); b = 60 / bpm; t = 0.0; bar = 0; rng = random.Random(seed)
    while t < d:
        ch = CHORDS[prog[bar % 4]]
        for i, m in enumerate([ch[0] + 24, ch[1] + 24, ch[2] + 24, ch[1] + 24, ch[2] + 24, ch[0] + 36]):
            _place(out, filt(pluck(m, 0.9, 0.35), 'lowpass', 5000), t + i * b * 0.66)
        _place(out, pad([m - 12 for m in ch], 4 * b + 1, 0.12, 900), t); t += 4 * b; bar += 1
    return norm(reverb(out[:int(d * SR)], 2.2, 0.3)[:int(d * SR)], 0.6)
def music_play(d, bpm=118, seed=12, prog=('C', 'G', 'Am', 'F')):
    """Bright, bouncy kids bed: marimba hook, plucked bass, claps and shaker."""
    out = np.zeros(int(d * SR) + 2 * SR); b = 60 / bpm; t = 0.0; bar = 0; rng = random.Random(seed)
    hook = [0, 4, 7, 9, 7, 4, 2, 4]
    while t < d:
        ch = CHORDS[prog[bar % 4]]
        for i in range(8):
            at = t + i * b / 2
            _place(out, marimba(ch[0] + 12 + hook[i] - (0 if hook[i] < 8 else 12), 0.4, 0.5), at)
            _place(out, hat(0.5 if i % 2 else 0.25), at)
        for i in range(4):
            _place(out, bass(ch[0] - 12 + (7 if i == 2 else 0), 0.3, 0.7), t + i * b)
            if i % 2: _place(out, clap(0.45), t + i * b)
            else: _place(out, kick(0.5), t + i * b)
        t += 4 * b; bar += 1
    return norm(out[:int(d * SR)], 0.65)
def swipe(seed=0): return _mixs(whoosh(0.18, 1500, 6000, seed) * 0.5, click() * 0.4)
def ball_kick(): return norm(_mixs(thud(0.25) * 0.8, pop(0.06, 500, 200)), 0.7)
def yawn(d=1.4):
    t = T(d); f = 260 + 120 * np.sin(np.pi * t / d); x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.6 * filt(noise(d, 9), 'bandpass', [400, 2500])
    return filt(x, 'lowpass', 1800) * np.sin(np.pi * t / d) ** 1.5 * 0.35


# ---------- story-short SFX ----------
def clink(seed=0, v=0.6):
    """Glass marble dropping into a glass jar: bright inharmonic partials + a second smaller bounce."""
    rng = random.Random(seed); out = np.zeros(int(0.9 * SR))
    for at, g in ((0, 1.0), (0.11 + rng.uniform(0, 0.03), 0.45), (0.19 + rng.uniform(0, 0.03), 0.2)):
        t = T(0.5); f0 = rng.uniform(2300, 3100); x = sum(np.sin(2 * np.pi * f0 * k * t) * np.exp(-t * (18 + 10 * k)) / k for k in (1, 2.76, 5.4))
        _place(out, x * g, at)
    return norm(out, v)
def whistle(d=0.7):
    t = T(d); f = 2900 + 120 * np.sign(np.sin(2 * np.pi * 34 * t)); x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * filt(noise(d, 4), 'bandpass', [2500, 3500])
    return norm(x * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.06), 0.55)
def crowd(d=3.0, seed=2, swell=1.0):
    """Cheering crowd: band-passed noise bed + many short 'hey' formant blips + claps."""
    rng = random.Random(seed); t = T(d); bed = filt(noise(d, seed), 'bandpass', [300, 2600]) * (0.5 + 0.5 * np.minimum(1, t / 0.4)) * 0.5
    out = bed.copy()
    for i in range(int(40 * d)):
        L = rng.uniform(0.15, 0.4); tt = T(L); f = rng.uniform(220, 520)
        v = np.sin(2 * np.pi * np.cumsum(f + 60 * np.sin(np.pi * tt / L)) / SR) * np.sin(np.pi * tt / L) * rng.uniform(0.05, 0.15)
        _place(out, filt(v, 'bandpass', [400, 3000]), rng.uniform(0, d - L))
    for i in range(int(25 * d)): _place(out, clap(rng.uniform(0.1, 0.3)), rng.uniform(0, d - 0.3))
    return norm(out, 0.7) * swell
def pant(n=4, rate=1.6, v=0.5):
    out = np.zeros(int((n / rate + 0.5) * SR))
    for i in range(n):
        for inh, L in ((True, 0.22), (False, 0.28)):
            tt = T(L); x = filt(noise(L, i * 2 + inh), 'bandpass', [500, 2200] if inh else [300, 1500]) * np.sin(np.pi * tt / L) ** 2
            _place(out, x * (0.6 if inh else 1.0), i / rate + (0 if inh else 0.26))
    return norm(out, v)
def beep(f=880, d=0.18): t = T(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.005) * np.exp(-t * 6) * 0.5
def tape_snap(): return norm(_mixs(filt(noise(0.08, 11), 'highpass', 1500) * np.exp(-T(0.08) * 60), pop(0.05, 700, 300)), 0.6)
