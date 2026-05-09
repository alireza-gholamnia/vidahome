# Generated manually to align agency onboarding with approval flow.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agencies", "0009_agencymembership_agency_members"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agency",
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
