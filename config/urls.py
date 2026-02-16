"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from config import admin as admin_config  # noqa: F401 — تنظیم عناوین ادمین
from django.urls import path, include

from apps.common import views as common_views
from apps.agencies import views as agency_views
from apps.listings import views as listing_views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("panel/", include("apps.panel.urls")),
    path("agencies/", agency_views.agency_list, name="agency_list"),
    path("listings/", listing_views.listing_catalog, name="listing_catalog"),
    path("a/", include("apps.agencies.urls")),
    path("agent/", include("apps.agencies.agent_urls")),
    path("cities/", include("apps.locations.urls")),
    path("s/", include("apps.listings.search_urls")),
    path("l/", include("apps.listings.detail_urls")),
    path("categories/", include("apps.categories.urls")),
    path("blog/", include("apps.blog.urls")),
    path("", common_views.home, name="home"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)