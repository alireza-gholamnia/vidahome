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

# Run development server
python manage.py runserver
```

### Admin

- URL: `/admin/`
- Manage: Provinces, Cities, Areas, Categories, Listings, SEO overrides (CityCategory, CityAreaCategory)

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
│   ├── common/           # Home view, context processors
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
| Rich Text | django-ckeditor |
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
- **City**: `slug` globally unique, exposed at `/s/{city}/`
- **Area**: `slug` unique per city, exposed at `/s/{city}/{area}/`

### 5.2 categories

- Tree-based (parent/child)
- `slug` globally unique
- Deal-independent
- Used in `/s/{category}/`, `/s/{city}/{category}/`, etc.

### 5.3 listings

- **Listing**: title, slug, city, area (optional), category, deal, status, published_at, short_description, description (RichText), price, price_unit, BaseSEO
- **ListingImage**: listing FK, image, alt, sort_order, is_cover

### 5.4 seo

- **BaseSEO**: seo_title, seo_meta_description, seo_h1, seo_canonical, seo_noindex, allow_index, seo_priority
- **CityCategory**: SEO override for `/s/{city}/{category}/`
- **CityAreaCategory**: SEO override for `/s/{city}/{area}/{category}/`

### 5.5 attributes (scaffolded)

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
│   ├── header.html      # Navbar, cities dropdown, logo
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
│   └── listing_detail.html
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
- `MEDIA_ROOT = config/media` (BASE_DIR / media)
- Used for: Listing images, CKEditor uploads

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

## Project Identity

**VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO — without frontend frameworks.**
