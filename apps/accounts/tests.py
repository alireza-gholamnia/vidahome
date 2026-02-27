from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import OTPRequest
from apps.accounts.services import verify_otp
from apps.accounts.views import LOGIN_NEXT_URL_KEY, LOGIN_OTP_PHONE_KEY
from apps.agencies.models import Agency
from apps.common.sms import normalize_phone

User = get_user_model()


class PhoneNormalizationTests(TestCase):
    def test_normalize_phone_with_persian_digits(self):
        self.assertEqual(normalize_phone("۰۹۱۲۱۲۳۴۵۶۷"), "09121234567")


class OTPSecurityTests(TestCase):
    def test_verify_otp_is_single_use(self):
        phone = "09121234567"
        OTPRequest.objects.create(phone=phone, code="12345")

        first_user = verify_otp(phone, "12345")
        self.assertIsNotNone(first_user)
        self.assertEqual(first_user.phone, phone)

        second_user = verify_otp(phone, "12345")
        self.assertIsNone(second_user)
        self.assertFalse(OTPRequest.objects.filter(phone=phone).exists())


class LoginRedirectSafetyTests(TestCase):
    @patch("apps.accounts.views.request_otp", return_value=(True, "ok"))
    def test_login_does_not_store_external_next_url(self, _mock_request_otp):
        response = self.client.post(
            reverse("accounts:login"),
            {"phone": "09121234567", "next": "https://evil.example/phish"},
        )
        self.assertRedirects(response, reverse("accounts:otp_verify"), fetch_redirect_response=False)

        session = self.client.session
        self.assertNotIn(LOGIN_NEXT_URL_KEY, session)
        self.assertEqual(session.get(LOGIN_OTP_PHONE_KEY), "09121234567")

    @patch("apps.accounts.views.verify_otp")
    def test_verify_otp_rejects_external_next_url(self, mock_verify_otp):
        user = User.objects.create_user(username="u1", phone="09120000001", password="x")
        mock_verify_otp.return_value = user

        session = self.client.session
        session[LOGIN_OTP_PHONE_KEY] = "09120000001"
        session.save()

        response = self.client.post(
            f"{reverse('accounts:otp_verify')}?next=https://evil.example/phish",
            {"code": "12345"},
        )
        self.assertRedirects(response, "/panel/", fetch_redirect_response=False)


class UserPhoneConstraintTests(TestCase):
    def test_phone_must_be_unique_when_not_empty(self):
        User.objects.create_user(username="p1", phone="09125550000", password="x")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="p2", phone="09125550000", password="x")


class AgencySlugUniquenessTests(TestCase):
    def test_agency_slug_collision_is_resolved(self):
        owner = User.objects.create_user(username="owner", phone="09123334444", password="x")
        first = Agency.objects.create(name="املاک تست", owner=owner)
        second = Agency.objects.create(name="املاک تست", owner=owner)

        self.assertNotEqual(first.slug, second.slug)
        self.assertTrue(second.slug.endswith("-2"))
