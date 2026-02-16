# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0006_add_pending_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="rejection_reason",
            field=models.TextField(
                blank=True,
                help_text="توضیح ادمین هنگام رد آگهی؛ به صاحب آگهی نمایش داده می‌شود.",
                verbose_name="علت رد",
            ),
        ),
    ]
