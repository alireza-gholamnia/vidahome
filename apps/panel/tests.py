from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.agencies.models import Agency, AgencyEmployeeInvite, AgencyMembership
from apps.attributes.models import Attribute, ListingAttribute
from apps.categories.models import Category
from apps.listings.models import Listing
from apps.locations.models import City, Province
from apps.services.models import ServiceProvider

User = get_user_model()


class AttributesJsonAccessTests(TestCase):
    def setUp(self):
        self.province = Province.objects.create(fa_name="تهران", en_name="tehran")
        self.city = City.objects.create(province=self.province, fa_name="تهران", en_name="tehran")
        self.category = Category.objects.create(fa_name="آپارتمان", en_name="apartment")
        self.attribute = Attribute.objects.create(
            name="طبقه",
            slug="floor",
            value_type=Attribute.ValueType.STRING,
            is_active=True,
        )
        self.attribute.categories.add(self.category)

        self.owner1 = User.objects.create_user(username="owner1", phone="09120000010", password="x")
        self.owner2 = User.objects.create_user(username="owner2", phone="09120000020", password="x")

        self.agency1 = Agency.objects.create(
            name="املاک یک",
            owner=self.owner1,
            approval_status=Agency.ApprovalStatus.APPROVED,
            is_active=True,
        )
        self.agency2 = Agency.objects.create(
            name="املاک دو",
            owner=self.owner2,
            approval_status=Agency.ApprovalStatus.APPROVED,
            is_active=True,
        )

        self.listing1 = Listing.objects.create(
            title="ملک یک",
            city=self.city,
            category=self.category,
            agency=self.agency1,
            created_by=self.owner1,
            status=Listing.Status.PENDING,
        )
        listing_attr, _ = ListingAttribute.objects.get_or_create(
            listing=self.listing1,
            attribute=self.attribute,
        )
        listing_attr.value_str = "طبقه سوم"
        listing_attr.save(update_fields=["value_str"])

    def test_current_values_are_hidden_for_other_users_listing(self):
        self.client.force_login(self.owner2)
        response = self.client.get(
            reverse("panel:attributes_json"),
            {"category_id": self.category.id, "listing_id": self.listing1.id},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        attr_payload = next(x for x in data if x["id"] == self.attribute.id)
        self.assertIsNone(attr_payload["current_value"])

    def test_current_values_are_visible_for_owner(self):
        self.client.force_login(self.owner1)
        response = self.client.get(
            reverse("panel:attributes_json"),
            {"category_id": self.category.id, "listing_id": self.listing1.id},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        attr_payload = next(x for x in data if x["id"] == self.attribute.id)
        self.assertEqual(attr_payload["current_value"], "طبقه سوم")


class InvitePolicyTests(TestCase):
    def setUp(self):
        self.inviter = User.objects.create_user(username="inviter", phone="09120000100", password="x")
        self.target = User.objects.create_user(username="target", phone="09120000200", password="x")

        self.approved_agency = Agency.objects.create(
            name="املاک فعال",
            owner=self.inviter,
            approval_status=Agency.ApprovalStatus.APPROVED,
            is_active=True,
        )
        self.pending_owned_agency = Agency.objects.create(
            name="املاک در انتظار",
            owner=self.target,
            approval_status=Agency.ApprovalStatus.PENDING,
            is_active=True,
        )

    def test_owner_cannot_be_invited_even_if_owns_only_pending_agency(self):
        self.client.force_login(self.inviter)
        response = self.client.post(
            reverse("panel:agency_employees"),
            {
                "action": "add_employee",
                "agency_id": self.approved_agency.id,
                "identifier": self.target.username,
            },
        )
        self.assertRedirects(response, reverse("panel:agency_employees"), fetch_redirect_response=False)
        self.assertFalse(
            AgencyEmployeeInvite.objects.filter(
                invited_user=self.target,
                agency=self.approved_agency,
                status=AgencyEmployeeInvite.Status.PENDING,
            ).exists()
        )

    def test_agency_owner_membership_is_created(self):
        self.assertTrue(
            AgencyMembership.objects.filter(
                agency=self.approved_agency,
                user=self.inviter,
                role=AgencyMembership.Role.OWNER,
                status=AgencyMembership.Status.ACTIVE,
            ).exists()
        )

    def test_accept_invite_creates_employee_membership(self):
        candidate = User.objects.create_user(username="candidate", phone="09120000300", password="x")
        invite = AgencyEmployeeInvite.objects.create(
            invited_user=candidate,
            agency=self.approved_agency,
            invited_by=self.inviter,
            status=AgencyEmployeeInvite.Status.PENDING,
        )

        self.client.force_login(candidate)
        response = self.client.post(
            reverse("panel:employee_request_join"),
            {"action": "accept_invite", "invite_id": invite.id},
        )

        self.assertRedirects(response, reverse("panel:employee_my_agency"), fetch_redirect_response=False)
        self.assertTrue(
            AgencyMembership.objects.filter(
                agency=self.approved_agency,
                user=candidate,
                role=AgencyMembership.Role.EMPLOYEE,
                status=AgencyMembership.Status.ACTIVE,
            ).exists()
        )


class ServiceProviderPanelTests(TestCase):
    def setUp(self):
        self.province = Province.objects.create(fa_name="تهران", en_name="tehran")
        self.city = City.objects.create(province=self.province, fa_name="تهران", en_name="tehran", is_active=True)
        self.category = Category.objects.create(
            category_type=Category.CategoryType.SERVICE,
            fa_name="بازسازی",
            en_name="renovation",
            is_active=True,
        )
        self.user = User.objects.create_user(username="service-owner", phone="09120000900", password="x")
        self.admin = User.objects.create_superuser(username="admin", phone="09120000999", password="x")

    def test_user_can_create_pending_service_provider_from_panel(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("panel:service_provider_add"),
            {
                "name": "گروه خدمات تست",
                "provider_type": ServiceProvider.ProviderType.COMPANY,
                "categories": [self.category.id],
                "cities": [self.city.id],
                "mobile": "09120000900",
                "phone": "",
                "email": "",
                "website": "",
                "address": "تهران",
                "intro_content": "توضیح کوتاه خدمات",
                "main_content": "",
            },
        )

        self.assertRedirects(response, reverse("panel:service_provider_list"), fetch_redirect_response=False)
        provider = ServiceProvider.objects.get(owner=self.user)
        self.assertEqual(provider.approval_status, ServiceProvider.ApprovalStatus.PENDING)
        self.assertEqual(provider.categories.get(), self.category)
        self.assertEqual(provider.cities.get(), self.city)

    def test_site_admin_can_approve_service_provider(self):
        provider = ServiceProvider.objects.create(
            name="ارائه‌دهنده در انتظار",
            owner=self.user,
            provider_type=ServiceProvider.ProviderType.PERSON,
            mobile="09120000900",
            approval_status=ServiceProvider.ApprovalStatus.PENDING,
            is_active=True,
        )
        provider.categories.add(self.category)
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("panel:approve_service_provider", args=[provider.id]),
            {"action": "approve"},
        )

        self.assertRedirects(
            response,
            reverse("panel:approve_dashboard") + "?tab=pending",
            fetch_redirect_response=False,
        )
        provider.refresh_from_db()
        self.assertEqual(provider.approval_status, ServiceProvider.ApprovalStatus.APPROVED)
        self.assertTrue(provider.is_active)
