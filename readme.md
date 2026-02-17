# VidaHome — Complete Project Description

**Django Monolith + Django Templates (SSR)**

> ⚠️ This document is written primarily for **AI systems** and automated agents.  
> It is the **single source of truth** for understanding, maintaining, and extending the VidaHome project.

---

## 1. Vision & Philosophy

VidaHome یک پلتفرم حرفه‌ای، مقیاس‌پذیر و **SEO-first** در حوزه املاک است که با هدف حل مشکلات بنیادی بازار املاک طراحی شده است؛  
نه صرفاً ساخت یک وب‌سایت آگهی.

### Problems VidaHome Solves

- ساختار ضعیف و غیرمنطقی دسته‌بندی در سایت‌های املاک
- فیلترهای محدود، غیرقابل توسعه و وابسته به UI
- SEO ناکارآمد، غیرقابل کنترل و وابسته به hardcode
- قاطی شدن مفاهیم دامنه‌ای (نوع ملک، نوع معامله، ویژگی‌ها)
- ناتوانی در توسعه به شهرها، مناطق و سناریوهای پیچیده

VidaHome از ابتدا با رویکردی **سیستمی، الگوریتمی و دیتامحور** طراحی شده و تمرکز آن روی **Correct Domain Modeling** است.

---

## 2. Quick Start

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone and enter project
cd vidahome

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install django django-ckeditor Pillow

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Seed sample data (optional)
python manage.py seed_data --clear

# Generate placeholder images (optional — برای شهرها، محلات، دسته‌ها، آگهی‌ها، مشاوره‌ها، بلاگ)
python manage.py generate_placeholder_images

