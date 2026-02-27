from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.agencies.models import Agency, AgencyEmployeeInvite
from apps.attributes.models import Attribute, ListingAttribute
from apps.categories.models import Category
from apps.listings.models import Listing
from apps.locations.models import City, Province

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
