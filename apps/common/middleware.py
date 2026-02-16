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
