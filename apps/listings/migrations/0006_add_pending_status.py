# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0005_add_deal_types_and_price_mortgage"),
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
                    ("archived", "بایگانی شده"),
                ],
                db_index=True,
                default="draft",
                max_length=12,
                verbose_name="وضعیت",
            ),
        ),
    ]
