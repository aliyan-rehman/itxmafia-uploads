"""Build a Short from an episode file:  python3 build_short.py ../episodes/ep13_ice_sinks.py [stills|video|all]
Output folder: /tmp/swirl/<id>/  ->  <id>.mp4, <id>_thumb.png, meta.json, stills/*.png
Episode file defines: LINES (list of dicts who/text/gap), META (dict), shots(K) and thumbnail(c, K)."""
import sys, os, json, importlib.util, subprocess
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shortkit as SK
from voice import make_voice
from mixer import build_mix

def load(ep_path):
    spec = importlib.util.spec_from_file_location('episode', ep_path); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep); return ep

EP = None; K = None
def init(ep_path):
    global EP, K
    EP = load(ep_path); out = os.path.join('/tmp/swirl', EP.META['id']); os.makedirs(out, exist_ok=True)
    if not os.path.exists(os.path.join(out, 'timeline.json')):
        make_voice(EP.LINES, out)
    K = SK.Kit(out, EP.META); EP.shots(K); K.finalize(); return out

def frame(i): return bytes(K.render(i/SK.FPS).get_data())

def main(ep_path, mode='all'):
    out = init(ep_path)
    if mode in ('stills', 'all'):
        sd = os.path.join(out, 'stills'); os.makedirs(sd, exist_ok=True)
        for k, (t0, f) in enumerate(K.edl):
            t1 = K.edl[k + 1][0] if k + 1 < len(K.edl) else K.TOTAL
            K.render(min(t0 + 0.7, (t0 + t1)/2)).write_to_png(os.path.join(sd, f'{k:02d}_{t0:05.2f}.png'))
        print('stills ->', sd)
    if mode in ('video', 'all'):
        N = int(K.TOTAL*SK.FPS); vpath = os.path.join(out, 'video_noaudio.mp4')
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{SK.W}x{SK.H}', '-r', str(SK.FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', vpath], stdin=subprocess.PIPE)
        with Pool(os.cpu_count() or 2, initializer=init, initargs=(ep_path,)) as pool:
            for i, b in enumerate(pool.imap(frame, range(N), chunksize=6)):
                p.stdin.write(b)
                if i % 240 == 0: print('frame', i, '/', N, flush=True)
        p.stdin.close(); p.wait()
        wav = os.path.join(out, 'mix.wav')
        build_mix(K.TOTAL, os.path.join(out, 'vo.wav'), K.LINES, K.sfx + getattr(EP, 'EXTRA_SFX', []), wav, wipe_t=K.wipe_t, drops=getattr(EP, 'DROPS', []))
        final = os.path.join(out, EP.META['id'] + '.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vpath, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', final], check=True)
        print('video ->', final)
    if mode in ('thumb', 'video', 'all'):
        import cairo
        from thumbkit import save_png_under
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, SK.W, SK.H); c = cairo.Context(surf)
        EP.thumbnail(c, K)
        tp = os.path.join(out, EP.META['id'] + '_thumb.png'); save_png_under(surf, tp); print('thumb ->', tp)
        meta = {k: EP.META[k] for k in ('title', 'description', 'tags')}; meta['made_for_kids'] = False
        json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1)

if __name__ == '__main__':
    main(*sys.argv[1:])
