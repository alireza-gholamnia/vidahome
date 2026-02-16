# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0007_add_rejection_reason"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "پیش‌نویس"),
                    ("pending", "در انتظار تأیید"),
                    ("published", "منتشر شده"),
                    ("rejected", "رد شده"),
                    ("archived", "بایگانی شده"),
                ],
                db_index=True,
                default="draft",
                max_length=12,
                verbose_name="وضعیت",
            ),
        ),
    ]
