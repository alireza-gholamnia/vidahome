"""
Context processors for global template variables.
"""


def header_cities(request):
    """
    Provides all active cities for the header dropdown.
    """
    from django.apps import apps

    City = apps.get_model("locations", "City")
    cities = City.objects.filter(is_active=True).order_by("sort_order", "id")
    return {"header_cities": list(cities)}
