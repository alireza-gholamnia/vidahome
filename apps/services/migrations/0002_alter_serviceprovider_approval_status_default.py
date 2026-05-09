# Generated manually to align service provider onboarding with approval flow.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceprovider",
            name="approval_status",
            field=models.CharField(
                choices=[
                    ("pending", "در انتظار تأیید"),
                    ("approved", "تأیید شده"),
                    ("rejected", "رد شده"),
                ],
                db_index=True,
                default="pending",
                max_length=12,
                verbose_name="وضعیت تأیید",
            ),
        ),
    ]
