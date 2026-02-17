"""
سرویس پیامک کاوه‌نگار — مطابق مستندات REST:
https://kavenegar.com/rest.html

- متد ارسال ساده: GET/POST به sms/send.json
- پارامترها: receptor (اجباری)، message (اجباری، حتماً URL-Encode)، sender (اختیاری)
- خروجی JSON: return.status == 200 یعنی موفق؛ غیره یعنی خطا و return.message توضیح
- حداکثر طول متن پیامک: ۹۰۰ کاراکتر
"""
import json
import logging
import random
import string
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from django.conf import settings

logger = logging.getLogger(__name__)

# مطابق داکیومنت: https://api.kavenegar.com/v1/{API-KEY}/Scope/MethodName.OutputFormat
KAVENEGAR_BASE = "https://api.kavenegar.com/v1"
MAX_MESSAGE_LENGTH = 900  # حداکثر طول متن پیامک طبق داکیومنت


def normalize_phone(phone: str) -> str:
    """
    نرمال‌سازی شماره موبایل به یکی از فرمت‌های مجاز کاوه‌نگار:
    09121234567، 00989121234567، +989121234567، 9121234567
    """
    if not phone:
        return ""
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("98") and len(digits) >= 10:
        return "0" + digits[2:]
    if digits.startswith("9") and len(digits) == 10:
        return "0" + digits
    return digits if digits.startswith("0") else "0" + digits


def _parse_kavenegar_response(body: str) -> tuple[int, str]:
    """
    پارس پاسخ JSON کاوه‌نگار. برمی‌گرداند: (status, message).
    ساختار: { "return": { "status": 200, "message": "تایید شد" }, "entries": ... }
    """
    try:
        data = json.loads(body)
        ret = data.get("return") or {}
        return (int(ret.get("status", 0)), (ret.get("message") or "").strip())
    except (json.JSONDecodeError, TypeError, ValueError):
        return (0, body[:200] if body else "پاسخ نامعتبر")


def _save_sms_log(receptor: str, message: str, response_json: str, is_success: bool) -> None:
    """ذخیرهٔ لاگ ارسال پیامک در دیتابیس (در صورت خطا لاگ می‌شود، ارسال قطع نمی‌شود)."""
    try:
        from .models import SmsLog

        SmsLog.objects.create(
            receptor=receptor,
            message=message,
            response_json=response_json or "{}",
            is_success=is_success,
        )
    except Exception as e:
        logger.warning("SmsLog save failed: %s", e)


def _kavenegar_send(api_key: str, receptor: str, message: str, sender: str) -> tuple[bool, str]:
    """
    ارسال پیامک با متد Send (sms/send.json) طبق داکیومنت.
    GET با پارامترهای URL-Encode شده.
    برمی‌گرداند: (موفق, پیام_خطا).
    """
    api_key = "".join(c for c in (api_key or "").strip() if ord(c) >= 32 and c not in " \t\n\r")
    if not api_key:
        return (False, "کلید API تنظیم نشده است.")
    if not receptor:
        return (False, "شماره گیرنده معتبر نیست.")
    if not message or len(message) > MAX_MESSAGE_LENGTH:
        return (False, "متن پیام خالی است یا طول آن بیش از حد مجاز است.")

    # داکیومنت: در GET حتماً پارامترها را URL Encode کنید
    params = {"receptor": receptor, "message": message, "sender": sender}
    url = f"{KAVENEGAR_BASE}/{api_key}/sms/send.json?{urlencode(params)}"
    try:
        with urlopen(url, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status, msg = _parse_kavenegar_response(body)
            if resp.status == 200 and status == 200:
                _save_sms_log(receptor, message, body, True)
                return (True, "")
            _save_sms_log(receptor, message, body, False)
            return (False, msg or f"وضعیت {status}")
    except HTTPError as e:
        body = ""
        try:
            body_bytes = e.fp.read() if e.fp else b""
            body = body_bytes.decode("utf-8", errors="replace")
            _, msg = _parse_kavenegar_response(body)
            _save_sms_log(receptor, message, body, False)
            if msg:
                return (False, msg)
        except Exception:
            _save_sms_log(receptor, message, "{}", False)
        logger.exception("KaveNegar HTTPError %s: %s", e.code, body or e)
        return (False, f"خطا از کاوه‌نگار: [{e.code}] {(body[:120] if body else str(e))}")
    except (URLError, OSError) as e:
        _save_sms_log(receptor, message, "{}", False)
        logger.exception("KaveNegar request failed: %s", e)
        return (False, f"خطا در ارتباط با سرور: {e}")


def send_sms(receptor: str, message: str, sender: str | None = None) -> bool:
    """ارسال پیامک ساده — یک گیرنده، یک متن."""
    api_key = (getattr(settings, "KAVENEGAR_API_KEY", None) or "").strip()
    if not api_key:
        return False
    sender = (sender or getattr(settings, "KAVENEGAR_SENDER", "") or "9982002624").strip()
    ok, _ = _kavenegar_send(api_key, normalize_phone(receptor), message, sender)
    return ok


def send_otp(receptor: str, code: str) -> tuple[bool, str]:
    """
    ارسال کد OTP برای ورود/ثبت‌نام.
    برمی‌گرداند: (موفق, پیام_خطا).
    """
    api_key = (getattr(settings, "KAVENEGAR_API_KEY", None) or "").strip()
    if not api_key:
        if getattr(settings, "DEBUG", False):
            logger.warning("[DEV] KAVENEGAR_API_KEY not set. OTP %s for %s", code, receptor)
        return (bool(getattr(settings, "DEBUG", False)), "")
    receptor = normalize_phone(receptor)
    sender = (getattr(settings, "KAVENEGAR_SENDER", "") or "9982002624").strip()
    message = f"کد تأیید VidaHome: {code}"
    return _kavenegar_send(api_key, receptor, message, sender)


def generate_otp_code(length: int = 5) -> str:
    """تولید کد عددی تصادفی برای OTP."""
    return "".join(random.choices(string.digits, k=length))
