"""Offline voices (Kokoro): Nova = bm_george (British male), Kiko = am_puck pitched up 2.5 semitones.
make_voice(lines, out_dir) -> writes vo.wav + timeline.json (line start/end, lip envelope at 24 Hz)."""
import os, json, subprocess, numpy as np, soundfile as sf
from scipy.signal import resample_poly, lfilter
SR = 48000
MODELS = os.path.expanduser('~/.swirl_models')
VOICES = {'NOVA': ('bm_george', 'en-gb', 1.0), 'KIKO': ('am_puck', 'en-us', 1.05)}

def _peq(x, f, g, q=1.0):
    A = 10**(g/40); w = 2*np.pi*f/SR; al = np.sin(w)/(2*q)
    b = [1 + al*A, -2*np.cos(w), 1 - al*A]; a = [1 + al/A, -2*np.cos(w), 1 - al/A]
    return lfilter(np.array(b)/a[0], np.array(a)/a[0], x)

def _comp(y, thr=0.25, ratio=3.0):
    env = np.sqrt(np.convolve(y**2, np.ones(480)/480, 'same')) + 1e-9
    g = np.where(env > thr, (thr*(env/thr)**(1/ratio))/env, 1.0)
    return y*np.convolve(g, np.ones(240)/240, 'same')

def make_voice(lines, out_dir, start=0.3):
    """lines: list of dicts {who, text, gap[, speed]} (gap = silence after the line, s)"""
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.int8.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
    raw = os.path.join(out_dir, 'raw'); os.makedirs(raw, exist_ok=True)
    t = start; parts = []; tl = []
    for i, l in enumerate(lines):
        v, lang, spd = VOICES[l['who']]
        a, sr = k.create(l['text'], voice=v, speed=l.get('speed', spd), lang=lang)
        p = os.path.join(raw, f'{i:02d}.wav'); sf.write(p, a, sr)
        if l['who'] == 'KIKO':
            r = 2**(2.5/12); q = os.path.join(raw, f'{i:02d}_p.wav')
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-af', f'asetrate={sr*r:.0f},aresample=48000,atempo={1/r:.5f}', '-ar', '48000', '-ac', '1', q], check=True)
            y, _ = sf.read(q)
        else:
            y = resample_poly(a, SR//sr if SR % sr == 0 else 2, 1) if sr != SR else a
        ab = np.abs(y); idx = np.where(ab > 0.01*ab.max())[0]; y = y[max(0, idx[0] - 480): idx[-1] + 2400]
        y = y/np.abs(y).max()*0.9
        y = _peq(y, 180, 2.0, 0.8) if l['who'] == 'NOVA' else y
        y = _peq(y, 3500 if l['who'] == 'NOVA' else 3200, 1.5 if l['who'] == 'NOVA' else 2.0, 0.9)
        y = _comp(y); y = y/np.abs(y).max()*0.9
        d = len(y)/SR; hop = SR//24; o = []
        for j in range(int(d*24) + 1):
            seg = y[j*hop:(j + 1)*hop]; o.append(float(np.sqrt((seg**2).mean())) if len(seg) else 0.0)
        pk = np.percentile(o, 95) + 1e-9; o = [round(float(np.clip((v/pk - 0.1)/0.8, 0, 1)), 2) for v in o]
        tl.append(dict(i=i, who=l['who'], text=l['text'], cap=l.get('cap', l['text']), ch=l.get('ch', 1), s=round(t, 3), e=round(t + d, 3), lip=o))
        parts.append((t, y)); t += d + l.get('gap', 0.35)
    total = round(t, 2)
    out = np.zeros(int(total*SR) + SR)
    for s0, y in parts: out[int(s0*SR):int(s0*SR) + len(y)] += y
    sf.write(os.path.join(out_dir, 'vo.wav'), out[:int(total*SR)].astype(np.float32), SR)
    json.dump(dict(total=total, lines=tl), open(os.path.join(out_dir, 'timeline.json'), 'w'))
    return total
