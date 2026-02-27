import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django_ratelimit.decorators import ratelimit
from django.views.generic import RedirectView
from django.db.models import Q
from django.urls import reverse

from apps.locations.models import City, Area
from apps.categories.models import Category
from apps.seo.models import CityCategory, CityAreaCategory

from apps.blog.models import BlogPost
from apps.attributes.models import Attribute, AttributeOption, ListingAttribute

from .models import Listing
from apps.lead.models import ListingLead, LandingLead
from apps.lead.forms import ListingLeadForm, LandingLeadForm


def _user_has_name_locked(user):
    """اگر کاربر از قبل نام و نام خانوادگی داشته باشد، در فرم لید قابل تغییر نباشد (فقط از پنل)."""
    if not user or not user.is_authenticated:
        return False
    return bool((getattr(user, "first_name", "") or "").strip()) and bool((getattr(user, "last_name", "") or "").strip())


def _category_listing_filter(category):
    """فیلتر آگهی‌ها: دسته خودش + دسته‌های فرزند."""
    return Q(category=category) | Q(category__parent=category)


# =============================================================
# /s  -> لیست آگهی‌ها با فیلتر (کاتالوگ)
# =============================================================

def listing_catalog(request):
    from django.core.paginator import Paginator

    qs = (
        Listing.objects.filter(status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images")
        .order_by("-published_at", "-id")
    )

    city_slug = request.GET.get("city", "").strip()
    category_slug = request.GET.get("category", "").strip()
    area_slug = request.GET.get("area", "").strip()
    deal = request.GET.get("deal", "").strip()
    q = request.GET.get("q", "").strip()
    price_min_str = request.GET.get("price_min", "").strip()
    price_max_str = request.GET.get("price_max", "").strip()

    if city_slug:
        qs = qs.filter(city__slug=city_slug)
    if category_slug:
        qs = qs.filter(Q(category__slug=category_slug) | Q(category__parent__slug=category_slug))
    if area_slug and city_slug:
        qs = qs.filter(area__slug=area_slug, city__slug=city_slug)
    if deal in ("buy", "rent", "daily_rent", "mortgage_rent"):
        qs = qs.filter(deal=deal)
    if price_min_str:
        try:
            price_min_val = int(price_min_str)
            if price_min_val > 0:
                qs = qs.filter(price__isnull=False, price__gte=price_min_val)
        except ValueError:
            pass
    if price_max_str:
        try:
            price_max_val = int(price_max_str)
            if price_max_val > 0:
                qs = qs.filter(price__isnull=False, price__lte=price_max_val)
        except ValueError:
            pass
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(short_description__icontains=q)
            | Q(description__icontains=q)
        )

    # فیلترهای ویژگی (EAV)
    filterable_attrs = []
    if category_slug:
        cat = Category.objects.filter(slug=category_slug).first()
        if cat:
            cat_ids = list(
                Category.objects.filter(Q(pk=cat.pk) | Q(parent=cat)).values_list("id", flat=True)
            )
            filterable_attrs = list(
                Attribute.objects.filter(
                    is_filterable=True,
                    is_active=True,
                    categories__in=cat_ids,
                )
                .distinct()
                .order_by("sort_order", "id")
            )
    else:
        filterable_attrs = list(
            Attribute.objects.filter(is_filterable=True, is_active=True).order_by("sort_order", "id")
        )

    filter_attr_values = {}
    for key, val in request.GET.items():
        if key.startswith("attr_") and val:
            slug = key[5:]
            attr = next((a for a in filterable_attrs if a.slug == slug), None)
            if attr:
                filter_attr_values[attr.slug] = val

    for attr in filterable_attrs:
        val = filter_attr_values.get(attr.slug)
        if not val:
            continue
        if attr.value_type == Attribute.ValueType.INTEGER:
            try:
                v = int(val)
                qs = qs.filter(attribute_values__attribute=attr, attribute_values__value_int=v)
            except ValueError:
                pass
        elif attr.value_type == Attribute.ValueType.BOOLEAN:
            qs = qs.filter(
                attribute_values__attribute=attr,
                attribute_values__value_bool=(val == "1"),
            )
        elif attr.value_type == Attribute.ValueType.CHOICE:
            try:
                opt_id = int(val)
                qs = qs.filter(
                    attribute_values__attribute=attr,
                    attribute_values__value_option_id=opt_id,
                )
            except ValueError:
                pass
        elif attr.value_type == Attribute.ValueType.STRING:
            qs = qs.filter(
                attribute_values__attribute=attr,
                attribute_values__value_str=val,
            )
    if filter_attr_values:
        qs = qs.distinct()

    paginator = Paginator(qs, 24)
    page = request.GET.get("page", 1)
    try:
        page_num = int(page)
        if page_num < 1:
            page_num = 1
    except ValueError:
        page_num = 1
    listings = paginator.get_page(page_num)

    cities = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")
    categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by("sort_order", "fa_name")
    areas = []
    if city_slug:
        city = City.objects.filter(slug=city_slug, is_active=True).first()
        if city:
            areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "fa_name")

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "آگهی‌های املاک", "url": None},
    ]
    title = "آگهی‌های املاک"
    if city_slug and (c := City.objects.filter(slug=city_slug).first()):
        title = f"آگهی‌های {c.fa_name}"

    # گزینه‌های فیلتر ویژگی‌ها
    attr_filters = []
    for attr in filterable_attrs:
        options = [("", "همه")]
        if attr.value_type == Attribute.ValueType.INTEGER:
            opts = AttributeOption.objects.filter(attribute=attr).order_by("sort_order", "id")
            options.extend((str(opt.value), opt.value) for opt in opts)
        elif attr.value_type == Attribute.ValueType.BOOLEAN:
            options.extend([("1", "بله"), ("0", "خیر")])
        elif attr.value_type == Attribute.ValueType.CHOICE:
            opts = AttributeOption.objects.filter(attribute=attr).order_by("sort_order", "id")
            options.extend((str(opt.id), opt.value) for opt in opts)
        current = filter_attr_values.get(attr.slug, "")
        attr_filters.append({"attr": attr, "options": options, "current": current})

    # Query string for pagination (exclude page)
    from urllib.parse import urlencode
    params = dict(request.GET)
    params.pop("page", None)
    pagination_query = urlencode(params, doseq=True)

    # آگهی‌های دارای مختصات برای نقشه (صفحه فعلی)
    map_listings = []
    for l in listings:
        if l.latitude is not None and l.longitude is not None:
            map_listings.append({
                "id": l.id,
                "title": l.title,
                "lat": float(l.latitude),
                "lng": float(l.longitude),
                "url": l.get_absolute_url(),
            })

    neshan_api_key = getattr(settings, "NESHAN_API_KEY", "") or ""

    return render(
        request,
        "pages/listing_catalog.html",
        {
            "listings": listings,
            "map_listings_json": json.dumps(map_listings),
            "neshan_api_key": neshan_api_key,
            "cities": cities,
            "categories": categories,
            "areas": areas,
            "attr_filters": attr_filters,
            "breadcrumbs": breadcrumbs,
            "seo_h1": title,
            "seo_title": f"{title} | VidaHome",
            "seo_meta_description": "جستجو و مشاهده آگهی‌های خرید، فروش و اجاره املاک در VidaHome",
            "filter_city": city_slug,
            "filter_category": category_slug,
            "filter_area": area_slug,
            "filter_deal": deal,
            "filter_q": q,
            "filter_price_min": price_min_str,
            "filter_price_max": price_max_str,
            "pagination_query": pagination_query,
        },
    )




