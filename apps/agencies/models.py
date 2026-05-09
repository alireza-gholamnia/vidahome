from django.db import models
from django.conf import settings
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from apps.seo.base import BaseSEO
from apps.common.upload_utils import agency_logo_upload_to, agency_image_upload_to
from apps.common.text_utils import slugify_from_title


class Agency(BaseSEO, models.Model):
    """
    مشاوره املاک — دارای لندینگ اختصاصی /a/{id}-{slug}/
    هر صاحب مشاوره می‌تواند چند مشاوره داشته باشد.
    """
    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    name = models.CharField(max_length=180, verbose_name="نام")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, verbose_name="اسلاگ")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_agencies",
        verbose_name="مالک",
    )
    approval_status = models.CharField(
        max_length=12,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.APPROVED,
        db_index=True,
        verbose_name="وضعیت تأیید",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    address = models.TextField(blank=True, verbose_name="آدرس")
    intro_content = models.TextField(blank=True, verbose_name="متن معرفی")
    main_content = RichTextUploadingField(blank=True, verbose_name="محتوای اصلی")
    logo = models.ImageField(upload_to=agency_logo_upload_to, blank=True, null=True, verbose_name="لوگو")
    cities = models.ManyToManyField(
        "locations.City",
        related_name="agencies",
        blank=True,
        verbose_name="شهرها",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="AgencyMembership",
        through_fields=("agency", "user"),
        related_name="member_agencies",
        blank=True,
        verbose_name="اعضا",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "مشاوره املاک"
        verbose_name_plural = "مشاوره‌های املاک"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_owner_id = None
        if self.pk:
            old_owner_id = (
                Agency.objects.filter(pk=self.pk)
                .values_list("owner_id", flat=True)
                .first()
            )
        if not self.slug:
            base_slug = slugify_from_title(self.name, max_length=200)
            candidate = base_slug
            suffix = 2
            while Agency.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                suffix_text = f"-{suffix}"
                candidate = f"{base_slug[: 200 - len(suffix_text)]}{suffix_text}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)
        self.sync_owner_membership(old_owner_id=old_owner_id)

    def sync_owner_membership(self, old_owner_id=None):
        if not self.owner_id:
            return
        now = timezone.now()
        AgencyMembership.objects.filter(
            agency=self,
            user_id=self.owner_id,
            status=AgencyMembership.Status.ACTIVE,
        ).exclude(role=AgencyMembership.Role.OWNER).update(
            status=AgencyMembership.Status.LEFT,
            left_at=now,
        )
        membership, created = AgencyMembership.objects.update_or_create(
            agency=self,
            user_id=self.owner_id,
            role=AgencyMembership.Role.OWNER,
            defaults={
                "status": AgencyMembership.Status.ACTIVE,
                "left_at": None,
                "created_by_id": self.owner_id,
            },
        )
        if not created and membership.left_at:
            membership.joined_at = now
            membership.save(update_fields=["joined_at"])
        if old_owner_id and old_owner_id != self.owner_id:
            AgencyMembership.objects.filter(
                agency=self,
                user_id=old_owner_id,
                role=AgencyMembership.Role.OWNER,
                status=AgencyMembership.Status.ACTIVE,
            ).update(status=AgencyMembership.Status.LEFT, left_at=now)

    def get_absolute_url(self):
        return f"/a/{self.id}-{self.slug}/"

    def get_landing_cover_image(self):
        images = list(self.images.all())
        for img in images:
            if img.is_landing_cover:
                return img
        return images[0] if images else None


class AgencyMembership(models.Model):
    """عضویت کاربر در مشاوره املاک با نقش و وضعیت مشخص."""

    class Role(models.TextChoices):
        OWNER = "owner", "مالک"
        MANAGER = "manager", "مدیر"
        EMPLOYEE = "employee", "کارمند"

    class Status(models.TextChoices):
        ACTIVE = "active", "فعال"
        INVITED = "invited", "دعوت‌شده"
        LEFT = "left", "خارج‌شده"
        REJECTED = "rejected", "رد‌شده"

    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name="مشاوره املاک",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agency_memberships",
        verbose_name="کاربر",
    )
    role = models.CharField(
        max_length=12,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        db_index=True,
        verbose_name="نقش",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name="وضعیت",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_agency_memberships",
        verbose_name="ایجادکننده",
    )
    joined_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ شروع عضویت")
    left_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ پایان عضویت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "عضویت مشاوره املاک"
        verbose_name_plural = "عضویت‌های مشاوره املاک"
        ordering = ("agency__name", "role", "user__username")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "agency"),
                condition=models.Q(status="active"),
                name="uniq_active_agency_membership_user_agency",
            ),
        ]
        indexes = [
            models.Index(fields=("agency", "status", "role")),
            models.Index(fields=("user", "status", "role")),
            models.Index(fields=("status", "created_at")),
        ]

    def __str__(self):
        return f"{self.user} / {self.agency} / {self.get_role_display()}"

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE


