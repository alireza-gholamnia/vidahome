# Generated manually to support service provider leads.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lead", "0004_alter_landinglead_source_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="landinglead",
            name="source_type",
            field=models.CharField(
                choices=[
                    ("city", "لندینگ شهر"),
                    ("category", "لندینگ دسته"),
                    ("area", "لندینگ محله"),
                    ("city_category", "لندینگ شهر+دسته"),
                    ("area_category", "لندینگ محله+دسته"),
                    ("contact", "صفحه تماس با ما"),
                    ("service_provider", "ارائه‌دهنده خدمات"),
                    ("other", "سایر"),
                ],
                db_index=True,
                max_length=20,
                verbose_name="نوع صفحه",
            ),
        ),
    ]
