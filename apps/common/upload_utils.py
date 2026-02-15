"""
نام‌گذاری خودکار و یکتا برای تصاویر آپلودی.
همه تصاویر با نام UUID و فرمت WebP ذخیره می‌شوند.
تبدیل به WebP در storage انجام می‌شود.
"""
import uuid
from django.utils import timezone

ALLOWED_EXT = frozenset(("jpg", "jpeg", "png", "gif", "webp"))

# خروجی همیشه WebP است (storage تصویر را تبدیل می‌کند)
OUTPUT_EXT = "webp"


def _safe_ext(filename: str) -> str:
    """استخراج پسوند امن برای تصویر."""
    ext = (filename.split(".")[-1] or "jpg").lower()
    return ext if ext in ALLOWED_EXT else "jpg"


def unique_filename(filename: str) -> str:
    """
    نام یکتای تصویر — برای CKEditor و سایر آپلودها.
    خروجی همیشه .webp (storage تبدیل می‌کند).
    """
    return f"{uuid.uuid4().hex}.{OUTPUT_EXT}"


def unique_upload_path(prefix: str):
    """
    Callable برای ImageField.upload_to
    مسیر: {prefix}/{سال}/{ماه}/{uuid}.webp
    """

    def _upload_to(instance, filename):
        unique_name = f"{uuid.uuid4().hex}.{OUTPUT_EXT}"
        date_path = timezone.now().strftime("%Y/%m")
        return f"{prefix}/{date_path}/{unique_name}"

    return _upload_to


# توابع قابل سریال‌سازی برای migrations:
def agency_logo_upload_to(instance, filename):
    return f"agencies/logos/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def agency_image_upload_to(instance, filename):
    return f"uploads/agencies/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def avatar_upload_to(instance, filename):
    return f"avatars/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def city_image_upload_to(instance, filename):
    return f"uploads/cities/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def area_image_upload_to(instance, filename):
    return f"uploads/areas/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def category_image_upload_to(instance, filename):
    return f"uploads/categories/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def city_category_image_upload_to(instance, filename):
    return f"uploads/city_category/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def area_category_image_upload_to(instance, filename):
    return f"uploads/area_category/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def listing_image_upload_to(instance, filename):
    return f"listings/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"


def blog_cover_upload_to(instance, filename):
    return f"blog/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}.{OUTPUT_EXT}"