# =============================================================
# SEO helpers
# =============================================================

def _build_seo_for_city(request, city: City):
    is_noindex = (not city.allow_index) or city.seo_noindex

    default_title = f"{city.fa_name} | VidaHome"
    default_h1 = f"شهر {city.fa_name}"
    default_desc = (city.seo_meta_description or "").strip()

    canonical = city.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (city.seo_title or default_title).strip(),
        "seo_meta_description": default_desc,
        "seo_h1": (city.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (city.intro_content or "").strip(),
        "main_content": city.main_content or "",
    }


def _build_seo_for_category(request, category: Category):
    is_noindex = (not category.allow_index) or category.seo_noindex

    default_title = f"{category.fa_name} | VidaHome"
    default_h1 = category.fa_name
    default_desc = (category.seo_meta_description or "").strip()

    canonical = category.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (category.seo_title or default_title).strip(),
        "seo_meta_description": default_desc,
        "seo_h1": (category.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (category.intro_content or "").strip(),
        "main_content": category.main_content or "",
    }


def _build_seo_for_area(request, area: Area):
    is_noindex = (not area.allow_index) or area.seo_noindex

    default_title = f"محله {area.fa_name} در {area.city.fa_name} | VidaHome"
    default_h1 = f"محله {area.fa_name}"
    default_desc = f"آگهی‌ها و فایل‌های ملکی در {area.fa_name} {area.city.fa_name}. خرید، فروش، رهن و اجاره در VidaHome."

    canonical = area.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (area.seo_title or default_title).strip(),
        "seo_meta_description": (area.seo_meta_description or default_desc).strip(),
        "seo_h1": (area.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (area.intro_content or "").strip(),
        "main_content": area.main_content or "",
    }


