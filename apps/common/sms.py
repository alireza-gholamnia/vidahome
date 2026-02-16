"""
سرویس پیامک کاوه‌نگار
"""
import logging
import random
import string

from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException

logger = logging.getLogger(__name__)


def normalize_phone(phone: str) -> str:
    """نرمال‌سازی شماره موبایل ایران به فرم 09xxxxxxxxx"""
    if not phone:
        return ""
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("98") and len(digits) >= 10:
        return "0" + digits[2:]
    if digits.startswith("9") and len(digits) == 10:
        return "0" + digits
    return digits if digits.startswith("0") else "0" + digits


def send_sms(receptor: str, message: str, sender: str | None = None) -> bool:
    """ارسال پیامک ساده"""
    api_key = getattr(settings, "KAVENEGAR_API_KEY", None)
    if not api_key:
        return False
    sender = sender or getattr(settings, "KAVENEGAR_SENDER", "")
    try:
        api = KavenegarAPI(api_key)
        params = {
            "receptor": normalize_phone(receptor),
            "message": message,
            "sender": sender,
        }
        api.sms_send(params)
        return True
    except (APIException, HTTPException) as e:
        logger.exception("KaveNegar sms_send failed: %s", e)
        return False


def send_otp(receptor: str, code: str) -> tuple[bool, str]:
    """
    ارسال کد OTP با sms_send (بدون نیاز به قالب verify).
    برمی‌گرداند: (موفق, پیام_خطا)
    """
    api_key = getattr(settings, "KAVENEGAR_API_KEY", None)
    if not api_key:
        if getattr(settings, "DEBUG", False):
            logger.warning("[DEV] KAVENEGAR_API_KEY not set. OTP %s for %s", code, receptor)
        return (bool(getattr(settings, "DEBUG", False)), "")
    receptor = normalize_phone(receptor)
    sender = getattr(settings, "KAVENEGAR_SENDER", "")
    message = f"کد تأیید VidaHome: {code}"
    try:
        api = KavenegarAPI(api_key)
        params = {
            "receptor": receptor,
            "message": message,
            "sender": sender,
        }
        api.sms_send(params)
        return (True, "")
    except (APIException, HTTPException) as e:
        err_msg = str(e)
        logger.exception("KaveNegar send_otp failed: %s", err_msg)
        return (False, f"خطا از کاوه‌نگار: {err_msg}")


def generate_otp_code(length: int = 5) -> str:
    """تولید کد عددی تصادفی برای OTP"""
    return "".join(random.choices(string.digits, k=length))
