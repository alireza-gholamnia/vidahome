# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("agencies", "0004_multi_agency_and_approval"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgencyJoinRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "در انتظار تأیید"),
                            ("approved", "تأیید شده"),
                            ("rejected", "رد شده"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=12,
                        verbose_name="وضعیت",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درخواست"),
                ),
                (
                    "reviewed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ بررسی"
                    ),
                ),
                (
                    "agency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="join_requests",
                        to="agencies.agency",
                        verbose_name="مشاوره املاک",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agency_join_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name": "درخواست عضویت کارمند",
                "verbose_name_plural": "درخواست‌های عضویت کارمند",
                "ordering": ("-created_at",),
            },
        ),
    ]
