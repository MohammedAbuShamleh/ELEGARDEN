"""Seamless diamond checker tile (stone slabs + lawn) for the services ground plane.

Stone and grass textures are sampled from the Unsplash stone-path photo (assets/img/services.jpg)."""
import os
import numpy as np
import cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
S = 600

photo = np.asarray(Image.open(os.path.join(IMG, "services.jpg")).convert("RGB")).astype(np.float32)  # PIL: unicode-safe paths
h, w = photo.shape[:2]
hsv = cv2.cvtColor(photo.astype(np.uint8), cv2.COLOR_RGB2HSV)
green = (hsv[..., 0] > 28) & (hsv[..., 0] < 75) & (hsv[..., 1] > 70)

def tile_from(mask, want, seed):
    """Pick the S×S window richest in `mask` and return it as texture."""
    rng = np.random.default_rng(seed)
    best, best_score = None, -1
    for _ in range(400):
        x, y = rng.integers(0, w - S), rng.integers(0, h - S)
        score = mask[y:y + S, x:x + S].mean() if want else 1 - mask[y:y + S, x:x + S].mean()
        if score > best_score:
            best, best_score = (x, y), score
    x, y = best
    return photo[y:y + S, x:x + S].copy(), best_score

stone, _ = tile_from(green, False, 1)
grass, _ = tile_from(green, True, 2)

# normalise: stone -> cool grey with its own grain, grass -> even green with its own blades
def regrade(tex, target, keep=0.85):
    g = cv2.GaussianBlur(tex, (0, 0), 25)
    detail = tex - g
    return np.clip(np.array(target, np.float32) + detail * keep, 0, 255)

stone = regrade(stone, (112, 110, 104), 0.9)
grass = regrade(grass, (60, 82, 42), 1.1)

yy, xx = np.mgrid[:S, :S].astype(np.float32)
c = S / 2
d = np.abs(xx - c) + np.abs(yy - c)            # diamond distance
edge = c - 16                                    # lawn joint
mask = np.clip((edge - d) / 3.0, 0, 1)[..., None]
bevel = np.clip((edge - d) / 22.0, 0, 1)[..., None]
stone_lit = stone * (0.72 + 0.28 * bevel)
out = grass * (1 - mask) + stone_lit * mask
# soft contact shadow on the lawn next to each slab
shadow = np.clip(1 - np.abs(d - edge - 6) / 14.0, 0, 1)[..., None] * (1 - mask)
out *= 1 - 0.35 * shadow

Image.fromarray(out.astype(np.uint8)).save(os.path.join(IMG, "ground.jpg"), quality=84)
print("ground.jpg", out.shape)