# Run development server
python manage.py runserver
```

### Admin

- URL: `/admin/`
- Manage: Users, Groups, Agencies, Provinces, Cities (با گالری تصاویر), Areas (با گالری تصاویر), Categories (با گالری تصاویر), Listings (با ویژگی‌های EAV), **Attributes** (ویژگی، گزینه ویژگی، ویژگی آگهی), SEO overrides (CityCategory, CityAreaCategory) هرکدام با گالری تصاویر

---

## 3. Architecture Overview

### Monolithic Django Architecture (Root-based)

پروژه به‌صورت **Django Monolith کلاسیک** و بدون لایه‌ی اضافی backend پیاده‌سازی شده است.  
Django مستقیماً در روت پروژه قرار دارد و مسئول **routing، rendering، ORM و SEO** است.

```
vidahome/
├── manage.py
├── db.sqlite3
├── config/
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── apps/
│   ├── common/           # Home view, context processors, upload_utils
│   ├── accounts/         # Custom User, login, signup, logout
│   ├── agencies/         # Agency, AgencyImage
│   ├── locations/        # Province, City, Area
│   ├── categories/       # Category (tree-based)
│   ├── attributes/       # EAV: Attribute, AttributeOption, ListingAttribute
│   ├── listings/         # Listing, ListingImage, search & detail views
│   ├── blog/             # (scaffolded)
│   └── seo/              # BaseSEO, CityCategory, CityAreaCategory
├── templates/
│   ├── base/             # base.html, head.html, scripts.html
│   ├── partials/         # header, footer, hero, carousels, modals, etc.
│   ├── pages/            # home, cities, categories, search landings, listing_detail
│   ├── accounts/         # login.html, signup.html
│   └── errors/           # 404.html
├── static/               # CSS, JS, img (Bootstrap RTL, theme, vendor)
└── media/                # User uploads (listings, ckeditor)
```

### Tech Stack

| Component | Choice |
|-----------|--------|
| Backend | Django 6.x |
| Database | SQLite (dev) / PostgreSQL (prod recommended) |
| Templates | Django Templates (SSR) |
| UI | Bootstrap 5 RTL, local assets |
| Rich Text | django-ckeditor, ckeditor-uploader (image upload) |
| Number formatting | django.contrib.humanize (intcomma برای جداکننده هزارگان) |
| Language | Persian (fa), RTL |

### Architectural Rationale

- سادگی عملیاتی و کاهش پیچیدگی ذهنی
- SEO طبیعی و قابل کنترل با Server-Side Rendering
- عدم نیاز به hydration، SPA routing یا frontend framework
- کنترل کامل HTML خروجی
- مناسب crawl گوگل و بازار ایران

---

## 4. URL System (Final & Non-Negotiable)

### Current Routes

| URL | Description |
|-----|-------------|
| `/` | Home |
| `/cities/` | Cities directory |
| `/categories/` | Categories directory |
| `/accounts/` | Redirect to `/accounts/login/` |
| `/accounts/login/` | ورود |
| `/accounts/signup/` | ثبت‌نام |
| `/accounts/logout/` | خروج (POST only) |
| `/agencies/` | لیست مشاوره‌های املاک (فیلتر شهر: `?city=`) |
| `/agents/` | لیست کارشناسان (صاحب/کارمند مشاوره — فیلتر شهر: `?city=`) |
| `/a/` | Redirect to `/agencies/` |
| `/a/{id}-{slug}/` | Agency landing (canonical) |
| `/a/{id}/` | Agency landing (ID-only) |
| `/agent/{id}-{slug}/` | Agent (کارشناس) landing (canonical) |
| `/agent/{id}/` | Agent landing (ID-only) |
| `/listings/` | کاتالوگ آگهی‌ها با فیلتر (شهر، دسته، محله، نوع معامله، جستجو) |
| `/s/` | Redirect to `/listings/` |
| `/s/{slug}/` | City landing OR Category landing (resolver) |
| `/s/{city}/{context}/` | Area landing OR City+Category landing (resolver) |
| `/s/{city}/{area}/{category}/` | Area + Category landing |
| `/l/{id}-{slug}/` | Listing detail (canonical) |
| `/l/{id}/` | Listing detail (ID-only) |
| `/blog/` | بلاگ (لیست پست‌ها) |
| `/blog/category/<slug>/` | پست‌های دسته‌بندی بلاگ |
| `/blog/<slug>/` | صفحه تک پست |
| `/admin/` | Django Admin |

### Rules

- `city / area / category` → URL path only
- `deal` → query param only (`?deal=buy` | `?deal=rent` | `?deal=daily_rent` | `?deal=mortgage_rent`)
- `attributes` → query params only
- Default deal = `buy`
- Redirects: `/s/` → `/listings/`، `/a/` → `/agencies/`

### Listing Detail

- ID = source of truth
- slug = SEO only
- Independent from city/category paths

### Planned (Not Yet Implemented)

- `/about`, `/contact`, `/terms`, `/privacy`

---

## 5. Domain Models

### 5.1 locations

**Province → City → Area**

- **Province**: DB-only (not in URL)
- **City**: `slug` globally unique, exposed at `/s/{city}/`; intro_content, main_content (RichTextUploadingField)
- **CityImage**: گالری تصاویر شهر — is_cover (کارت شهر), is_landing_cover (کاور لندینگ), is_content_image, alt, caption
- **Area**: `slug` unique per city, exposed at `/s/{city}/{area}/`; intro_content, main_content (RichTextUploadingField)
- **AreaImage**: گالری تصاویر محله — همان ساختار CityImage

### 5.2 categories

- Tree-based (parent/child)
- `slug` globally unique
- Deal-independent
- intro_content, main_content (RichTextUploadingField)
- **CategoryImage**: گالری تصاویر دسته — is_cover, is_landing_cover, is_content_image, alt, caption
- Used in `/s/{category}/`, `/s/{city}/{category}/`, etc.

### 5.3 listings

- **Listing**: title, slug (پر شده خودکار از عنوان با ترانسلیتریشن فارسی), city, area (optional), category, deal, status, published_at, short_description, description (RichText), price, price_mortgage, price_unit, BaseSEO
- **Deal types:** `buy` (فروش), `rent` (اجاره), `daily_rent` (اجاره روزانه), `mortgage_rent` (رهن و اجاره)
- **Pricing (deal-dependent):**
  - فروش/اجاره/اجاره روزانه: `price` + `price_unit`
  - رهن و اجاره: `price_mortgage` (مبلغ رهن) + `price` (اجاره ماهانه) + `price_unit`
- **Helpers:** `get_deal_display_fa()`, `has_price_display()`
- **ListingImage**: listing FK, image, alt, sort_order, is_cover

### 5.4 seo

- **BaseSEO**: seo_title, seo_meta_description, seo_h1, seo_canonical, seo_noindex, allow_index, seo_priority
- **CityCategory**: SEO override for `/s/{city}/{category}/`; intro_content, main_content (RichTextUploadingField)
- **CityCategoryImage**: گالری تصاویر لندینگ شهر+دسته
- **CityAreaCategory**: SEO override for `/s/{city}/{area}/{category}/`; intro_content, main_content (RichTextUploadingField)
- **CityAreaCategoryImage**: گالری تصاویر لندینگ محله+دسته

### 5.5 accounts

- **User** (Custom User, `AUTH_USER_MODEL`): extends AbstractUser
  - `phone`, `avatar`, `is_verified`, `agency` (FK to Agency)
  - `get_role_display()` — نقش از Django Groups
- **نقش‌ها:** از طریق Django Groups تعیین می‌شوند — `site_admin`, `seo_admin`, `member`, `agency_owner`, `agency_employee`
- **نقش پیش‌فرض:** کاربران جدید به‌طور خودکار نقش `member` دریافت می‌کنند (سیگنال `post_save`)
- **انحصار نقش‌ها:** `member`, `agency_owner`, `agency_employee` انحصاری‌اند — هر کاربر فقط یکی را دارد؛ هنگام تأیید درخواست تغییر نقش، نقش قبلی حذف و نقش جدید اضافه می‌شود
- **جلوگیری از درخواست نقش دوم:** کاربران دارای `agency_owner` یا `agency_employee` نمی‌توانند نقش دیگر درخواست دهند
- Login: OTP (موبایل), `SignUpView`, Logout: `CustomLogoutView` (POST)

### 5.6 agencies

- **Agency**: name, slug (انگلیسی خودکار از نام با slugify_from_title), owner (OneToOne User), logo, cities (M2M), intro_content, main_content
- **AgencyImage**: گالری تصاویر مشاوره
- **employees**: reverse از `User.agency` — کاربران با agency پر شده
- **URL:** `/a/{id}-{slug}/` (مثل آگهی‌ها)

### 5.7 blog

- **BlogCategory**: slug, fa_name, sort_order, is_active — دسته‌بندی داخلی بلاگ
- **BlogPost**: title, slug, excerpt, content, cover_image, published_at, status, author, blog_category, city, area, listing_category — ارتباط با لندینگ‌ها (city, area, listing_category)

### 5.8 attributes (EAV)

- **Attribute**: name, slug, value_type (integer | boolean | choice | string), unit, **icon** (FileField، آپلود PNG/SVG، max 64KB، 128×128)، categories (M2M), sort_order, is_active, is_filterable (نمایش در فیلتر کاتالوگ)
- **AttributeOption**: مقادیر از پیش تعریف‌شده (مثل ۱، ۲، ۳ برای تعداد اتاق)
- **ListingAttribute**: مقدار هر ویژگی برای هر آگهی — value_int, value_bool, value_str, value_option (FK)
- همگام‌سازی خودکار با دسته‌بندی: سینگال رکوردهای ListingAttribute را بر اساس دستهٔ آگهی ایجاد/حذف می‌کند
- همگام‌سازی به AttributeOption: مقادیر جدید واردشده در آگهی به گزینه‌های ویژگی اضافه می‌شوند
- ادمین آگهی: دکمه «بارگذاری ویژگی‌های دسته‌بندی» برای ذخیره و لود ویژگی‌ها؛ اسکرول خودکار به بخش ویژگی‌ها
- Unique: (listing, attribute)

---

## 6. Templates System

### Structure

```
templates/
├── base/
│   ├── base.html        # Main layout, dir="rtl"
│   ├── head.html        # Meta, CSS, SEO injection
│   └── scripts.html     # JS vendors
├── partials/
│   ├── header.html      # Navbar, cities dropdown, logo, ورود/خروج/منوی کاربر
│   ├── footer.html
│   ├── hero.html
│   ├── services.html
│   ├── Topofferscarousel.html
│   ├── Recentlyadded.html
│   ├── Citiescarousel.html
│   ├── Partnerscarousel.html
│   ├── Topagentslnkedcarousel.html
│   ├── Propertycostcalculator.html
│   ├── Propertycostcalculatormodal.html
│   ├── Propertycategories.html
│   ├── SignInModal.html
│   ├── SignUpModal.html
│   ├── breadcrumbs.html
│   ├── blog_post_card.html
│   ├── loading_spinner.html
│   └── Backtotopbutton.html
├── pages/
│   ├── home.html
│   ├── cities.html
│   ├── categories.html
│   ├── city_landing.html
│   ├── area_landing.html
│   ├── category_landing.html
│   ├── city_category_landing.html
│   ├── area_category_landing.html
│   ├── agency_landing.html
│   ├── agency_list.html
│   ├── agent_list.html
│   ├── listing_catalog.html
│   ├── listing_detail.html
│   ├── blog_index.html
│   ├── blog_category.html
│   └── blog_post_detail.html
├── accounts/
│   ├── login.html        # صفحه ورود (قالب signin-light)
│   └── signup.html       # صفحه ثبت‌نام (قالب signup-light)
└── errors/
    └── 404.html
