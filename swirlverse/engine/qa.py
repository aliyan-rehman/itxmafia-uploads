"""Quality gate. Run before ANY upload:  python3 qa.py <video.mp4> <thumb.png> <meta.json> [short|long]
Exit code 0 = pass. Prints a JSON report. Also writes <video>_sheet.png (contact sheet) that the agent MUST look at."""
import sys, json, subprocess, re, os

def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)

def probe(path):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height,r_frame_rate', '-of', 'json', path])
    return json.loads(r.stdout)

def main(video, thumb, meta_path, kind='short'):
    meta = json.load(open(meta_path)); fails = []; info = {}
    p = probe(video); dur = float(p['format']['duration']); info['duration'] = round(dur, 2)
    v = [s for s in p['streams'] if s['codec_type'] == 'video']; a = [s for s in p['streams'] if s['codec_type'] == 'audio']
    if not v: fails.append('no video stream')
    if not a: fails.append('no audio stream')
    if v:
        w, h = v[0]['width'], v[0]['height']; info['size'] = f'{w}x{h}'
        if kind == 'short' and (w, h) != (1080, 1920): fails.append(f'short must be 1080x1920, got {w}x{h}')
        if kind == 'long' and (w, h) != (1920, 1080): fails.append(f'long must be 1920x1080, got {w}x{h}')
    if kind == 'short' and not (15 <= dur <= 59.5): fails.append(f'short duration {dur:.1f}s not in 15-59.5 s')
    if kind == 'long' and not (120 <= dur <= 300): fails.append(f'long duration {dur:.1f}s not in 2-5 min')
    # loudness
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr); TP = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r.stderr)
    if I:
        info['lufs'] = float(I[-1])
        if not (-16.0 <= info['lufs'] <= -12.0): fails.append(f"loudness {info['lufs']} LUFS outside -16..-12")
    else: fails.append('could not measure loudness')
    if TP:
        info['true_peak'] = float(TP[-1])
        if info['true_peak'] > -0.5: fails.append(f"true peak {info['true_peak']} dBFS too hot")
    # black / frozen frames
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-vf', 'blackdetect=d=0.5:pix_th=0.06,freezedetect=n=0.002:d=4', '-an', '-f', 'null', '-'])
    blacks = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', r.stderr)
    bad_black = [b for b in blacks if float(b[0]) < dur - 0.8]
    if bad_black: fails.append(f'black frames at {bad_black}')
    if 'freeze_start' in r.stderr: fails.append('frozen picture for 4+ s: ' + ','.join(re.findall(r'freeze_start: ([\d.]+)', r.stderr)))
    # silence in the middle (voice dropout)
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-af', 'silencedetect=n=-45dB:d=2.5', '-f', 'null', '-'])
    sil = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    sil = [s for s in sil if 1.0 < s < dur - 3.0]
    if sil: fails.append(f'2.5 s+ of silence at {sil}')
    # thumbnail
    if not os.path.exists(thumb): fails.append('thumbnail missing')
    else:
        sz = os.path.getsize(thumb); info['thumb_bytes'] = sz
        if sz >= 2_000_000: fails.append('thumbnail must be < 2 MB')
        from PIL import Image
        tw, th = Image.open(thumb).size; info['thumb_size'] = f'{tw}x{th}'
        if tw < 640: fails.append('thumbnail too small')
    # metadata
    t = meta.get('title', ''); d = meta.get('description', ''); tags = meta.get('tags', [])
    if not t or len(t) > 100: fails.append('title empty or > 100 chars')
    if '<' in t or '>' in t or '<' in d or '>' in d: fails.append('no < or > allowed in title/description')
    if len(d) > 4900: fails.append('description too long')
    if sum(len(x) + 3 for x in tags) > 480: fails.append('tags too long (500 char limit)')
    if kind == 'short' and '#shorts' not in d.lower(): fails.append('short description should contain #shorts')
    if meta.get('made_for_kids') not in (False, 'false'): fails.append('made_for_kids must be false')
    # contact sheet for the visual check
    sheet = video.rsplit('.', 1)[0] + '_sheet.png'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-vf', f"fps={12/dur:.4f},scale={270 if kind == 'short' else 480}:-1,tile=6x2", '-frames:v', '1', sheet])
    info['sheet'] = sheet
    rep = dict(ok=not fails, fails=fails, info=info)
    print(json.dumps(rep, indent=1)); return 0 if not fails else 1

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
