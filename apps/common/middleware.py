"""
میدلور برای فعال‌سازی زبان فارسی و RTL در پنل مدیریت
"""
from django.utils import translation


class AdminLocaleMiddleware:
    """
    برای URLهای /admin/ زبان را به فارسی تنظیم می‌کند
    تا ترجمه‌ها و جهت RTL درست اعمال شوند.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            translation.activate("fa")
            request.LANGUAGE_CODE = "fa"
        response = self.get_response(request)
        if request.path.startswith("/admin/"):
            translation.deactivate()
        return response
