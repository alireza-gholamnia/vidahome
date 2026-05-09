from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.categories.models import Category
from apps.lead.models import LandingLead
from apps.services.models import ServiceProvider

User = get_user_model()


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

    def test_logged_in_user_can_submit_service_provider_lead(self):
        user = User.objects.create_user(
            username="service-lead-user",
            phone="09120000001",
            password="x",
            first_name="علی",
            last_name="رضایی",
        )
        self.client.force_login(user)

        response = self.client.post(
            self.provider.get_absolute_url(),
            {
                "service_lead": "1",
                "service-email": "ali@example.com",
                "service-subject": "درخواست بازسازی",
                "service-message": "برای بازسازی خانه تماس بگیرید.",
            },
        )

        self.assertRedirects(response, self.provider.get_absolute_url(), fetch_redirect_response=False)
        lead = LandingLead.objects.get(source_type=LandingLead.SourceType.SERVICE_PROVIDER)
        self.assertEqual(lead.source_path, str(self.provider.id))
        self.assertEqual(lead.name, "علی رضایی")
        self.assertEqual(lead.phone, "09120000001")
