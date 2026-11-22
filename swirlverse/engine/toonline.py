"""Swirlverse sitcom-toon look: flat fills, hard shadows, thick boiling outlines of constant screen width.
World points go through a 2D camera (cx, cy, zoom) to the screen, then get resampled and wobbled
(3 boil drawings cycling at 12 fps). Line width never scales with zoom."""
import math, cairo, numpy as np

LINE = (0x1b/255, 0x14/255, 0x22/255)
W, H = 1080, 1920

def hexc(h, a=1.0):
    h = h.lstrip('#'); return (int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255, a)

def mixc(a, b, k):
    A, B = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(round((A[i]*(1-k) + B[i]*k)*255)) for i in range(3))

def ellipse_pts(cx, cy, rx, ry, n=48, a0=0, a1=2*math.pi):
    return [(cx + rx*math.cos(a0+(a1-a0)*i/n), cy + ry*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]

def rect(x, y, w, h): return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]

def star(cx, cy, r1, r2, n, rot=0):
    return [(cx + (r1 if i%2==0 else r2)*math.cos(rot+i*math.pi/n), cy + (r1 if i%2==0 else r2)*math.sin(rot+i*math.pi/n)) for i in range(2*n)]

def resample(pts, step=7.0, closed=True):
    P = list(pts) + ([pts[0]] if closed else [])
    out = []
    for (x0,y0),(x1,y1) in zip(P[:-1], P[1:]):
        d = math.hypot(x1-x0, y1-y0); k = max(1, int(d/step))
        for i in range(k): out.append((x0+(x1-x0)*i/k, y0+(y1-y0)*i/k))
    if not closed: out.append(P[-1])
    return out

_rngcache = {}
def boil(pts, seed, amp=1.8, closed=True):
    R = resample(pts, 7, closed); n = len(R)
    if n < 3: return R
    key = seed % 5000
    if key not in _rngcache:
        rng = np.random.default_rng(key); _rngcache[key] = (rng.uniform(0, 6.28, 3), rng.uniform(0.15, 0.35, 3))
    ph, fr = _rngcache[key]
    A = np.array(R); prev = np.roll(A, 1, 0); nxt = np.roll(A, -1, 0)
    if not closed: prev[0] = A[0]; nxt[-1] = A[-1]
    tg = nxt - prev; L = np.hypot(tg[:,0], tg[:,1]) + 1e-9
    nx, ny = -tg[:,1]/L, tg[:,0]/L
    i = np.arange(n)
    o = amp*(np.sin(i*fr[0]+ph[0]) + np.sin(i*fr[1]+ph[1]) + np.sin(i*fr[2]+ph[2]))/2.2
    return list(zip(A[:,0]+nx*o, A[:,1]+ny*o))

