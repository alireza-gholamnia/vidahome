from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.upload_utils import avatar_upload_to


# نقش از طریق Django Group تعیین می‌شود
GROUP_ROLE_LABELS = {
    "site_admin": "مدیر سایت",
    "seo_admin": "کاربر سئو",
    "member": "کاربر معمولی",
    "independent_agent": "مشاور مستقل",
    "agency_owner": "صاحب مشاوره",
    "agency_employee": "کارمند مشاوره",
}


class User(AbstractUser):
    """مدل کاربر با فیلدهای اضافی پروفایل."""

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
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
