from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponse
from django.conf import settings
from django.apps import apps
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm
from apps.lead.models import LandingLead


STATIC_PAGES = {
    "about": {
        "title": "درباره VidaHome",
        "subtitle": "پلتفرم تخصصی جستجو، معرفی و مدیریت خدمات و آگهی‌های ملکی",
        "description": "VidaHome با تمرکز بر مدل‌سازی درست داده، SEO و تجربه کاربری فارسی ساخته شده تا مسیر جستجوی ملک، مشاور املاک و سرویس‌های مرتبط با ملک شفاف‌تر شود.",
        "sections": [
            {
                "title": "ماموریت ما",
                "body": "ساخت یک مرجع قابل اعتماد برای جستجوی ملک، معرفی مشاوران املاک و اتصال کاربران به سرویس‌دهندگان معتبر حوزه ملک.",
                "items": [
                    "لندینگ‌های SEO محور برای شهر، محله و دسته‌بندی",
                    "ساختار داده قابل توسعه برای آگهی‌ها و ویژگی‌ها",
                    "تفکیک شفاف بین مشاور املاک، کارشناس و ارائه‌دهنده خدمات",
                ],
            },
            {
                "title": "رویکرد فنی",
                "body": "پروژه به‌صورت Django Monolith و Server-Side Rendered توسعه داده شده تا صفحات سریع، قابل crawl و قابل نگهداری باشند.",
                "items": [
                    "Django Templates برای خروجی HTML پایدار",
                    "مدل‌های دامنه‌ای برای شهر، محله، دسته، آگهی، مشاوره و سرویس",
                    "SEO قابل کنترل از دیتابیس و مسیرهای تمیز URL",
                ],
            },
        ],
        "cards": [
            {"title": "SEO-first", "text": "لینک‌سازی داخلی و صفحات لندینگ برای رشد ارگانیک طراحی شده‌اند."},
            {"title": "Data-driven", "text": "محتوا، تصاویر، دسته‌ها، شهرها و ویژگی‌ها از دیتابیس مدیریت می‌شوند."},
            {"title": "RTL Native", "text": "رابط کاربری برای زبان فارسی و بازار ایران ساخته شده است."},
        ],
        "cta_title": "برای همکاری یا ارسال پیشنهاد آماده‌ایم",
        "cta_text": "اگر مشاور املاک، ارائه‌دهنده خدمات یا مالک کسب‌وکار مرتبط با ملک هستید، از صفحه تماس با ما پیام بفرستید.",
        "cta_label": "تماس با ما",
        "cta_url_name": "contact",
        "seo_meta_description": "درباره VidaHome؛ پلتفرم تخصصی جستجوی ملک، مشاوران املاک و خدمات مرتبط با ملک.",
    },
    "terms": {
        "title": "قوانین و مقررات",
        "subtitle": "شرایط استفاده از VidaHome",
        "description": "استفاده از VidaHome به معنی پذیرش قوانین عمومی پلتفرم است. این متن نسخه اولیه برای محصول در حال توسعه است و باید پیش از انتشار نهایی با مشاور حقوقی بازبینی شود.",
        "sections": [
            {
                "title": "مسئولیت کاربران",
                "body": "کاربران باید اطلاعات صحیح، قابل بررسی و غیرگمراه‌کننده ثبت کنند.",
                "items": [
                    "ثبت آگهی تکراری، جعلی یا دارای اطلاعات نادرست مجاز نیست.",
                    "شماره تماس، قیمت، موقعیت و توضیحات باید با واقعیت آگهی هماهنگ باشد.",
                    "کاربر مسئول محتوایی است که در پنل یا فرم‌های سایت ثبت می‌کند.",
                ],
            },
            {
                "title": "مسئولیت پلتفرم",
                "body": "VidaHome بستر انتشار و معرفی است و طرف معامله ملکی محسوب نمی‌شود.",
                "items": [
                    "تأیید آگهی به معنی تضمین حقوقی معامله نیست.",
                    "کاربران باید پیش از هر پرداخت یا قرارداد، بررسی حقوقی و میدانی انجام دهند.",
                    "VidaHome می‌تواند آگهی یا حساب ناقض قوانین را حذف یا محدود کند.",
                ],
            },
        ],
        "cta_title": "ابهام حقوقی دارید؟",
        "cta_text": "برای سؤال درباره قوانین استفاده از سایت، با پشتیبانی تماس بگیرید.",
        "cta_label": "ارسال پیام",
        "cta_url_name": "contact",
        "seo_meta_description": "قوانین و مقررات استفاده از VidaHome برای کاربران، مشاوران و ارائه‌دهندگان خدمات.",
    },
    "privacy": {
        "title": "حریم خصوصی",
        "subtitle": "نحوه جمع‌آوری، نگهداری و استفاده از داده‌ها",
        "description": "VidaHome برای ارائه خدمات بهتر، بخشی از اطلاعات حساب، تماس و فعالیت کاربران را ذخیره می‌کند. این متن نسخه اولیه سیاست حریم خصوصی است.",
        "sections": [
            {
                "title": "داده‌هایی که ذخیره می‌شود",
                "body": "اطلاعات مورد نیاز برای ورود، ثبت آگهی، ارسال استعلام و مدیریت پنل ذخیره می‌شود.",
                "items": [
                    "شماره موبایل برای ورود OTP و ارتباط ضروری",
                    "نام، ایمیل و پیام‌های ارسالی در فرم‌های تماس و استعلام",
                    "آگهی‌ها، تصاویر، موقعیت ملک و داده‌های پنل کاربری",
                ],
            },
            {
                "title": "استفاده از داده‌ها",
                "body": "داده‌ها برای احراز هویت، پاسخ‌گویی، مدیریت آگهی و بهبود تجربه کاربری استفاده می‌شود.",
                "items": [
                    "ارسال کد ورود و پیام‌های ضروری",
                    "پیگیری درخواست‌های تماس و استعلام",
                    "بهبود کیفیت محتوا، امنیت و گزارش‌های مدیریتی",
                ],
            },
        ],
        "cta_title": "درخواست مرتبط با اطلاعات شخصی",
        "cta_text": "برای اصلاح یا پیگیری اطلاعات ثبت‌شده، از فرم تماس با ما استفاده کنید.",
        "cta_label": "تماس با پشتیبانی",
        "cta_url_name": "contact",
        "seo_meta_description": "سیاست حریم خصوصی VidaHome درباره اطلاعات کاربران، OTP، آگهی‌ها و فرم‌های تماس.",
    },
    "faq": {
        "title": "سوالات متداول",
        "subtitle": "پاسخ کوتاه به پرسش‌های رایج کاربران",
        "description": "در این صفحه پاسخ سوال‌های پرتکرار درباره جستجوی ملک، ثبت آگهی، مشاوران املاک و سرویس‌ها آمده است.",
        "sections": [
            {
                "title": "چطور ملک پیدا کنم؟",
                "body": "از صفحه آگهی‌ها، شهر، محله، دسته‌بندی، نوع معامله و ویژگی‌ها را انتخاب کنید تا نتایج محدودتر شوند.",
                "items": ["مسیر اصلی جستجو: `/listings/`", "صفحات لندینگ: `/s/{city}/` و `/s/{city}/{area}/{category}/`"],
            },
            {
                "title": "چطور آگهی ثبت کنم؟",
                "body": "بعد از ورود با شماره موبایل، از پنل کاربری وارد بخش آگهی‌ها شوید. آگهی‌های جدید ابتدا در وضعیت انتظار تأیید قرار می‌گیرند.",
                "items": ["ورود با OTP انجام می‌شود.", "برای ثبت آگهی فعال باید دسترسی مشاوره املاک معتبر داشته باشید."],
            },
            {
                "title": "سرویس‌ها چه کاربردی دارند؟",
                "body": "بخش سرویس‌ها برای معرفی شرکت‌ها یا افراد ارائه‌دهنده خدمات مرتبط با ملک مثل بازسازی، طراحی داخلی و مشاوره حقوقی است.",
                "items": ["دایرکتوری سرویس‌ها: `/services/`", "لیست ارائه‌دهندگان: `/services/providers/`"],
            },
        ],
        "cta_title": "پاسخ سوال خود را پیدا نکردید؟",
        "cta_text": "پیام خود را برای تیم پشتیبانی ارسال کنید.",
        "cta_label": "تماس با ما",
        "cta_url_name": "contact",
        "seo_meta_description": "سوالات متداول VidaHome درباره جستجوی ملک، ثبت آگهی، مشاوران املاک و سرویس‌ها.",
    },
    "safety": {
        "title": "راهنمای امنیت معاملات",
        "subtitle": "نکات ضروری قبل از بازدید، پرداخت و امضای قرارداد",
        "description": "معاملات ملکی نیازمند بررسی دقیق است. VidaHome بستر معرفی و جستجو است و جایگزین مشاوره حقوقی، کارشناسی رسمی یا بررسی حضوری نیست.",
        "sections": [
            {
                "title": "قبل از بازدید",
                "body": "اطلاعات آگهی، مالکیت، قیمت و موقعیت ملک را با چند منبع بررسی کنید.",
                "items": [
                    "از پرداخت بیعانه قبل از احراز هویت طرف مقابل خودداری کنید.",
                    "آدرس و مشخصات ملک را با سند و مدارک معتبر تطبیق دهید.",
                    "بازدید را در زمان مناسب و با همراه انجام دهید.",
                ],
            },
            {
                "title": "قبل از قرارداد",
                "body": "قرارداد ملکی را بدون بررسی حقوقی و احراز مالکیت امضا نکنید.",
                "items": [
                    "استعلام سند، پایان‌کار، بدهی‌ها و محدودیت‌های حقوقی ضروری است.",
                    "از قراردادهای دستی مبهم یا بدون شاهد معتبر پرهیز کنید.",
                    "پرداخت‌ها را فقط از مسیرهای قابل پیگیری انجام دهید.",
                ],
            },
        ],
        "cta_title": "نیاز به راهنمایی دارید؟",
        "cta_text": "برای دریافت مشاوره اولیه، از فرم تماس یا ارائه‌دهندگان خدمات حقوقی استفاده کنید.",
        "cta_label": "مشاهده سرویس‌ها",
        "cta_url_name": "services:directory",
        "seo_meta_description": "راهنمای امنیت معاملات ملکی؛ نکات بازدید، پرداخت، قرارداد و احراز مالکیت در VidaHome.",
    },
    "advertising": {
        "title": "تبلیغات و همکاری",
        "subtitle": "همکاری با VidaHome برای مشاوران، کسب‌وکارها و ارائه‌دهندگان خدمات",
        "description": "VidaHome امکان معرفی مشاوران املاک، کارشناسان و ارائه‌دهندگان خدمات مرتبط با ملک را در ساختاری SEO محور فراهم می‌کند.",
        "sections": [
            {
                "title": "مناسب چه کسانی است؟",
                "body": "کسب‌وکارهای فعال در اکوسیستم ملک می‌توانند از صفحات اختصاصی و لینک‌سازی هدفمند استفاده کنند.",
                "items": [
                    "مشاوران و آژانس‌های املاک",
                    "شرکت‌ها و افراد ارائه‌دهنده خدمات ملک",
                    "تولیدکنندگان محتوای تخصصی حوزه ملک",
                ],
            },
            {
                "title": "مزیت همکاری",
                "body": "ساختار صفحات بر اساس شهر، محله، دسته‌بندی و سرویس طراحی شده تا مخاطب هدف دقیق‌تر به شما برسد.",
                "items": [
                    "صفحه اختصاصی برای برند یا شخص",
                    "نمایش در دسته‌بندی‌ها و شهرهای مرتبط",
                    "فرم‌های تماس و لید برای پیگیری درخواست‌ها",
                ],
            },
        ],
        "cta_title": "درخواست همکاری ثبت کنید",
        "cta_text": "اطلاعات کسب‌وکار خود را ارسال کنید تا شرایط همکاری بررسی شود.",
        "cta_label": "ارسال درخواست",
        "cta_url_name": "contact",
        "seo_meta_description": "تبلیغات و همکاری با VidaHome برای مشاوران املاک، ارائه‌دهندگان خدمات و کسب‌وکارهای حوزه ملک.",
    },
}


