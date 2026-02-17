"""انتقال داده از ListingInquiry به ListingLead."""
from django.db import migrations


def migrate_inquiries(apps, schema_editor):
    ListingInquiry = apps.get_model("listings", "ListingInquiry")
    ListingLead = apps.get_model("lead", "ListingLead")
    for inv in ListingInquiry.objects.all():
        ListingLead.objects.create(
            listing_id=inv.listing_id,
            name=inv.name,
            phone=inv.phone,
            message=inv.message or "",
            status=inv.status,
            created_at=inv.created_at,
        )


def reverse_migrate(apps, schema_editor):
    ListingLead = apps.get_model("lead", "ListingLead")
    ListingLead.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("lead", "0001_initial"),
        ("listings", "0012_add_inquiry_status"),
    ]

    operations = [
        migrations.RunPython(migrate_inquiries, reverse_migrate),
    ]
