"""Build a LONG video (1920x1080):  python3 build_long.py ../episodes/long04_xxx.py [stills|video|thumb|all]
Episode defines: LINES (dicts with who/text/gap/ch, optional cap), META (id,title,description,tags), CHAPTERS {n: title},
shots(LK) -> (edl list of (t0, fn(T, t))), wipe_t, memory_t set), thumbnail(c, LK) drawing on 1920x1080, optional THINK=(ch_a, ch_b).
Chapter timestamps are appended to the description automatically (each chapter must be >= 10 s; QA checks it)."""
import sys, os, json, importlib.util, subprocess
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from voice import make_voice

EP = None; LK = None
def init(ep_path):
    global EP, LK
    spec = importlib.util.spec_from_file_location('ep_long_meta', ep_path); m = importlib.util.module_from_spec(spec)
    # first pass: we only need LINES/META to make the voice -> exec with longkit unavailable is not possible, so read via env flag
    os.environ['SV_LONG_META_ONLY'] = '1'
    src = open(ep_path).read()
    head = src.split('# ===== SHOTS =====')[0]
    ns = {}; exec(compile(head, ep_path, 'exec'), ns)
    out = os.path.join('/tmp/swirl', ns['META']['id']); os.makedirs(out, exist_ok=True)
    if not os.path.exists(os.path.join(out, 'timeline.json')):
        make_voice(ns['LINES'], out)
    os.environ['SV_LONG_DIR'] = out
    import longkit
    LK = longkit
    longkit.CHAPTERS.update(ns['CHAPTERS'])
    spec = importlib.util.spec_from_file_location('ep_long', ep_path); EP = importlib.util.module_from_spec(spec); spec.loader.exec_module(EP)
    edl, wipe_t, memory_t = EP.shots(longkit)
    longkit.set_edl(edl, wipe_t, memory_t)
    return out

def frame(i): return bytes(LK.render(i/LK.FPS).get_data())

def chapters_text():
    out = []
    for ch, t in sorted(LK.CH_START.items()):
        out.append(f"{int(t)//60}:{int(t) % 60:02d} {LK.CHAPTERS.get(ch, '')}")
    return '\n'.join(out)

def main(ep_path, mode='all'):
    out = init(ep_path)
    if mode in ('stills', 'all'):
        sd = os.path.join(out, 'stills'); os.makedirs(sd, exist_ok=True)
        for k, (t0, f) in enumerate(LK.EDL):
            t1 = LK.EDL[k + 1][0] if k + 1 < len(LK.EDL) else LK.TOTAL
            LK.render(min(t0 + 1.0, (t0 + t1)/2)).write_to_png(os.path.join(sd, f'{k:02d}_{t0:06.2f}.png'))
        print('stills ->', sd)
    if mode in ('video', 'all'):
        N = int(LK.TOTAL*LK.FPS); vpath = os.path.join(out, 'video_noaudio.mp4')
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{LK.W}x{LK.H}', '-r', str(LK.FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', vpath], stdin=subprocess.PIPE)
        with Pool(os.cpu_count() or 2, initializer=init, initargs=(ep_path,)) as pool:
            for i, b in enumerate(pool.imap(frame, range(N), chunksize=6)):
                p.stdin.write(b)
                if i % 480 == 0: print('frame', i, '/', N, flush=True)
        p.stdin.close(); p.wait()
        from mixer import build_mix
        think = None
        if getattr(EP, 'THINK', None):
            a, b = EP.THINK; think = (LK.CH_START[a], LK.CH_START[b])
        wav = os.path.join(out, 'mix.wav')
        build_mix(LK.TOTAL, os.path.join(out, 'vo.wav'), LK.LINES, getattr(EP, 'SFX', []), wav, wipe_t=LK.WIPE_T, drops=getattr(EP, 'DROPS', []), think=think)
        final = os.path.join(out, EP.META['id'] + '.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vpath, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', final], check=True)
        print('video ->', final)
    if mode in ('thumb', 'video', 'all'):
        import cairo
        from thumbkit import save_png_under
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 1920, 1080); c = cairo.Context(surf)
        EP.thumbnail(c, LK)
        tp = os.path.join(out, EP.META['id'] + '_thumb.png'); save_png_under(surf, tp); print('thumb ->', tp)
        desc = EP.META['description'].replace('{CHAPTERS}', chapters_text())
        meta = dict(title=EP.META['title'], description=desc, tags=EP.META['tags'], made_for_kids=False)
        json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1)
        print(chapters_text())

if __name__ == '__main__':
    main(*sys.argv[1:])