def home(request):
    City = apps.get_model("locations", "City")
    Category = apps.get_model("categories", "Category")
    Listing = apps.get_model("listings", "Listing")
    User = apps.get_model("accounts", "User")
    Agency = apps.get_model("agencies", "Agency")
    AgencyMembership = apps.get_model("agencies", "AgencyMembership")

    top_cities = (
        City.objects.filter(is_active=True)
        .annotate(
            listing_count=Count(
                "listings",
                filter=Q(listings__status=Listing.Status.PUBLISHED),
                distinct=True,
            )
        )
        .prefetch_related("images")
        .order_by("-listing_count", "sort_order", "fa_name")[:12]
    )
    top_categories = (
        Category.listing_queryset()
        .filter(is_active=True, parent__isnull=True)
        .exclude(category_type=Category.CategoryType.SERVICE)
        .annotate(
            listing_count=Count(
                "listings",
                filter=Q(listings__status=Listing.Status.PUBLISHED),
                distinct=True,
            )
            + Count(
                "children__listings",
                filter=Q(children__listings__status=Listing.Status.PUBLISHED),
                distinct=True,
            )
        )
        .prefetch_related("images", "children")
        .order_by("-listing_count", "sort_order", "fa_name")[:12]
    )
    service_categories = (
        Category.objects.filter(
            category_type=Category.CategoryType.SERVICE,
            is_active=True,
            parent__isnull=True,
        )
        .annotate(
            provider_count=Count(
                "service_providers",
                filter=Q(
                    service_providers__approval_status="approved",
                    service_providers__is_active=True,
                ),
                distinct=True,
            )
        )
        .prefetch_related("images")
        .order_by("-provider_count", "sort_order", "fa_name")[:6]
    )
    recent_listings = (
        Listing.objects.filter(status=Listing.Status.PUBLISHED)
        .select_related("city", "area", "category")
        .prefetch_related("images", "attribute_values__attribute")
        .order_by("-published_at", "-id")[:8]
    )
    top_offers = (
        Listing.objects.filter(status=Listing.Status.PUBLISHED, price__isnull=False)
        .select_related("city", "area", "category")
        .prefetch_related("images", "attribute_values__attribute")
        .order_by("-published_at", "-id")[:8]
    )
    top_agents = (
        User.objects.filter(is_active=True)
        .filter(
            (
                Q(agency_memberships__status=AgencyMembership.Status.ACTIVE)
                & Q(agency_memberships__agency__is_active=True)
                & Q(agency_memberships__agency__approval_status=Agency.ApprovalStatus.APPROVED)
            )
            | Q(owned_agencies__is_active=True, owned_agencies__approval_status=Agency.ApprovalStatus.APPROVED)
            | Q(agency__is_active=True, agency__approval_status=Agency.ApprovalStatus.APPROVED)
        )
        .select_related("agency")
        .prefetch_related(
            "owned_agencies",
            Prefetch(
                "agency_memberships",
                queryset=AgencyMembership.objects.filter(
                    status=AgencyMembership.Status.ACTIVE,
                    agency__is_active=True,
                    agency__approval_status=Agency.ApprovalStatus.APPROVED,
                ).select_related("agency"),
                to_attr="active_agency_memberships",
            ),
            "groups",
        )
        .distinct()
        .order_by("first_name", "last_name", "username")[:6]
    )

    return render(
        request,
        "pages/home.html",
        {
            "top_cities": top_cities,
            "top_categories": top_categories,
            "service_categories": service_categories,
            "recent_listings": recent_listings,
            "top_offers": top_offers,
            "top_agents": top_agents,
        },
    )


def _static_page(request, key):
    page = STATIC_PAGES[key]
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": page["title"], "url": None},
    ]
    return render(
        request,
        "pages/static_page.html",
        {
            "page": page,
            "breadcrumbs": breadcrumbs,
            "seo_title": f"{page['title']} | VidaHome",
            "seo_meta_description": page.get("seo_meta_description", page.get("description", "")),
        },
    )


def about(request):
    return _static_page(request, "about")


def terms(request):
    return _static_page(request, "terms")


def privacy(request):
    return _static_page(request, "privacy")


def faq(request):
    return _static_page(request, "faq")


def safety(request):
    return _static_page(request, "safety")


def advertising(request):
    return _static_page(request, "advertising")


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