def _build_seo_for_landing(request, landing, *, default_title: str, default_h1: str, default_desc: str):
    is_noindex = (not landing.allow_index) or landing.seo_noindex
    canonical = landing.seo_canonical or request.build_absolute_uri()

    return {
        "seo_title": (landing.seo_title or default_title).strip(),
        "seo_meta_description": (landing.seo_meta_description or default_desc).strip(),
        "seo_h1": (landing.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": (landing.intro_content or "").strip(),
        "main_content": landing.main_content or "",
    }


def _build_seo_for_listing(request, listing: Listing):
    is_noindex = (not listing.allow_index) or listing.seo_noindex

    default_title = f"{listing.title} | VidaHome"
    default_h1 = listing.title

    if listing.short_description:
        default_desc = listing.short_description.strip()
    else:
        default_desc = f"جزئیات آگهی {listing.title} در {listing.city.fa_name}."

    canonical_default = request.build_absolute_uri(listing.get_absolute_url())
    canonical = (listing.seo_canonical or canonical_default).strip()

    return {
        "seo_title": (listing.seo_title or default_title).strip(),
        "seo_meta_description": (listing.seo_meta_description or default_desc).strip(),
        "seo_h1": (listing.seo_h1 or default_h1).strip(),
        "seo_canonical": canonical,
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
        "intro_content": "",
        "main_content": "",
    }


# =============================================================
# Landing lead form helper
# =============================================================

def _landing_lead_initial_from_user(request):
    """مقادیر اولیه فرم لید لندینگ براساس پروفایل کاربر لاگین‌شده."""
    initial = {}
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        if getattr(user, "first_name", ""):
            initial["first_name"] = user.first_name
        if getattr(user, "last_name", ""):
            initial["last_name"] = user.last_name
        phone = getattr(user, "phone", "") or ""
        if phone:
            initial["phone"] = phone
        email = getattr(user, "email", "") or ""
        if email:
            initial["email"] = email
    return initial


def _landing_lead_initial(request, source_type: str, source_path: str):
    """
    مقادیر اولیه فرم لید لندینگ: اول از session (بازگشت از لاگین)، وگرنه از پروفایل کاربر.
    اگر نام قفل باشد، نام و نام‌خانوادگی همیشه از دیتابیس (پروفایل) به‌عنوان دیفالت قرار می‌گیرد.
    """
    saved = request.session.pop("landing_return_form", None)
    if saved and saved.get("source_type") == source_type and saved.get("source_path") == source_path:
        initial = {}
        if saved.get("first_name"):
            initial["first_name"] = saved["first_name"]
        if saved.get("last_name"):
            initial["last_name"] = saved["last_name"]
        if saved.get("phone"):
            initial["phone"] = saved["phone"]
        if saved.get("email"):
            initial["email"] = saved["email"]
        if saved.get("subject"):
            initial["subject"] = saved["subject"]
        if saved.get("message"):
            initial["message"] = saved["message"]
        if not initial:
            initial = _landing_lead_initial_from_user(request)
    else:
        initial = _landing_lead_initial_from_user(request)
    user = getattr(request, "user", None)
    if _user_has_name_locked(user) and user and user.is_authenticated:
        initial["first_name"] = (user.first_name or "").strip()
        initial["last_name"] = (user.last_name or "").strip()
    return initial


def _process_landing_lead_post(request, source_type: str, source_path: str, redirect_url: str):
    """اگر POST مربوط به فرم لید لندینگ باشد، پردازش کن. برمی‌گرداند (redirect_response | None, form)."""
    lock_name = _user_has_name_locked(getattr(request, "user", None))
    lock_phone = getattr(request, "user", None) and request.user.is_authenticated and bool((getattr(request.user, "phone", "") or "").strip())
    if request.method != "POST" or request.POST.get("landing_lead") != "1":
        initial = _landing_lead_initial(request, source_type, source_path)
        if lock_phone:
            initial["phone"] = (request.user.phone or "").strip()
        return None, LandingLeadForm(prefix="landing", initial=initial, lock_name_fields=lock_name, lock_phone_field=lock_phone)

    if not request.user.is_authenticated:
        first_name = (request.POST.get("landing-first_name") or "").strip()
        last_name = (request.POST.get("landing-last_name") or "").strip()
        phone = (request.POST.get("landing-phone") or "").strip()
        email = (request.POST.get("landing-email") or "").strip()
        subject = (request.POST.get("landing-subject") or "").strip()
        message = (request.POST.get("landing-message") or "").strip()
        request.session["landing_return_form"] = {
            "source_type": source_type,
            "source_path": source_path,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "subject": subject,
            "message": message,
        }
        if phone:
            request.session["login_otp_phone"] = phone
        login_url = reverse("accounts:login")
        return redirect(f"{login_url}?next={redirect_url}"), LandingLeadForm(prefix="landing")

    if getattr(request, "limited", False):
        messages.error(request, "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً یک ساعت دیگر تلاش کنید.")
        post_data = request.POST
        if (lock_name or lock_phone) and request.user.is_authenticated:
            post_data = request.POST.copy()
            if lock_name:
                post_data["landing-first_name"] = (request.user.first_name or "").strip()
                post_data["landing-last_name"] = (request.user.last_name or "").strip()
            if lock_phone:
                post_data["landing-phone"] = (request.user.phone or "").strip()
        return None, LandingLeadForm(post_data, prefix="landing", lock_name_fields=lock_name, lock_phone_field=lock_phone)

    post_data = request.POST
    if (lock_name or lock_phone) and request.user.is_authenticated:
        post_data = request.POST.copy()
        if lock_name:
            post_data["landing-first_name"] = (request.user.first_name or "").strip()
            post_data["landing-last_name"] = (request.user.last_name or "").strip()
        if lock_phone:
            post_data["landing-phone"] = (request.user.phone or "").strip()
    form = LandingLeadForm(post_data, prefix="landing", lock_name_fields=lock_name, lock_phone_field=lock_phone)
    if form.is_valid():
        user = getattr(request, "user", None)
        if lock_name and user and user.is_authenticated:
            first_name = (user.first_name or "").strip()
            last_name = (user.last_name or "").strip()
        else:
            first_name = (form.cleaned_data.get("first_name") or "").strip()
            last_name = (form.cleaned_data.get("last_name") or "").strip()
        if lock_phone and user and user.is_authenticated:
            phone = (user.phone or "").strip()
        else:
            phone = (form.cleaned_data.get("phone") or "").strip()
        email = (form.cleaned_data.get("email") or "").strip()
        subject = (form.cleaned_data.get("subject") or "").strip()
        message = (form.cleaned_data.get("message") or "").strip()
        full_name = f"{first_name} {last_name}".strip() or first_name or last_name

        LandingLead.objects.create(
            source_type=source_type,
            source_path=source_path,
            name=full_name,
            phone=phone,
            email=email,
            subject=subject,
            message=message,
        )

        if user is not None and user.is_authenticated and not lock_name:
            updated_fields = []
            if first_name and (user.first_name or "").strip() != first_name:
                user.first_name = first_name
                updated_fields.append("first_name")
            if last_name and (user.last_name or "").strip() != last_name:
                user.last_name = last_name
                updated_fields.append("last_name")
            if email and (getattr(user, "email", "") or "").strip() != email:
                user.email = email
                updated_fields.append("email")
            if updated_fields:
                user.save(update_fields=updated_fields)

        messages.success(request, "درخواست شما با موفقیت ارسال شد. به زودی با شما تماس گرفته می‌شود.")
        return redirect(redirect_url), form

    return None, form


# =============================================================
# /s/{slug}  -> City OR Category
# =============================================================

@ratelimit(key="ip", rate="5/h", method="POST")
def s_one_segment(request, slug):
    city = City.objects.filter(slug=slug, is_active=True).prefetch_related("images").first()
    if city:
        areas = Area.objects.filter(city=city, is_active=True).order_by("sort_order", "id")
        listings = (
            Listing.objects.filter(city=city, status=Listing.Status.PUBLISHED)
            .select_related("category", "area")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        seo = _build_seo_for_city(request, city)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": None},
        ]
        city_posts = (
            BlogPost.objects.filter(city=city, status=BlogPost.Status.PUBLISHED)
            .select_related("blog_category", "author")
            .order_by("-published_at", "-id")[:6]
        )
        redirect_resp, lead_form = _process_landing_lead_post(
            request, LandingLead.SourceType.CITY, city.slug, request.path
        )
        if redirect_resp:
            return redirect_resp
        return render(
            request,
            "pages/city_landing.html",
            {
                "city": city,
                "areas": areas,
                "listings": listings,
                "city_posts": city_posts,
                "breadcrumbs": breadcrumbs,
                "landing_lead_form": lead_form,
                "landing_lead_source_type": LandingLead.SourceType.CITY,
                "landing_lead_source_path": city.slug,
                **seo,
            },
        )

    category = Category.objects.filter(slug=slug, is_active=True).prefetch_related("images").first()
    if category:
        listings = (
            Listing.objects.filter(_category_listing_filter(category), status=Listing.Status.PUBLISHED)
            .select_related("city", "area", "category")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        children = Category.objects.filter(parent=category, is_active=True).order_by("sort_order", "id")
        seo = _build_seo_for_category(request, category)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "دسته‌بندی‌ها", "url": "/categories/"},
            {"title": category.fa_name, "url": None},
        ]
        category_posts = (
            BlogPost.objects.filter(
                Q(listing_category=category) | Q(listing_category__parent=category),
                status=BlogPost.Status.PUBLISHED,
            )
            .select_related("blog_category", "author")
            .order_by("-published_at", "-id")[:6]
        )
        redirect_resp, lead_form = _process_landing_lead_post(
            request, LandingLead.SourceType.CATEGORY, category.slug, request.path
        )
        if redirect_resp:
            return redirect_resp
        return render(
            request,
            "pages/category_landing.html",
            {
                "category": category,
                "listings": listings,
                "children": children,
                "category_posts": category_posts,
                "breadcrumbs": breadcrumbs,
                "landing_lead_form": lead_form,
                "landing_lead_source_type": LandingLead.SourceType.CATEGORY,
                "landing_lead_source_path": category.slug,
                **seo,
            },
        )

    raise Http404()


