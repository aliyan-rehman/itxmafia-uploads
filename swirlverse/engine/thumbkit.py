"""Pro thumbnail toolkit: burst backgrounds, huge outlined text with a highlight word, arrows, circles.
Rules: 2-4 huge words, one highlighted, 1-2 BIG characters with exaggerated faces, one clear hero object,
max 3 colours fighting for attention. Text must be true to the video (curiosity, not lies).
Shorts: 1080x1920, keep text in the top 45% (bottom is covered by the Shorts UI). Long: 1280x720 or 1920x1080."""
import math, cairo, io
from toonline import hexc, LINE

def burst(c, W, H, cx, cy, c1, c2, rays=22, spin=0.0):
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, max(W, H)*0.9)
    g.add_color_stop_rgb(0, *hexc(c1)[:3]); g.add_color_stop_rgb(1, *hexc(c2)[:3])
    c.set_source(g); c.paint()
    R = max(W, H)*1.5
    for i in range(rays):
        a0 = spin + 2*math.pi*i/rays; a1 = a0 + math.pi/rays
        c.move_to(cx, cy); c.line_to(cx + R*math.cos(a0), cy + R*math.sin(a0)); c.line_to(cx + R*math.cos(a1), cy + R*math.sin(a1)); c.close_path()
        c.set_source_rgba(1, 1, 1, 0.07); c.fill()
    v = cairo.RadialGradient(W/2, H/2, min(W, H)*0.35, W/2, H/2, max(W, H)*0.8)
    v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, 0, 0, 0, 0.45)
    c.set_source(v); c.paint()

def big_text(c, words, x, y, size, col='#ffffff', hl=None, hl_col='#ffd43b', hl_box=None, rot=-0.04, max_w=None, align='center'):
    """words: one line of text. hl: word index to colour hl_col (or put on a box if hl_box colour given)."""
    c.save(); c.translate(x, y); c.rotate(rot)
    c.select_font_face('Luckiest Guy'); c.set_font_size(size)
    toks = words.split(' '); sp = c.text_extents(' ').x_advance*1.1
    widths = [c.text_extents(w).x_advance for w in toks]
    total = sum(widths) + sp*(len(toks) - 1)
    if max_w and total > max_w:
        k = max_w/total; size *= k; c.set_font_size(size); sp *= k; widths = [w*k for w in widths]; total = max_w
    cx = -total/2 if align == 'center' else 0
    asc = size*0.72
    for i, (w, wd) in enumerate(zip(toks, widths)):
        if hl == i and hl_box:
            pad = size*0.12
            c.rectangle(cx - pad, -asc - pad, wd + 2*pad, asc + 2*pad); c.set_source_rgba(*hexc(hl_box)); c.fill()
        # drop shadow
        c.move_to(cx + size*0.06, size*0.07); c.text_path(w); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
        c.move_to(cx, 0); c.text_path(w)
        c.set_source_rgb(*LINE); c.set_line_width(size*0.2); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgba(*hexc(hl_col if (hl == i and not hl_box) else col)); c.fill()
        cx += wd + sp
    c.restore()
    return size

def arrow(c, x0, y0, x1, y1, col='#ff2d55', w=34):
    """chunky curved arrow with outline"""
    mx, my = (x0 + x1)/2 + (y1 - y0)*0.25, (y0 + y1)/2 - (x1 - x0)*0.25
    for lw, cc in ((w + 18, LINE), (w, None)):
        c.move_to(x0, y0); c.curve_to(mx, my, mx, my, x1, y1)
        c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.set_source_rgb(*cc) if cc else c.set_source_rgba(*hexc(col)); c.stroke()
    a = math.atan2(y1 - my, x1 - mx); L = w*2.4
    pts = [(x1 + L*0.5*math.cos(a), y1 + L*0.5*math.sin(a)), (x1 + L*math.cos(a + 2.4), y1 + L*math.sin(a + 2.4)), (x1 + L*math.cos(a - 2.4), y1 + L*math.sin(a - 2.4))]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(9); c.stroke()

def ring(c, x, y, rx, ry, col='#ff2d55', w=16):
    c.save(); c.translate(x, y); c.scale(1, ry/rx); c.arc(0, 0, rx, 0, 2*math.pi); c.restore()
    c.set_line_width(w + 12); c.set_source_rgb(*LINE); c.stroke_preserve(); c.set_line_width(w); c.set_source_rgba(*hexc(col)); c.stroke()

def emoji_burst(c, x, y, r, txt, col='#ffd43b', rot=0.15):
    """starburst sticker with a short word ('!?', 'x10', 'NO WAY')"""
    c.save(); c.translate(x, y); c.rotate(rot)
    n = 14
    for i in range(2*n + 1):
        a = math.pi*i/n; rr = r if i % 2 == 0 else r*0.72
        (c.move_to if i == 0 else c.line_to)(rr*math.cos(a), rr*math.sin(a))
    c.close_path(); c.set_source_rgba(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(10); c.stroke()
    c.select_font_face('Luckiest Guy'); fs = r*0.62; c.set_font_size(fs)
    e = c.text_extents(txt)
    if e.x_advance > r*1.3: fs *= r*1.3/e.x_advance; c.set_font_size(fs); e = c.text_extents(txt)
    c.move_to(-e.x_advance/2, fs*0.36); c.text_path(txt); c.set_source_rgb(*LINE); c.set_line_width(fs*0.16); c.stroke_preserve(); c.set_source_rgb(1, 1, 1); c.fill()
    c.restore()

def save_png_under(surf, path, limit=1_900_000):
    """YouTube thumbnails must be < 2 MB: save PNG, quantize if needed."""
    surf.write_to_png(path)
    import os
    if os.path.getsize(path) <= limit: return path
    from PIL import Image
    im = Image.open(path).convert('RGB')
    for colors in (256, 128, 64):
        im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
        if os.path.getsize(path) <= limit: return path
    w, h = im.size
    im.resize((w*3//4, h*3//4)).quantize(colors=128).save(path, optimize=True)
    return path
