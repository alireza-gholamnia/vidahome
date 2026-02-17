"""
پاک‌سازی تمام ارتباطات کاربر با مشاوره‌ها (بدون حذف خود کاربر).
استفاده: python manage.py clear_user_agency_data <username>
مثال: python manage.py clear_user_agency_data farzad
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = "پاک‌سازی agency، مالکیت مشاوره‌ها و گروه‌های کاربر — بدون حذف خود کاربر"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="نام کاربری کاربر (مثل farzad یا 09121234567)")

    def handle(self, *args, **options):
        username = options["username"].strip()
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            user = User.objects.filter(
                first_name__icontains="فرزاد",
                last_name__icontains="رضازاده",
            ).first()
        if not user:
            self.stderr.write(self.style.ERROR(f"User not found: {username}"))
            return

        self.stdout.write(f"Processing user: {user.username}")

        # 1. Clear user.agency
        if user.agency_id:
            self.stdout.write(f"  - Clearing agency (pk={user.agency_id})")
            user.agency = None
            user.save(update_fields=["agency"])

        # 2. Transfer agency ownership to first superuser
        from apps.agencies.models import Agency

        agencies = Agency.objects.filter(owner=user)
        if agencies.exists():
            new_owner = User.objects.filter(is_superuser=True).exclude(pk=user.pk).first()
            if not new_owner:
                new_owner = User.objects.filter(is_staff=True).exclude(pk=user.pk).first()
            if not new_owner:
                new_owner = User.objects.exclude(pk=user.pk).first()
            if not new_owner:
                self.stderr.write(self.style.ERROR("No other user found. Agencies not transferred."))
            else:
                for ag in agencies:
                    self.stdout.write(f"  - Transferring agency pk={ag.pk} to {new_owner.username}")
                    ag.owner = new_owner
                    ag.save(update_fields=["owner"])

        # 3. Remove from agency_owner and agency_employee groups
        for group_name in ("agency_owner", "agency_employee"):
            g = Group.objects.filter(name=group_name).first()
            if g and user.groups.filter(pk=g.pk).exists():
                user.groups.remove(g)
                self.stdout.write(f"  - Removed from group: {group_name}")

        self.stdout.write(self.style.SUCCESS("Done."))
