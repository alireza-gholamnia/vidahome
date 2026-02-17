from django.db import models


class ContactMessage(models.Model):
    """پیام تماس کاربر از صفحه تماس با ما."""
    name = models.CharField(max_length=120, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    subject = models.CharField(max_length=200, blank=True, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"


class SmsLog(models.Model):
    """لاگ پیامک‌های ارسالی — محتوا و پاسخ JSON کاوه‌نگار."""
    receptor = models.CharField(max_length=20, verbose_name="شماره گیرنده", db_index=True)
    message = models.TextField(verbose_name="محتوا")
    response_json = models.TextField(blank=True, verbose_name="پاسخ JSON کاوه‌نگار")
    is_success = models.BooleanField(default=False, verbose_name="موفق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "لاگ پیامک"
        verbose_name_plural = "لاگ پیامک‌های ارسالی"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.receptor} — {self.created_at:%Y-%m-%d %H:%M}"