```

### Conventions

- All pages extend `base/base.html`
- Content in `{% block content %}` or `{% block body %}`
- Images use `{% load static %}` and `{% static 'path' %}`
- SEO injected via context (seo_title, seo_meta_description, etc.)

---

## 7. Context Processors

| Processor | Purpose |
|-----------|---------|
| `apps.common.context_processors.header_cities` | Provides `header_cities` (all active cities) for the header dropdown |

Registered in `config/settings/base.py` → `TEMPLATES['OPTIONS']['context_processors']`.

---

## 8. Static & Media

### Static

- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [PROJECT_DIR / "static"]`
- Assets: Bootstrap RTL, theme.min.css, vendor libs, img/logo, img/real-estate/*

### Media

- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = PROJECT_DIR / "media"`
- `CKEDITOR_UPLOAD_PATH = "uploads/"` — مسیر واحد آپلود ریچ‌تکست و تصاویر محتوا
- **مسیرهای ذخیره تصاویر:**
  - آیکون ویژگی‌ها: `attribute_icons/`
  - لیستینگ: `listings/%Y/%m/`
  - شهر، محله، دسته، لندینگ‌ها: `uploads/cities/`, `uploads/areas/`, `uploads/categories/`, `uploads/city_category/`, `uploads/area_category/`
  - CKEditor (ریچ‌تکست): `uploads/%Y/%m/`

### Image Paths

All template image references use `{% static 'img/...' %}`.  
Placeholder/demo images (e.g. `img/real-estate/recent/`, `img/real-estate/catalog/`) must exist in `static/img/` or will 404.

### Placeholder Images (Pillow)

دستور `generate_placeholder_images` تصاویر placeholder با Pillow می‌سازد و به مدل‌ها متصل می‌کند:

```bash
python manage.py generate_placeholder_images       # فقط برای موارد بدون تصویر
python manage.py generate_placeholder_images --force  # جایگزینی همه
```

**موجودیت‌ها:** City, Area, Category, Listing, ListingImage, Agency, AgencyImage, CityCategory, CityAreaCategory, BlogPost  
**متن روی تصاویر:** انگلیسی (en_name، slug، …)

---

## 9. Rendering Strategy

- Full server-side HTML rendering
- Data fetched directly from ORM
- JavaScript is optional and UX-only (carousels, modals)
- Fast, Crawlable, Debuggable, Stable

---

## 10. Routing Resolver Logic

### `/s/{slug}/`

1. City (if `City.slug` matches)
2. Category (if `Category.slug` matches)
3. 404

### `/s/{city}/{context}/`

1. Area (if `Area.slug` matches and belongs to city)
2. Category (if `Category.slug` matches)
3. 404

### Slug Collision Prevention

- `Category.slug` must not match any `City.slug`
- `Area.slug` must not match any `Category.slug`

---

## 11. Documentation & Update Protocol (MANDATORY)

This README is a **living document** and the only authoritative reference.

### Update Rules

- After **every meaningful commit**, add a new entry to the Change Log.
- Each entry must describe: What, Why, Next step.
- Any AI reading this file must be able to **continue development without asking clarifying questions**.

---

## 12. Project Change Log

### Version 0 — Project Bootstrap (Completed)

- Django monolith initialized, multi-env settings, domain apps scaffolded.
- **Next step:** Implement location domain model.

---

### Version 1 — Locations Domain & Cities Directory (Completed)

- Province, City, Area models; `/cities/` page.
- **Next step:** Implement `/s/{city}` search entry.

---

### Version 2 — Search Namespace + City Landing (Completed)

- `/s/` namespace; `/s/{city}/` city landing.
- **Next step:** Add categories and `/s/{city}/{category}/`.

---

### Version 3 — Area Discovery + Area Landing (Completed)

- Area discovery on city landing; `/s/{city}/{area}/`.
- **Next step:** Categories domain.

---

### Version 4 — Categories Domain (Tree-Based) (Completed)

- Category model with parent/child; Admin.
- **Next step:** Search URL resolver for `/s/{slug}/`, `/s/{city}/{category}/`.

---

### Version 5 — Search URL System Completed (Completed)

- Full grammar: category, city, city+category, city+area, city+area+category.
- **Next step:** Listing model + ORM filtering.

---

### Version 6 — Fix `/s/{slug}` Ambiguity (Completed)

- Single resolver for City vs Category.
- **Next step:** Listing model.

---

### Version 7 — Prevent Slug Collisions (Completed)

- Cross-app validation; no circular imports.
- **Next step:** Listing model.

---

### Version 8 — Template System Rebuild + Bootstrap RTL (Completed)

- New template structure; local Bootstrap RTL.
- **Next step:** Listing model.

---

### Version 9 — SEO Landing System (Completed)

- BaseSEO, CityCategory, CityAreaCategory; DB-driven SEO for all search routes.
- **Next step:** Listing model.

---

### Version 10 — Listings Domain + /l/ Detail Routes (Completed)

- Listing, ListingImage models; `/l/{id}-{slug}/`, `/l/{id}/`; Listing SEO.
- **Next step:** Wire listings to search landing pages (ORM filtering + pagination).

---

### Version 11 — Header & Navigation + Static Image Paths (Completed)

**Scope:** Fix navigation and static asset loading.

**What was implemented**

- Replaced demo header links with real project URLs (`/`, `/cities/`, `/categories/`).
- Added cities dropdown under "شهرها" with "همه شهرها" + all active cities from DB.
- Created `apps.common.context_processors.header_cities` to provide `header_cities` to all templates.
- Registered context processor in `config/settings/base.py`.
- Fixed all image paths in templates to use `{% static 'img/...' %}`:
  - hero.html, footer.html, SignInModal.html, SignUpModal.html
  - services.html, Propertycostcalculator.html
  - Topofferscarousel.html, Topagentslnkedcarousel.html
  - Partnerscarousel.html, Citiescarousel.html, Recentlyadded.html

**Architectural intent**

- Single source of navigation; no broken links to static HTML demos.
- Cities dropdown populated from DB; no hardcoding.
- All assets loaded via Django static system for correct resolution in any URL context.

**Result**

- Header navigation works correctly.
- Cities dropdown shows all active cities.
- Image paths resolve correctly (404 only if file missing in static/).

**Next step**

- Add missing image files to `static/img/real-estate/recent/`, `static/img/real-estate/catalog/`, `static/img/real-estate/city/` if needed.
- Wire listing ORM filtering + pagination to search landing pages.
- Replace static "ملک های جدید" content in Recentlyadded with real listings from DB.

---

### Version 12 — Image Galleries + RichText Upload (Completed)

**Scope:** گالری تصاویر و آپلود تصویر در ریچ‌تکست برای City, Area, Category و ترکیب‌ها.

**What was implemented**

- **CityImage, AreaImage, CategoryImage, CityCategoryImage, CityAreaCategoryImage** — مدل‌های گالری با فیلدهای:
  - `is_cover`: تصویر کارت (صفحه لیست شهرها/دسته‌ها)
  - `is_landing_cover`: کاور صفحه لندینگ
  - `is_content_image`: تصاویر محتوا
  - `alt`, `caption`
- **RichTextUploadingField** برای `main_content` در City, Area, Category, CityCategory, CityAreaCategory — امکان آپلود تصویر در ویرایشگر
- مسیر واحد آپلود: `uploads/` (CKEditor + تصاویر گالری)
- Inline گالری تصاویر در ادمین City, Area, Category, CityCategory, CityAreaCategory
- نمایش تصویر کاور در صفحات لندینگ شهر، محله، دسته، شهر+دسته، محله+دسته
- نمایش تصویر کارت در صفحه لیست شهرها و دسته‌ها

**Architectural intent**

- ساختار یکسان برای همه موجودیت‌های لندینگ
- مسیر تمیز برای آپلودها (همه زیر `media/uploads/`)

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 13 — Custom User, Accounts, Agencies (Completed)

**Scope:** مدل کاربر سفارشی، ورود/ثبت‌نام/خروج، مشاوره املاک.

**What was implemented**

- **Custom User** (`AUTH_USER_MODEL = "accounts.User"`): فیلدهای `phone`, `agency`, `avatar`, `is_verified` داخل مدل User؛ حذف UserProfile
- **نقش‌ها:** از Django Groups — سوپرکاربر گروه‌ها را در ادمین می‌سازد
- **Accounts:** `/accounts/login/`, `/accounts/signup/`, `/accounts/logout/` با قالب‌های signin-light و signup-light
- **Header:** ورود وقتی لاگین نیست؛ منوی کاربر + دکمه خروج وقتی لاگین است (خروج با POST)
- **SignUpView:** ریدایرکت به صفحه اصلی اگر کاربر لاگین باشد
- **Agencies:** مدل Agency با owner، employees (از User.agency)، لندینگ `/a/{slug}/`
- **.gitignore:** به‌روزرسانی جامع (Python, Django, venv, env, staticfiles, IDE, OS, …)

**Architectural intent**

- یک مدل User برای هویت و پروفایل؛ نقش‌ها با Groups قابل توسعه
- صفحات ورود/ثبت‌نام مستقل با قالب‌های Finder

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 14 — Seed Data, Listing Slug, URL Fixes (Completed)

**Scope:** اسکریپت seed، اسلاگ از عنوان، رفع مشکل لینک آگهی‌ها.

**What was implemented**

- **seed_data:** دستور `python manage.py seed_data [--clear]` — پر کردن دیتابیس با استان‌ها، شهرها، محلات، دسته‌ها، کاربران، مشاوره‌ها، آگهی‌ها
- **slugify_from_title:** تابع در `apps.common.text_utils` — تبدیل عنوان فارسی به اسلاگ لاتین با ترانسلیتریشن
- **Listing.slug:** پر شدن خودکار از عنوان هنگام ذخیره؛ پشتیبانی از متن فارسی
- **لینک آگهی:** رفع ۴۰۴ برای `/l/{id}-/` (اسلاگ خالی) — ریدایرکت به `/l/{id}/`؛ `get_absolute_url` برای اسلاگ خالی فرمت id-only برمی‌گرداند
- **.gitignore:** اضافه شدن پوشه `test/`

**Architectural intent**

- داده‌های نمونه واقعی برای توسعه و تست
- اسلاگ خوانا و SEO-friendly از عنوان فارسی

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 15 — Blog (Completed)

**Scope:** بلاگ با دسته‌بندی و ارتباط با لندینگ‌ها.

**What was implemented**

- **BlogCategory, BlogPost** — مدل‌های بلاگ با BaseSEO
- **ارتباط با لندینگ:** city, area, listing_category در BlogPost
- **URLها:** `/blog/`, `/blog/category/<slug>/`, `/blog/<slug>/`
- **تمپلیت‌ها:** blog_index, blog_category, blog_post_detail, blog_post_card
- **ادمین:** مدیریت دسته‌بندی و پست با autocomplete برای city, area, listing_category
- **Header:** لینک بلاگ در منو
- **seed_data:** دسته‌بندی‌ها و پست‌های نمونه بلاگ

---

### Version 16 — لیست آگهی‌ها، مشاوره‌ها، URLها و ظاهر (Completed)

**Scope:** صفحه لیست آگهی‌ها و مشاوره‌ها، ریدایرکت‌ها، اسلاگ انگلیسی، بردکرامپ.

**What was implemented**

- **/listings/:** کاتالوگ آگهی‌ها با سایدبار فیلتر (شهر، محله، دسته، نوع معامله، جستجو) — ظاهر مشابه city-guide-catalog
- **/s/:** ریدایرکت به `/listings/`
- **/agencies/:** لیست مشاوره‌های املاک با سایدبار فیلتر شهر — ظاهر مشابه لیستینگ فید
- **/a/:** ریدایرکت به `/agencies/`
- **صفحه مشاوره:** URL با ID مثل آگهی‌ها — `/a/{id}-{slug}/`، `/a/{id}/`، ریدایرکت اسلاگ قدیم به فرم جدید
- **اسلاگ مشاوره:** پر شدن خودکار به انگلیسی با slugify_from_title (مثل آگهی‌ها)
- **بردکرامپ:** در صفحات شهر، محله، دسته، آگهی، مشاوره، بلاگ، اکانت
- **فیلتر دسته‌بندی:** نمایش آگهی‌های دسته والد + فرزند در صفحات لندینگ
- **بلاگ مرتبط:** نمایش پست‌های بلاگ در انتهای صفحات شهر و دسته‌بندی
- **Header:** لینک «آگهی‌های املاک»، «مشاوران املاک» (لیست مشاوره‌ها) و «کارشناسان» (لیست کارشناسان فردی) در منو

