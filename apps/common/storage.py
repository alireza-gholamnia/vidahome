"""
ذخیره‌سازی تصاویر با تبدیل خودکار به WebP.
همه تصاویر آپلودی با پایتون (Pillow) به فرمت WebP تبدیل می‌شوند.
"""
import io
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from PIL import Image


# فرمت‌های ورودی قابل تبدیل
IMAGE_EXTENSIONS = frozenset((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"))


class WebPImageStorage(FileSystemStorage):
    """
    Storage که همه تصاویر را به WebP تبدیل می‌کند.
    کیفیت: 85 (متعادل با کیفیت خوب)
    """

    def _save(self, name, content, max_length=None):
        path = Path(name)
        ext = path.suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            try:
                content = self._convert_to_webp(content)
                name = str(path.with_suffix(".webp"))
            except Exception:
                pass  # در صورت خطا، فایل با فرمت اصلی ذخیره می‌شود
        return super()._save(name, content)

    def _convert_to_webp(self, content) -> ContentFile:
        """تبدیل تصویر به WebP با Pillow — کیفیت 85."""
        if hasattr(content, "seek"):
            content.seek(0)
        img = Image.open(content).copy()
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        out = io.BytesIO()
        img.save(out, format="WEBP", quality=85, method=6)
        out.seek(0)
        return ContentFile(out.read(), name="")
