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

# Run development server
python manage.py runserver
```

### Admin

- URL: `/admin/`
- Manage: Users, Groups, Agencies, Provinces, Cities (با گالری تصاویر), Areas (با گالری تصاویر), Categories (با گالری تصاویر), Listings, SEO overrides (CityCategory, CityAreaCategory) هرکدام با گالری تصاویر

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
│   ├── attributes/       # (scaffolded)
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
| `/a/{slug}/` | Agency landing |
| `/s/` | Redirect to `/` (no search root) |
| `/s/{slug}/` | City landing OR Category landing (resolver) |
| `/s/{city}/{context}/` | Area landing OR City+Category landing (resolver) |
| `/s/{city}/{area}/{category}/` | Area + Category landing |
| `/l/{id}-{slug}/` | Listing detail (canonical) |
| `/l/{id}/` | Listing detail (ID-only) |
| `/admin/` | Django Admin |

### Rules

- `city / area / category` → URL path only
- `deal` → query param only (`?deal=rent`)
- `attributes` → query params only
- Default deal = `buy`
- ❌ No redirects allowed in backend (except `/s/` → `/`)

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

- **Listing**: title, slug (پر شده خودکار از عنوان با ترانسلیتریشن فارسی), city, area (optional), category, deal, status, published_at, short_description, description (RichText), price, price_unit, BaseSEO
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
- **نقش‌ها:** از طریق Django Groups تعیین می‌شوند (سوپرکاربر گروه‌ها را در ادمین می‌سازد)
- Login: `CustomLoginView`, Signup: `SignUpView`, Logout: `CustomLogoutView` (POST)

### 5.6 agencies

- **Agency**: name, slug, owner (OneToOne User), logo, cities (M2M), intro_content, main_content
- **AgencyImage**: گالری تصاویر مشاوره
- **employees**: reverse از `User.agency` — کاربران با agency پر شده

### 5.7 attributes (scaffolded)

- Dynamic, category-based (planned)

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
│   └── listing_detail.html
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
  - لیستینگ: `listings/%Y/%m/`
  - شهر، محله، دسته، لندینگ‌ها: `uploads/cities/`, `uploads/areas/`, `uploads/categories/`, `uploads/city_category/`, `uploads/area_category/`
  - CKEditor (ریچ‌تکست): `uploads/%Y/%m/`

### Image Paths

All template image references use `{% static 'img/...' %}`.  
Placeholder/demo images (e.g. `img/real-estate/recent/`, `img/real-estate/catalog/`) must exist in `static/img/` or will 404.

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

## Project Identity

**VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO — without frontend frameworks.**
