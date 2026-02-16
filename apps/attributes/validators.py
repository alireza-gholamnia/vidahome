"""
اعتبارسنجی فایل آیکون ویژگی‌ها.
"""
import os

from django.core.exceptions import ValidationError


# حداکثر حجم: ۶۴ کیلوبایت
ICON_MAX_SIZE = 64 * 1024

# پسوندهای مجاز
ALLOWED_EXTENSIONS = (".png", ".svg")


def validate_attribute_icon(file):
    """فقط PNG و SVG، حداکثر ۶۴ کیلوبایت."""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"فقط فایل‌های با پسوند {' یا '.join(ALLOWED_EXTENSIONS)} مجاز است."
        )
    if file.size > ICON_MAX_SIZE:
        raise ValidationError(
            f"حداکثر حجم مجاز {ICON_MAX_SIZE // 1024} کیلوبایت است."
        )
    if ext == ".png":
        from PIL import Image
        try:
            img = Image.open(file)
            w, h = img.size
            if w > 128 or h > 128:
                raise ValidationError(
                    "ابعاد تصویر نباید از ۱۲۸×۱۲۸ پیکسل بیشتر باشد."
                )
            if hasattr(file, "seek"):
                file.seek(0)
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError("فایل تصویر نامعتبر است.") from e
