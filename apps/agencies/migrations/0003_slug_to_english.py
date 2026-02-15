# Generated manually - convert existing agency slugs from Persian to English

from django.db import migrations


def slug_to_english(apps, schema_editor):
    from apps.common.text_utils import slugify_from_title

    Agency = apps.get_model("agencies", "Agency")
    for agency in Agency.objects.all():
        base = slugify_from_title(agency.name, max_length=200) or f"agency-{agency.id}"
        slug = base
        n = 1
        while Agency.objects.filter(slug=slug).exclude(pk=agency.pk).exists():
            slug = f"{base}-{n}"[:200]
            n += 1
        agency.slug = slug
        agency.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("agencies", "0002_slug_blank_english"),
    ]

    operations = [
        migrations.RunPython(slug_to_english, noop),
    ]
