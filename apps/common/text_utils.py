"""
ابزارهای متن — تبدیل عنوان فارسی به اسلاگ
"""
from django.utils.text import slugify


# نگاشت حروف فارسی/عربی به لاتین
_PERSIAN_MAP = {
    "ا": "a", "آ": "a", "أ": "a", "إ": "a", "ئ": "e",
    "ب": "b", "پ": "p", "ت": "t", "ث": "s", "ج": "j", "چ": "c",
    "ح": "h", "خ": "k", "د": "d", "ذ": "z", "ر": "r", "ز": "z",
    "ژ": "zh", "س": "s", "ش": "sh", "ص": "s", "ض": "z", "ط": "t",
    "ظ": "z", "ع": "a", "غ": "gh", "ف": "f", "ق": "gh", "ک": "k",
    "ك": "k", "گ": "g", "ل": "l", "م": "m", "ن": "n", "و": "v",
    "ه": "h", "ة": "h", "ی": "y", "ي": "y", "ؤ": "o", "ء": "",
}


def slugify_from_title(title: str, max_length: int = 255) -> str:
    """
    ساخت اسلاگ از عنوان — پشتیبانی از متن فارسی با ترانسلیتریشن به لاتین.
    """
    if not title or not str(title).strip():
        return "listing"
    s = str(title).strip().replace("\u200c", " ")  # نیم‌فاصله
    parts = []
    for c in s:
        if c in _PERSIAN_MAP:
            parts.append(_PERSIAN_MAP[c])
        elif c.isspace():
            parts.append(" ")
        elif c.isalnum() or c in "-_":
            parts.append(c)
    text = "".join(parts)
    result = slugify(text, allow_unicode=False)
    return (result or "listing")[:max_length]
