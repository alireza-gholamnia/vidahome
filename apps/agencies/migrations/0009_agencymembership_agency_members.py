import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def backfill_agency_memberships(apps, schema_editor):
    Agency = apps.get_model("agencies", "Agency")
    AgencyMembership = apps.get_model("agencies", "AgencyMembership")
    User = apps.get_model("accounts", "User")
    now = timezone.now()

    for agency in Agency.objects.exclude(owner_id__isnull=True).iterator():
        AgencyMembership.objects.update_or_create(
            agency_id=agency.id,
            user_id=agency.owner_id,
            role="owner",
            defaults={
                "status": "active",
                "created_by_id": agency.owner_id,
                "joined_at": now,
                "left_at": None,
            },
        )

    for user in User.objects.exclude(agency_id__isnull=True).iterator():
        if AgencyMembership.objects.filter(
            agency_id=user.agency_id,
            user_id=user.id,
            status="active",
        ).exists():
            continue
        AgencyMembership.objects.update_or_create(
            agency_id=user.agency_id,
            user_id=user.id,
            role="employee",
            defaults={
                "status": "active",
                "joined_at": now,
                "left_at": None,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("agencies", "0008_agencyemployeeinvite"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AgencyMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("owner", "مالک"), ("manager", "مدیر"), ("employee", "کارمند")], db_index=True, default="employee", max_length=12, verbose_name="نقش")),
                ("status", models.CharField(choices=[("active", "فعال"), ("invited", "دعوت‌شده"), ("left", "خارج‌شده"), ("rejected", "رد‌شده")], db_index=True, default="active", max_length=12, verbose_name="وضعیت")),
                ("joined_at", models.DateTimeField(default=timezone.now, verbose_name="تاریخ شروع عضویت")),
                ("left_at", models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پایان عضویت")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")),
                ("agency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="agencies.agency", verbose_name="مشاوره املاک")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_agency_memberships", to=settings.AUTH_USER_MODEL, verbose_name="ایجادکننده")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="agency_memberships", to=settings.AUTH_USER_MODEL, verbose_name="کاربر")),
            ],
            options={
                "verbose_name": "عضویت مشاوره املاک",
                "verbose_name_plural": "عضویت‌های مشاوره املاک",
                "ordering": ("agency__name", "role", "user__username"),
                "indexes": [
                    models.Index(fields=["agency", "status", "role"], name="agencies_ag_agency__b3b7ea_idx"),
                    models.Index(fields=["user", "status", "role"], name="agencies_ag_user_id_deb922_idx"),
                    models.Index(fields=["status", "created_at"], name="agencies_ag_status_4f6d2e_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(condition=models.Q(("status", "active")), fields=("user", "agency"), name="uniq_active_agency_membership_user_agency"),
                ],
            },
        ),
        migrations.AddField(
            model_name="agency",
            name="members",
            field=models.ManyToManyField(blank=True, related_name="member_agencies", through="agencies.AgencyMembership", through_fields=("agency", "user"), to=settings.AUTH_USER_MODEL, verbose_name="اعضا"),
        ),
        migrations.RunPython(backfill_agency_memberships, migrations.RunPython.noop),
    ]