**Next step**

- پروفایل کاربر، لیست آگهی‌های کاربر، و غیره.

---

### Version 17 — EAV ویژگی‌های آگهی (Completed)

**Scope:** الگوی Entity-Attribute-Value برای ویژگی‌های پویا بر اساس دسته‌بندی.

**What was implemented**

- **Attribute**: تعریف ویژگی با نام، اسلاگ، نوع مقدار (عددی، بله/خیر، انتخابی، متن)، واحد، دسته‌بندی‌ها (M2M)
- **AttributeOption**: گزینه‌های از پیش تعریف‌شده (مثل ۱، ۲، ۳ برای تعداد اتاق)
- **ListingAttribute**: ذخیره مقدار هر ویژگی برای هر آگهی (value_int, value_bool, value_str, value_option)
- **سینگال همگام‌سازی دسته‌بندی:** با ذخیره آگهی، رکوردهای ListingAttribute بر اساس دستهٔ آن ایجاد/حذف می‌شوند
- **سینگال همگام‌سازی گزینه‌ها:** مقادیر جدید واردشده در آگهی به AttributeOption اضافه می‌شوند
- **ادمین:** نمایش دسته‌بندی هر ویژگی؛ فیلتر ویژگی‌ها بر اساس دستهٔ آگهی؛ فقط فیلد مقدار متناسب با نوع ویژگی نمایش داده می‌شود
- **صفحه ویرایش آگهی:** دکمه «بارگذاری ویژگی‌های دسته‌بندی»، datalist برای مقادیر عددی، اسکرول خودکار به بخش ویژگی‌ها پس از بارگذاری

