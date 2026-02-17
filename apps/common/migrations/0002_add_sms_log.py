# Generated manually for SmsLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_add_contact_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="SmsLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("receptor", models.CharField(db_index=True, max_length=20, verbose_name="شماره گیرنده")),
                ("message", models.TextField(verbose_name="محتوا")),
                ("response_json", models.TextField(blank=True, verbose_name="پاسخ JSON کاوه‌نگار")),
                ("is_success", models.BooleanField(default=False, verbose_name="موفق")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")),
            ],
            options={
                "verbose_name": "لاگ پیامک",
                "verbose_name_plural": "لاگ پیامک‌های ارسالی",
                "ordering": ("-created_at",),
            },
        ),
    ]
