from django.test import TestCase

from apps.categories.models import Category
from apps.listings.models import Listing
from apps.locations.models import Area, City, Province


class LandingInternalLinkTests(TestCase):
    def setUp(self):
        self.province = Province.objects.create(
            fa_name="تهران",
            en_name="tehran",
            slug="tehran-province",
        )
        self.city = City.objects.create(
            province=self.province,
            fa_name="تهران",
            en_name="tehran",
            slug="tehran",
            is_active=True,
        )
        self.area = Area.objects.create(
            city=self.city,
            fa_name="الهیه",
            en_name="elahiyeh",
            slug="elahiyeh",
            is_active=True,
        )
        self.category = Category.objects.create(
            fa_name="ویلا",
            en_name="Villa Test",
            slug="villa-test",
            is_active=True,
        )
        self.child_category = Category.objects.create(
            parent=self.category,
            fa_name="ویلا لاکچری",
            en_name="Luxury Villa Test",
            slug="luxury-villa-test",
            is_active=True,
        )
        Listing.objects.create(
            title="ویلا در الهیه",
            city=self.city,
            area=self.area,
            category=self.child_category,
            status=Listing.Status.PUBLISHED,
        )

    def test_city_landing_shows_category_and_area_category_links(self):
        response = self.client.get(f"/s/{self.city.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"ویلا در {self.city.fa_name}")
        self.assertContains(response, f"/s/{self.city.slug}/{self.category.slug}/")
        self.assertContains(response, f"ویلا در {self.area.fa_name} {self.city.fa_name}")
        self.assertContains(response, f"/s/{self.city.slug}/{self.area.slug}/{self.category.slug}/")

    def test_category_landing_shows_corresponding_city_and_area_links(self):
        response = self.client.get(f"/s/{self.category.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"ویلا در {self.city.fa_name}")
        self.assertContains(response, f"/s/{self.city.slug}/{self.category.slug}/")
        self.assertContains(response, f"ویلا در {self.area.fa_name} {self.city.fa_name}")
        self.assertContains(response, f"/s/{self.city.slug}/{self.area.slug}/{self.category.slug}/")