# =============================================================
# /s/{city}/{category} OR /s/{city}/{area}
# =============================================================

@ratelimit(key="ip", rate="5/h", method="POST")
def city_context(request, city_slug, context_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)

    area = Area.objects.filter(city=city, slug=context_slug, is_active=True).prefetch_related("images").first()
    if area:
        listings = (
            Listing.objects.filter(city=city, area=area, status=Listing.Status.PUBLISHED)
            .select_related("category", "area")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        seo = _build_seo_for_area(request, area)
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": f"/s/{city.slug}/"},
            {"title": area.fa_name, "url": None},
        ]
        redirect_resp, lead_form = _process_landing_lead_post(
            request, LandingLead.SourceType.AREA, f"{city.slug}/{area.slug}", request.path
        )
        if redirect_resp:
            return redirect_resp
        return render(
            request,
            "pages/area_landing.html",
            {
                "city": city,
                "area": area,
                "listings": listings,
                "breadcrumbs": breadcrumbs,
                "landing_lead_form": lead_form,
                "landing_lead_source_type": LandingLead.SourceType.AREA,
                "landing_lead_source_path": f"{city.slug}/{area.slug}",
                **seo,
            },
        )

    category = Category.objects.filter(slug=context_slug, is_active=True).prefetch_related("images").first()
    if category:
        landing = CityCategory.objects.filter(city=city, category=category, is_active=True).prefetch_related("images").first()

        listings = (
            Listing.objects.filter(city=city, status=Listing.Status.PUBLISHED)
            .filter(_category_listing_filter(category))
            .select_related("area", "category")
            .prefetch_related("images")
            .order_by("-published_at", "-id")[:24]
        )
        breadcrumbs = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "شهرها", "url": "/cities/"},
            {"title": city.fa_name, "url": f"/s/{city.slug}/"},
            {"title": category.fa_name, "url": None},
        ]
        redirect_resp, lead_form = _process_landing_lead_post(
            request, LandingLead.SourceType.CITY_CATEGORY, f"{city.slug}/{category.slug}", request.path
        )
        if redirect_resp:
            return redirect_resp
        lead_ctx = {
            "landing_lead_form": lead_form,
            "landing_lead_source_type": LandingLead.SourceType.CITY_CATEGORY,
            "landing_lead_source_path": f"{city.slug}/{category.slug}",
        }

        if landing:
            seo = _build_seo_for_landing(
                request,
                landing,
                default_title=f"{category.fa_name} در {city.fa_name} | VidaHome",
                default_h1=f"{category.fa_name} در {city.fa_name}",
                default_desc=f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            )
            landing_cover = landing.get_landing_cover_image()
            return render(
                request,
                "pages/city_category_landing.html",
                {"city": city, "category": category, "landing": landing, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **lead_ctx, **seo},
            )

        landing_cover = category.get_landing_cover_image()
        seo = {
            "seo_title": f"{category.fa_name} در {city.fa_name} | VidaHome",
            "seo_meta_description": f"آگهی‌های {category.fa_name} در {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
            "seo_h1": f"{category.fa_name} در {city.fa_name}",
            "seo_canonical": request.build_absolute_uri(),
            "seo_robots": "index, follow",
            "intro_content": "",
            "main_content": "",
        }
        return render(
            request,
            "pages/city_category_landing.html",
            {"city": city, "category": category, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **lead_ctx, **seo},
        )

    raise Http404()


