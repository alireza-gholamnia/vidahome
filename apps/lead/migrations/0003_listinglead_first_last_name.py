# Generated migration: first_name, last_name on ListingLead + backfill from name

from django.db import migrations, models


def backfill_first_last_name(apps, schema_editor):
    ListingLead = apps.get_model("lead", "ListingLead")
    for lead in ListingLead.objects.all():
        if lead.name:
            parts = lead.name.strip().split(None, 1)
            lead.first_name = parts[0] if parts else ""
            lead.last_name = parts[1] if len(parts) > 1 else ""
            lead.save(update_fields=["first_name", "last_name"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("lead", "0002_migrate_listing_inquiry"),
    ]

    operations = [
        migrations.AddField(
            model_name="listinglead",
            name="first_name",
            field=models.CharField(blank=True, max_length=60, verbose_name="نام"),
        ),
        migrations.AddField(
            model_name="listinglead",
            name="last_name",
            field=models.CharField(blank=True, max_length=60, verbose_name="نام خانوادگی"),
        ),
        migrations.AlterField(
            model_name="listinglead",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="نام + نام خانوادگی؛ برای نمایش و جستجو",
                max_length=120,
                verbose_name="نام کامل",
            ),
        ),
        migrations.RunPython(backfill_first_last_name, noop),
    ]
