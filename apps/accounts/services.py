"""
سرویس‌های مرتبط با احراز هویت
"""
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.common.sms import send_otp, generate_otp_code, normalize_phone

from .models import OTPRequest, OTP_EXPIRE_SECONDS, OTP_COOLDOWN_SECONDS

User = get_user_model()
logger = logging.getLogger(__name__)


def request_otp(phone: str) -> tuple[bool, str]:
    """
    درخواست ارسال OTP.
    برمی‌گرداند: (موفق, پیام)
    """
    phone = normalize_phone(phone)
    if len(phone) != 11 or not phone.startswith("09"):
        return False, "شماره موبایل معتبر نیست."

    # چک cooldown
    last = OTPRequest.objects.filter(phone=phone).first()
    if last:
        elapsed = (timezone.now() - last.created_at).total_seconds()
        if elapsed < OTP_COOLDOWN_SECONDS:
            remaining = int(OTP_COOLDOWN_SECONDS - elapsed)
            return False, f"لطفاً {remaining} ثانیه صبر کنید."

    code = generate_otp_code(5)
    ok, err = send_otp(phone, code)
    if not ok:
        return False, err or "خطا در ارسال پیامک. لطفاً دوباره تلاش کنید."

    OTPRequest.objects.create(phone=phone, code=code)
    return True, "کد تأیید به شماره شما ارسال شد."


def verify_otp(phone: str, code: str) -> User | None:
    """
    تأیید کد OTP و برگرداندن کاربر (موجود یا ایجادشده).
    در صورت نامعتبر بودن کد None برمی‌گرداند.
    """
    phone = normalize_phone(phone)
    otp = OTPRequest.objects.filter(phone=phone, code=code).order_by("-created_at").first()
    if not otp or otp.is_expired():
        return None

    phone_users = User.objects.filter(phone=phone).order_by("id")
    username_users = User.objects.filter(username=phone).order_by("id")

    if phone_users.count() > 1:
        logger.error("OTP verify blocked: duplicate users with same phone=%s", phone)
        return None

    if username_users.count() > 1:
        logger.error("OTP verify blocked: duplicate users with same username=%s", phone)
        return None

    user = phone_users.first() or username_users.first()
    if not user:
        user = User(username=phone, phone=phone, is_active=True)
        user.set_unusable_password()
        user.save()
    elif not user.phone:
        user.phone = phone
        user.save(update_fields=["phone"])

    # OTP is strictly single-use.
    OTPRequest.objects.filter(phone=phone).delete()
    return user