# =============================================================
# /s/{city}/{area}/{category}
# =============================================================

@ratelimit(key="ip", rate="5/h", method="POST")
def area_category(request, city_slug, area_slug, category_slug):
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    area = get_object_or_404(Area, city=city, slug=area_slug, is_active=True)
    category = get_object_or_404(Category.objects.prefetch_related("images"), slug=category_slug, is_active=True)

    landing = CityAreaCategory.objects.filter(
        city=city,
        area=area,
        category=category,
        is_active=True
    ).prefetch_related("images").first()

    listings = (
        Listing.objects.filter(city=city, area=area, status=Listing.Status.PUBLISHED)
        .filter(_category_listing_filter(category))
        .select_related("category", "area")
        .prefetch_related("images")
        .order_by("-published_at", "-id")[:24]
    )
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "شهرها", "url": "/cities/"},
        {"title": city.fa_name, "url": f"/s/{city.slug}/"},
        {"title": area.fa_name, "url": f"/s/{city.slug}/{area.slug}/"},
        {"title": category.fa_name, "url": None},
    ]
    redirect_resp, lead_form = _process_landing_lead_post(
        request, LandingLead.SourceType.AREA_CATEGORY, f"{city.slug}/{area.slug}/{category.slug}", request.path
    )
    if redirect_resp:
        return redirect_resp
    lead_ctx = {
        "landing_lead_form": lead_form,
        "landing_lead_source_type": LandingLead.SourceType.AREA_CATEGORY,
        "landing_lead_source_path": f"{city.slug}/{area.slug}/{category.slug}",
    }

    if landing:
        seo = _build_seo_for_landing(
            request,
            landing,
            default_title=f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
            default_h1=f"{category.fa_name} در {area.fa_name}",
            default_desc=f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        )
        landing_cover = landing.get_landing_cover_image()
        return render(
            request,
            "pages/area_category_landing.html",
            {"city": city, "area": area, "category": category, "landing": landing, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **lead_ctx, **seo},
        )

    landing_cover = category.get_landing_cover_image()
    seo = {
        "seo_title": f"{category.fa_name} در {area.fa_name} {city.fa_name} | VidaHome",
        "seo_meta_description": f"آگهی‌های {category.fa_name} در {area.fa_name} {city.fa_name}. خرید، فروش، رهن و اجاره با VidaHome.",
        "seo_h1": f"{category.fa_name} در {area.fa_name}",
        "seo_canonical": request.build_absolute_uri(),
        "seo_robots": "index, follow",
        "intro_content": "",
        "main_content": "",
    }
    return render(
        request,
        "pages/area_category_landing.html",
        {"city": city, "area": area, "category": category, "landing_cover": landing_cover, "listings": listings, "breadcrumbs": breadcrumbs, **lead_ctx, **seo},
    )


