#!/usr/bin/env python3
"""Собирает баннер-шапку профиля: assets/banner.png

Нужен Pillow:  python3 -m pip install pillow
Запуск из корня репозитория:  python3 scripts/make-banner.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

W, H = 1600, 640
PINK = (255, 155, 210)
VIOLET = (192, 132, 252)
INDIGO = (129, 140, 248)
MINT = (123, 227, 176)
PEACH = (255, 196, 107)
CORAL = (255, 123, 138)
TEXT = (245, 240, 250)
MUTED = (185, 178, 204)
BG_TOP = (10, 9, 18)
BG_BOT = (26, 17, 42)

UNBOUNDED = str(ASSETS / "fonts" / "Unbounded.ttf")
MANROPE = str(ASSETS / "fonts" / "Manrope.ttf")

NAME = "moldren"
BAR_URL = "github.com/moldren"


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        f.set_variation_by_axes([weight])
    return f


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diagonal_gradient(size, top, bottom, angle=0.7):
    w, h = size
    sw, sh = 96, 48
    small = Image.new("RGB", (sw, sh))
    px = small.load()
    for y in range(sh):
        for x in range(sw):
            t = (x / (sw - 1)) * angle + (y / (sh - 1)) * (1 - angle)
            px[x, y] = lerp(top, bottom, t)
    return small.resize(size, Image.BICUBIC)


def radial_layer(size, center, radius, color, alpha, blur):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def sparkle(draw, x, y, size, color, alpha=180):
    p = size
    draw.polygon(
        [(x, y - p), (x + p * 0.28, y - p * 0.28), (x + p, y),
         (x + p * 0.28, y + p * 0.28), (x, y + p),
         (x - p * 0.28, y + p * 0.28), (x - p, y),
         (x - p * 0.28, y - p * 0.28)],
        fill=color + (alpha,),
    )


def gradient_text(base, xy, text, fnt, colors):
    """Рисует текст с горизонтальным градиентом. xy — левый верхний край чернил."""
    bbox = fnt.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 3
    mask = Image.new("L", (tw + pad * 2, th + pad * 2), 0)
    ImageDraw.Draw(mask).text((pad - bbox[0], pad - bbox[1]), text, font=fnt, fill=255)

    strip = Image.new("RGB", (mask.width, 1))
    sp = strip.load()
    for x in range(mask.width):
        t = x / max(mask.width - 1, 1)
        if t < 0.5:
            c = lerp(colors[0], colors[1], t / 0.5)
        else:
            c = lerp(colors[1], colors[2], (t - 0.5) / 0.5)
        sp[x, 0] = c
    grad = strip.resize(mask.size, Image.BICUBIC).convert("RGBA")
    grad.putalpha(mask)
    base.alpha_composite(grad, (int(xy[0] - pad), int(xy[1] - pad)))
    return tw, th


def pill(draw, x, y, label, fnt, dot=None, pad_x=20, h=46):
    tw = draw.textlength(label, font=fnt)
    w = int(tw + pad_x * 2 + (18 if dot else 0))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2,
                           fill=(255, 255, 255, 14), outline=(255, 255, 255, 48), width=1)
    tx = x + pad_x
    if dot:
        cy = y + h / 2
        draw.ellipse((tx, cy - 4, tx + 8, cy + 4), fill=dot + (255,))
        tx += 18
    draw.text((tx, y + h / 2 + 1), label, font=fnt, fill=(233, 228, 244, 255), anchor="lm")
    return w


# ---------- фон ----------
img = diagonal_gradient((W, H), BG_TOP, BG_BOT, 0.65).convert("RGBA")

img = Image.alpha_composite(img, radial_layer((W, H), (250, 130), 520, PINK, 55, 170))
img = Image.alpha_composite(img, radial_layer((W, H), (1380, 580), 520, VIOLET, 48, 170))
img = Image.alpha_composite(img, radial_layer((W, H), (900, -80), 420, INDIGO, 38, 160))

# сетка точек
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for gy in range(80, H, 38):
    for gx in range(24, W, 38):
        gd.ellipse((gx, gy, gx + 2, gy + 2), fill=(255, 255, 255, 16))
img = Image.alpha_composite(img, grid)

# виньетка
vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse((-300, -240, W + 300, H + 240), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(190))
dark = Image.new("RGBA", (W, H), (4, 3, 9, 255))
img = Image.composite(img, Image.alpha_composite(img, dark), vig)

# ---------- фейковая верхняя панель сайта ----------
BAR = 52
bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bar)
bd.rectangle((0, 0, W, BAR), fill=(255, 255, 255, 10))
bd.line((0, BAR, W, BAR), fill=(255, 255, 255, 28), width=1)

for i, c in enumerate((CORAL, PEACH, MINT)):
    cx = 34 + i * 24
    bd.ellipse((cx, BAR / 2 - 6, cx + 12, BAR / 2 + 6), fill=c + (255,))

url_label = BAR_URL
f_url = font(MANROPE, 17, 600)
uw = bd.textlength(url_label, font=f_url)
ux = W / 2 - (uw + 74) / 2
bd.rounded_rectangle((ux, 12, ux + uw + 74, BAR - 12), radius=14,
                     fill=(255, 255, 255, 14), outline=(255, 255, 255, 34), width=1)
bd.ellipse((ux + 22, BAR / 2 - 4, ux + 30, BAR / 2 + 4), fill=MINT + (255,))
bd.text((ux + 42, BAR / 2 + 1), url_label, font=f_url, fill=MUTED + (255,), anchor="lm")

f_tiny = font(MANROPE, 16, 600)
bd.ellipse((W - 132, BAR / 2 - 5, W - 122, BAR / 2 + 5), fill=MINT + (255,))
bd.text((W - 112, BAR / 2 + 1), "онлайн", font=f_tiny, fill=MUTED + (255,), anchor="lm")
img = Image.alpha_composite(img, bar)

# ---------- аватар ----------
AV_R = 166
AV_C = (300, 362)

img = Image.alpha_composite(img, radial_layer((W, H), AV_C, AV_R + 76, PINK, 62, 70))
img = Image.alpha_composite(img, radial_layer((W, H), (AV_C[0] + 26, AV_C[1] + 40), AV_R + 40, VIOLET, 48, 60))

avatar = Image.open(ASSETS / "waifu.jpg").convert("RGB")
side = min(avatar.size)
avatar = avatar.crop(((avatar.width - side) // 2, (avatar.height - side) // 2,
                      (avatar.width + side) // 2, (avatar.height + side) // 2))
avatar = avatar.resize((AV_R * 2, AV_R * 2), Image.LANCZOS).convert("RGBA")

mask = Image.new("L", avatar.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, avatar.width - 1, avatar.height - 1), fill=255)
avatar.putalpha(mask)
img.alpha_composite(avatar, (AV_C[0] - AV_R, AV_C[1] - AV_R))

# кольцо с градиентом
ring_size = (AV_R + 10) * 2
ring_mask = Image.new("L", (ring_size, ring_size), 0)
ImageDraw.Draw(ring_mask).ellipse((0, 0, ring_size - 1, ring_size - 1), fill=255)
ImageDraw.Draw(ring_mask).ellipse((10, 10, ring_size - 11, ring_size - 11), fill=0)
ring_strip = Image.new("RGB", (1, ring_size))
rp = ring_strip.load()
for y in range(ring_size):
    rp[0, y] = lerp((255, 214, 236), VIOLET, y / (ring_size - 1))
ring = ring_strip.resize((ring_size, ring_size), Image.BICUBIC).convert("RGBA")
ring.putalpha(ring_mask)
img.alpha_composite(ring, (AV_C[0] - ring_size // 2, AV_C[1] - ring_size // 2))

deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(deco)
sparkle(dd, 118, 230, 14, (255, 214, 236), 210)
sparkle(dd, 492, 176, 10, VIOLET, 190)
sparkle(dd, 470, 526, 8, INDIGO, 170)
img = Image.alpha_composite(img, deco)

# ---------- текстовый блок ----------
X = 560
draw = ImageDraw.Draw(img)

# плашка «аниме-тянка × девелопер»
f_eyebrow = font(MANROPE, 19, 700)
eyebrow = "аниме-тянка  ×  девелопер"
ew = draw.textlength(eyebrow, font=f_eyebrow)
badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bdr = ImageDraw.Draw(badge)
bdr.rounded_rectangle((X, 112, X + ew + 58, 160), radius=24,
                      fill=(255, 155, 210, 26), outline=(255, 155, 210, 100), width=1)
sparkle(bdr, X + 25, 136, 7, PINK, 255)
bdr.text((X + 42, 137), eyebrow, font=f_eyebrow, fill=(255, 208, 234, 255), anchor="lm")
img = Image.alpha_composite(img, badge)
draw = ImageDraw.Draw(img)

f_name = font(UNBOUNDED, 148, 700)
y = 192
wn, hn = gradient_text(img, (X, y), NAME, f_name, ((255, 255, 255), PINK, VIOLET))
draw = ImageDraw.Draw(img)
block_bottom = y + hn

# линия-разделитель
line_y = block_bottom + 26
line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(line_layer).line((X, line_y, X + 128, line_y), fill=PINK + (210,), width=3)
img = Image.alpha_composite(img, line_layer)
draw = ImageDraw.Draw(img)

f_sub = font(MANROPE, 28, 600)
draw.text((X, line_y + 16), "Пишу интерфейсы, которые выглядят как опенинг —",
          font=f_sub, fill=(206, 198, 222, 255))
draw.text((X, line_y + 56), "и грузятся быстрее титров.",
          font=f_sub, fill=(206, 198, 222, 255))

# пилюли со стеком
f_pill = font(MANROPE, 21, 700)
pill_y = line_y + 118
pills = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(pills)
px = X
for label, dot in (("TypeScript", INDIGO), ("React", (97, 218, 251)),
                   ("Next.js", (245, 240, 250)), ("лоу-фай", PINK),
                   ("matcha latte", MINT)):
    px += pill(pd, px, pill_y, label, f_pill, dot) + 12
img = Image.alpha_composite(img, pills)
draw = ImageDraw.Draw(img)

# нижняя строка
f_foot = font(MANROPE, 19, 600)
foot_y = pill_y + 76
draw.text((X, foot_y), "github.com/moldren", font=f_foot, fill=(168, 160, 188, 255))
draw.text((X + 214, foot_y), "· открыта к коллаборациям", font=f_foot, fill=(255, 155, 210, 255))

# ---------- зерно ----------
noise = Image.effect_noise((W, H), 16).convert("L").convert("RGBA")
noise.putalpha(6)
img = Image.alpha_composite(img, noise)

img.convert("RGB").save(ASSETS / "banner.png", optimize=True)
print("saved", ASSETS / "banner.png", img.size)
