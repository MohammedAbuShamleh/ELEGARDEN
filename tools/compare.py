"""Full-page capture with headless Edge + side-by-side with the reference comp.

usage: python tools/compare.py <reference.jpg> [y0 y1]   (y in 1920-px page coordinates)
"""
import os, sys, subprocess, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "shots")
os.makedirs(OUT, exist_ok=True)
EDGE = next(p for p in [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    shutil.which("msedge") or "",
] if p and os.path.exists(p))

W, H = 1920, 4820

def capture(lang="ar"):
    shot = os.path.join(OUT, f"page_{lang}.png")
    shutil.rmtree(os.path.join(OUT, "profile"), ignore_errors=True)  # never reuse a cached CSS/JS
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=8000", f"--screenshot={shot}",
                    "--user-data-dir=" + os.path.join(OUT, "profile"), f"http://127.0.0.1:5190/?capture&lang={lang}"],
                   check=True, capture_output=True, timeout=120)
    return shot

def side_by_side(ref_path, y0=0, y1=None):
    page = Image.open(capture()).convert("RGB")
    ref = Image.open(ref_path).convert("RGB")
    ref = ref.resize((W, round(ref.height * W / ref.width)), Image.LANCZOS)
    y1 = y1 or max(page.height, ref.height)
    a, b = ref.crop((0, y0, W, y1)), page.crop((0, y0, W, y1))
    out = Image.new("RGB", (W * 2 + 20, y1 - y0), "red")
    out.paste(a, (0, 0)); out.paste(b, (W + 20, 0))
    scale = 1500 / out.width
    out = out.resize((1500, round(out.height * scale)), Image.LANCZOS)
    path = os.path.join(OUT, f"cmp_{y0}_{y1}.jpg")
    out.save(path, quality=86)
    print(path, page.size)

if __name__ == "__main__":
    ref = sys.argv[1]
    y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    y1 = int(sys.argv[3]) if len(sys.argv) > 3 else None
    side_by_side(ref, y0, y1)
