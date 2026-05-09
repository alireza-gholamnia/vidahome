from django.test import TestCase


class StaticPageTests(TestCase):
    def test_required_static_pages_render(self):
        pages = [
            ("/about/", "درباره VidaHome"),
            ("/contact/", "تماس با ما"),
            ("/terms/", "قوانین و مقررات"),
            ("/privacy/", "حریم خصوصی"),
            ("/faq/", "سوالات متداول"),
            ("/safety/", "راهنمای امنیت معاملات"),
            ("/advertising/", "تبلیغات و همکاری"),
        ]

        for path, title in pages:
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, title)
