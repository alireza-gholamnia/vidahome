"""
ساخت تصاویر placeholder با Pillow برای سایت VidaHome.
هر تصویر شامل متن وسط (مثلاً نام شهر، عنوان آگهی و...) روی پس‌زمینه گرادیان است.
"""
import io
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


# رنگ‌های پس‌زمینه گرادیان (سبز-آبی ملایم)
COLORS = [
    ((52, 152, 219), (41, 128, 185)),   # آبی
    ((46, 204, 113), (39, 174, 96)),    # سبز
    ((155, 89, 182), (142, 68, 173)),   # بنفش
    ((241, 196, 15), (243, 156, 18)),   # طلایی
    ((231, 76, 60), (192, 57, 43)),     # قرمز
    ((26, 188, 156), (22, 160, 133)),   # فیروزه‌ای
]

# سایزهای پیش‌فرض
SIZE_COVER = (800, 600)      # کارت و کاور
SIZE_LANDING = (1200, 600)   # کاور لندینگ
SIZE_LOGO = (200, 200)       # لوگو


def _find_font(size: int = 48):
    """پیدا کردن فونت مناسب برای فارسی (Tahoma, Arial و...)"""
    candidates = [
        Path("C:/Windows/Fonts/tahoma.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def _gradient_background(width: int, height: int, color_pair: tuple) -> Image.Image:
    """ساخت پس‌زمینه گرادیان از بالا به پایین."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    c1, c2 = color_pair
    for y in range(height):
        r = int(c1[0] + (c2[0] - c1[0]) * y / height)
        g = int(c1[1] + (c2[1] - c1[1]) * y / height)
        b = int(c1[2] + (c2[2] - c1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def _draw_centered_text(img: Image.Image, text: str, font_size: int = 48) -> None:
    """نوشتن متن وسط تصویر."""
    draw = ImageDraw.Draw(img)
    font = _find_font(font_size)

    # اندازه متن
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (img.width - tw) // 2
    y = (img.height - th) // 2

    # سایه ملایم
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))


def create_placeholder_image(
    text: str,
    width: int = 800,
    height: int = 600,
    color_index: int = 0,
    font_size: int = 48,
) -> ContentFile:
    """
    ساخت تصویر placeholder با متن وسط.
    برگرداندن ContentFile آماده برای ذخیره در ImageField.
    """
    color_pair = COLORS[color_index % len(COLORS)]
    img = _gradient_background(width, height, color_pair)
    _draw_centered_text(img, text, font_size)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name="placeholder.png")