class Toon:
    def __init__(self, c, t, cam=(540, 960, 1.0), fps_draw=12, shake=(0, 0)):
        self.c = c; self.frame = int(t*fps_draw) % 3; self.uid = 0
        self.cx, self.cy, self.z = cam; self.shake = shake
    def xf(self, p):
        return ((p[0]-self.cx)*self.z + W/2 + self.shake[0], (p[1]-self.cy)*self.z + H/2 + self.shake[1])
    def X(self, pts): return [self.xf(p) for p in pts]
    def _path(self, pts, closed=True):
        c = self.c; c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        if closed: c.close_path()
    def shape(self, pts, fill, shadow=None, shade_dir=(1, 0.4), shade_w=0.35, lw=8, line=True, closed=True, seed=None, alpha=1.0, amp=1.8, screen=False):
        c = self.c; self.uid += 1
        sp = pts if screen else self.X(pts)
        sd = (seed if seed is not None else self.uid*7919) + self.frame*104729
        bp = boil(sp, sd, amp=amp, closed=closed) if amp > 0 else resample(sp, 7, closed)
        if len(bp) < 2: return
        if fill and closed:
            self._path(bp); c.set_source_rgba(*hexc(fill, alpha))
            if shadow: c.fill_preserve()
            else: c.fill()
            if shadow:
                c.save(); c.clip()
                xs=[p[0] for p in sp]; ys=[p[1] for p in sp]
                w = max(xs)-min(xs); h = max(ys)-min(ys); dx, dy = shade_dir
                ox, oy = -dx*w*shade_w, -dy*h*shade_w*0.6
                c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
                c.rectangle(min(xs)-w-50, min(ys)-h-50, 3*w+100, 3*h+100)
                self._path([(x+ox, y+oy) for x,y in boil(sp, sd+1, amp=1.2)])
                c.set_source_rgba(*hexc(shadow, alpha)); c.fill(); c.restore()
                c.set_fill_rule(cairo.FILL_RULE_WINDING)
        if line and lw > 0:
            self._path(bp, closed); c.set_source_rgba(*LINE, alpha); c.set_line_width(lw)
            c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    def stroke(self, pts, lw=8, col=None, seed=None, alpha=1.0, screen=False):
        self.uid += 1
        sp = pts if screen else self.X(pts)
        bp = boil(sp, (seed if seed is not None else self.uid*31) + self.frame*7, closed=False)
        self._path(bp, False)
        self.c.set_source_rgba(*(hexc(col, alpha) if col else (*LINE, alpha))); self.c.set_line_width(lw)
        self.c.set_line_cap(cairo.LINE_CAP_ROUND); self.c.set_line_join(cairo.LINE_JOIN_ROUND); self.c.stroke()
    def flat(self, pts, col, alpha=1.0):
        """fill only, no outline, no boil (sky bands, glows)"""
        self._path(self.X(pts)); self.c.set_source_rgba(*hexc(col, alpha)); self.c.fill()
    def glow(self, x, y, r, col, rings=((1.6, 0.10), (1.3, 0.16)), sy=1.0):
        X, Y = self.xf((x, y))
        for k, a in rings:
            self.c.save(); self.c.translate(X, Y); self.c.scale(1, sy)
            self.c.arc(0, 0, r*k*self.z, 0, 2*math.pi); self.c.restore()
            self.c.set_source_rgba(*hexc(col, a)); self.c.fill()
    def dot(self, x, y, r, col=None):
        X, Y = self.xf((x, y)); self.c.arc(X, Y, max(2.5, r*self.z), 0, 2*math.pi)
        self.c.set_source_rgba(*(hexc(col) if col else (*LINE, 1))); self.c.fill()

def noodle_pts(a, b, bend, w0, w1=None):
    """outline of a bent tube from a to b (world coords)"""
    w1 = w0 if w1 is None else w1
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L
    m = ((a[0]+b[0])/2 + nx*bend, (a[1]+b[1])/2 + ny*bend)
    cen = []
    for i in range(15):
        u = i/14
        cen.append(((1-u)**2*a[0]+2*(1-u)*u*m[0]+u*u*b[0], (1-u)**2*a[1]+2*(1-u)*u*m[1]+u*u*b[1]))
    Lp, Rp = [], []
    for i, (x, y) in enumerate(cen):
        p = cen[max(i-1, 0)]; q = cen[min(i+1, 14)]; tx, ty = q[0]-p[0], q[1]-p[1]; d = math.hypot(tx, ty) or 1
        w = (w0 + (w1-w0)*i/14)/2
        Lp.append((x - ty/d*w, y + tx/d*w)); Rp.append((x + ty/d*w, y - tx/d*w))
    # round caps
    ea = math.atan2(cen[-1][1]-cen[-2][1], cen[-1][0]-cen[-2][0])
    capb = [(b[0] + w1/2*math.cos(ea + math.pi/2 - k*math.pi/6), b[1] + w1/2*math.sin(ea + math.pi/2 - k*math.pi/6)) for k in range(7)]
    sa = math.atan2(cen[1][1]-cen[0][1], cen[1][0]-cen[0][0])
    capa = [(a[0] + w0/2*math.cos(sa - math.pi/2 - k*math.pi/6), a[1] + w0/2*math.sin(sa - math.pi/2 - k*math.pi/6)) for k in range(7)]
    return Lp + capb + Rp[::-1] + capa
