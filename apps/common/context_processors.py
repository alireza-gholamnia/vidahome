"""
Context processors for global template variables.
"""
from django.conf import settings
from django.templatetags.static import static


def header_cities(request):
    """
    Provides all active cities for the header dropdown.
    """
    from django.apps import apps

    City = apps.get_model("locations", "City")
    cities = City.objects.filter(is_active=True).order_by("sort_order", "id")
    return {"header_cities": list(cities)}


def seo_defaults(request):
    """Global SEO defaults for all templates."""
    site_name = getattr(settings, "SITE_NAME", "VidaHome")
    default_desc = getattr(
        settings,
        "SEO_DEFAULT_DESCRIPTION",
        "پلتفرم آگهی، جستجو و مدیریت املاک و خدمات مرتبط با پوشش شهر و محله.",
    )
    current_url = request.build_absolute_uri()
    default_og_image = request.build_absolute_uri(
        static(getattr(settings, "SEO_DEFAULT_OG_IMAGE_PATH", "img/real-estate/illustrations/find.jpg"))
    )
    return {
        "site_name": site_name,
        "default_meta_description": default_desc,
        "current_url": current_url,
        "default_og_image": default_og_image,
    }
