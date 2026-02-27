from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from apps.common.sms import normalize_phone
from apps.common.upload_utils import avatar_upload_to

# مدت اعتبار OTP به ثانیه (۲ دقیقه)
OTP_EXPIRE_SECONDS = 120
OTP_COOLDOWN_SECONDS = 60  # حداقل فاصله بین دو درخواست


# نقش از طریق Django Group تعیین می‌شود
GROUP_ROLE_LABELS = {
    "site_admin": "مدیر سایت",
    "seo_admin": "کاربر سئو",
    "member": "کاربر معمولی",
    "agency_owner": "صاحب مشاوره",
    "agency_employee": "کارمند مشاوره",
}


class User(AbstractUser):
    """مدل کاربر با فیلدهای اضافی پروفایل."""

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        constraints = [
            models.UniqueConstraint(
                fields=("phone",),
                condition=~models.Q(phone=""),
                name="uniq_accounts_user_phone_nonempty",
            ),
        ]

    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    slug = models.SlugField(
        max_length=120, blank=True, db_index=True, verbose_name="اسلاگ",
        help_text="برای لندینگ مشاور/صاحب مشاوره — خالی=غیرفعال",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        verbose_name="تصویر پروفایل",
    )
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده")
    agency = models.ForeignKey(
        "agencies.Agency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name="مشاوره املاک",
    )

    def get_role_display(self):
        """نقش از اولین گروه کاربر گرفته می‌شود."""
        for g in self.groups.all():
            return GROUP_ROLE_LABELS.get(g.name, g.name)
        return "-"

    def is_agent(self):
        """آیا کاربر صاحب یا کارمند مشاوره است و لندینگ دارد؟"""
        from apps.agencies.models import Agency

        if self.owned_agencies.filter(
            is_active=True, approval_status=Agency.ApprovalStatus.APPROVED
        ).exists():
            return True
        if self.agency_id and self.agency.is_active and self.agency.approval_status == Agency.ApprovalStatus.APPROVED:
            return True
        return False

    def get_absolute_url(self):
        """آدرس لندینگ مشاور — فقط برای صاحبان و کارمندان مشاوره."""
        if self.slug:
            return f"/agent/{self.id}-{self.slug}/"
        return f"/agent/{self.id}/"

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)


class OTPRequest(models.Model):
    """کد OTP برای ورود با موبایل"""
    phone = models.CharField(max_length=20, verbose_name="شماره موبایل", db_index=True)
    code = models.CharField(max_length=10, verbose_name="کد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "درخواست OTP"
        verbose_name_plural = "درخواست‌های OTP"
        ordering = ("-created_at",)

    def is_expired(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() > OTP_EXPIRE_SECONDS

    def __str__(self):
        return f"OTP {self.phone[:4]}***"


class RoleChangeRequest(models.Model):
    """درخواست تغییر نقش کاربر به صاحب مشاوره یا کارمند مشاوره — تأیید توسط ادمین."""

    class RequestedRole(models.TextChoices):
        AGENCY_OWNER = "agency_owner", "صاحب مشاوره املاک"
        AGENCY_EMPLOYEE = "agency_employee", "کارمند مشاوره املاک"

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="role_change_requests",
        verbose_name="کاربر",
    )
    requested_role = models.CharField(
        max_length=20,
        choices=RequestedRole.choices,
        db_index=True,
        verbose_name="نقش درخواستی",
    )
    message = models.TextField(verbose_name="توضیحات درخواست", blank=True)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name="وضعیت",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درخواست")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ بررسی")

    class Meta:
        verbose_name = "درخواست تغییر نقش"
        verbose_name_plural = "درخواست‌های تغییر نقش"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "requested_role"),
                condition=models.Q(status="pending"),
                name="uniq_pending_rolechange_user_role",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.get_requested_role_display()}"