**Architectural intent**

- ویژگی‌های متغیر بدون تغییر اسکیمای دیتابیس
- هر دسته‌بندی می‌تواند ویژگی‌های مخصوص خود را داشته باشد

**Next step**

- استفاده از ویژگی‌ها در فیلتر و نمایش صفحات جستجو و جزئیات آگهی

---

### Version 18 — محدودیت ادمین آگهی برای صاحب/کارمند مشاوره (Completed)

**Scope:** ایجادکننده و مشاوره املاک قابل تغییر فقط توسط سوپرادمین؛ فیلتر لیست آگهی‌ها بر اساس نقش.

**What was implemented**

- **created_by و agency:** برای غیر سوپرادمین readonly؛ هنگام افزودن آگهی خودکار (created_by = کاربر فعلی، agency = مشاوره کاربر)
- **فیلتر لیست آگهی‌ها:**
  - سوپرادمین: همهٔ آگهی‌ها
  - صاحب مشاوره (owned_agency): تمام آگهی‌های مشاوره خودش
  - کارمند مشاوره: فقط آگهی‌هایی که خودش ثبت کرده
- **نکته دسترسی‌ها:** برای کار autocomplete شهر و دسته‌بندی، گروه‌ها باید View روی City، Category و Area داشته باشند

**Next step**

- پروفایل کاربر، لیست آگهی‌های کاربر

---

### Version 19 — نوع معامله + قیمت متناسب (Completed)

**Scope:** گسترش نوع معامله به چهار نوع؛ فیلد مبلغ رهن؛ نمایش شرطی قیمت؛ جداکننده هزارگان.

