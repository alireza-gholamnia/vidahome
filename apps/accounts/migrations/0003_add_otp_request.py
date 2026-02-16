from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_agency"),
    ]

    operations = [
        migrations.CreateModel(
            name="OTPRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(db_index=True, max_length=20, verbose_name="شماره موبایل")),
                ("code", models.CharField(max_length=10, verbose_name="کد")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")),
            ],
            options={
                "verbose_name": "درخواست OTP",
                "verbose_name_plural": "درخواست‌های OTP",
                "ordering": ("-created_at",),
            },
        ),
    ]
