"""Build the transparent cut-outs (plants, compass, sketch) from the Unsplash sources."""
import os, sys, urllib.request
import numpy as np
import cv2
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "src")
IMG = os.path.join(ROOT, "assets", "img")

_session = None
def rembg_alpha(rgb):
    """Alpha matte (0..1 float) from rembg / isnet."""
    global _session
    from rembg import remove, new_session
    if _session is None:
        _session = new_session("isnet-general-use")
    out = remove(Image.fromarray(rgb), session=_session, only_mask=True)
    return np.asarray(out).astype(np.float32) / 255.0

def load(name):
    return np.asarray(Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB"))

def smooth(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)

def sat_alpha(rgb, lo=0.12, hi=0.28):
    """Key leaves off a pale, desaturated backdrop (drops grey shadows too)."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    s, v = hsv[..., 1] / 255, hsv[..., 2] / 255
    a = smooth(s, lo, hi)
    a = np.maximum(a, smooth(1 - v, 0.55, 0.75))  # very dark stems
    return a

def keep_big(alpha, min_frac=0.01):
    m = (alpha > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        return alpha
    big = stats[1:, cv2.CC_STAT_AREA].max()
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= big * min_frac
    mask = keep[lab].astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    return alpha * mask

def decontaminate(rgb, alpha, bg):
    a = alpha[..., None]
    f = rgb.astype(np.float32)
    out = (f - (1 - a) * np.array(bg, np.float32)) / np.maximum(a, 0.05)
    out = np.where(a > 0.98, f, out)
    return np.clip(out, 0, 255).astype(np.uint8)

def save(rgb, alpha, name, max_side, quality=86):
    a8 = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    im = Image.fromarray(np.dstack([rgb, a8]), "RGBA")
    bbox = im.getchannel("A").point(lambda p: 255 if p > 8 else 0).getbbox()
    im = im.crop(bbox)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    path = os.path.join(IMG, name + ".webp")
    im.save(path, "WEBP", quality=quality, method=6)
    print(f"{name:12s} {im.size}  {os.path.getsize(path)//1024} KB")
    return im

def bg_color(rgb):
    border = np.concatenate([rgb[:20].reshape(-1, 3), rgb[-20:].reshape(-1, 3), rgb[:, :20].reshape(-1, 3), rgb[:, -20:].reshape(-1, 3)])
    return np.median(border, axis=0)

# ---------------------------------------------------------------- builders
def leaves_like(name, out, max_side, lo=0.12, hi=0.28, rotate=0, flip=False):
    rgb = load(name)
    a = keep_big(sat_alpha(rgb, lo, hi), 0.02)
    a = cv2.GaussianBlur(a, (3, 3), 0)
    rgb = decontaminate(rgb, a, bg_color(rgb))
    if rotate or flip:
        im = Image.fromarray(np.dstack([rgb, (a * 255).astype(np.uint8)]), "RGBA")
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if rotate:
            im = im.rotate(rotate, Image.BICUBIC, expand=True)
        arr = np.asarray(im)
        rgb, a = arr[..., :3], arr[..., 3] / 255.0
    return save(rgb, a, out, max_side)

def organic_fade(a, start, span, seed=7):
    """Fade alpha toward the bottom along a wobbly line, so a photo's crop edge never reads as a straight cut."""
    h, w = a.shape
    yy = np.mgrid[:h, :w][0].astype(np.float32)
    rng = np.random.default_rng(seed)
    wob = cv2.resize(cv2.GaussianBlur(rng.random((h // 30 + 2, w // 30 + 2)).astype(np.float32), (3, 3), 0), (w, h), interpolation=cv2.INTER_CUBIC)
    return a * smooth(h * start - yy + (wob - 0.5) * h * 0.06, 0, h * span)

def bonsai():
    rgb = load("bonsai")
    a = rembg_alpha(rgb)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    white = smooth(hsv[..., 2] / 255, 0.80, 0.92) * (1 - smooth(hsv[..., 1] / 255, 0.08, 0.20))
    a = a * (1 - white)                               # backdrop showing through the branches
    a = np.where(a < 0.08, 0, a)                      # drop faint halo specks
    a = keep_big(a, 0.01)
    rgb = decontaminate(rgb, a, (255, 255, 255))
    a = organic_fade(a, 0.90, 0.16)                   # trunk / lower pad leave the frame in the source photo
    save(rgb, a, "bonsai", 1100)

def sphere():
    rgb = load("sphere")
    h, w = rgb.shape[:2]
    cx, cy, r = 944, 643, 404
    a = rembg_alpha(rgb)
    yy, xx = np.mgrid[:h, :w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    circle = smooth(r * 1.03 - d, 0, r * 0.04)
    # cut the trunk / lawn below the ball
    circle *= np.where(yy > cy + r * 0.80, smooth(r * 0.97 - d, 0, r * 0.06), 1)
    a = np.minimum(np.maximum(a, smooth(r * 0.9 - d, 0, 20)), circle)
    # paint out the tiny white/yellow blossoms so it reads as dense boxwood
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    speck = smooth(v, 0.42, 0.66) * np.maximum(1 - smooth(s, 0.28, 0.55), ((hue > 18) & (hue < 38)).astype(np.float32))
    speck = cv2.GaussianBlur(cv2.dilate(speck, np.ones((3, 3), np.uint8)), (5, 5), 0)
    tinted = hsv.copy()
    tinted[..., 0] = 44 + (hsv[..., 0] % 6)
    tinted[..., 1] = np.maximum(hsv[..., 1], 150)
    tinted[..., 2] = hsv[..., 2] * 0.66
    tinted = cv2.cvtColor(tinted.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
    rgb = rgb.astype(np.float32) * (1 - speck[..., None]) + tinted * speck[..., None]
    hsv = cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 0] = np.clip(hsv[..., 0] + 4, 0, 179)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.18, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.86, 0, 255)
    rgb = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    # gentle 3-D shading: darker rim, lighter upper-left
    f = rgb.astype(np.float32) / 255
    nd = np.clip(d / r, 0, 1)
    light = 1.05 - 0.55 * nd ** 2.4
    tl = np.clip(((cx - xx) + (cy - yy)) / (2 * r), -1, 1)
    light *= 1 + 0.10 * tl
    f = np.clip(f * light[..., None], 0, 1)
    f[..., 1] = np.clip(f[..., 1] * 1.02, 0, 1)
    rgb = (f * 255).astype(np.uint8)
    rgb = rgb[cy - r - 40: cy + r + 40, cx - r - 40: cx + r + 40]
    a = a[cy - r - 40: cy + r + 40, cx - r - 40: cx + r + 40]
    save(rgb, a, "sphere", 760)

def plumeria():
    rgb = load("plumeria")[150:1080, 640:1560]
    a = rembg_alpha(rgb)
    m = cv2.morphologyEx((a > 0.4).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    filled = m.copy()
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(filled, cnts, -1, 1, -1)
    a = np.maximum(a, cv2.GaussianBlur(cv2.erode(filled, np.ones((9, 9), np.uint8)).astype(np.float32), (7, 7), 0))
    a = keep_big(a, 0.3)
    save(rgb, a, "plumeria", 700)
def compass():
    path = os.path.join(SRC, "compass2.jpg")
    if not os.path.exists(path):
        url = "https://images.unsplash.com/photo-1605066902012-ba3ed05b8a2c?w=2600&q=85&fm=jpg"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    rgb = load("compass2")
    a = rembg_alpha(rgb)
    # two objects in frame (compass + yellow pen): keep the one on the left
    n, lab, stats, cent = cv2.connectedComponentsWithStats((a > 0.35).astype(np.uint8), 8)
    order = sorted(range(1, n), key=lambda i: -stats[i, cv2.CC_STAT_AREA])[:2]
    pick = min(order, key=lambda i: cent[i][0])
    keep = cv2.dilate((lab == pick).astype(np.uint8), np.ones((15, 15), np.uint8))
    a = a * keep
    im = Image.fromarray(np.dstack([rgb, (a * 255).astype(np.uint8)]), "RGBA")
    im = im.crop(im.getchannel("A").point(lambda p: 255 if p > 8 else 0).getbbox())
    im = im.rotate(-8, Image.BICUBIC, expand=True)
    arr = np.asarray(im)
    save(arr[..., :3], arr[..., 3] / 255.0, "compass", 900)
def niwaki():
    """Cloud-pruned tree shot against the sky; the trunk exits the frame, so it is faded out organically."""
    path = os.path.join(SRC, "niwaki.jpg")
    if not os.path.exists(path):
        url = "https://images.unsplash.com/photo-1604646291954-edcec5c8e652?w=1700&q=85&fm=jpg"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    rgb = load("niwaki")
    h, w = rgb.shape[:2]
    a = rembg_alpha(rgb)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    sky = ((hue > 90) & (hue < 130) & (s > 0.12)).astype(np.float32)          # blue sky
    sky = np.maximum(sky, smooth(v, 0.80, 0.92) * (1 - smooth(s, 0.10, 0.22)))  # white cloud
    foliage = ((hue > 25) & (hue < 85) & (s > 0.25)).astype(np.float32)
    a = np.clip(np.maximum(a * (1 - sky), foliage * (a > 0.15)), 0, 1)
    a = cv2.GaussianBlur(a, (3, 3), 0)
    a = keep_big(a, 0.02)
    # organic fade along the bottom so no straight crop edge shows
    yy, xx = np.mgrid[:h, :w].astype(np.float32)
    rng = np.random.default_rng(7)
    wob = cv2.GaussianBlur(rng.random((h // 40 + 1, w // 40 + 1)).astype(np.float32), (3, 3), 0)
    wob = cv2.resize(wob, (w, h), interpolation=cv2.INTER_CUBIC)
    a *= smooth(h * 0.965 - yy + (wob - 0.5) * h * 0.05, 0, h * 0.12)
    rgb = decontaminate(rgb, a, (205, 222, 240))
    save(rgb, a, "niwaki", 1200)

def sketch():
    rgb = load("sketch")
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    inv = 255 - g
    blur = cv2.GaussianBlur(inv, (0, 0), 6)
    dodge = cv2.divide(g, 255 - blur, scale=256)
    lines = 1 - np.clip(dodge / 255.0, 0, 1)
    edges = cv2.Canny(cv2.GaussianBlur(g, (5, 5), 0), 40, 110) / 255.0
    a = np.clip(lines * 1.6 + edges * 0.55, 0, 1)
    a = smooth(a, 0.08, 0.7)
    h, w = a.shape
    yy, xx = np.mgrid[:h, :w]
    fade = np.clip(1.25 - np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2), 0, 1)
    a *= fade
    col = np.zeros_like(rgb); col[...] = (92, 84, 72)
    save(col, a, "sketch", 1800, quality=80)

def inner_scene():
    im = Image.open(os.path.join(SRC, "..", "..", "assets", "img", "fog.jpg")).convert("RGB")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2 + s // 6, (h - s) // 2, (w - s) // 2 + s // 6 + s * 2 // 3, (h - s) // 2 + s * 2 // 3))
    im = im.resize((520, 520), Image.LANCZOS)
    im.save(os.path.join(IMG, "ring-scene.jpg"), quality=82)
    print("ring-scene  (520,520)")

JOBS = {
    "leaves": lambda: leaves_like("leaves", "leaves", 1300),
    "vine": lambda: leaves_like("vine", "vine", 1400, 0.14, 0.30),
    "sprout": lambda: leaves_like("sprout", "sprout", 600, 0.12, 0.26),
    "eucalyptus": lambda: leaves_like("eucalyptus", "eucalyptus", 1100, 0.06, 0.16),
    "bonsai": bonsai, "sphere": sphere, "plumeria": plumeria, "compass": compass,
    "sketch": sketch, "inner": inner_scene, "niwaki": niwaki,
}

if __name__ == "__main__":
    for job in (sys.argv[1:] or JOBS):
        JOBS[job]()