**What was implemented**

- **Deal types:** فروش، اجاره، اجاره روزانه، رهن و اجاره (`buy`, `rent`, `daily_rent`, `mortgage_rent`)
- **price_mortgage:** فیلد جدید برای مبلغ رهن (فقط در رهن و اجاره)
- **نمایش شرطی در ادمین:** فیلد مبلغ رهن فقط هنگام انتخاب «رهن و اجاره» نمایش داده می‌شود
- **فیلتر کاتالوگ:** گزینه‌های اجاره روزانه و رهن و اجاره در سایدبار فیلتر
- **نمایش قیمت در تمپلیت‌ها:** متناسب با نوع معامله — رهن و اجاره: هر دو مبلغ با برچسب؛ بقیه: یک قیمت
- **جداکننده هزارگان:** استفاده از `django.contrib.humanize` و فیلتر `intcomma` برای نمایش قیمت‌ها (مثلاً ۱۵٬۰۰۰٬۰۰۰)
- **Attribute.is_filterable:** ویژگی‌های قابل فیلتر در کاتالوگ

**Architectural intent**

- پوشش سناریوهای رایج بازار املاک ایران
- UX روشن برای نوع معامله و قیمت‌گذاری

**Next step**

- فیلتر بازه قیمت در کاتالوگ؛ فرم تماس/استعلام آگهی

---

### Version 20 — OTP ورود، پنل کاربری، مشاوره چندگانه، منوی ریسپانسیو (Completed)

**Scope:** ورود با شماره موبایل (OTP)، پنل کاربری، کارمند چند مشاوره، تأیید مشاوره، صفحه مشاور، منوی offcanvas ریسپانسیو.

**What was implemented**

- **OTP ورود:** سرویس `apps.accounts.services` (request_otp, verify_otp)، صفحه ورود با شماره موبایل (`phone_login.html`)، مدل OTPRequest، محدودیت cooldown و انقضا
- **SMS:** سرویس ارسال پیامک در `apps.common.sms` (send_otp، قابل اتصال به درگاه SMS)
- **پنل کاربری:** اپلیکیشن `apps.panel` — داشبورد، مدیریت آگهی‌ها، تنظیمات کاربر، ...
- **کاربر چند مشاوره:** مدل AgencyEmployee و درخواست عضویت (AgencyJoinRequest)، تأیید/رد کارمند توسط مالک مشاوره
- **Role change request:** درخواست تغییر نقش کاربر (سینگال و flow مربوطه)
- **User slug:** اسلاگ کاربر برای URL پروفایل
- **وضعیت آگهی:** pending، rejected و rejection_reason؛ گردش کار تأیید آگهی
- **صفحه مشاور:** لندینگ `/agent/{slug}/` برای پروفایل مشاوران (agent_urls، agent_landing)
- **منوی ریسپانسیو:** تبدیل navbar از collapse به offcanvas — در موبایل پنل کشویی از سمت راست؛ در دسکتاپ منوی افقی معمول (theme Finder)

**Architectural intent**

- ورود بدون رمز با OTP مناسب موبایل
- پنل اختصاصی برای کاربران و مشاوران
- پشتیبانی از عضویت کارمند در چند مشاوره با تأیید مالک

**Next step**

- ریسپانسیو سایر صفحات؛ فیلتر بازه قیمت

---

### Version 21 — تصاویر Placeholder با Pillow (Completed)

**Scope:** ساخت تصاویر placeholder برای شهرها، محلات، دسته‌ها، آگهی‌ها، مشاوره‌ها و بلاگ.

**What was implemented**

- **placeholder_images.py:** ماژول Pillow — تصویر با متن وسط، گرادیان، فونت فارسی (Tahoma/DejaVu)
- **generate_placeholder_images:** دستور مدیریت — ساخت تصویر برای City, Area, Category, Listing, Agency, CityCategory, CityAreaCategory, BlogPost
- **متن روی تصاویر:** انگلیسی (en_name، slug)
- **گزینه --force:** جایگزینی تصاویر قبلی
- **منوی ریسپانسیو:** بازگشت از offcanvas به collapse مطابق دمو real-estate-home-v1
- **mobile-app.css:** ساده‌سازی برای هماهنگی با تم پیش‌فرض دمو

**Next step**

- فیلتر بازه قیمت؛ ریسپانسیو سایر صفحات

---

### Version 22 — صفحه لیست کارشناسان و جداسازی منو (Completed)

**Scope:** جداسازی لینک «کارشناسان» از «مشاوران املاک»؛ صفحه لیست کارشناسان فردی.

**What was implemented**

- **/agents/:** لیست کارشناسان (صاحبان و کارمندان مشاوره‌های تأییدشده) با سایدبار فیلتر شهر
- **agent_list view:** کوئری کاربران با `owned_agencies` یا `agency` تأییدشده؛ فیلتر بر اساس شهرهای مشاوره/مشاورهٔ کارمند
- **تمپلیت agent_list.html:** ظاهر مشابه agency_list؛ کارت با آواتار، نام، نقش، تلفن، نام مشاوره
- **Header:** «مشاوران املاک» → `/agencies/`؛ «کارشناسان» → `/agents/`

**Architectural intent**

- تفکیک لیست مشاوره‌ها (آژانس‌ها) از لیست کارشناسان (افراد)

**Next step**

- فیلتر بازه قیمت؛ پروفایل کاربر

---

### Version 23 — آیکون ویژگی با آپلود فایل (Completed)

**Scope:** آیکون برای هر ویژگی (Attribute) با آپلود فایل PNG/SVG، نمایش در جزئیات آگهی.

**What was implemented**

