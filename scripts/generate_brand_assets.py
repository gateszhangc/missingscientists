from pathlib import Path
from math import cos, sin, radians

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#15191a"
PAPER = "#f5f1e8"
PAPER_DEEP = "#ebe2d4"
TEAL = "#243b3c"
TEAL_SOFT = "#d7e4df"
OXIDE = "#b54f37"
AMBER = "#d6a23a"
MIST = "#eef2ee"

FONT_CANDIDATES = {
    "sans": [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
    "serif": [
        "/System/Library/Fonts/NewYork.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ],
    "mono": [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ],
}


def font(kind, size):
    for candidate in FONT_CANDIDATES[kind]:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size=size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def scaled_canvas(size, background):
    scale = 3
    image = Image.new("RGBA", (size[0] * scale, size[1] * scale), background)
    return image, ImageDraw.Draw(image), scale


def xy(values, scale):
    return tuple(int(round(value * scale)) for value in values)


def resize_down(image, size):
    return image.resize(size, Image.Resampling.LANCZOS)


def draw_centered(draw, box, text, fill, typeface):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=typeface)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(
        (left + (right - left - width) / 2, top + (bottom - top - height) / 2 - bbox[1]),
        text,
        fill=fill,
        font=typeface,
    )


def draw_logo_mark(size=1024):
    image, draw, scale = scaled_canvas((size, size), (0, 0, 0, 0))
    s = scale

    draw.rounded_rectangle(xy((64, 64, size - 64, size - 64), s), radius=120 * s, fill=rgba(TEAL, 255))
    draw.rounded_rectangle(xy((96, 96, size - 96, size - 96), s), radius=92 * s, outline=rgba(PAPER, 92), width=5 * s)

    for offset in range(190, 850, 110):
        draw.line(xy((offset, 140, offset, 884), s), fill=rgba(PAPER, 30), width=2 * s)
        draw.line(xy((140, offset, 884, offset), s), fill=rgba(PAPER, 30), width=2 * s)

    center = size / 2
    for radius, alpha in ((330, 34), (242, 42), (152, 52)):
        draw.ellipse(
            xy((center - radius, center - radius, center + radius, center + radius), s),
            outline=rgba(PAPER, alpha),
            width=4 * s,
        )

    points = [(250, 690), (348, 438), (472, 596), (620, 350), (748, 350)]
    for a, b in zip(points, points[1:]):
        draw.line(xy((*a, *b), s), fill=rgba(PAPER, 228), width=26 * s)
    draw.line(xy((620, 350, 748, 350), s), fill=rgba(TEAL, 255), width=34 * s)
    for dash_x in range(628, 742, 34):
        draw.line(xy((dash_x, 350, dash_x + 16, 350), s), fill=rgba(PAPER, 180), width=13 * s)

    nodes = [(250, 690), (348, 438), (472, 596), (620, 350)]
    for x, y in nodes:
        draw.ellipse(xy((x - 30, y - 30, x + 30, y + 30), s), fill=rgba(PAPER, 255))
        draw.ellipse(xy((x - 12, y - 12, x + 12, y + 12), s), fill=rgba(TEAL, 255))

    draw.ellipse(xy((712, 314, 784, 386), s), fill=rgba(TEAL, 255), outline=rgba(OXIDE, 255), width=16 * s)
    draw.line(xy((718, 320, 778, 380), s), fill=rgba(OXIDE, 255), width=10 * s)
    draw.line(xy((778, 320, 718, 380), s), fill=rgba(OXIDE, 255), width=10 * s)

    draw_centered(draw, xy((382, 760, 642, 846), s), "MS", rgba(PAPER, 225), font("mono", 48 * s))

    return resize_down(image, (size, size))


def draw_wordmark():
    image, draw, scale = scaled_canvas((1400, 420), (0, 0, 0, 0))
    mark = draw_logo_mark(300).resize((300 * scale, 300 * scale), Image.Resampling.LANCZOS)
    image.alpha_composite(mark, (60 * scale, 60 * scale))
    draw.text((408 * scale, 112 * scale), "Missing", fill=rgba(INK), font=font("serif", 88 * scale))
    draw.text((410 * scale, 212 * scale), "Scientists", fill=rgba(TEAL), font=font("sans", 82 * scale))
    draw.line(xy((410, 326, 980, 326), scale), fill=rgba(OXIDE, 180), width=5 * scale)
    draw.text((1015 * scale, 299 * scale), "SOURCE-LED ARCHIVE", fill=rgba(OXIDE), font=font("mono", 23 * scale))
    return resize_down(image, (1400, 420))


def draw_archive_map():
    image, draw, scale = scaled_canvas((960, 720), rgba(PAPER, 255))
    s = scale

    for y in range(52, 690, 42):
        draw.line(xy((42, y, 918, y), s), fill=rgba(TEAL, 28), width=s)
    for x in range(54, 930, 42):
        draw.line(xy((x, 40, x, 678), s), fill=rgba(TEAL, 24), width=s)

    draw.rounded_rectangle(xy((58, 58, 902, 662), s), radius=8 * s, outline=rgba(INK, 62), width=2 * s)
    draw.text((82 * s, 82 * s), "MS-ARCHIVE / OBSERVATION FIELD", fill=rgba(TEAL), font=font("mono", 18 * s))
    draw.text((82 * s, 610 * s), "VERIFIED PUBLIC RECORDS ONLY", fill=rgba(OXIDE), font=font("mono", 18 * s))

    origin = (210, 380)
    for radius in (88, 158, 228, 298):
        draw.ellipse(
            xy((origin[0] - radius, origin[1] - radius, origin[0] + radius, origin[1] + radius), s),
            outline=rgba(TEAL, 32),
            width=2 * s,
        )
    for angle in range(-40, 221, 26):
        x = origin[0] + 322 * cos(radians(angle))
        y = origin[1] + 322 * sin(radians(angle))
        draw.line(xy((origin[0], origin[1], x, y), s), fill=rgba(TEAL, 24), width=s)

    path = [(164, 482), (286, 288), (414, 338), (536, 226), (662, 298), (784, 202)]
    for start, end in zip(path, path[1:]):
        draw.line(xy((*start, *end), s), fill=rgba(TEAL, 145), width=5 * s)

    missing_nodes = [(414, 338), (662, 298), (784, 202)]
    for x, y in path:
        draw.ellipse(xy((x - 14, y - 14, x + 14, y + 14), s), fill=rgba(PAPER, 255), outline=rgba(TEAL, 190), width=5 * s)
    for x, y in missing_nodes:
        draw.ellipse(xy((x - 24, y - 24, x + 24, y + 24), s), outline=rgba(OXIDE, 230), width=6 * s)
        draw.line(xy((x - 15, y - 15, x + 15, y + 15), s), fill=rgba(OXIDE, 210), width=4 * s)
        draw.line(xy((x + 15, y - 15, x - 15, y + 15), s), fill=rgba(OXIDE, 210), width=4 * s)

    labels = [("1938", 126, 520), ("1965", 374, 388), ("1985", 622, 350), ("2007", 746, 254)]
    for text, x, y in labels:
        draw.rounded_rectangle(xy((x, y, x + 88, y + 34), s), radius=4 * s, fill=rgba(PAPER_DEEP, 230))
        draw.text((x * s + 10 * s, y * s + 8 * s), text, fill=rgba(INK, 220), font=font("mono", 15 * s))

    for x in (138, 516, 842):
        draw.rectangle(xy((x, 126, x + 76, 132), s), fill=rgba(AMBER, 190))
    for x in (310, 590, 718):
        draw.rectangle(xy((x, 542, x + 118, 548), s), fill=rgba(OXIDE, 150))

    image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    return resize_down(image, (960, 720))


def draw_social_card():
    image, draw, scale = scaled_canvas((1200, 630), rgba(PAPER, 255))
    s = scale

    for y in range(42, 610, 38):
        draw.line(xy((34, y, 1166, y), s), fill=rgba(TEAL, 24), width=s)
    for x in range(44, 1180, 38):
        draw.line(xy((x, 32, x, 598), s), fill=rgba(TEAL, 18), width=s)

    draw.rectangle(xy((0, 0, 1200, 18), s), fill=rgba(TEAL, 255))
    draw.rectangle(xy((0, 612, 1200, 630), s), fill=rgba(TEAL, 255))
    draw.rectangle(xy((34, 34, 1166, 596), s), outline=rgba(INK, 68), width=2 * s)

    mark = draw_logo_mark(1024).resize((160 * s, 160 * s), Image.Resampling.LANCZOS)
    image.alpha_composite(mark, (78 * s, 74 * s))
    draw.text((276 * s, 92 * s), "Missing", fill=rgba(INK), font=font("serif", 86 * s))
    draw.text((276 * s, 188 * s), "Scientists", fill=rgba(TEAL), font=font("sans", 82 * s))
    draw.line(xy((278, 300, 842, 300), s), fill=rgba(OXIDE, 180), width=5 * s)
    draw.text((278 * s, 336 * s), "Verified cases. Public records. No speculation.", fill=rgba(INK, 210), font=font("sans", 32 * s))
    draw.text((278 * s, 389 * s), "missingscientists.lol", fill=rgba(OXIDE), font=font("mono", 24 * s))

    route = [(830, 472), (914, 354), (1004, 396), (1088, 260)]
    for start, end in zip(route, route[1:]):
        draw.line(xy((*start, *end), s), fill=rgba(TEAL, 150), width=5 * s)
    for x, y in route:
        draw.ellipse(xy((x - 13, y - 13, x + 13, y + 13), s), fill=rgba(PAPER, 255), outline=rgba(TEAL, 190), width=5 * s)
    draw.ellipse(xy((1070, 242, 1106, 278), s), outline=rgba(OXIDE, 235), width=6 * s)
    draw.line(xy((1076, 248, 1100, 272), s), fill=rgba(OXIDE, 220), width=4 * s)
    draw.line(xy((1100, 248, 1076, 272), s), fill=rgba(OXIDE, 220), width=4 * s)

    for text, x, y in (("1938", 782, 506), ("1965", 866, 390), ("1985", 956, 432), ("2007", 1040, 294)):
        draw.text((x * s, y * s), text, fill=rgba(INK, 170), font=font("mono", 18 * s))

    image = image.filter(ImageFilter.UnsharpMask(radius=1.1, percent=85, threshold=3))
    return resize_down(image, (1200, 630))


def save_assets():
    logo = draw_logo_mark(1024)
    logo.save(OUT / "logo-mark.png")

    favicon = logo.resize((512, 512), Image.Resampling.LANCZOS)
    favicon.save(OUT / "favicon.png")
    favicon.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    apple = logo.resize((180, 180), Image.Resampling.LANCZOS)
    apple.save(OUT / "apple-touch-icon.png")

    draw_wordmark().save(OUT / "logo-wordmark.png")
    draw_archive_map().save(OUT / "archive-map.png")
    draw_social_card().save(OUT / "social-card.png")


if __name__ == "__main__":
    save_assets()
    for path in sorted(OUT.glob("*")):
        print(path.relative_to(ROOT))
