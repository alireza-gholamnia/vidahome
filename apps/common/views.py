from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.apps import apps
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm
from apps.lead.models import LandingLead


def home(request):
    City = apps.get_model("locations", "City")
    Category = apps.get_model("categories", "Category")
    Listing = apps.get_model("listings", "Listing")

    top_cities = City.objects.filter(is_active=True).order_by("sort_order")[:12]
    top_categories = Category.landing_queryset().filter(is_active=True, parent__isnull=True).order_by("sort_order")[:12]
    recent_listings = (
        Listing.objects.filter(status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images", "attribute_values__attribute")
        .order_by("-published_at", "-id")[:8]
    )

    return render(
        request,
        "pages/home.html",
        {
            "top_cities": top_cities,
            "top_categories": top_categories,
            "recent_listings": recent_listings,
        },
    )


@ratelimit(key="ip", rate="5/h", method="POST")
def contact(request):
    """صفحه تماس با ما."""
    was_limited = getattr(request, "limited", False)
    if request.method == "POST" and was_limited:
        messages.error(request, "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً یک ساعت دیگر تلاش کنید.")
        form = ContactForm()
    elif request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            LandingLead.objects.create(
                source_type=LandingLead.SourceType.CONTACT,
                source_path="contact",
                name=form.cleaned_data["name"],
                email=form.cleaned_data.get("email", ""),
                phone=form.cleaned_data.get("phone", ""),
                subject=form.cleaned_data.get("subject", ""),
                message=form.cleaned_data["message"],
            )
            messages.success(request, "پیام شما با موفقیت ارسال شد. به زودی با شما تماس گرفته می‌شود.")
            return redirect("contact")
    else:
        form = ContactForm()

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "تماس با ما", "url": None},
    ]
    return render(
        request,
        "pages/contact.html",
        {
            "form": form,
            "breadcrumbs": breadcrumbs,
            "seo_title": "تماس با ما | VidaHome",
            "seo_meta_description": "با VidaHome تماس بگیرید. سوالات و پیشنهادات خود را با ما در میان بگذارید.",
        },
    )


def robots_txt(request):
    """Dynamic robots.txt with sitemap location."""
    site_url = (getattr(settings, "SITE_URL", "") or "").strip().rstrip("/")
    if not site_url:
        site_url = request.build_absolute_uri("/").rstrip("/")

    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /panel/",
            f"Sitemap: {site_url}/sitemap.xml",
            "",
        ]
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
