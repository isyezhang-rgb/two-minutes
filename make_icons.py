from PIL import Image, ImageDraw
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)

RED = (250, 17, 79)     # Apple Fitness move red
GREEN = (146, 232, 42)  # exercise green
CYAN = (29, 255, 223)   # stand cyan

def track(c, f=0.22):
    return tuple(int(v * f) for v in c)

def draw_rings(size=512, scale=1.0, frac=(0.82, 0.62, 0.38)):
    img = Image.new("RGB", (size, size), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = size / 2
    radii = [196, 144, 92]
    w = 40
    cols = [RED, GREEN, CYAN]
    k = scale * (size / 512.0)
    for i, (r0, col) in enumerate(zip(radii, cols)):
        r = r0 * k
        sw = w * k
        bb = [cx - r - sw / 2, cy - r - sw / 2, cx + r + sw / 2, cy + r + sw / 2]
        d.ellipse(bb, outline=track(col), width=max(1, int(round(sw))))
        a0 = -90.0
        a1 = -90.0 + 360.0 * frac[i]
        d.arc([cx - r, cy - r, cx + r, cx + r], a0, a1, fill=col, width=max(1, int(round(sw))))
        for a in (a0, a1):
            rad = math.radians(a)
            x = cx + r * math.cos(rad)
            y = cy + r * math.sin(rad)
            cr = sw / 2
            d.ellipse([x - cr, y - cr, x + cr, y + cr], fill=col)
    return img

img = draw_rings(512)
img.save(os.path.join(OUT, "icon-512.png"))
img.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "icon-192.png"))
img.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))
draw_rings(512, scale=0.74).save(os.path.join(OUT, "icon-512-maskable.png"))
print("icons ok:", os.listdir(OUT))
