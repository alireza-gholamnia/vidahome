"""
میدلور برای فعال‌سازی زبان فارسی و RTL در پنل مدیریت
و محدود کردن دسترسی به ادمین Django فقط برای superuser
"""
from django.shortcuts import redirect
from django.utils import translation


class AdminAccessMiddleware:
    """
    دسترسی به /admin/ فقط برای superuser و site_admin لاگین‌شده.
    کاربر لاگین‌نشده → ریدایرکت به صفحه ورود.
    کاربر لاگین‌شده ولی بدون دسترسی → ریدایرکت به پنل.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated:
                return redirect("/accounts/login/")
            if not (request.user.is_superuser or request.user.groups.filter(name="site_admin").exists()):
                return redirect("/panel/")
        return self.get_response(request)


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


class ResponseCacheControlMiddleware:
    """
    Set pragmatic cache headers for HTML responses.
    - Authenticated or panel/admin/account pages: private/no-store
    - Public HTML pages: short public cache
    - sitemap/robots: longer cache
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method not in ("GET", "HEAD"):
            return response
        if response.status_code != 200:
            return response

        path = (request.path or "").lower()
        content_type = (response.get("Content-Type") or "").lower()

        if path.endswith("/sitemap.xml") or path.endswith("/robots.txt"):
            response["Cache-Control"] = "public, max-age=3600"
            return response

        if request.user.is_authenticated or path.startswith(("/panel/", "/accounts/", "/admin/", "/ckeditor/")):
            response["Cache-Control"] = "private, no-store"
            return response

        if "text/html" in content_type:
            response["Cache-Control"] = "public, max-age=300, s-maxage=600, stale-while-revalidate=30"

        return response
