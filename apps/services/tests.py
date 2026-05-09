from django.test import TestCase

from apps.categories.models import Category
from apps.services.models import ServiceProvider


class ServicesSmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_type=Category.CategoryType.SERVICE,
            fa_name="بازسازی",
            en_name="Renovation Test",
            slug="renovation-test",
        )
        self.provider = ServiceProvider.objects.create(
            name="شرکت تست سرویس",
            slug="test-service-provider",
            provider_type=ServiceProvider.ProviderType.COMPANY,
            approval_status=ServiceProvider.ApprovalStatus.APPROVED,
            is_active=True,
            mobile="09120000000",
        )
        self.provider.categories.add(self.category)

    def test_service_directory_renders(self):
        response = self.client.get("/services/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "سرویس‌های ملک")

    def test_service_provider_list_renders(self):
        response = self.client.get("/services/providers/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ارائه‌دهندگان خدمات")
        self.assertContains(response, self.provider.name)

    def test_service_provider_list_filters_by_category(self):
        other_category = Category.objects.create(
            category_type=Category.CategoryType.SERVICE,
            fa_name="نظافت",
            en_name="Cleaning Test",
            slug="cleaning-test",
        )

        response = self.client.get("/services/providers/", {"category": other_category.slug})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.provider.name)

    def test_service_category_renders_providers(self):
        response = self.client.get(f"/services/{self.category.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.provider.name)

    def test_service_provider_detail_renders(self):
        response = self.client.get(self.provider.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.provider.name)