# =============================================================
# /l/{id}-{slug}  -> Listing Detail
# =============================================================

def _listing_breadcrumbs(listing: Listing):
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "شهرها", "url": "/cities/"},
        {"title": listing.city.fa_name, "url": listing.city.get_absolute_url()},
    ]
    if listing.area:
        breadcrumbs.append({"title": listing.area.fa_name, "url": listing.area.get_absolute_url()})
    breadcrumbs.append({"title": listing.title, "url": None})
    return breadcrumbs


def _listing_detail_render(request, listing, **extra):
    """ریندر مشترک برای listing_detail و listing_detail_by_id."""
    if request.method == "POST" and "inquiry" in request.POST:
        # اگر کاربر لاگین نیست، قبل از ثبت استعلام او را به صفحه ورود هدایت می‌کنیم
        # و بعد از ورود، دوباره به صفحه همین آگهی برمی‌گردانیم.
        if not request.user.is_authenticated:
            # داده‌های فرم را در session ذخیره کن تا بعد از برگشت از لاگین پر شوند
            first_name = (request.POST.get("first_name") or "").strip()
            last_name = (request.POST.get("last_name") or "").strip()
            phone = (request.POST.get("phone") or "").strip()
            message = (request.POST.get("message") or "").strip()
            request.session["inquiry_return_form"] = {
                "listing_id": listing.id,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "message": message,
            }
            # شماره کاربر را برای فرم لاگین هم اتوفیل کن
            if phone:
                request.session["login_otp_phone"] = phone
            login_url = reverse("accounts:login")
            next_url = listing.get_absolute_url()
            return redirect(f"{login_url}?next={next_url}")

        lock_name = _user_has_name_locked(request.user)
        lock_phone = request.user.is_authenticated and bool((getattr(request.user, "phone", "") or "").strip())
        if getattr(request, "limited", False):
            messages.error(request, "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً یک ساعت دیگر تلاش کنید.")
            initial = {}
            if lock_name and request.user.is_authenticated:
                initial["first_name"] = (request.user.first_name or "").strip()
                initial["last_name"] = (request.user.last_name or "").strip()
            if lock_phone:
                initial["phone"] = (request.user.phone or "").strip()
            form = ListingLeadForm(initial=initial, lock_name_fields=lock_name, lock_phone_field=lock_phone)
        else:
            post_data = request.POST
            if (lock_name or lock_phone) and request.user.is_authenticated:
                post_data = request.POST.copy()
                if lock_name:
                    post_data["first_name"] = (request.user.first_name or "").strip()
                    post_data["last_name"] = (request.user.last_name or "").strip()
                if lock_phone:
                    post_data["phone"] = (request.user.phone or "").strip()
            form = ListingLeadForm(post_data, lock_name_fields=lock_name, lock_phone_field=lock_phone)
            if form.is_valid():
                user = request.user
                if lock_name:
                    first_name = (user.first_name or "").strip()
                    last_name = (user.last_name or "").strip()
                else:
                    first_name = (form.cleaned_data.get("first_name") or "").strip()
                    last_name = (form.cleaned_data.get("last_name") or "").strip()
                if lock_phone:
                    phone = (user.phone or "").strip()
                else:
                    phone = (form.cleaned_data.get("phone") or "").strip()
                message = (form.cleaned_data.get("message") or "").strip()
                ListingLead.objects.create(
                    listing=listing,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    message=message,
                )
                # تکمیل پروفایل فقط برای نام/نام خانوادگی
                if user.is_authenticated and not lock_name:
                    updated_fields = []
                    if first_name and (user.first_name or "").strip() != first_name:
                        user.first_name = first_name
                        updated_fields.append("first_name")
                    if last_name and (user.last_name or "").strip() != last_name:
                        user.last_name = last_name
                        updated_fields.append("last_name")
                    if updated_fields:
                        user.save(update_fields=updated_fields)
                messages.success(request, "استعلام شما با موفقیت ارسال شد. به زودی با شما تماس گرفته می‌شود.")
                return redirect(listing.get_absolute_url())
    else:
        # مقادیر اولیه فرم: اول از session (بازگشت از لاگین)، وگرنه از پروفایل کاربر
        initial = {}
        saved = request.session.pop("inquiry_return_form", None)
        if saved and saved.get("listing_id") == listing.id:
            if saved.get("first_name"):
                initial["first_name"] = saved["first_name"]
            if saved.get("last_name"):
                initial["last_name"] = saved["last_name"]
            if saved.get("phone"):
                initial["phone"] = saved["phone"]
            if saved.get("message"):
                initial["message"] = saved["message"]
        if not initial and request.user.is_authenticated:
            user = request.user
            if getattr(user, "first_name", None):
                initial["first_name"] = user.first_name
            if getattr(user, "last_name", None):
                initial["last_name"] = user.last_name
            phone = getattr(user, "phone", "") or ""
            if phone:
                initial["phone"] = phone
        lock_name = _user_has_name_locked(request.user)
        lock_phone = request.user.is_authenticated and bool((getattr(request.user, "phone", "") or "").strip())
        if lock_name and request.user.is_authenticated:
            initial["first_name"] = (request.user.first_name or "").strip()
            initial["last_name"] = (request.user.last_name or "").strip()
        if lock_phone:
            initial["phone"] = (request.user.phone or "").strip()
        form = ListingLeadForm(initial=initial, lock_name_fields=lock_name, lock_phone_field=lock_phone)

    related_listings = (
        Listing.objects.filter(
            status=Listing.Status.PUBLISHED
        )
        .exclude(id=listing.id)
        .filter(city=listing.city)
        .select_related("city", "area", "category")
        .prefetch_related("images", "attribute_values__attribute")
        .order_by("-published_at", "-id")[:8]
    )
    if not related_listings.exists():
        related_listings = (
            Listing.objects.filter(status=Listing.Status.PUBLISHED)
            .exclude(id=listing.id)
            .select_related("city", "area", "category")
            .prefetch_related("images", "attribute_values__attribute")
            .order_by("-published_at", "-id")[:8]
        )

    amenity_attrs = [av for av in listing.attribute_values.all() if av.value_bool]
    seo = _build_seo_for_listing(request, listing)
    breadcrumbs = _listing_breadcrumbs(listing)
    neshan_api_key = getattr(settings, "NESHAN_API_KEY", "") or ""
    return render(
        request,
        "pages/listing_detail.html",
        {
            "listing": listing,
            "breadcrumbs": breadcrumbs,
            "related_listings": related_listings,
            "amenity_attrs": amenity_attrs,
            "neshan_api_key": neshan_api_key,
            "inquiry_form": form,
            **seo,
            **extra,
        },
    )


@ratelimit(key="ip", rate="10/h", method="POST")
def listing_detail(request, listing_id: int, slug: str):
    listing = (
        Listing.objects
        .select_related("city", "area", "category", "agency", "created_by", "created_by__agency")
        .prefetch_related("images", "attribute_values__attribute", "attribute_values__value_option", "created_by__owned_agencies")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )
    if not listing:
        raise Http404()
    return _listing_detail_render(request, listing)


@ratelimit(key="ip", rate="10/h", method="POST")
def listing_detail_by_id(request, listing_id: int):
    listing = (
        Listing.objects
        .select_related("city", "area", "category", "agency", "created_by", "created_by__agency")
        .prefetch_related("images", "attribute_values__attribute", "attribute_values__value_option", "created_by__owned_agencies")
        .filter(id=listing_id, status=Listing.Status.PUBLISHED)
        .first()
    )
    if not listing:
        raise Http404()
    return _listing_detail_render(
        request,
        listing,
        seo_canonical=request.build_absolute_uri(listing.get_absolute_url()),
    )