class AgencyImage(models.Model):
    """گالری تصاویر مشاوره املاک."""
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="مشاوره املاک",
    )
    image = models.ImageField(upload_to=agency_image_upload_to, verbose_name="تصویر")
    alt = models.CharField(max_length=180, blank=True, verbose_name="متن جایگزین")
    caption = models.CharField(max_length=200, blank=True, verbose_name="عنوان")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_cover = models.BooleanField(default=False, verbose_name="تصویر شاخص")
    is_landing_cover = models.BooleanField(default=False, verbose_name="کاور لندینگ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر مشاوره"
        verbose_name_plural = "تصاویر مشاوره"

    def __str__(self):
        return f"Image {self.id} for {self.agency.name}"


class AgencyJoinRequest(models.Model):
    """درخواست عضویت کاربر به عنوان کارمند در مشاوره املاک."""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agency_join_requests",
        verbose_name="کاربر",
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="join_requests",
        verbose_name="مشاوره املاک",
    )
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
        verbose_name = "درخواست عضویت کارمند"
        verbose_name_plural = "درخواست‌های عضویت کارمند"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "agency"),
                condition=models.Q(status="pending"),
                name="uniq_pending_join_user_agency",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.agency}"


class AgencyEmployeeInvite(models.Model):
    """دعوت کاربر به همکاری در یک املاک توسط مالک همان املاک."""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تایید"
        ACCEPTED = "accepted", "پذیرفته شده"
        REJECTED = "rejected", "رد شده"
        CANCELED = "canceled", "لغو شده"

    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agency_invites",
        verbose_name="کاربر دعوت‌شده",
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="employee_invites",
        verbose_name="املاک",
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agency_invites_sent",
        verbose_name="دعوت‌کننده",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name="وضعیت",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ پاسخ",
    )

    class Meta:
        verbose_name = "دعوت همکاری در املاک"
        verbose_name_plural = "دعوت‌های همکاری در املاک"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("invited_user", "agency"),
                condition=models.Q(status="pending"),
                name="uniq_pending_invite_user_agency",
            ),
        ]

    def __str__(self):
        return f"دعوت {self.invited_user} برای {self.agency}"


class EmployeeRemoveRequest(models.Model):
    """درخواست حذف کارمند از مشاوره املاک — توسط صاحب مشاوره، تأیید توسط ادمین."""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="remove_requests",
        verbose_name="کارمند",
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="remove_requests",
        verbose_name="مشاوره املاک",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_remove_requests_sent",
        verbose_name="درخواست‌کننده",
    )
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
        verbose_name = "درخواست حذف کارمند"
        verbose_name_plural = "درخواست‌های حذف کارمند"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "agency"),
                condition=models.Q(status="pending"),
                name="uniq_pending_remove_user_agency",
            ),
        ]

    def __str__(self):
        return f"حذف {self.user} از {self.agency}"
