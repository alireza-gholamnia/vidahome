# Generated manually - multi-agency per owner + approval workflow

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("agencies", "0003_slug_to_english"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="agency",
            name="approval_status",
            field=models.CharField(
                choices=[
                    ("pending", "در انتظار تأیید"),
                    ("approved", "تأیید شده"),
                    ("rejected", "رد شده"),
                ],
                db_index=True,
                default="approved",
                max_length=12,
                verbose_name="وضعیت تأیید",
            ),
        ),
        migrations.AlterField(
            model_name="agency",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_agencies",
                to=settings.AUTH_USER_MODEL,
                verbose_name="مالک",
            ),
        ),
    ]