- **Attribute.icon:** فیلد FileField با مسیر `attribute_icons/`؛ اعتبارسنجی: PNG یا SVG، حداکثر ۶۴KB، برای PNG ابعاد حداکثر ۱۲۸×۱۲۸
- **validators.py:** `validate_attribute_icon` در `apps.attributes`
- **ادمین:** فیلد آیکون با ClearableFileInput و `accept=".png,.svg"`
- **پنل:** فرم ویژگی (افزودن/ویرایش) با فیلد آیکون، `enctype="multipart/form-data"` و پاس‌دادن `request.FILES`؛ override CSS برای نمایش input فایل (theme `display:none` روی file input را لغو می‌کند)
- **صفحه جزئیات آگهی:** نمایش آیکون کنار ویژگی‌ها در بخش‌های برجسته، مشخصات، امکانات و کارت آگهی‌های مشابه

**Architectural intent**

- آیکون اختیاری برای هر ویژگی، بدون وابستگی به فونت آیکون
- اعتبارسنجی سمت سرور برای نوع، حجم و ابعاد

**Next step**

- فیلتر بازه قیمت؛ پروفایل کاربر

---

### Version 24 — نقش پیش‌فرض member، انحصار نقش‌ها، صفحه مشاوره کارمند، حذف مشاور مستقل (Completed)

**Scope:** نقش‌های انحصاری، نقش پیش‌فرض برای کاربران جدید، منوی کارمند قابل کلیک، حذف نقش independent_agent.

**What was implemented**

- **نقش member برای کاربران جدید:** سیگنال `post_save` در `apps.accounts.signals` — کاربران تازه‌ایجادشده (ثبت‌نام یا ورود OTP) در صورت نداشتن نقش، به گروه `member` اضافه می‌شوند
- **انحصار نقش‌ها:** `member`, `agency_owner`, `agency_employee` با هم انحصاری‌اند؛ در `approve_role_change_request` هنگام تأیید، تمام این نقش‌ها حذف و نقش درخواستی اضافه می‌شود
- **جلوگیری از درخواست نقش دوم:** کاربران دارای `agency_owner` یا `agency_employee` امکان درخواست نقش دیگر را ندارند — `can_request_role` و فرم `RoleChangeRequestForm` محدود شده‌اند
- **منوی کارمند قابل کلیک:** «شما عضو این آژانس املاک هستید» در پنل لینک به صفحه `employee_my_agency` است
- **صفحه اطلاعات مشاوره کارمند:** ویو `employee_my_agency` و قالب `employee_my_agency.html` — نمایش نام، تلفن، آدرس، معرفی و محتوای اصلی مشاوره؛ دکمه مشاهده صفحه عمومی
- **حذف نقش independent_agent:** از `GROUP_ROLE_LABELS` و `seed_data` حذف شد
- **دستور clear_user_agency_data:** پاک‌سازی ارتباطات کاربر با مشاوره‌ها (بدون حذف خود کاربر) — مالکیت آژانس به سوپرکاربر منتقل، حذف از گروه‌های agency

**Architectural intent**

- نقش‌های واضح و انحصاری برای ممبر، صاحب مشاوره و کارمند مشاوره
- دسترسی کارمند به اطلاعات مشاوره‌ای که عضو آن است

**Next step**

- فیلتر بازه قیمت؛ پروفایل کاربر

---

### Version 25 — لید با لاگین اجباری، مودال ورود، لاگ پیامک، محدودیت‌های پنل، نمایش نقش (Completed)

**Scope:** فرم استعلام آگهی و فرم لید لندینگ با ورود اجباری و مودال OTP؛ لاگ پیامک در ادمین؛ استعلام‌های آگهی فقط برای ادمین؛ تب عضویت مشاوره فقط برای نقش کارمند؛ نمایش نقش فعلی در صفحه تغییر نقش؛ متن‌های پنل.

**What was implemented**

- **لید استعلام آگهی و لید لندینگ:** قبل از لاگین به‌جای فرم فقط دکمه «ورود برای ارسال استعلام/درخواست»؛ پس از کلیک مودال ورود OTP (شماره + کد) باز می‌شود؛ APIهای JSON برای request-otp و verify-otp؛ بعد از ورود موفق رفرش همان صفحه و نمایش فرم با پری‌فیل از پروفایل.
- **قفل نام و تلفن:** اگر کاربر نام/نام‌خانوادگی یا شماره در پروفایل داشته باشد، فیلدهای مربوط در فرم لید غیرفعال و از پروفایل پر می‌شوند؛ مقدار از POST تزریق می‌شود تا اعتبارسنجی خطا ندهد (فیلدهای disabled در Django در cleaned_data نمی‌آیند؛ برای نام/تلفن قفل‌شده required=False).
- **لاگ پیامک:** مدل SmsLog (receptor, message, response_json, is_success, created_at)؛ ذخیرهٔ هر ارسال به کاوه‌نگار در ادمین؛ بخش «لاگ پیامک‌های ارسالی» در ادمین common، فقط برای مشاهده.
- **پنل:** «استعلام‌های آگهی» فقط برای ادمین سایت (لینک در منو و دسترسی به ویو)؛ «درخواست عضویت در مشاوره» فقط وقتی نمایش داده می‌شود که کاربر نقش کارمند (agency_employee) داشته باشد؛ کاربران بدون نقش کارمند باید از «درخواست تغییر نقش» ابتدا نقش کارمند بگیرند.
- **صفحه تغییر نقش:** نمایش «نقش فعلی شما: …» (از get_role_display؛ در صورت بدون گروه یا member → «کاربر سایت»).
- **متن‌های پنل:** منو «مشاوره املاک من» به‌جای «شما عضو این آژانس املاک هستید»؛ صفحه عضویت «عضویت شما در این مشاوره فعال است».

**Architectural intent**

- لید فقط از کاربران احراز هویت‌شده؛ UX با مودال بدون خروج از صفحه.
- شفافیت نقش و دسترسی در پنل؛ لاگ پیامک برای دیباگ و پشتیبانی.

**Next step**

- فیلتر بازه قیمت؛ پروفایل کاربر؛ اعتبارسنجی next_url در لاگین.

---

## Project Identity

**VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO — without frontend frameworks.**

---

## Known Issues & Findings (2026-02-17 Analysis)

این بخش نتیجه یک مرور منطقی/امنیتی روی کد است تا **ایرادهای فعلی** شفاف ثبت شوند.  
هر موردی که رفع شد، لطفاً این لیست را به‌روزرسانی کنید.

- **Settings & Security**
  - `SECRET_KEY` در `config/settings/base.py` هاردکد است و `DEBUG=True` است. در محیط واقعی باید `SECRET_KEY` فقط از `.env` و `DEBUG=False` باشد.
  - در `config/settings/dev.py` مقدار `ALLOWED_HOSTS = ["*"]` است (برای dev قابل قبول، اما هرگز برای prod).
  - در `config/settings/prod.py` مقدار `ALLOWED_HOSTS = []` خالی است و در صورت استفاده مستقیم از این کانفیگ، منجر به خطای `DisallowedHost` می‌شود؛ باید با دامنه/هاست‌های واقعی پر شود.
  - پکیج `django-ckeditor` از CKEditor 4 استفاده می‌کند که طبق هشدار `manage.py check` دیگر پشتیبانی امنیتی رسمی ندارد؛ برای محیط واقعی باید به CKEditor 5 یا راه‌حل امن‌تر مهاجرت شود.

- **OTP Login Flow**
  - در `apps/accounts/views.py` هنگام لاگین با OTP، مقدار `next` از `GET/POST` و سشن خوانده می‌شود و مستقیماً `redirect(next_url)` انجام می‌شود؛ هیچ چک `url_has_allowed_host_and_scheme` روی `next_url` نیست → **ریسک Open Redirect**.
  - در `apps/accounts/services.py` تابع `verify_otp` بعد از موفقیت، رکورد `OTPRequest` را حذف یا مصرف‌شده علامت‌گذاری نمی‌کند؛ تا قبل از انقضا، امکان استفادهٔ مجدد از همان کد (replay) وجود دارد.

- **Panel & Listings Logic**
  - در `apps/panel/views.py` تابع `_save_listing_attributes_from_post` برای ویژگی‌های عددی (`INTEGER`) مقدار را بدون `try/except` به `int(val)` تبدیل می‌کند؛ ورودی نامعتبر می‌تواند باعث خطای runtime در ذخیره آگهی شود.
  - در `apps/panel/views.py` ویوی `agency_employees`:
    - `pending_removes` فقط درخواست‌های حذف با `requested_by=request.user` را در UI نشان می‌دهد.
    - اما در هنگام POST، برای جلوگیری از ایجاد درخواست تکراری، فقط روی `(user, agency, status=PENDING)` فیلتر می‌شود و **`requested_by` را در نظر نمی‌گیرد**؛ نتیجه: اگر کاربر دیگری قبلاً درخواست حذف داده باشد، صاحب مشاوره جدید دکمه را می‌زند ولی هیچ تغییری در «در انتظار» خود نمی‌بیند.
  - در `apps/agencies/models.py` فیلد `approval_status` در مدل `Agency` پیش‌فرض را `APPROVED` قرار داده است؛ در حالی که در پنل هنگام ساخت، وضعیت به `PENDING` ست می‌شود. برای سازگاری منطقی، بهتر است پیش‌فرض مدل هم `PENDING` باشد تا هیچ Agency به‌طور ناخواسته auto-approved نشود.

- **Error Handling & Diagnostics**
  - چندین بلاک `except ...: pass` وجود دارد که خطا را کاملاً قورت می‌دهند و دیباگ را سخت می‌کنند:
    - `apps/common/storage.py` در `_save` برای تبدیل WebP: در صورت خطا فایل اصلی ذخیره می‌شود (رفتار قابل قبول)، اما برای لاگ بهتر است حداقل خطا log شود.
    - `apps/common/management/commands/seed_data.py` در `_seed_city_area_categories` همهٔ Exceptionها را `pass` می‌کند؛ این می‌تواند مشکلات داده‌ای را پنهان کند.
    - چند جای `apps/panel/views.py` و `apps/listings/views.py` روی `ValueError` فقط `pass` دارند (مثلاً هنگام parse کردن `int` از ورودی) که در صورت ورودی خراب، مسیر خطا را مبهم می‌کند.

- **Performance Considerations**
  - در `apps/listings/views.py` برای ساخت گزینه‌های فیلتر ویژگی‌ها، برای هر `Attribute` جداگانه روی `AttributeOption` کوئری زده می‌شود (الگوی N+1) — برای دسته‌بندی‌های پر ویژگی می‌تواند کند شود؛ می‌شود با prefetch یا جمع‌کردن کوئری‌ها بهینه کرد.
  - در `_save_listing_attributes_from_post` (`apps/panel/views.py`) داخل حلقهٔ ویژگی‌ها، برای هر ویژگی `Attribute.objects.get(pk=attr_id)` صدا زده می‌شود که با تعداد ویژگی بالا به N+1 تبدیل می‌شود؛ می‌توان همهٔ Attributeها را یک‌باره کش کرد.

- **Dependency Versioning**
  - در `requirements.txt` فقط `Django>=4.2` ذکر شده، در حالی که venv فعلی روی Django 6.0.2 است؛ برای ثبات محیط‌ها بهتر است نسخه Django و سایر پکیج‌ها به‌صورت مشخص (یا حداقل بازه محدود) پین شوند.

> **Next Actions (پیشنهادی):**  
> 1) اعتبارسنجی `next_url` با `django.utils.http.url_has_allowed_host_and_scheme`،  
> 2) invalid کردن OTP پس از اولین استفاده،  
> 3) اضافه کردن هندل امن برای `int(...)` و حذف/کاهش `except: pass`های کلی،  
> 4) هم‌تراز کردن پیش‌فرض `Agency.approval_status` با فلوی پنل و تنظیم دقیق `ALLOWED_HOSTS` در prod.
