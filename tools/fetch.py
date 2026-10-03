"""Download the Unsplash photos used by the landing page (Unsplash License)."""
import os, urllib.request, concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
SRC = os.path.join(ROOT, "tools", "src")
os.makedirs(IMG, exist_ok=True)
os.makedirs(SRC, exist_ok=True)

# name -> (photo id, width, folder)
PHOTOS = {
    "hero":       ("photo-1728721529009-bfaab6fcc8e6", 2400, IMG),
    "contacts":   ("photo-1767025982130-4526af349ab4", 2000, IMG),
    "services":   ("photo-1759774314429-758cda4a2708", 2400, IMG),
    "fog":        ("photo-1754638994880-32c4e651a838", 2000, IMG),
    "project-1":  ("photo-1789144528441-0657974d294d", 900, IMG),
    "project-2":  ("photo-1685514823717-7e1ff6ee0563", 900, IMG),
    "project-3":  ("photo-1757361652977-218a1173e8d6", 900, IMG),
    "project-4":  ("photo-1698994705178-d244d73ea573", 900, IMG),
    "project-5":  ("photo-1767610077733-dfe810cc5308", 900, IMG),
    "project-6":  ("photo-1757361653037-dbf0d0a820ae", 900, IMG),
    "blog-1":     ("photo-1752776132465-39ff6d6d7132", 700, IMG),
    "blog-2":     ("photo-1713383659120-5d8013d3348a", 700, IMG),
    "blog-3":     ("photo-1705591935362-21fa1053195e", 700, IMG),
    "blog-4":     ("photo-1657793623447-13f47cddfa37", 700, IMG),
    "blog-5":     ("photo-1774799661763-99fef20dcdfe", 700, IMG),
    "blog-6":     ("photo-1609887943360-2f568680d389", 700, IMG),
    # sources for transparent cut-outs / sketch
    "bonsai":     ("photo-1765810655660-c3e907524d1e", 1800, SRC),
    "sphere":     ("photo-1745488176096-8936c2dcfecd", 1800, SRC),
    "plumeria":   ("photo-1762075959891-e3dd56fb5adf", 2400, SRC),
    "vine":       ("photo-1783699373767-9236bd7d262e", 2400, SRC),
    "leaves":     ("photo-1783699373449-b7c815bffbee", 2400, SRC),
    "sprout":     ("photo-1587334274328-64186a80aeee", 1400, SRC),
    "compass":    ("photo-1503789101408-444b37749472", 2400, SRC),
    "eucalyptus": ("photo-1592295880235-e276a337ddf1", 1800, SRC),
    "sketch":     ("photo-1748063578185-3d68121b11ff", 2000, SRC),
}

def get(item):
    name, (pid, w, folder) = item
    path = os.path.join(folder, name + ".jpg")
    if os.path.exists(path):
        return name, "cached"
    url = f"https://images.unsplash.com/{pid}?w={w}&q=82&fm=jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    open(path, "wb").write(data)
    return name, f"{len(data)//1024} KB"

if __name__ == "__main__":
    with cf.ThreadPoolExecutor(8) as ex:
        for name, info in ex.map(get, PHOTOS.items()):
            print(f"{name:12s} {info}")
