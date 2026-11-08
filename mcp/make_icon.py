"""وێنۆچکەی کوردیی پەتی: ئاڵای کوردستان و خۆری ٢١ تیشک.

python make_icon.py  ->  favicon.ico, icon.png, icon.svg
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).parent
RED, WHITE, GREEN, SUN = "#ED2024", "#FFFFFF", "#278E43", "#FEBD11"
RAYS = 21


def sun_points(cx, cy, r_in, r_out):
    pts = []
    for i in range(RAYS * 2):
        a = math.pi * i / RAYS - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def png(size=512):
    s = 4  # supersample for smooth edges
    n = size * s
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1], radius=n // 5, fill=255)
    flag = Image.new("RGBA", (n, n))
    d = ImageDraw.Draw(flag)
    d.rectangle([0, 0, n, n / 3], fill=RED)
    d.rectangle([0, n / 3, n, 2 * n / 3], fill=WHITE)
    d.rectangle([0, 2 * n / 3, n, n], fill=GREEN)
    c = n / 2
    d.polygon(sun_points(c, c, n * 0.19, n * 0.30), fill=SUN)
    d.ellipse([c - n * 0.17, c - n * 0.17, c + n * 0.17, c + n * 0.17], fill=SUN)
    img.paste(flag, (0, 0), mask)
    return img.resize((size, size), Image.LANCZOS)


def svg():
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in sun_points(50, 50, 19, 30))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<clipPath id="r"><rect width="100" height="100" rx="20"/></clipPath><g clip-path="url(#r)">'
        f'<rect width="100" height="33.4" fill="{RED}"/><rect y="33.3" width="100" height="33.4" fill="{WHITE}"/>'
        f'<rect y="66.6" width="100" height="33.4" fill="{GREEN}"/>'
        f'<polygon points="{pts}" fill="{SUN}"/><circle cx="50" cy="50" r="17" fill="{SUN}"/></g></svg>'
    )


if __name__ == "__main__":
    big = png(512)
    big.save(HERE / "icon.png")
    big.save(HERE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])
    (HERE / "icon.svg").write_text(svg(), encoding="utf-8")
    print("icon.png, favicon.ico, icon.svg")
