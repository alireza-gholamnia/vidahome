# VidaHome â€” Complete Project Description

**Django Monolith + Django Templates (SSR)**

> âš ï¸ This document is written primarily for **AI systems** and automated agents.  
> It is the **single source of truth** for understanding, maintaining, and extending the VidaHome project.

---

## 1. Vision & Philosophy

VidaHome ÛŒÚ© Ù¾Ù„ØªÙØ±Ù… Ø­Ø±ÙÙ‡â€ŒØ§ÛŒØŒ Ù…Ù‚ÛŒØ§Ø³â€ŒÙ¾Ø°ÛŒØ± Ùˆ **SEO-first** Ø¯Ø± Ø­ÙˆØ²Ù‡ Ø§Ù…Ù„Ø§Ú© Ø§Ø³Øª Ú©Ù‡ Ø¨Ø§ Ù‡Ø¯Ù Ø­Ù„ Ù…Ø´Ú©Ù„Ø§Øª Ø¨Ù†ÛŒØ§Ø¯ÛŒ Ø¨Ø§Ø²Ø§Ø± Ø§Ù…Ù„Ø§Ú© Ø·Ø±Ø§Ø­ÛŒ Ø´Ø¯Ù‡ Ø§Ø³ØªØ›  
Ù†Ù‡ ØµØ±ÙØ§Ù‹ Ø³Ø§Ø®Øª ÛŒÚ© ÙˆØ¨â€ŒØ³Ø§ÛŒØª Ø¢Ú¯Ù‡ÛŒ.

### Problems VidaHome Solves

- Ø³Ø§Ø®ØªØ§Ø± Ø¶Ø¹ÛŒÙ Ùˆ ØºÛŒØ±Ù…Ù†Ø·Ù‚ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¯Ø± Ø³Ø§ÛŒØªâ€ŒÙ‡Ø§ÛŒ Ø§Ù…Ù„Ø§Ú©
- ÙÛŒÙ„ØªØ±Ù‡Ø§ÛŒ Ù…Ø­Ø¯ÙˆØ¯ØŒ ØºÛŒØ±Ù‚Ø§Ø¨Ù„ ØªÙˆØ³Ø¹Ù‡ Ùˆ ÙˆØ§Ø¨Ø³ØªÙ‡ Ø¨Ù‡ UI
- SEO Ù†Ø§Ú©Ø§Ø±Ø¢Ù…Ø¯ØŒ ØºÛŒØ±Ù‚Ø§Ø¨Ù„ Ú©Ù†ØªØ±Ù„ Ùˆ ÙˆØ§Ø¨Ø³ØªÙ‡ Ø¨Ù‡ hardcode
- Ù‚Ø§Ø·ÛŒ Ø´Ø¯Ù† Ù…ÙØ§Ù‡ÛŒÙ… Ø¯Ø§Ù…Ù†Ù‡â€ŒØ§ÛŒ (Ù†ÙˆØ¹ Ù…Ù„Ú©ØŒ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ØŒ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§)
- Ù†Ø§ØªÙˆØ§Ù†ÛŒ Ø¯Ø± ØªÙˆØ³Ø¹Ù‡ Ø¨Ù‡ Ø´Ù‡Ø±Ù‡Ø§ØŒ Ù…Ù†Ø§Ø·Ù‚ Ùˆ Ø³Ù†Ø§Ø±ÛŒÙˆÙ‡Ø§ÛŒ Ù¾ÛŒÚ†ÛŒØ¯Ù‡

VidaHome Ø§Ø² Ø§Ø¨ØªØ¯Ø§ Ø¨Ø§ Ø±ÙˆÛŒÚ©Ø±Ø¯ÛŒ **Ø³ÛŒØ³ØªÙ…ÛŒØŒ Ø§Ù„Ú¯ÙˆØ±ÛŒØªÙ…ÛŒ Ùˆ Ø¯ÛŒØªØ§Ù…Ø­ÙˆØ±** Ø·Ø±Ø§Ø­ÛŒ Ø´Ø¯Ù‡ Ùˆ ØªÙ…Ø±Ú©Ø² Ø¢Ù† Ø±ÙˆÛŒ **Correct Domain Modeling** Ø§Ø³Øª.

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

# Generate placeholder images (optional â€” Ø¨Ø±Ø§ÛŒ Ø´Ù‡Ø±Ù‡Ø§ØŒ Ù…Ø­Ù„Ø§ØªØŒ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ØŒ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ØŒ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ØŒ Ø¨Ù„Ø§Ú¯)
python manage.py generate_placeholder_images

# Run development server
python manage.py runserver
```

### Git Hygiene (Important)

- Do not commit local runtime artifacts:
  - `media/` (user uploads)
  - `db.sqlite3` and `*.sqlite3`
  - `.env` and private secret files
- Keep only `.env.example` in git for shared config template.
- If `media/` was committed before, adding `.gitignore` is not enough.
  You must untrack once with:

```bash
git rm -r --cached media db.sqlite3
git commit -m "chore: stop tracking local media and sqlite db"
```

### Admin

- URL: `/admin/`
- Manage: Users, Groups, Agencies, Provinces, Cities (Ø¨Ø§ Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ±), Areas (Ø¨Ø§ Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ±), Categories (Ø¨Ø§ Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ±), Listings (Ø¨Ø§ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ EAV), **Attributes** (ÙˆÛŒÚ˜Ú¯ÛŒØŒ Ú¯Ø²ÛŒÙ†Ù‡ ÙˆÛŒÚ˜Ú¯ÛŒØŒ ÙˆÛŒÚ˜Ú¯ÛŒ Ø¢Ú¯Ù‡ÛŒ), SEO overrides (CityCategory, CityAreaCategory) Ù‡Ø±Ú©Ø¯Ø§Ù… Ø¨Ø§ Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ±

---

## 3. Architecture Overview

### Monolithic Django Architecture (Root-based)

Ù¾Ø±ÙˆÚ˜Ù‡ Ø¨Ù‡â€ŒØµÙˆØ±Øª **Django Monolith Ú©Ù„Ø§Ø³ÛŒÚ©** Ùˆ Ø¨Ø¯ÙˆÙ† Ù„Ø§ÛŒÙ‡â€ŒÛŒ Ø§Ø¶Ø§ÙÛŒ backend Ù¾ÛŒØ§Ø¯Ù‡â€ŒØ³Ø§Ø²ÛŒ Ø´Ø¯Ù‡ Ø§Ø³Øª.  
Django Ù…Ø³ØªÙ‚ÛŒÙ…Ø§Ù‹ Ø¯Ø± Ø±ÙˆØª Ù¾Ø±ÙˆÚ˜Ù‡ Ù‚Ø±Ø§Ø± Ø¯Ø§Ø±Ø¯ Ùˆ Ù…Ø³Ø¦ÙˆÙ„ **routingØŒ renderingØŒ ORM Ùˆ SEO** Ø§Ø³Øª.

```
vidahome/
â”œâ”€â”€ manage.py
â”œâ”€â”€ db.sqlite3
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ asgi.py
â”‚   â”œâ”€â”€ wsgi.py
â”‚   â”œâ”€â”€ urls.py
â”‚   â””â”€â”€ settings/
â”‚       â”œâ”€â”€ base.py
â”‚       â”œâ”€â”€ dev.py
â”‚       â””â”€â”€ prod.py
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ common/           # Home view, context processors, upload_utils
â”‚   â”œâ”€â”€ accounts/         # Custom User, login, signup, logout
â”‚   â”œâ”€â”€ agencies/         # Agency, AgencyImage
â”‚   â”œâ”€â”€ locations/        # Province, City, Area
â”‚   â”œâ”€â”€ categories/       # Category (tree-based)
â”‚   â”œâ”€â”€ attributes/       # EAV: Attribute, AttributeOption, ListingAttribute
â”‚   â”œâ”€â”€ listings/         # Listing, ListingImage, search & detail views
â”‚   â”œâ”€â”€ blog/             # (scaffolded)
â”‚   â””â”€â”€ seo/              # BaseSEO, CityCategory, CityAreaCategory
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ base/             # base.html, head.html, scripts.html
â”‚   â”œâ”€â”€ partials/         # header, footer, hero, carousels, modals, etc.
â”‚   â”œâ”€â”€ pages/            # home, cities, categories, search landings, listing_detail
â”‚   â”œâ”€â”€ accounts/         # login.html, signup.html
â”‚   â””â”€â”€ errors/           # 404.html
â”œâ”€â”€ static/               # CSS, JS, img (Bootstrap RTL, theme, vendor)
â””â”€â”€ media/                # User uploads (listings, ckeditor)
```

### Tech Stack

| Component | Choice |
|-----------|--------|
| Backend | Django 6.x |
| Database | SQLite (dev) / PostgreSQL (prod recommended) |
| Templates | Django Templates (SSR) |
| UI | Bootstrap 5 RTL, local assets |
| Rich Text | django-ckeditor, ckeditor-uploader (image upload) |
| Number formatting | django.contrib.humanize (intcomma Ø¨Ø±Ø§ÛŒ Ø¬Ø¯Ø§Ú©Ù†Ù†Ø¯Ù‡ Ù‡Ø²Ø§Ø±Ú¯Ø§Ù†) |
| Language | Persian (fa), RTL |

### Architectural Rationale

- Ø³Ø§Ø¯Ú¯ÛŒ Ø¹Ù…Ù„ÛŒØ§ØªÛŒ Ùˆ Ú©Ø§Ù‡Ø´ Ù¾ÛŒÚ†ÛŒØ¯Ú¯ÛŒ Ø°Ù‡Ù†ÛŒ
- SEO Ø·Ø¨ÛŒØ¹ÛŒ Ùˆ Ù‚Ø§Ø¨Ù„ Ú©Ù†ØªØ±Ù„ Ø¨Ø§ Server-Side Rendering
- Ø¹Ø¯Ù… Ù†ÛŒØ§Ø² Ø¨Ù‡ hydrationØŒ SPA routing ÛŒØ§ frontend framework
- Ú©Ù†ØªØ±Ù„ Ú©Ø§Ù…Ù„ HTML Ø®Ø±ÙˆØ¬ÛŒ
- Ù…Ù†Ø§Ø³Ø¨ crawl Ú¯ÙˆÚ¯Ù„ Ùˆ Ø¨Ø§Ø²Ø§Ø± Ø§ÛŒØ±Ø§Ù†

---

## 4. URL System (Final & Non-Negotiable)

### Current Routes

| URL | Description |
|-----|-------------|
| `/` | Home |
| `/cities/` | Cities directory |
| `/categories/` | Categories directory |
| `/accounts/` | Redirect to `/accounts/login/` |
| `/accounts/login/` | ÙˆØ±ÙˆØ¯ |
| `/accounts/signup/` | Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… |
| `/accounts/logout/` | Ø®Ø±ÙˆØ¬ (POST only) |
| `/agencies/` | Ù„ÛŒØ³Øª Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ù…Ù„Ø§Ú© (ÙÛŒÙ„ØªØ± Ø´Ù‡Ø±: `?city=`) |
| `/agents/` | Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† (ØµØ§Ø­Ø¨/Ú©Ø§Ø±Ù…Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡ â€” ÙÛŒÙ„ØªØ± Ø´Ù‡Ø±: `?city=`) |
| `/a/` | Redirect to `/agencies/` |
| `/a/{id}-{slug}/` | Agency landing (canonical) |
| `/a/{id}/` | Agency landing (ID-only) |
| `/agent/{id}-{slug}/` | Agent (Ú©Ø§Ø±Ø´Ù†Ø§Ø³) landing (canonical) |
| `/agent/{id}/` | Agent landing (ID-only) |
| `/listings/` | Ú©Ø§ØªØ§Ù„ÙˆÚ¯ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ Ø¨Ø§ ÙÛŒÙ„ØªØ± (Ø´Ù‡Ø±ØŒ Ø¯Ø³ØªÙ‡ØŒ Ù…Ø­Ù„Ù‡ØŒ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ØŒ Ø¬Ø³ØªØ¬Ùˆ) |
| `/s/` | Redirect to `/listings/` |
| `/s/{slug}/` | City landing OR Category landing (resolver) |
| `/s/{city}/{context}/` | Area landing OR City+Category landing (resolver) |
| `/s/{city}/{area}/{category}/` | Area + Category landing |
| `/l/{id}-{slug}/` | Listing detail (canonical) |
| `/l/{id}/` | Listing detail (ID-only) |
| `/blog/` | Ø¨Ù„Ø§Ú¯ (Ù„ÛŒØ³Øª Ù¾Ø³Øªâ€ŒÙ‡Ø§) |
| `/blog/category/<slug>/` | Ù¾Ø³Øªâ€ŒÙ‡Ø§ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¨Ù„Ø§Ú¯ |
| `/blog/<slug>/` | ØµÙØ­Ù‡ ØªÚ© Ù¾Ø³Øª |
| `/admin/` | Django Admin |

### Rules

- `city / area / category` â†’ URL path only
- `deal` â†’ query param only (`?deal=buy` | `?deal=rent` | `?deal=daily_rent` | `?deal=mortgage_rent`)
- `attributes` â†’ query params only
- Default deal = `buy`
- Redirects: `/s/` â†’ `/listings/`ØŒ `/a/` â†’ `/agencies/`

### Listing Detail

- ID = source of truth
- slug = SEO only
- Independent from city/category paths

### Planned (Not Yet Implemented)

- `/about`, `/contact`, `/terms`, `/privacy`

---

## 5. Domain Models

### 5.1 locations

**Province â†’ City â†’ Area**

- **Province**: DB-only (not in URL)
- **City**: `slug` globally unique, exposed at `/s/{city}/`; intro_content, main_content (RichTextUploadingField)
- **CityImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ø´Ù‡Ø± â€” is_cover (Ú©Ø§Ø±Øª Ø´Ù‡Ø±), is_landing_cover (Ú©Ø§ÙˆØ± Ù„Ù†Ø¯ÛŒÙ†Ú¯), is_content_image, alt, caption
- **Area**: `slug` unique per city, exposed at `/s/{city}/{area}/`; intro_content, main_content (RichTextUploadingField)
- **AreaImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ù…Ø­Ù„Ù‡ â€” Ù‡Ù…Ø§Ù† Ø³Ø§Ø®ØªØ§Ø± CityImage

### 5.2 categories

- Tree-based (parent/child)
- `slug` globally unique
- Deal-independent
- intro_content, main_content (RichTextUploadingField)
- **CategoryImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ø¯Ø³ØªÙ‡ â€” is_cover, is_landing_cover, is_content_image, alt, caption
- Used in `/s/{category}/`, `/s/{city}/{category}/`, etc.

### 5.3 listings

- **Listing**: title, slug (Ù¾Ø± Ø´Ø¯Ù‡ Ø®ÙˆØ¯Ú©Ø§Ø± Ø§Ø² Ø¹Ù†ÙˆØ§Ù† Ø¨Ø§ ØªØ±Ø§Ù†Ø³Ù„ÛŒØªØ±ÛŒØ´Ù† ÙØ§Ø±Ø³ÛŒ), city, area (optional), category, deal, status, published_at, short_description, description (RichText), price, price_mortgage, price_unit, BaseSEO
- **Deal types:** `buy` (ÙØ±ÙˆØ´), `rent` (Ø§Ø¬Ø§Ø±Ù‡), `daily_rent` (Ø§Ø¬Ø§Ø±Ù‡ Ø±ÙˆØ²Ø§Ù†Ù‡), `mortgage_rent` (Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡)
- **Pricing (deal-dependent):**
  - ÙØ±ÙˆØ´/Ø§Ø¬Ø§Ø±Ù‡/Ø§Ø¬Ø§Ø±Ù‡ Ø±ÙˆØ²Ø§Ù†Ù‡: `price` + `price_unit`
  - Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡: `price_mortgage` (Ù…Ø¨Ù„Øº Ø±Ù‡Ù†) + `price` (Ø§Ø¬Ø§Ø±Ù‡ Ù…Ø§Ù‡Ø§Ù†Ù‡) + `price_unit`
- **Helpers:** `get_deal_display_fa()`, `has_price_display()`
- **ListingImage**: listing FK, image, alt, sort_order, is_cover

### 5.4 seo

- **BaseSEO**: seo_title, seo_meta_description, seo_h1, seo_canonical, seo_noindex, allow_index, seo_priority
- **CityCategory**: SEO override for `/s/{city}/{category}/`; intro_content, main_content (RichTextUploadingField)
- **CityCategoryImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ù„Ù†Ø¯ÛŒÙ†Ú¯ Ø´Ù‡Ø±+Ø¯Ø³ØªÙ‡
- **CityAreaCategory**: SEO override for `/s/{city}/{area}/{category}/`; intro_content, main_content (RichTextUploadingField)
- **CityAreaCategoryImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ù„Ù†Ø¯ÛŒÙ†Ú¯ Ù…Ø­Ù„Ù‡+Ø¯Ø³ØªÙ‡

### 5.5 accounts

- **User** (Custom User, `AUTH_USER_MODEL`): extends AbstractUser
  - `phone`, `avatar`, `is_verified`, `agency` (FK to Agency)
  - `get_role_display()` â€” Ù†Ù‚Ø´ Ø§Ø² Django Groups
- **Ù†Ù‚Ø´â€ŒÙ‡Ø§:** Ø§Ø² Ø·Ø±ÛŒÙ‚ Django Groups ØªØ¹ÛŒÛŒÙ† Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯ â€” `site_admin`, `seo_admin`, `member`, `agency_owner`, `agency_employee`
- **Ù†Ù‚Ø´ Ù¾ÛŒØ´â€ŒÙØ±Ø¶:** Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¬Ø¯ÛŒØ¯ Ø¨Ù‡â€ŒØ·ÙˆØ± Ø®ÙˆØ¯Ú©Ø§Ø± Ù†Ù‚Ø´ `member` Ø¯Ø±ÛŒØ§ÙØª Ù…ÛŒâ€ŒÚ©Ù†Ù†Ø¯ (Ø³ÛŒÚ¯Ù†Ø§Ù„ `post_save`)
- **Ø§Ù†Ø­ØµØ§Ø± Ù†Ù‚Ø´â€ŒÙ‡Ø§:** `member`, `agency_owner`, `agency_employee` Ø§Ù†Ø­ØµØ§Ø±ÛŒâ€ŒØ§Ù†Ø¯ â€” Ù‡Ø± Ú©Ø§Ø±Ø¨Ø± ÙÙ‚Ø· ÛŒÚ©ÛŒ Ø±Ø§ Ø¯Ø§Ø±Ø¯Ø› Ù‡Ù†Ú¯Ø§Ù… ØªØ£ÛŒÛŒØ¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØºÛŒÛŒØ± Ù†Ù‚Ø´ØŒ Ù†Ù‚Ø´ Ù‚Ø¨Ù„ÛŒ Ø­Ø°Ù Ùˆ Ù†Ù‚Ø´ Ø¬Ø¯ÛŒØ¯ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯
- **Ø¬Ù„ÙˆÚ¯ÛŒØ±ÛŒ Ø§Ø² Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù†Ù‚Ø´ Ø¯ÙˆÙ…:** Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¯Ø§Ø±Ø§ÛŒ `agency_owner` ÛŒØ§ `agency_employee` Ù†Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ù†Ø¯ Ù†Ù‚Ø´ Ø¯ÛŒÚ¯Ø± Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø¯Ù‡Ù†Ø¯
- Login: OTP (Ù…ÙˆØ¨Ø§ÛŒÙ„), `SignUpView`, Logout: `CustomLogoutView` (POST)
- Role-change and manual join-request flows are deprecated in panel routes; active flow is owner invite + user accept (`AgencyEmployeeInvite`).

### 5.6 agencies

- **Agency**: name, slug (Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ Ø®ÙˆØ¯Ú©Ø§Ø± Ø§Ø² Ù†Ø§Ù… Ø¨Ø§ slugify_from_title), owner (**ForeignKey** User), logo, cities (M2M), intro_content, main_content
- **AgencyImage**: Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ù…Ø´Ø§ÙˆØ±Ù‡
- **employees**: reverse Ø§Ø² `User.agency` â€” Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¨Ø§ agency Ù¾Ø± Ø´Ø¯Ù‡
- **AgencyEmployeeInvite**: Ø¯Ø¹ÙˆØª Ù‡Ù…Ú©Ø§Ø±ÛŒ ØªÙˆØ³Ø· Ù…Ø§Ù„Ú© Ø§Ù…Ù„Ø§Ú©Ø› Ø¹Ø¶ÙˆÛŒØª ÙÙ‚Ø· Ø¨Ø¹Ø¯ Ø§Ø² ØªØ§ÛŒÛŒØ¯ Ú©Ø§Ø±Ø¨Ø± Ø¯Ø¹ÙˆØªâ€ŒØ´Ø¯Ù‡ ÙØ¹Ø§Ù„ Ù…ÛŒâ€ŒØ´ÙˆØ¯
- **URL:** `/a/{id}-{slug}/` (Ù…Ø«Ù„ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§)

### 5.7 blog

- **BlogCategory**: slug, fa_name, sort_order, is_active â€” Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¯Ø§Ø®Ù„ÛŒ Ø¨Ù„Ø§Ú¯
- **BlogPost**: title, slug, excerpt, content, cover_image, published_at, status, author, blog_category, city, area, listing_category â€” Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ Ù„Ù†Ø¯ÛŒÙ†Ú¯â€ŒÙ‡Ø§ (city, area, listing_category)

### 5.8 attributes (EAV)

- **Attribute**: name, slug, value_type (integer | boolean | choice | string), unit, **icon** (FileFieldØŒ Ø¢Ù¾Ù„ÙˆØ¯ PNG/SVGØŒ max 64KBØŒ 128Ã—128)ØŒ categories (M2M), sort_order, is_active, is_filterable (Ù†Ù…Ø§ÛŒØ´ Ø¯Ø± ÙÛŒÙ„ØªØ± Ú©Ø§ØªØ§Ù„ÙˆÚ¯)
- **AttributeOption**: Ù…Ù‚Ø§Ø¯ÛŒØ± Ø§Ø² Ù¾ÛŒØ´ ØªØ¹Ø±ÛŒÙâ€ŒØ´Ø¯Ù‡ (Ù…Ø«Ù„ Û±ØŒ Û²ØŒ Û³ Ø¨Ø±Ø§ÛŒ ØªØ¹Ø¯Ø§Ø¯ Ø§ØªØ§Ù‚)
- **ListingAttribute**: Ù…Ù‚Ø¯Ø§Ø± Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒ Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ø¢Ú¯Ù‡ÛŒ â€” value_int, value_bool, value_str, value_option (FK)
- Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ Ø®ÙˆØ¯Ú©Ø§Ø± Ø¨Ø§ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ: Ø³ÛŒÙ†Ú¯Ø§Ù„ Ø±Ú©ÙˆØ±Ø¯Ù‡Ø§ÛŒ ListingAttribute Ø±Ø§ Ø¨Ø± Ø§Ø³Ø§Ø³ Ø¯Ø³ØªÙ‡Ù” Ø¢Ú¯Ù‡ÛŒ Ø§ÛŒØ¬Ø§Ø¯/Ø­Ø°Ù Ù…ÛŒâ€ŒÚ©Ù†Ø¯
- Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ Ø¨Ù‡ AttributeOption: Ù…Ù‚Ø§Ø¯ÛŒØ± Ø¬Ø¯ÛŒØ¯ ÙˆØ§Ø±Ø¯Ø´Ø¯Ù‡ Ø¯Ø± Ø¢Ú¯Ù‡ÛŒ Ø¨Ù‡ Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ ÙˆÛŒÚ˜Ú¯ÛŒ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯
- Ø§Ø¯Ù…ÛŒÙ† Ø¢Ú¯Ù‡ÛŒ: Ø¯Ú©Ù…Ù‡ Â«Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒÂ» Ø¨Ø±Ø§ÛŒ Ø°Ø®ÛŒØ±Ù‡ Ùˆ Ù„ÙˆØ¯ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§Ø› Ø§Ø³Ú©Ø±ÙˆÙ„ Ø®ÙˆØ¯Ú©Ø§Ø± Ø¨Ù‡ Ø¨Ø®Ø´ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§
- Unique: (listing, attribute)

---

## 6. Templates System

### Structure

```
templates/
â”œâ”€â”€ base/
â”‚   â”œâ”€â”€ base.html        # Main layout, dir="rtl"
â”‚   â”œâ”€â”€ head.html        # Meta, CSS, SEO injection
â”‚   â””â”€â”€ scripts.html     # JS vendors
â”œâ”€â”€ partials/
â”‚   â”œâ”€â”€ header.html      # Navbar, cities dropdown, logo, ÙˆØ±ÙˆØ¯/Ø®Ø±ÙˆØ¬/Ù…Ù†ÙˆÛŒ Ú©Ø§Ø±Ø¨Ø±
â”‚   â”œâ”€â”€ footer.html
â”‚   â”œâ”€â”€ hero.html
â”‚   â”œâ”€â”€ services.html
â”‚   â”œâ”€â”€ Topofferscarousel.html
â”‚   â”œâ”€â”€ Recentlyadded.html
â”‚   â”œâ”€â”€ Citiescarousel.html
â”‚   â”œâ”€â”€ Partnerscarousel.html
â”‚   â”œâ”€â”€ Topagentslnkedcarousel.html
â”‚   â”œâ”€â”€ Propertycostcalculator.html
â”‚   â”œâ”€â”€ Propertycostcalculatormodal.html
â”‚   â”œâ”€â”€ Propertycategories.html
â”‚   â”œâ”€â”€ SignInModal.html
â”‚   â”œâ”€â”€ SignUpModal.html
â”‚   â”œâ”€â”€ breadcrumbs.html
â”‚   â”œâ”€â”€ blog_post_card.html
â”‚   â”œâ”€â”€ loading_spinner.html
â”‚   â””â”€â”€ Backtotopbutton.html
â”œâ”€â”€ pages/
â”‚   â”œâ”€â”€ home.html
â”‚   â”œâ”€â”€ cities.html
â”‚   â”œâ”€â”€ categories.html
â”‚   â”œâ”€â”€ city_landing.html
â”‚   â”œâ”€â”€ area_landing.html
â”‚   â”œâ”€â”€ category_landing.html
â”‚   â”œâ”€â”€ city_category_landing.html
â”‚   â”œâ”€â”€ area_category_landing.html
â”‚   â”œâ”€â”€ agency_landing.html
â”‚   â”œâ”€â”€ agency_list.html
â”‚   â”œâ”€â”€ agent_list.html
â”‚   â”œâ”€â”€ listing_catalog.html
â”‚   â”œâ”€â”€ listing_detail.html
â”‚   â”œâ”€â”€ blog_index.html
â”‚   â”œâ”€â”€ blog_category.html
â”‚   â””â”€â”€ blog_post_detail.html
â”œâ”€â”€ accounts/
â”‚   â”œâ”€â”€ login.html        # ØµÙØ­Ù‡ ÙˆØ±ÙˆØ¯ (Ù‚Ø§Ù„Ø¨ signin-light)
â”‚   â””â”€â”€ signup.html       # ØµÙØ­Ù‡ Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… (Ù‚Ø§Ù„Ø¨ signup-light)
â””â”€â”€ errors/
    â””â”€â”€ 404.html
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

Registered in `config/settings/base.py` â†’ `TEMPLATES['OPTIONS']['context_processors']`.

---

## 8. Static & Media

### Static

- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [PROJECT_DIR / "static"]`
- Assets: Bootstrap RTL, theme.min.css, vendor libs, img/logo, img/real-estate/*

### Media

- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = PROJECT_DIR / "media"`
- `CKEDITOR_UPLOAD_PATH = "uploads/"` â€” Ù…Ø³ÛŒØ± ÙˆØ§Ø­Ø¯ Ø¢Ù¾Ù„ÙˆØ¯ Ø±ÛŒÚ†â€ŒØªÚ©Ø³Øª Ùˆ ØªØµØ§ÙˆÛŒØ± Ù…Ø­ØªÙˆØ§
- **Ù…Ø³ÛŒØ±Ù‡Ø§ÛŒ Ø°Ø®ÛŒØ±Ù‡ ØªØµØ§ÙˆÛŒØ±:**
  - Ø¢ÛŒÚ©ÙˆÙ† ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§: `attribute_icons/`
  - Ù„ÛŒØ³ØªÛŒÙ†Ú¯: `listings/%Y/%m/`
  - Ø´Ù‡Ø±ØŒ Ù…Ø­Ù„Ù‡ØŒ Ø¯Ø³ØªÙ‡ØŒ Ù„Ù†Ø¯ÛŒÙ†Ú¯â€ŒÙ‡Ø§: `uploads/cities/`, `uploads/areas/`, `uploads/categories/`, `uploads/city_category/`, `uploads/area_category/`
  - CKEditor (Ø±ÛŒÚ†â€ŒØªÚ©Ø³Øª): `uploads/%Y/%m/`

### Image Paths

All template image references use `{% static 'img/...' %}`.  
Placeholder/demo images (e.g. `img/real-estate/recent/`, `img/real-estate/catalog/`) must exist in `static/img/` or will 404.

### Placeholder Images (Pillow)

Ø¯Ø³ØªÙˆØ± `generate_placeholder_images` ØªØµØ§ÙˆÛŒØ± placeholder Ø¨Ø§ Pillow Ù…ÛŒâ€ŒØ³Ø§Ø²Ø¯ Ùˆ Ø¨Ù‡ Ù…Ø¯Ù„â€ŒÙ‡Ø§ Ù…ØªØµÙ„ Ù…ÛŒâ€ŒÚ©Ù†Ø¯:

```bash
python manage.py generate_placeholder_images       # ÙÙ‚Ø· Ø¨Ø±Ø§ÛŒ Ù…ÙˆØ§Ø±Ø¯ Ø¨Ø¯ÙˆÙ† ØªØµÙˆÛŒØ±
python manage.py generate_placeholder_images --force  # Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ†ÛŒ Ù‡Ù…Ù‡
```

**Ù…ÙˆØ¬ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§:** City, Area, Category, Listing, ListingImage, Agency, AgencyImage, CityCategory, CityAreaCategory, BlogPost  
**Ù…ØªÙ† Ø±ÙˆÛŒ ØªØµØ§ÙˆÛŒØ±:** Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ (en_nameØŒ slugØŒ â€¦)

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

### Version 0 â€” Project Bootstrap (Completed)

- Django monolith initialized, multi-env settings, domain apps scaffolded.
- **Next step:** Implement location domain model.

---

### Version 1 â€” Locations Domain & Cities Directory (Completed)

- Province, City, Area models; `/cities/` page.
- **Next step:** Implement `/s/{city}` search entry.

---

### Version 2 â€” Search Namespace + City Landing (Completed)

- `/s/` namespace; `/s/{city}/` city landing.
- **Next step:** Add categories and `/s/{city}/{category}/`.

---

### Version 3 â€” Area Discovery + Area Landing (Completed)

- Area discovery on city landing; `/s/{city}/{area}/`.
- **Next step:** Categories domain.

---

### Version 4 â€” Categories Domain (Tree-Based) (Completed)

- Category model with parent/child; Admin.
- **Next step:** Search URL resolver for `/s/{slug}/`, `/s/{city}/{category}/`.

---

### Version 5 â€” Search URL System Completed (Completed)

- Full grammar: category, city, city+category, city+area, city+area+category.
- **Next step:** Listing model + ORM filtering.

---

### Version 6 â€” Fix `/s/{slug}` Ambiguity (Completed)

- Single resolver for City vs Category.
- **Next step:** Listing model.

---

### Version 7 â€” Prevent Slug Collisions (Completed)

- Cross-app validation; no circular imports.
- **Next step:** Listing model.

---

### Version 8 â€” Template System Rebuild + Bootstrap RTL (Completed)

- New template structure; local Bootstrap RTL.
- **Next step:** Listing model.

---

### Version 9 â€” SEO Landing System (Completed)

- BaseSEO, CityCategory, CityAreaCategory; DB-driven SEO for all search routes.
- **Next step:** Listing model.

---

### Version 10 â€” Listings Domain + /l/ Detail Routes (Completed)

- Listing, ListingImage models; `/l/{id}-{slug}/`, `/l/{id}/`; Listing SEO.
- **Next step:** Wire listings to search landing pages (ORM filtering + pagination).

---

### Version 11 â€” Header & Navigation + Static Image Paths (Completed)

**Scope:** Fix navigation and static asset loading.

**What was implemented**

- Replaced demo header links with real project URLs (`/`, `/cities/`, `/categories/`).
- Added cities dropdown under "Ø´Ù‡Ø±Ù‡Ø§" with "Ù‡Ù…Ù‡ Ø´Ù‡Ø±Ù‡Ø§" + all active cities from DB.
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
- Replace static "Ù…Ù„Ú© Ù‡Ø§ÛŒ Ø¬Ø¯ÛŒØ¯" content in Recentlyadded with real listings from DB.

---

### Version 12 â€” Image Galleries + RichText Upload (Completed)

**Scope:** Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ùˆ Ø¢Ù¾Ù„ÙˆØ¯ ØªØµÙˆÛŒØ± Ø¯Ø± Ø±ÛŒÚ†â€ŒØªÚ©Ø³Øª Ø¨Ø±Ø§ÛŒ City, Area, Category Ùˆ ØªØ±Ú©ÛŒØ¨â€ŒÙ‡Ø§.

**What was implemented**

- **CityImage, AreaImage, CategoryImage, CityCategoryImage, CityAreaCategoryImage** â€” Ù…Ø¯Ù„â€ŒÙ‡Ø§ÛŒ Ú¯Ø§Ù„Ø±ÛŒ Ø¨Ø§ ÙÛŒÙ„Ø¯Ù‡Ø§ÛŒ:
  - `is_cover`: ØªØµÙˆÛŒØ± Ú©Ø§Ø±Øª (ØµÙØ­Ù‡ Ù„ÛŒØ³Øª Ø´Ù‡Ø±Ù‡Ø§/Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§)
  - `is_landing_cover`: Ú©Ø§ÙˆØ± ØµÙØ­Ù‡ Ù„Ù†Ø¯ÛŒÙ†Ú¯
  - `is_content_image`: ØªØµØ§ÙˆÛŒØ± Ù…Ø­ØªÙˆØ§
  - `alt`, `caption`
- **RichTextUploadingField** Ø¨Ø±Ø§ÛŒ `main_content` Ø¯Ø± City, Area, Category, CityCategory, CityAreaCategory â€” Ø§Ù…Ú©Ø§Ù† Ø¢Ù¾Ù„ÙˆØ¯ ØªØµÙˆÛŒØ± Ø¯Ø± ÙˆÛŒØ±Ø§ÛŒØ´Ú¯Ø±
- Ù…Ø³ÛŒØ± ÙˆØ§Ø­Ø¯ Ø¢Ù¾Ù„ÙˆØ¯: `uploads/` (CKEditor + ØªØµØ§ÙˆÛŒØ± Ú¯Ø§Ù„Ø±ÛŒ)
- Inline Ú¯Ø§Ù„Ø±ÛŒ ØªØµØ§ÙˆÛŒØ± Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ† City, Area, Category, CityCategory, CityAreaCategory
- Ù†Ù…Ø§ÛŒØ´ ØªØµÙˆÛŒØ± Ú©Ø§ÙˆØ± Ø¯Ø± ØµÙØ­Ø§Øª Ù„Ù†Ø¯ÛŒÙ†Ú¯ Ø´Ù‡Ø±ØŒ Ù…Ø­Ù„Ù‡ØŒ Ø¯Ø³ØªÙ‡ØŒ Ø´Ù‡Ø±+Ø¯Ø³ØªÙ‡ØŒ Ù…Ø­Ù„Ù‡+Ø¯Ø³ØªÙ‡
- Ù†Ù…Ø§ÛŒØ´ ØªØµÙˆÛŒØ± Ú©Ø§Ø±Øª Ø¯Ø± ØµÙØ­Ù‡ Ù„ÛŒØ³Øª Ø´Ù‡Ø±Ù‡Ø§ Ùˆ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§

**Architectural intent**

- Ø³Ø§Ø®ØªØ§Ø± ÛŒÚ©Ø³Ø§Ù† Ø¨Ø±Ø§ÛŒ Ù‡Ù…Ù‡ Ù…ÙˆØ¬ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§ÛŒ Ù„Ù†Ø¯ÛŒÙ†Ú¯
- Ù…Ø³ÛŒØ± ØªÙ…ÛŒØ² Ø¨Ø±Ø§ÛŒ Ø¢Ù¾Ù„ÙˆØ¯Ù‡Ø§ (Ù‡Ù…Ù‡ Ø²ÛŒØ± `media/uploads/`)

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 13 â€” Custom User, Accounts, Agencies (Completed)

**Scope:** Ù…Ø¯Ù„ Ú©Ø§Ø±Ø¨Ø± Ø³ÙØ§Ø±Ø´ÛŒØŒ ÙˆØ±ÙˆØ¯/Ø«Ø¨Øªâ€ŒÙ†Ø§Ù…/Ø®Ø±ÙˆØ¬ØŒ Ù…Ø´Ø§ÙˆØ±Ù‡ Ø§Ù…Ù„Ø§Ú©.

**What was implemented**

- **Custom User** (`AUTH_USER_MODEL = "accounts.User"`): ÙÛŒÙ„Ø¯Ù‡Ø§ÛŒ `phone`, `agency`, `avatar`, `is_verified` Ø¯Ø§Ø®Ù„ Ù…Ø¯Ù„ UserØ› Ø­Ø°Ù UserProfile
- **Ù†Ù‚Ø´â€ŒÙ‡Ø§:** Ø§Ø² Django Groups â€” Ø³ÙˆÙ¾Ø±Ú©Ø§Ø±Ø¨Ø± Ú¯Ø±ÙˆÙ‡â€ŒÙ‡Ø§ Ø±Ø§ Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ† Ù…ÛŒâ€ŒØ³Ø§Ø²Ø¯
- **Accounts:** `/accounts/login/`, `/accounts/signup/`, `/accounts/logout/` Ø¨Ø§ Ù‚Ø§Ù„Ø¨â€ŒÙ‡Ø§ÛŒ signin-light Ùˆ signup-light
- **Header:** ÙˆØ±ÙˆØ¯ ÙˆÙ‚ØªÛŒ Ù„Ø§Ú¯ÛŒÙ† Ù†ÛŒØ³ØªØ› Ù…Ù†ÙˆÛŒ Ú©Ø§Ø±Ø¨Ø± + Ø¯Ú©Ù…Ù‡ Ø®Ø±ÙˆØ¬ ÙˆÙ‚ØªÛŒ Ù„Ø§Ú¯ÛŒÙ† Ø§Ø³Øª (Ø®Ø±ÙˆØ¬ Ø¨Ø§ POST)
- **SignUpView:** Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øª Ø¨Ù‡ ØµÙØ­Ù‡ Ø§ØµÙ„ÛŒ Ø§Ú¯Ø± Ú©Ø§Ø±Ø¨Ø± Ù„Ø§Ú¯ÛŒÙ† Ø¨Ø§Ø´Ø¯
- **Agencies:** Ù…Ø¯Ù„ Agency Ø¨Ø§ ownerØŒ employees (Ø§Ø² User.agency)ØŒ Ù„Ù†Ø¯ÛŒÙ†Ú¯ `/a/{slug}/`
- **.gitignore:** Ø¨Ù‡â€ŒØ±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ Ø¬Ø§Ù…Ø¹ (Python, Django, venv, env, staticfiles, IDE, OS, â€¦)

**Architectural intent**

- ÛŒÚ© Ù…Ø¯Ù„ User Ø¨Ø±Ø§ÛŒ Ù‡ÙˆÛŒØª Ùˆ Ù¾Ø±ÙˆÙØ§ÛŒÙ„Ø› Ù†Ù‚Ø´â€ŒÙ‡Ø§ Ø¨Ø§ Groups Ù‚Ø§Ø¨Ù„ ØªÙˆØ³Ø¹Ù‡
- ØµÙØ­Ø§Øª ÙˆØ±ÙˆØ¯/Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… Ù…Ø³ØªÙ‚Ù„ Ø¨Ø§ Ù‚Ø§Ù„Ø¨â€ŒÙ‡Ø§ÛŒ Finder

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 14 â€” Seed Data, Listing Slug, URL Fixes (Completed)

**Scope:** Ø§Ø³Ú©Ø±ÛŒÙ¾Øª seedØŒ Ø§Ø³Ù„Ø§Ú¯ Ø§Ø² Ø¹Ù†ÙˆØ§Ù†ØŒ Ø±ÙØ¹ Ù…Ø´Ú©Ù„ Ù„ÛŒÙ†Ú© Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§.

**What was implemented**

- **seed_data:** Ø¯Ø³ØªÙˆØ± `python manage.py seed_data [--clear]` â€” Ù¾Ø± Ú©Ø±Ø¯Ù† Ø¯ÛŒØªØ§Ø¨ÛŒØ³ Ø¨Ø§ Ø§Ø³ØªØ§Ù†â€ŒÙ‡Ø§ØŒ Ø´Ù‡Ø±Ù‡Ø§ØŒ Ù…Ø­Ù„Ø§ØªØŒ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ØŒ Ú©Ø§Ø±Ø¨Ø±Ø§Ù†ØŒ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ØŒ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§
- **slugify_from_title:** ØªØ§Ø¨Ø¹ Ø¯Ø± `apps.common.text_utils` â€” ØªØ¨Ø¯ÛŒÙ„ Ø¹Ù†ÙˆØ§Ù† ÙØ§Ø±Ø³ÛŒ Ø¨Ù‡ Ø§Ø³Ù„Ø§Ú¯ Ù„Ø§ØªÛŒÙ† Ø¨Ø§ ØªØ±Ø§Ù†Ø³Ù„ÛŒØªØ±ÛŒØ´Ù†
- **Listing.slug:** Ù¾Ø± Ø´Ø¯Ù† Ø®ÙˆØ¯Ú©Ø§Ø± Ø§Ø² Ø¹Ù†ÙˆØ§Ù† Ù‡Ù†Ú¯Ø§Ù… Ø°Ø®ÛŒØ±Ù‡Ø› Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø§Ø² Ù…ØªÙ† ÙØ§Ø±Ø³ÛŒ
- **Ù„ÛŒÙ†Ú© Ø¢Ú¯Ù‡ÛŒ:** Ø±ÙØ¹ Û´Û°Û´ Ø¨Ø±Ø§ÛŒ `/l/{id}-/` (Ø§Ø³Ù„Ø§Ú¯ Ø®Ø§Ù„ÛŒ) â€” Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øª Ø¨Ù‡ `/l/{id}/`Ø› `get_absolute_url` Ø¨Ø±Ø§ÛŒ Ø§Ø³Ù„Ø§Ú¯ Ø®Ø§Ù„ÛŒ ÙØ±Ù…Øª id-only Ø¨Ø±Ù…ÛŒâ€ŒÚ¯Ø±Ø¯Ø§Ù†Ø¯
- **.gitignore:** Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯Ù† Ù¾ÙˆØ´Ù‡ `test/`

**Architectural intent**

- Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ Ù†Ù…ÙˆÙ†Ù‡ ÙˆØ§Ù‚Ø¹ÛŒ Ø¨Ø±Ø§ÛŒ ØªÙˆØ³Ø¹Ù‡ Ùˆ ØªØ³Øª
- Ø§Ø³Ù„Ø§Ú¯ Ø®ÙˆØ§Ù†Ø§ Ùˆ SEO-friendly Ø§Ø² Ø¹Ù†ÙˆØ§Ù† ÙØ§Ø±Ø³ÛŒ

**Next step**

- Wire listing ORM filtering + pagination to search landing pages.

---

### Version 15 â€” Blog (Completed)

**Scope:** Ø¨Ù„Ø§Ú¯ Ø¨Ø§ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ùˆ Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ Ù„Ù†Ø¯ÛŒÙ†Ú¯â€ŒÙ‡Ø§.

**What was implemented**

- **BlogCategory, BlogPost** â€” Ù…Ø¯Ù„â€ŒÙ‡Ø§ÛŒ Ø¨Ù„Ø§Ú¯ Ø¨Ø§ BaseSEO
- **Ø§Ø±ØªØ¨Ø§Ø· Ø¨Ø§ Ù„Ù†Ø¯ÛŒÙ†Ú¯:** city, area, listing_category Ø¯Ø± BlogPost
- **URLÙ‡Ø§:** `/blog/`, `/blog/category/<slug>/`, `/blog/<slug>/`
- **ØªÙ…Ù¾Ù„ÛŒØªâ€ŒÙ‡Ø§:** blog_index, blog_category, blog_post_detail, blog_post_card
- **Ø§Ø¯Ù…ÛŒÙ†:** Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ùˆ Ù¾Ø³Øª Ø¨Ø§ autocomplete Ø¨Ø±Ø§ÛŒ city, area, listing_category
- **Header:** Ù„ÛŒÙ†Ú© Ø¨Ù„Ø§Ú¯ Ø¯Ø± Ù…Ù†Ùˆ
- **seed_data:** Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ Ùˆ Ù¾Ø³Øªâ€ŒÙ‡Ø§ÛŒ Ù†Ù…ÙˆÙ†Ù‡ Ø¨Ù„Ø§Ú¯

---

### Version 16 â€” Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ØŒ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ØŒ URLÙ‡Ø§ Ùˆ Ø¸Ø§Ù‡Ø± (Completed)

**Scope:** ØµÙØ­Ù‡ Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ Ùˆ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ØŒ Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øªâ€ŒÙ‡Ø§ØŒ Ø§Ø³Ù„Ø§Ú¯ Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒØŒ Ø¨Ø±Ø¯Ú©Ø±Ø§Ù…Ù¾.

**What was implemented**

- **/listings/:** Ú©Ø§ØªØ§Ù„ÙˆÚ¯ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ Ø¨Ø§ Ø³Ø§ÛŒØ¯Ø¨Ø§Ø± ÙÛŒÙ„ØªØ± (Ø´Ù‡Ø±ØŒ Ù…Ø­Ù„Ù‡ØŒ Ø¯Ø³ØªÙ‡ØŒ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ØŒ Ø¬Ø³ØªØ¬Ùˆ) â€” Ø¸Ø§Ù‡Ø± Ù…Ø´Ø§Ø¨Ù‡ city-guide-catalog
- **/s/:** Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øª Ø¨Ù‡ `/listings/`
- **/agencies/:** Ù„ÛŒØ³Øª Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ù…Ù„Ø§Ú© Ø¨Ø§ Ø³Ø§ÛŒØ¯Ø¨Ø§Ø± ÙÛŒÙ„ØªØ± Ø´Ù‡Ø± â€” Ø¸Ø§Ù‡Ø± Ù…Ø´Ø§Ø¨Ù‡ Ù„ÛŒØ³ØªÛŒÙ†Ú¯ ÙÛŒØ¯
- **/a/:** Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øª Ø¨Ù‡ `/agencies/`
- **ØµÙØ­Ù‡ Ù…Ø´Ø§ÙˆØ±Ù‡:** URL Ø¨Ø§ ID Ù…Ø«Ù„ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ â€” `/a/{id}-{slug}/`ØŒ `/a/{id}/`ØŒ Ø±ÛŒØ¯Ø§ÛŒØ±Ú©Øª Ø§Ø³Ù„Ø§Ú¯ Ù‚Ø¯ÛŒÙ… Ø¨Ù‡ ÙØ±Ù… Ø¬Ø¯ÛŒØ¯
- **Ø§Ø³Ù„Ø§Ú¯ Ù…Ø´Ø§ÙˆØ±Ù‡:** Ù¾Ø± Ø´Ø¯Ù† Ø®ÙˆØ¯Ú©Ø§Ø± Ø¨Ù‡ Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ Ø¨Ø§ slugify_from_title (Ù…Ø«Ù„ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§)
- **Ø¨Ø±Ø¯Ú©Ø±Ø§Ù…Ù¾:** Ø¯Ø± ØµÙØ­Ø§Øª Ø´Ù‡Ø±ØŒ Ù…Ø­Ù„Ù‡ØŒ Ø¯Ø³ØªÙ‡ØŒ Ø¢Ú¯Ù‡ÛŒØŒ Ù…Ø´Ø§ÙˆØ±Ù‡ØŒ Ø¨Ù„Ø§Ú¯ØŒ Ø§Ú©Ø§Ù†Øª
- **ÙÛŒÙ„ØªØ± Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ:** Ù†Ù…Ø§ÛŒØ´ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ø¯Ø³ØªÙ‡ ÙˆØ§Ù„Ø¯ + ÙØ±Ø²Ù†Ø¯ Ø¯Ø± ØµÙØ­Ø§Øª Ù„Ù†Ø¯ÛŒÙ†Ú¯
- **Ø¨Ù„Ø§Ú¯ Ù…Ø±ØªØ¨Ø·:** Ù†Ù…Ø§ÛŒØ´ Ù¾Ø³Øªâ€ŒÙ‡Ø§ÛŒ Ø¨Ù„Ø§Ú¯ Ø¯Ø± Ø§Ù†ØªÙ‡Ø§ÛŒ ØµÙØ­Ø§Øª Ø´Ù‡Ø± Ùˆ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ
- **Header:** Ù„ÛŒÙ†Ú© Â«Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ø§Ù…Ù„Ø§Ú©Â»ØŒ Â«Ù…Ø´Ø§ÙˆØ±Ø§Ù† Ø§Ù…Ù„Ø§Ú©Â» (Ù„ÛŒØ³Øª Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§) Ùˆ Â«Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù†Â» (Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† ÙØ±Ø¯ÛŒ) Ø¯Ø± Ù…Ù†Ùˆ

**Next step**

- Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±ØŒ Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±ØŒ Ùˆ ØºÛŒØ±Ù‡.

---

### Version 17 â€” EAV ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø¢Ú¯Ù‡ÛŒ (Completed)

**Scope:** Ø§Ù„Ú¯ÙˆÛŒ Entity-Attribute-Value Ø¨Ø±Ø§ÛŒ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ù¾ÙˆÛŒØ§ Ø¨Ø± Ø§Ø³Ø§Ø³ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ.

**What was implemented**

- **Attribute**: ØªØ¹Ø±ÛŒÙ ÙˆÛŒÚ˜Ú¯ÛŒ Ø¨Ø§ Ù†Ø§Ù…ØŒ Ø§Ø³Ù„Ø§Ú¯ØŒ Ù†ÙˆØ¹ Ù…Ù‚Ø¯Ø§Ø± (Ø¹Ø¯Ø¯ÛŒØŒ Ø¨Ù„Ù‡/Ø®ÛŒØ±ØŒ Ø§Ù†ØªØ®Ø§Ø¨ÛŒØŒ Ù…ØªÙ†)ØŒ ÙˆØ§Ø­Ø¯ØŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ (M2M)
- **AttributeOption**: Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø² Ù¾ÛŒØ´ ØªØ¹Ø±ÛŒÙâ€ŒØ´Ø¯Ù‡ (Ù…Ø«Ù„ Û±ØŒ Û²ØŒ Û³ Ø¨Ø±Ø§ÛŒ ØªØ¹Ø¯Ø§Ø¯ Ø§ØªØ§Ù‚)
- **ListingAttribute**: Ø°Ø®ÛŒØ±Ù‡ Ù…Ù‚Ø¯Ø§Ø± Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒ Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ø¢Ú¯Ù‡ÛŒ (value_int, value_bool, value_str, value_option)
- **Ø³ÛŒÙ†Ú¯Ø§Ù„ Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ:** Ø¨Ø§ Ø°Ø®ÛŒØ±Ù‡ Ø¢Ú¯Ù‡ÛŒØŒ Ø±Ú©ÙˆØ±Ø¯Ù‡Ø§ÛŒ ListingAttribute Ø¨Ø± Ø§Ø³Ø§Ø³ Ø¯Ø³ØªÙ‡Ù” Ø¢Ù† Ø§ÛŒØ¬Ø§Ø¯/Ø­Ø°Ù Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯
- **Ø³ÛŒÙ†Ú¯Ø§Ù„ Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§:** Ù…Ù‚Ø§Ø¯ÛŒØ± Ø¬Ø¯ÛŒØ¯ ÙˆØ§Ø±Ø¯Ø´Ø¯Ù‡ Ø¯Ø± Ø¢Ú¯Ù‡ÛŒ Ø¨Ù‡ AttributeOption Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯
- **Ø§Ø¯Ù…ÛŒÙ†:** Ù†Ù…Ø§ÛŒØ´ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒØ› ÙÛŒÙ„ØªØ± ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ Ø¨Ø± Ø§Ø³Ø§Ø³ Ø¯Ø³ØªÙ‡Ù” Ø¢Ú¯Ù‡ÛŒØ› ÙÙ‚Ø· ÙÛŒÙ„Ø¯ Ù…Ù‚Ø¯Ø§Ø± Ù…ØªÙ†Ø§Ø³Ø¨ Ø¨Ø§ Ù†ÙˆØ¹ ÙˆÛŒÚ˜Ú¯ÛŒ Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯
- **ØµÙØ­Ù‡ ÙˆÛŒØ±Ø§ÛŒØ´ Ø¢Ú¯Ù‡ÛŒ:** Ø¯Ú©Ù…Ù‡ Â«Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒÂ»ØŒ datalist Ø¨Ø±Ø§ÛŒ Ù…Ù‚Ø§Ø¯ÛŒØ± Ø¹Ø¯Ø¯ÛŒØŒ Ø§Ø³Ú©Ø±ÙˆÙ„ Ø®ÙˆØ¯Ú©Ø§Ø± Ø¨Ù‡ Ø¨Ø®Ø´ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ Ù¾Ø³ Ø§Ø² Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ

**Architectural intent**

- ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ù…ØªØºÛŒØ± Ø¨Ø¯ÙˆÙ† ØªØºÛŒÛŒØ± Ø§Ø³Ú©ÛŒÙ…Ø§ÛŒ Ø¯ÛŒØªØ§Ø¨ÛŒØ³
- Ù‡Ø± Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ù…Ø®ØµÙˆØµ Ø®ÙˆØ¯ Ø±Ø§ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ø¯

**Next step**

- Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ Ø¯Ø± ÙÛŒÙ„ØªØ± Ùˆ Ù†Ù…Ø§ÛŒØ´ ØµÙØ­Ø§Øª Ø¬Ø³ØªØ¬Ùˆ Ùˆ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¢Ú¯Ù‡ÛŒ

---

### Version 18 â€” Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø§Ø¯Ù…ÛŒÙ† Ø¢Ú¯Ù‡ÛŒ Ø¨Ø±Ø§ÛŒ ØµØ§Ø­Ø¨/Ú©Ø§Ø±Ù…Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡ (Completed)

**Scope:** Ø§ÛŒØ¬Ø§Ø¯Ú©Ù†Ù†Ø¯Ù‡ Ùˆ Ù…Ø´Ø§ÙˆØ±Ù‡ Ø§Ù…Ù„Ø§Ú© Ù‚Ø§Ø¨Ù„ ØªØºÛŒÛŒØ± ÙÙ‚Ø· ØªÙˆØ³Ø· Ø³ÙˆÙ¾Ø±Ø§Ø¯Ù…ÛŒÙ†Ø› ÙÛŒÙ„ØªØ± Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ Ø¨Ø± Ø§Ø³Ø§Ø³ Ù†Ù‚Ø´.

**What was implemented**

- **created_by Ùˆ agency:** Ø¨Ø±Ø§ÛŒ ØºÛŒØ± Ø³ÙˆÙ¾Ø±Ø§Ø¯Ù…ÛŒÙ† readonlyØ› Ù‡Ù†Ú¯Ø§Ù… Ø§ÙØ²ÙˆØ¯Ù† Ø¢Ú¯Ù‡ÛŒ Ø®ÙˆØ¯Ú©Ø§Ø± (created_by = Ú©Ø§Ø±Ø¨Ø± ÙØ¹Ù„ÛŒØŒ agency = Ù…Ø´Ø§ÙˆØ±Ù‡ Ú©Ø§Ø±Ø¨Ø±)
- **ÙÛŒÙ„ØªØ± Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§:**
  - Ø³ÙˆÙ¾Ø±Ø§Ø¯Ù…ÛŒÙ†: Ù‡Ù…Ù‡Ù” Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§
  - ØµØ§Ø­Ø¨ Ù…Ø´Ø§ÙˆØ±Ù‡ (owned_agency): ØªÙ…Ø§Ù… Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ù…Ø´Ø§ÙˆØ±Ù‡ Ø®ÙˆØ¯Ø´
  - Ú©Ø§Ø±Ù…Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡: ÙÙ‚Ø· Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒÛŒ Ú©Ù‡ Ø®ÙˆØ¯Ø´ Ø«Ø¨Øª Ú©Ø±Ø¯Ù‡
- **Ù†Ú©ØªÙ‡ Ø¯Ø³ØªØ±Ø³ÛŒâ€ŒÙ‡Ø§:** Ø¨Ø±Ø§ÛŒ Ú©Ø§Ø± autocomplete Ø´Ù‡Ø± Ùˆ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒØŒ Ú¯Ø±ÙˆÙ‡â€ŒÙ‡Ø§ Ø¨Ø§ÛŒØ¯ View Ø±ÙˆÛŒ CityØŒ Category Ùˆ Area Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù†Ø¯

**Next step**

- Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±ØŒ Ù„ÛŒØ³Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±

---

### Version 19 â€” Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ + Ù‚ÛŒÙ…Øª Ù…ØªÙ†Ø§Ø³Ø¨ (Completed)

**Scope:** Ú¯Ø³ØªØ±Ø´ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ Ø¨Ù‡ Ú†Ù‡Ø§Ø± Ù†ÙˆØ¹Ø› ÙÛŒÙ„Ø¯ Ù…Ø¨Ù„Øº Ø±Ù‡Ù†Ø› Ù†Ù…Ø§ÛŒØ´ Ø´Ø±Ø·ÛŒ Ù‚ÛŒÙ…ØªØ› Ø¬Ø¯Ø§Ú©Ù†Ù†Ø¯Ù‡ Ù‡Ø²Ø§Ø±Ú¯Ø§Ù†.

**What was implemented**

- **Deal types:** ÙØ±ÙˆØ´ØŒ Ø§Ø¬Ø§Ø±Ù‡ØŒ Ø§Ø¬Ø§Ø±Ù‡ Ø±ÙˆØ²Ø§Ù†Ù‡ØŒ Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡ (`buy`, `rent`, `daily_rent`, `mortgage_rent`)
- **price_mortgage:** ÙÛŒÙ„Ø¯ Ø¬Ø¯ÛŒØ¯ Ø¨Ø±Ø§ÛŒ Ù…Ø¨Ù„Øº Ø±Ù‡Ù† (ÙÙ‚Ø· Ø¯Ø± Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡)
- **Ù†Ù…Ø§ÛŒØ´ Ø´Ø±Ø·ÛŒ Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ†:** ÙÛŒÙ„Ø¯ Ù…Ø¨Ù„Øº Ø±Ù‡Ù† ÙÙ‚Ø· Ù‡Ù†Ú¯Ø§Ù… Ø§Ù†ØªØ®Ø§Ø¨ Â«Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡Â» Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯
- **ÙÛŒÙ„ØªØ± Ú©Ø§ØªØ§Ù„ÙˆÚ¯:** Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø¬Ø§Ø±Ù‡ Ø±ÙˆØ²Ø§Ù†Ù‡ Ùˆ Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡ Ø¯Ø± Ø³Ø§ÛŒØ¯Ø¨Ø§Ø± ÙÛŒÙ„ØªØ±
- **Ù†Ù…Ø§ÛŒØ´ Ù‚ÛŒÙ…Øª Ø¯Ø± ØªÙ…Ù¾Ù„ÛŒØªâ€ŒÙ‡Ø§:** Ù…ØªÙ†Ø§Ø³Ø¨ Ø¨Ø§ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ â€” Ø±Ù‡Ù† Ùˆ Ø§Ø¬Ø§Ø±Ù‡: Ù‡Ø± Ø¯Ùˆ Ù…Ø¨Ù„Øº Ø¨Ø§ Ø¨Ø±Ú†Ø³Ø¨Ø› Ø¨Ù‚ÛŒÙ‡: ÛŒÚ© Ù‚ÛŒÙ…Øª
- **Ø¬Ø¯Ø§Ú©Ù†Ù†Ø¯Ù‡ Ù‡Ø²Ø§Ø±Ú¯Ø§Ù†:** Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² `django.contrib.humanize` Ùˆ ÙÛŒÙ„ØªØ± `intcomma` Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ Ù‚ÛŒÙ…Øªâ€ŒÙ‡Ø§ (Ù…Ø«Ù„Ø§Ù‹ Û±ÛµÙ¬Û°Û°Û°Ù¬Û°Û°Û°)
- **Attribute.is_filterable:** ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ù‚Ø§Ø¨Ù„ ÙÛŒÙ„ØªØ± Ø¯Ø± Ú©Ø§ØªØ§Ù„ÙˆÚ¯

**Architectural intent**

- Ù¾ÙˆØ´Ø´ Ø³Ù†Ø§Ø±ÛŒÙˆÙ‡Ø§ÛŒ Ø±Ø§ÛŒØ¬ Ø¨Ø§Ø²Ø§Ø± Ø§Ù…Ù„Ø§Ú© Ø§ÛŒØ±Ø§Ù†
- UX Ø±ÙˆØ´Ù† Ø¨Ø±Ø§ÛŒ Ù†ÙˆØ¹ Ù…Ø¹Ø§Ù…Ù„Ù‡ Ùˆ Ù‚ÛŒÙ…Øªâ€ŒÚ¯Ø°Ø§Ø±ÛŒ

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…Øª Ø¯Ø± Ú©Ø§ØªØ§Ù„ÙˆÚ¯Ø› ÙØ±Ù… ØªÙ…Ø§Ø³/Ø§Ø³ØªØ¹Ù„Ø§Ù… Ø¢Ú¯Ù‡ÛŒ

---

### Version 20 â€” OTP ÙˆØ±ÙˆØ¯ØŒ Ù¾Ù†Ù„ Ú©Ø§Ø±Ø¨Ø±ÛŒØŒ Ù…Ø´Ø§ÙˆØ±Ù‡ Ú†Ù†Ø¯Ú¯Ø§Ù†Ù‡ØŒ Ù…Ù†ÙˆÛŒ Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ (Completed)

**Scope:** ÙˆØ±ÙˆØ¯ Ø¨Ø§ Ø´Ù…Ø§Ø±Ù‡ Ù…ÙˆØ¨Ø§ÛŒÙ„ (OTP)ØŒ Ù¾Ù†Ù„ Ú©Ø§Ø±Ø¨Ø±ÛŒØŒ Ú©Ø§Ø±Ù…Ù†Ø¯ Ú†Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡ØŒ ØªØ£ÛŒÛŒØ¯ Ù…Ø´Ø§ÙˆØ±Ù‡ØŒ ØµÙØ­Ù‡ Ù…Ø´Ø§ÙˆØ±ØŒ Ù…Ù†ÙˆÛŒ offcanvas Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ.

**What was implemented**

- **OTP ÙˆØ±ÙˆØ¯:** Ø³Ø±ÙˆÛŒØ³ `apps.accounts.services` (request_otp, verify_otp)ØŒ ØµÙØ­Ù‡ ÙˆØ±ÙˆØ¯ Ø¨Ø§ Ø´Ù…Ø§Ø±Ù‡ Ù…ÙˆØ¨Ø§ÛŒÙ„ (`phone_login.html`)ØŒ Ù…Ø¯Ù„ OTPRequestØŒ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª cooldown Ùˆ Ø§Ù†Ù‚Ø¶Ø§
- **SMS:** Ø³Ø±ÙˆÛŒØ³ Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù…Ú© Ø¯Ø± `apps.common.sms` (send_otpØŒ Ù‚Ø§Ø¨Ù„ Ø§ØªØµØ§Ù„ Ø¨Ù‡ Ø¯Ø±Ú¯Ø§Ù‡ SMS)
- **Ù¾Ù†Ù„ Ú©Ø§Ø±Ø¨Ø±ÛŒ:** Ø§Ù¾Ù„ÛŒÚ©ÛŒØ´Ù† `apps.panel` â€” Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ØŒ Ù…Ø¯ÛŒØ±ÛŒØª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ØŒ ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ú©Ø§Ø±Ø¨Ø±ØŒ ...
- **Membership model update:** direct join-request flow is legacy; active membership flow is owner invite + user acceptance (`AgencyEmployeeInvite`).
- **Role change request:** legacy flow (historical, no active panel route).
- **User slug:** Ø§Ø³Ù„Ø§Ú¯ Ú©Ø§Ø±Ø¨Ø± Ø¨Ø±Ø§ÛŒ URL Ù¾Ø±ÙˆÙØ§ÛŒÙ„
- **ÙˆØ¶Ø¹ÛŒØª Ø¢Ú¯Ù‡ÛŒ:** pendingØŒ rejected Ùˆ rejection_reasonØ› Ú¯Ø±Ø¯Ø´ Ú©Ø§Ø± ØªØ£ÛŒÛŒØ¯ Ø¢Ú¯Ù‡ÛŒ
- **ØµÙØ­Ù‡ Ù…Ø´Ø§ÙˆØ±:** Ù„Ù†Ø¯ÛŒÙ†Ú¯ `/agent/{slug}/` Ø¨Ø±Ø§ÛŒ Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ù…Ø´Ø§ÙˆØ±Ø§Ù† (agent_urlsØŒ agent_landing)
- **Ù…Ù†ÙˆÛŒ Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ:** ØªØ¨Ø¯ÛŒÙ„ navbar Ø§Ø² collapse Ø¨Ù‡ offcanvas â€” Ø¯Ø± Ù…ÙˆØ¨Ø§ÛŒÙ„ Ù¾Ù†Ù„ Ú©Ø´ÙˆÛŒÛŒ Ø§Ø² Ø³Ù…Øª Ø±Ø§Ø³ØªØ› Ø¯Ø± Ø¯Ø³Ú©ØªØ§Ù¾ Ù…Ù†ÙˆÛŒ Ø§ÙÙ‚ÛŒ Ù…Ø¹Ù…ÙˆÙ„ (theme Finder)

**Architectural intent**

- ÙˆØ±ÙˆØ¯ Ø¨Ø¯ÙˆÙ† Ø±Ù…Ø² Ø¨Ø§ OTP Ù…Ù†Ø§Ø³Ø¨ Ù…ÙˆØ¨Ø§ÛŒÙ„
- Ù¾Ù†Ù„ Ø§Ø®ØªØµØ§ØµÛŒ Ø¨Ø±Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ùˆ Ù…Ø´Ø§ÙˆØ±Ø§Ù†
- Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø§Ø² Ø¹Ø¶ÙˆÛŒØª Ú©Ø§Ø±Ù…Ù†Ø¯ Ø¯Ø± Ú†Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡ Ø¨Ø§ ØªØ£ÛŒÛŒØ¯ Ù…Ø§Ù„Ú©

**Next step**

- Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ Ø³Ø§ÛŒØ± ØµÙØ­Ø§ØªØ› ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…Øª

---

### Version 21 â€” ØªØµØ§ÙˆÛŒØ± Placeholder Ø¨Ø§ Pillow (Completed)

**Scope:** Ø³Ø§Ø®Øª ØªØµØ§ÙˆÛŒØ± placeholder Ø¨Ø±Ø§ÛŒ Ø´Ù‡Ø±Ù‡Ø§ØŒ Ù…Ø­Ù„Ø§ØªØŒ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ØŒ Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ØŒ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ Ùˆ Ø¨Ù„Ø§Ú¯.

**What was implemented**

- **placeholder_images.py:** Ù…Ø§Ú˜ÙˆÙ„ Pillow â€” ØªØµÙˆÛŒØ± Ø¨Ø§ Ù…ØªÙ† ÙˆØ³Ø·ØŒ Ú¯Ø±Ø§Ø¯ÛŒØ§Ù†ØŒ ÙÙˆÙ†Øª ÙØ§Ø±Ø³ÛŒ (Tahoma/DejaVu)
- **generate_placeholder_images:** Ø¯Ø³ØªÙˆØ± Ù…Ø¯ÛŒØ±ÛŒØª â€” Ø³Ø§Ø®Øª ØªØµÙˆÛŒØ± Ø¨Ø±Ø§ÛŒ City, Area, Category, Listing, Agency, CityCategory, CityAreaCategory, BlogPost
- **Ù…ØªÙ† Ø±ÙˆÛŒ ØªØµØ§ÙˆÛŒØ±:** Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ (en_nameØŒ slug)
- **Ú¯Ø²ÛŒÙ†Ù‡ --force:** Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ†ÛŒ ØªØµØ§ÙˆÛŒØ± Ù‚Ø¨Ù„ÛŒ
- **Ù…Ù†ÙˆÛŒ Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ:** Ø¨Ø§Ø²Ú¯Ø´Øª Ø§Ø² offcanvas Ø¨Ù‡ collapse Ù…Ø·Ø§Ø¨Ù‚ Ø¯Ù…Ùˆ real-estate-home-v1
- **mobile-app.css:** Ø³Ø§Ø¯Ù‡â€ŒØ³Ø§Ø²ÛŒ Ø¨Ø±Ø§ÛŒ Ù‡Ù…Ø§Ù‡Ù†Ú¯ÛŒ Ø¨Ø§ ØªÙ… Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ø¯Ù…Ùˆ

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…ØªØ› Ø±ÛŒØ³Ù¾Ø§Ù†Ø³ÛŒÙˆ Ø³Ø§ÛŒØ± ØµÙØ­Ø§Øª

---

### Version 22 â€” ØµÙØ­Ù‡ Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† Ùˆ Ø¬Ø¯Ø§Ø³Ø§Ø²ÛŒ Ù…Ù†Ùˆ (Completed)

**Scope:** Ø¬Ø¯Ø§Ø³Ø§Ø²ÛŒ Ù„ÛŒÙ†Ú© Â«Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù†Â» Ø§Ø² Â«Ù…Ø´Ø§ÙˆØ±Ø§Ù† Ø§Ù…Ù„Ø§Ú©Â»Ø› ØµÙØ­Ù‡ Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† ÙØ±Ø¯ÛŒ.

**What was implemented**

- **/agents/:** Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† (ØµØ§Ø­Ø¨Ø§Ù† Ùˆ Ú©Ø§Ø±Ù…Ù†Ø¯Ø§Ù† Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ÛŒ ØªØ£ÛŒÛŒØ¯Ø´Ø¯Ù‡) Ø¨Ø§ Ø³Ø§ÛŒØ¯Ø¨Ø§Ø± ÙÛŒÙ„ØªØ± Ø´Ù‡Ø±
- **agent_list view:** Ú©ÙˆØ¦Ø±ÛŒ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¨Ø§ `owned_agencies` ÛŒØ§ `agency` ØªØ£ÛŒÛŒØ¯Ø´Ø¯Ù‡Ø› ÙÛŒÙ„ØªØ± Ø¨Ø± Ø§Ø³Ø§Ø³ Ø´Ù‡Ø±Ù‡Ø§ÛŒ Ù…Ø´Ø§ÙˆØ±Ù‡/Ù…Ø´Ø§ÙˆØ±Ù‡Ù” Ú©Ø§Ø±Ù…Ù†Ø¯
- **ØªÙ…Ù¾Ù„ÛŒØª agent_list.html:** Ø¸Ø§Ù‡Ø± Ù…Ø´Ø§Ø¨Ù‡ agency_listØ› Ú©Ø§Ø±Øª Ø¨Ø§ Ø¢ÙˆØ§ØªØ§Ø±ØŒ Ù†Ø§Ù…ØŒ Ù†Ù‚Ø´ØŒ ØªÙ„ÙÙ†ØŒ Ù†Ø§Ù… Ù…Ø´Ø§ÙˆØ±Ù‡
- **Header:** Â«Ù…Ø´Ø§ÙˆØ±Ø§Ù† Ø§Ù…Ù„Ø§Ú©Â» â†’ `/agencies/`Ø› Â«Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù†Â» â†’ `/agents/`

**Architectural intent**

- ØªÙÚ©ÛŒÚ© Ù„ÛŒØ³Øª Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ (Ø¢Ú˜Ø§Ù†Ø³â€ŒÙ‡Ø§) Ø§Ø² Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø´Ù†Ø§Ø³Ø§Ù† (Ø§ÙØ±Ø§Ø¯)

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…ØªØ› Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±

---

### Version 23 â€” Ø¢ÛŒÚ©ÙˆÙ† ÙˆÛŒÚ˜Ú¯ÛŒ Ø¨Ø§ Ø¢Ù¾Ù„ÙˆØ¯ ÙØ§ÛŒÙ„ (Completed)

**Scope:** Ø¢ÛŒÚ©ÙˆÙ† Ø¨Ø±Ø§ÛŒ Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒ (Attribute) Ø¨Ø§ Ø¢Ù¾Ù„ÙˆØ¯ ÙØ§ÛŒÙ„ PNG/SVGØŒ Ù†Ù…Ø§ÛŒØ´ Ø¯Ø± Ø¬Ø²Ø¦ÛŒØ§Øª Ø¢Ú¯Ù‡ÛŒ.

**What was implemented**

- **Attribute.icon:** ÙÛŒÙ„Ø¯ FileField Ø¨Ø§ Ù…Ø³ÛŒØ± `attribute_icons/`Ø› Ø§Ø¹ØªØ¨Ø§Ø±Ø³Ù†Ø¬ÛŒ: PNG ÛŒØ§ SVGØŒ Ø­Ø¯Ø§Ú©Ø«Ø± Û¶Û´KBØŒ Ø¨Ø±Ø§ÛŒ PNG Ø§Ø¨Ø¹Ø§Ø¯ Ø­Ø¯Ø§Ú©Ø«Ø± Û±Û²Û¸Ã—Û±Û²Û¸
- **validators.py:** `validate_attribute_icon` Ø¯Ø± `apps.attributes`
- **Ø§Ø¯Ù…ÛŒÙ†:** ÙÛŒÙ„Ø¯ Ø¢ÛŒÚ©ÙˆÙ† Ø¨Ø§ ClearableFileInput Ùˆ `accept=".png,.svg"`
- **Ù¾Ù†Ù„:** ÙØ±Ù… ÙˆÛŒÚ˜Ú¯ÛŒ (Ø§ÙØ²ÙˆØ¯Ù†/ÙˆÛŒØ±Ø§ÛŒØ´) Ø¨Ø§ ÙÛŒÙ„Ø¯ Ø¢ÛŒÚ©ÙˆÙ†ØŒ `enctype="multipart/form-data"` Ùˆ Ù¾Ø§Ø³â€ŒØ¯Ø§Ø¯Ù† `request.FILES`Ø› override CSS Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ input ÙØ§ÛŒÙ„ (theme `display:none` Ø±ÙˆÛŒ file input Ø±Ø§ Ù„ØºÙˆ Ù…ÛŒâ€ŒÚ©Ù†Ø¯)
- **ØµÙØ­Ù‡ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¢Ú¯Ù‡ÛŒ:** Ù†Ù…Ø§ÛŒØ´ Ø¢ÛŒÚ©ÙˆÙ† Ú©Ù†Ø§Ø± ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ Ø¯Ø± Ø¨Ø®Ø´â€ŒÙ‡Ø§ÛŒ Ø¨Ø±Ø¬Ø³ØªÙ‡ØŒ Ù…Ø´Ø®ØµØ§ØªØŒ Ø§Ù…Ú©Ø§Ù†Ø§Øª Ùˆ Ú©Ø§Ø±Øª Ø¢Ú¯Ù‡ÛŒâ€ŒÙ‡Ø§ÛŒ Ù…Ø´Ø§Ø¨Ù‡

**Architectural intent**

- Ø¢ÛŒÚ©ÙˆÙ† Ø§Ø®ØªÛŒØ§Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒØŒ Ø¨Ø¯ÙˆÙ† ÙˆØ§Ø¨Ø³ØªÚ¯ÛŒ Ø¨Ù‡ ÙÙˆÙ†Øª Ø¢ÛŒÚ©ÙˆÙ†
- Ø§Ø¹ØªØ¨Ø§Ø±Ø³Ù†Ø¬ÛŒ Ø³Ù…Øª Ø³Ø±ÙˆØ± Ø¨Ø±Ø§ÛŒ Ù†ÙˆØ¹ØŒ Ø­Ø¬Ù… Ùˆ Ø§Ø¨Ø¹Ø§Ø¯

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…ØªØ› Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±

---

### Version 24 â€” Ù†Ù‚Ø´ Ù¾ÛŒØ´â€ŒÙØ±Ø¶ memberØŒ Ø§Ù†Ø­ØµØ§Ø± Ù†Ù‚Ø´â€ŒÙ‡Ø§ØŒ ØµÙØ­Ù‡ Ù…Ø´Ø§ÙˆØ±Ù‡ Ú©Ø§Ø±Ù…Ù†Ø¯ØŒ Ø­Ø°Ù Ù…Ø´Ø§ÙˆØ± Ù…Ø³ØªÙ‚Ù„ (Completed)

**Scope:** Ù†Ù‚Ø´â€ŒÙ‡Ø§ÛŒ Ø§Ù†Ø­ØµØ§Ø±ÛŒØŒ Ù†Ù‚Ø´ Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ø¨Ø±Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¬Ø¯ÛŒØ¯ØŒ Ù…Ù†ÙˆÛŒ Ú©Ø§Ø±Ù…Ù†Ø¯ Ù‚Ø§Ø¨Ù„ Ú©Ù„ÛŒÚ©ØŒ Ø­Ø°Ù Ù†Ù‚Ø´ independent_agent.

**What was implemented**

- **Ù†Ù‚Ø´ member Ø¨Ø±Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¬Ø¯ÛŒØ¯:** Ø³ÛŒÚ¯Ù†Ø§Ù„ `post_save` Ø¯Ø± `apps.accounts.signals` â€” Ú©Ø§Ø±Ø¨Ø±Ø§Ù† ØªØ§Ø²Ù‡â€ŒØ§ÛŒØ¬Ø§Ø¯Ø´Ø¯Ù‡ (Ø«Ø¨Øªâ€ŒÙ†Ø§Ù… ÛŒØ§ ÙˆØ±ÙˆØ¯ OTP) Ø¯Ø± ØµÙˆØ±Øª Ù†Ø¯Ø§Ø´ØªÙ† Ù†Ù‚Ø´ØŒ Ø¨Ù‡ Ú¯Ø±ÙˆÙ‡ `member` Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯
- **Ø§Ù†Ø­ØµØ§Ø± Ù†Ù‚Ø´â€ŒÙ‡Ø§:** `member`, `agency_owner`, `agency_employee` Ø¨Ø§ Ù‡Ù… Ø§Ù†Ø­ØµØ§Ø±ÛŒâ€ŒØ§Ù†Ø¯Ø› Ø¯Ø± `approve_role_change_request` Ù‡Ù†Ú¯Ø§Ù… ØªØ£ÛŒÛŒØ¯ØŒ ØªÙ…Ø§Ù… Ø§ÛŒÙ† Ù†Ù‚Ø´â€ŒÙ‡Ø§ Ø­Ø°Ù Ùˆ Ù†Ù‚Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³ØªÛŒ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯
- **Ø¬Ù„ÙˆÚ¯ÛŒØ±ÛŒ Ø§Ø² Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù†Ù‚Ø´ Ø¯ÙˆÙ…:** Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¯Ø§Ø±Ø§ÛŒ `agency_owner` ÛŒØ§ `agency_employee` Ø§Ù…Ú©Ø§Ù† Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù†Ù‚Ø´ Ø¯ÛŒÚ¯Ø± Ø±Ø§ Ù†Ø¯Ø§Ø±Ù†Ø¯ â€” `can_request_role` Ùˆ ÙØ±Ù… `RoleChangeRequestForm` Ù…Ø­Ø¯ÙˆØ¯ Ø´Ø¯Ù‡â€ŒØ§Ù†Ø¯
- **Ù…Ù†ÙˆÛŒ Ú©Ø§Ø±Ù…Ù†Ø¯ Ù‚Ø§Ø¨Ù„ Ú©Ù„ÛŒÚ©:** Â«Ø´Ù…Ø§ Ø¹Ø¶Ùˆ Ø§ÛŒÙ† Ø¢Ú˜Ø§Ù†Ø³ Ø§Ù…Ù„Ø§Ú© Ù‡Ø³ØªÛŒØ¯Â» Ø¯Ø± Ù¾Ù†Ù„ Ù„ÛŒÙ†Ú© Ø¨Ù‡ ØµÙØ­Ù‡ `employee_my_agency` Ø§Ø³Øª
- **ØµÙØ­Ù‡ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù…Ø´Ø§ÙˆØ±Ù‡ Ú©Ø§Ø±Ù…Ù†Ø¯:** ÙˆÛŒÙˆ `employee_my_agency` Ùˆ Ù‚Ø§Ù„Ø¨ `employee_my_agency.html` â€” Ù†Ù…Ø§ÛŒØ´ Ù†Ø§Ù…ØŒ ØªÙ„ÙÙ†ØŒ Ø¢Ø¯Ø±Ø³ØŒ Ù…Ø¹Ø±ÙÛŒ Ùˆ Ù…Ø­ØªÙˆØ§ÛŒ Ø§ØµÙ„ÛŒ Ù…Ø´Ø§ÙˆØ±Ù‡Ø› Ø¯Ú©Ù…Ù‡ Ù…Ø´Ø§Ù‡Ø¯Ù‡ ØµÙØ­Ù‡ Ø¹Ù…ÙˆÙ…ÛŒ
- **Ø­Ø°Ù Ù†Ù‚Ø´ independent_agent:** Ø§Ø² `GROUP_ROLE_LABELS` Ùˆ `seed_data` Ø­Ø°Ù Ø´Ø¯
- **Ø¯Ø³ØªÙˆØ± clear_user_agency_data:** Ù¾Ø§Ú©â€ŒØ³Ø§Ø²ÛŒ Ø§Ø±ØªØ¨Ø§Ø·Ø§Øª Ú©Ø§Ø±Ø¨Ø± Ø¨Ø§ Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒÙ‡Ø§ (Ø¨Ø¯ÙˆÙ† Ø­Ø°Ù Ø®ÙˆØ¯ Ú©Ø§Ø±Ø¨Ø±) â€” Ù…Ø§Ù„Ú©ÛŒØª Ø¢Ú˜Ø§Ù†Ø³ Ø¨Ù‡ Ø³ÙˆÙ¾Ø±Ú©Ø§Ø±Ø¨Ø± Ù…Ù†ØªÙ‚Ù„ØŒ Ø­Ø°Ù Ø§Ø² Ú¯Ø±ÙˆÙ‡â€ŒÙ‡Ø§ÛŒ agency

**Architectural intent**

- Ù†Ù‚Ø´â€ŒÙ‡Ø§ÛŒ ÙˆØ§Ø¶Ø­ Ùˆ Ø§Ù†Ø­ØµØ§Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ù…Ù…Ø¨Ø±ØŒ ØµØ§Ø­Ø¨ Ù…Ø´Ø§ÙˆØ±Ù‡ Ùˆ Ú©Ø§Ø±Ù…Ù†Ø¯ Ù…Ø´Ø§ÙˆØ±Ù‡
- Ø¯Ø³ØªØ±Ø³ÛŒ Ú©Ø§Ø±Ù…Ù†Ø¯ Ø¨Ù‡ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù…Ø´Ø§ÙˆØ±Ù‡â€ŒØ§ÛŒ Ú©Ù‡ Ø¹Ø¶Ùˆ Ø¢Ù† Ø§Ø³Øª

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…ØªØ› Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±

---

### Version 25 â€” Ù„ÛŒØ¯ Ø¨Ø§ Ù„Ø§Ú¯ÛŒÙ† Ø§Ø¬Ø¨Ø§Ø±ÛŒØŒ Ù…ÙˆØ¯Ø§Ù„ ÙˆØ±ÙˆØ¯ØŒ Ù„Ø§Ú¯ Ù¾ÛŒØ§Ù…Ú©ØŒ Ù…Ø­Ø¯ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§ÛŒ Ù¾Ù†Ù„ØŒ Ù†Ù…Ø§ÛŒØ´ Ù†Ù‚Ø´ (Completed)

**Scope:** ÙØ±Ù… Ø§Ø³ØªØ¹Ù„Ø§Ù… Ø¢Ú¯Ù‡ÛŒ Ùˆ ÙØ±Ù… Ù„ÛŒØ¯ Ù„Ù†Ø¯ÛŒÙ†Ú¯ Ø¨Ø§ ÙˆØ±ÙˆØ¯ Ø§Ø¬Ø¨Ø§Ø±ÛŒ Ùˆ Ù…ÙˆØ¯Ø§Ù„ OTPØ› Ù„Ø§Ú¯ Ù¾ÛŒØ§Ù…Ú© Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ†Ø› Ø§Ø³ØªØ¹Ù„Ø§Ù…â€ŒÙ‡Ø§ÛŒ Ø¢Ú¯Ù‡ÛŒ ÙÙ‚Ø· Ø¨Ø±Ø§ÛŒ Ø§Ø¯Ù…ÛŒÙ†Ø› ØªØ¨ Ø¹Ø¶ÙˆÛŒØª Ù…Ø´Ø§ÙˆØ±Ù‡ ÙÙ‚Ø· Ø¨Ø±Ø§ÛŒ Ù†Ù‚Ø´ Ú©Ø§Ø±Ù…Ù†Ø¯Ø› Ù†Ù…Ø§ÛŒØ´ Ù†Ù‚Ø´ ÙØ¹Ù„ÛŒ Ø¯Ø± ØµÙØ­Ù‡ ØªØºÛŒÛŒØ± Ù†Ù‚Ø´Ø› Ù…ØªÙ†â€ŒÙ‡Ø§ÛŒ Ù¾Ù†Ù„.

**What was implemented**

- **Ù„ÛŒØ¯ Ø§Ø³ØªØ¹Ù„Ø§Ù… Ø¢Ú¯Ù‡ÛŒ Ùˆ Ù„ÛŒØ¯ Ù„Ù†Ø¯ÛŒÙ†Ú¯:** Ù‚Ø¨Ù„ Ø§Ø² Ù„Ø§Ú¯ÛŒÙ† Ø¨Ù‡â€ŒØ¬Ø§ÛŒ ÙØ±Ù… ÙÙ‚Ø· Ø¯Ú©Ù…Ù‡ Â«ÙˆØ±ÙˆØ¯ Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ø§Ø³ØªØ¹Ù„Ø§Ù…/Ø¯Ø±Ø®ÙˆØ§Ø³ØªÂ»Ø› Ù¾Ø³ Ø§Ø² Ú©Ù„ÛŒÚ© Ù…ÙˆØ¯Ø§Ù„ ÙˆØ±ÙˆØ¯ OTP (Ø´Ù…Ø§Ø±Ù‡ + Ú©Ø¯) Ø¨Ø§Ø² Ù…ÛŒâ€ŒØ´ÙˆØ¯Ø› APIÙ‡Ø§ÛŒ JSON Ø¨Ø±Ø§ÛŒ request-otp Ùˆ verify-otpØ› Ø¨Ø¹Ø¯ Ø§Ø² ÙˆØ±ÙˆØ¯ Ù…ÙˆÙÙ‚ Ø±ÙØ±Ø´ Ù‡Ù…Ø§Ù† ØµÙØ­Ù‡ Ùˆ Ù†Ù…Ø§ÛŒØ´ ÙØ±Ù… Ø¨Ø§ Ù¾Ø±ÛŒâ€ŒÙÛŒÙ„ Ø§Ø² Ù¾Ø±ÙˆÙØ§ÛŒÙ„.
- **Ù‚ÙÙ„ Ù†Ø§Ù… Ùˆ ØªÙ„ÙÙ†:** Ø§Ú¯Ø± Ú©Ø§Ø±Ø¨Ø± Ù†Ø§Ù…/Ù†Ø§Ù…â€ŒØ®Ø§Ù†ÙˆØ§Ø¯Ú¯ÛŒ ÛŒØ§ Ø´Ù…Ø§Ø±Ù‡ Ø¯Ø± Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ø¯ØŒ ÙÛŒÙ„Ø¯Ù‡Ø§ÛŒ Ù…Ø±Ø¨ÙˆØ· Ø¯Ø± ÙØ±Ù… Ù„ÛŒØ¯ ØºÛŒØ±ÙØ¹Ø§Ù„ Ùˆ Ø§Ø² Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ù¾Ø± Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯Ø› Ù…Ù‚Ø¯Ø§Ø± Ø§Ø² POST ØªØ²Ø±ÛŒÙ‚ Ù…ÛŒâ€ŒØ´ÙˆØ¯ ØªØ§ Ø§Ø¹ØªØ¨Ø§Ø±Ø³Ù†Ø¬ÛŒ Ø®Ø·Ø§ Ù†Ø¯Ù‡Ø¯ (ÙÛŒÙ„Ø¯Ù‡Ø§ÛŒ disabled Ø¯Ø± Django Ø¯Ø± cleaned_data Ù†Ù…ÛŒâ€ŒØ¢ÛŒÙ†Ø¯Ø› Ø¨Ø±Ø§ÛŒ Ù†Ø§Ù…/ØªÙ„ÙÙ† Ù‚ÙÙ„â€ŒØ´Ø¯Ù‡ required=False).
- **Ù„Ø§Ú¯ Ù¾ÛŒØ§Ù…Ú©:** Ù…Ø¯Ù„ SmsLog (receptor, message, response_json, is_success, created_at)Ø› Ø°Ø®ÛŒØ±Ù‡Ù” Ù‡Ø± Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ú©Ø§ÙˆÙ‡â€ŒÙ†Ú¯Ø§Ø± Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ†Ø› Ø¨Ø®Ø´ Â«Ù„Ø§Ú¯ Ù¾ÛŒØ§Ù…Ú©â€ŒÙ‡Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ÛŒÂ» Ø¯Ø± Ø§Ø¯Ù…ÛŒÙ† commonØŒ ÙÙ‚Ø· Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡.
- **Ù¾Ù†Ù„:** Â«Ø§Ø³ØªØ¹Ù„Ø§Ù…â€ŒÙ‡Ø§ÛŒ Ø¢Ú¯Ù‡ÛŒÂ» ÙÙ‚Ø· Ø¨Ø±Ø§ÛŒ Ø§Ø¯Ù…ÛŒÙ† Ø³Ø§ÛŒØª (Ù„ÛŒÙ†Ú© Ø¯Ø± Ù…Ù†Ùˆ Ùˆ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¨Ù‡ ÙˆÛŒÙˆ)Ø› Â«Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø¹Ø¶ÙˆÛŒØª Ø¯Ø± Ù…Ø´Ø§ÙˆØ±Ù‡Â» ÙÙ‚Ø· ÙˆÙ‚ØªÛŒ Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯ Ú©Ù‡ Ú©Ø§Ø±Ø¨Ø± Ù†Ù‚Ø´ Ú©Ø§Ø±Ù…Ù†Ø¯ (agency_employee) Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ø¯Ø› Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø¨Ø¯ÙˆÙ† Ù†Ù‚Ø´ Ú©Ø§Ø±Ù…Ù†Ø¯ Ø¨Ø§ÛŒØ¯ Ø§Ø² Â«Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØºÛŒÛŒØ± Ù†Ù‚Ø´Â» Ø§Ø¨ØªØ¯Ø§ Ù†Ù‚Ø´ Ú©Ø§Ø±Ù…Ù†Ø¯ Ø¨Ú¯ÛŒØ±Ù†Ø¯.
- **ØµÙØ­Ù‡ ØªØºÛŒÛŒØ± Ù†Ù‚Ø´:** Ù†Ù…Ø§ÛŒØ´ Â«Ù†Ù‚Ø´ ÙØ¹Ù„ÛŒ Ø´Ù…Ø§: â€¦Â» (Ø§Ø² get_role_displayØ› Ø¯Ø± ØµÙˆØ±Øª Ø¨Ø¯ÙˆÙ† Ú¯Ø±ÙˆÙ‡ ÛŒØ§ member â†’ Â«Ú©Ø§Ø±Ø¨Ø± Ø³Ø§ÛŒØªÂ»).
- **Ù…ØªÙ†â€ŒÙ‡Ø§ÛŒ Ù¾Ù†Ù„:** Ù…Ù†Ùˆ Â«Ù…Ø´Ø§ÙˆØ±Ù‡ Ø§Ù…Ù„Ø§Ú© Ù…Ù†Â» Ø¨Ù‡â€ŒØ¬Ø§ÛŒ Â«Ø´Ù…Ø§ Ø¹Ø¶Ùˆ Ø§ÛŒÙ† Ø¢Ú˜Ø§Ù†Ø³ Ø§Ù…Ù„Ø§Ú© Ù‡Ø³ØªÛŒØ¯Â»Ø› ØµÙØ­Ù‡ Ø¹Ø¶ÙˆÛŒØª Â«Ø¹Ø¶ÙˆÛŒØª Ø´Ù…Ø§ Ø¯Ø± Ø§ÛŒÙ† Ù…Ø´Ø§ÙˆØ±Ù‡ ÙØ¹Ø§Ù„ Ø§Ø³ØªÂ».

**Architectural intent**

- Ù„ÛŒØ¯ ÙÙ‚Ø· Ø§Ø² Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ø§Ø­Ø±Ø§Ø² Ù‡ÙˆÛŒØªâ€ŒØ´Ø¯Ù‡Ø› UX Ø¨Ø§ Ù…ÙˆØ¯Ø§Ù„ Ø¨Ø¯ÙˆÙ† Ø®Ø±ÙˆØ¬ Ø§Ø² ØµÙØ­Ù‡.
- Ø´ÙØ§ÙÛŒØª Ù†Ù‚Ø´ Ùˆ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø± Ù¾Ù†Ù„Ø› Ù„Ø§Ú¯ Ù¾ÛŒØ§Ù…Ú© Ø¨Ø±Ø§ÛŒ Ø¯ÛŒØ¨Ø§Ú¯ Ùˆ Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ.

**Next step**

- ÙÛŒÙ„ØªØ± Ø¨Ø§Ø²Ù‡ Ù‚ÛŒÙ…ØªØ› Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±Ø› Ø§Ø¹ØªØ¨Ø§Ø±Ø³Ù†Ø¬ÛŒ next_url Ø¯Ø± Ù„Ø§Ú¯ÛŒÙ†.

---

## Project Identity

**VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO â€” without frontend frameworks.**

---

## Known Issues & Findings (2026-02-17 Analysis)

Ø§ÛŒÙ† Ø¨Ø®Ø´ Ù†ØªÛŒØ¬Ù‡ ÛŒÚ© Ù…Ø±ÙˆØ± Ù…Ù†Ø·Ù‚ÛŒ/Ø§Ù…Ù†ÛŒØªÛŒ Ø±ÙˆÛŒ Ú©Ø¯ Ø§Ø³Øª ØªØ§ **Ø§ÛŒØ±Ø§Ø¯Ù‡Ø§ÛŒ ÙØ¹Ù„ÛŒ** Ø´ÙØ§Ù Ø«Ø¨Øª Ø´ÙˆÙ†Ø¯.  
Ù‡Ø± Ù…ÙˆØ±Ø¯ÛŒ Ú©Ù‡ Ø±ÙØ¹ Ø´Ø¯ØŒ Ù„Ø·ÙØ§Ù‹ Ø§ÛŒÙ† Ù„ÛŒØ³Øª Ø±Ø§ Ø¨Ù‡â€ŒØ±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ Ú©Ù†ÛŒØ¯.

- **Settings & Security**
  - `SECRET_KEY` Ø¯Ø± `config/settings/base.py` Ù‡Ø§Ø±Ø¯Ú©Ø¯ Ø§Ø³Øª Ùˆ `DEBUG=True` Ø§Ø³Øª. Ø¯Ø± Ù…Ø­ÛŒØ· ÙˆØ§Ù‚Ø¹ÛŒ Ø¨Ø§ÛŒØ¯ `SECRET_KEY` ÙÙ‚Ø· Ø§Ø² `.env` Ùˆ `DEBUG=False` Ø¨Ø§Ø´Ø¯.
  - Ø¯Ø± `config/settings/dev.py` Ù…Ù‚Ø¯Ø§Ø± `ALLOWED_HOSTS = ["*"]` Ø§Ø³Øª (Ø¨Ø±Ø§ÛŒ dev Ù‚Ø§Ø¨Ù„ Ù‚Ø¨ÙˆÙ„ØŒ Ø§Ù…Ø§ Ù‡Ø±Ú¯Ø² Ø¨Ø±Ø§ÛŒ prod).
  - Ø¯Ø± `config/settings/prod.py` Ù…Ù‚Ø¯Ø§Ø± `ALLOWED_HOSTS = []` Ø®Ø§Ù„ÛŒ Ø§Ø³Øª Ùˆ Ø¯Ø± ØµÙˆØ±Øª Ø§Ø³ØªÙØ§Ø¯Ù‡ Ù…Ø³ØªÙ‚ÛŒÙ… Ø§Ø² Ø§ÛŒÙ† Ú©Ø§Ù†ÙÛŒÚ¯ØŒ Ù…Ù†Ø¬Ø± Ø¨Ù‡ Ø®Ø·Ø§ÛŒ `DisallowedHost` Ù…ÛŒâ€ŒØ´ÙˆØ¯Ø› Ø¨Ø§ÛŒØ¯ Ø¨Ø§ Ø¯Ø§Ù…Ù†Ù‡/Ù‡Ø§Ø³Øªâ€ŒÙ‡Ø§ÛŒ ÙˆØ§Ù‚Ø¹ÛŒ Ù¾Ø± Ø´ÙˆØ¯.
  - Ù¾Ú©ÛŒØ¬ `django-ckeditor` Ø§Ø² CKEditor 4 Ø§Ø³ØªÙØ§Ø¯Ù‡ Ù…ÛŒâ€ŒÚ©Ù†Ø¯ Ú©Ù‡ Ø·Ø¨Ù‚ Ù‡Ø´Ø¯Ø§Ø± `manage.py check` Ø¯ÛŒÚ¯Ø± Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø§Ù…Ù†ÛŒØªÛŒ Ø±Ø³Ù…ÛŒ Ù†Ø¯Ø§Ø±Ø¯Ø› Ø¨Ø±Ø§ÛŒ Ù…Ø­ÛŒØ· ÙˆØ§Ù‚Ø¹ÛŒ Ø¨Ø§ÛŒØ¯ Ø¨Ù‡ CKEditor 5 ÛŒØ§ Ø±Ø§Ù‡â€ŒØ­Ù„ Ø§Ù…Ù†â€ŒØªØ± Ù…Ù‡Ø§Ø¬Ø±Øª Ø´ÙˆØ¯.

- **OTP Login Flow**
  - Ø¯Ø± `apps/accounts/views.py` Ù‡Ù†Ú¯Ø§Ù… Ù„Ø§Ú¯ÛŒÙ† Ø¨Ø§ OTPØŒ Ù…Ù‚Ø¯Ø§Ø± `next` Ø§Ø² `GET/POST` Ùˆ Ø³Ø´Ù† Ø®ÙˆØ§Ù†Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯ Ùˆ Ù…Ø³ØªÙ‚ÛŒÙ…Ø§Ù‹ `redirect(next_url)` Ø§Ù†Ø¬Ø§Ù… Ù…ÛŒâ€ŒØ´ÙˆØ¯Ø› Ù‡ÛŒÚ† Ú†Ú© `url_has_allowed_host_and_scheme` Ø±ÙˆÛŒ `next_url` Ù†ÛŒØ³Øª â†’ **Ø±ÛŒØ³Ú© Open Redirect**.
  - Ø¯Ø± `apps/accounts/services.py` ØªØ§Ø¨Ø¹ `verify_otp` Ø¨Ø¹Ø¯ Ø§Ø² Ù…ÙˆÙÙ‚ÛŒØªØŒ Ø±Ú©ÙˆØ±Ø¯ `OTPRequest` Ø±Ø§ Ø­Ø°Ù ÛŒØ§ Ù…ØµØ±Ùâ€ŒØ´Ø¯Ù‡ Ø¹Ù„Ø§Ù…Øªâ€ŒÚ¯Ø°Ø§Ø±ÛŒ Ù†Ù…ÛŒâ€ŒÚ©Ù†Ø¯Ø› ØªØ§ Ù‚Ø¨Ù„ Ø§Ø² Ø§Ù†Ù‚Ø¶Ø§ØŒ Ø§Ù…Ú©Ø§Ù† Ø§Ø³ØªÙØ§Ø¯Ù‡Ù” Ù…Ø¬Ø¯Ø¯ Ø§Ø² Ù‡Ù…Ø§Ù† Ú©Ø¯ (replay) ÙˆØ¬ÙˆØ¯ Ø¯Ø§Ø±Ø¯.

- **Panel & Listings Logic**
  - Ø¯Ø± `apps/panel/views.py` ØªØ§Ø¨Ø¹ `_save_listing_attributes_from_post` Ø¨Ø±Ø§ÛŒ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø¹Ø¯Ø¯ÛŒ (`INTEGER`) Ù…Ù‚Ø¯Ø§Ø± Ø±Ø§ Ø¨Ø¯ÙˆÙ† `try/except` Ø¨Ù‡ `int(val)` ØªØ¨Ø¯ÛŒÙ„ Ù…ÛŒâ€ŒÚ©Ù†Ø¯Ø› ÙˆØ±ÙˆØ¯ÛŒ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ Ø¨Ø§Ø¹Ø« Ø®Ø·Ø§ÛŒ runtime Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡ Ø¢Ú¯Ù‡ÛŒ Ø´ÙˆØ¯.
  - Ø¯Ø± `apps/panel/views.py` ÙˆÛŒÙˆÛŒ `agency_employees`:
    - `pending_removes` ÙÙ‚Ø· Ø¯Ø±Ø®ÙˆØ§Ø³Øªâ€ŒÙ‡Ø§ÛŒ Ø­Ø°Ù Ø¨Ø§ `requested_by=request.user` Ø±Ø§ Ø¯Ø± UI Ù†Ø´Ø§Ù† Ù…ÛŒâ€ŒØ¯Ù‡Ø¯.
    - Ø§Ù…Ø§ Ø¯Ø± Ù‡Ù†Ú¯Ø§Ù… POSTØŒ Ø¨Ø±Ø§ÛŒ Ø¬Ù„ÙˆÚ¯ÛŒØ±ÛŒ Ø§Ø² Ø§ÛŒØ¬Ø§Ø¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªÚ©Ø±Ø§Ø±ÛŒØŒ ÙÙ‚Ø· Ø±ÙˆÛŒ `(user, agency, status=PENDING)` ÙÛŒÙ„ØªØ± Ù…ÛŒâ€ŒØ´ÙˆØ¯ Ùˆ **`requested_by` Ø±Ø§ Ø¯Ø± Ù†Ø¸Ø± Ù†Ù…ÛŒâ€ŒÚ¯ÛŒØ±Ø¯**Ø› Ù†ØªÛŒØ¬Ù‡: Ø§Ú¯Ø± Ú©Ø§Ø±Ø¨Ø± Ø¯ÛŒÚ¯Ø±ÛŒ Ù‚Ø¨Ù„Ø§Ù‹ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø­Ø°Ù Ø¯Ø§Ø¯Ù‡ Ø¨Ø§Ø´Ø¯ØŒ ØµØ§Ø­Ø¨ Ù…Ø´Ø§ÙˆØ±Ù‡ Ø¬Ø¯ÛŒØ¯ Ø¯Ú©Ù…Ù‡ Ø±Ø§ Ù…ÛŒâ€ŒØ²Ù†Ø¯ ÙˆÙ„ÛŒ Ù‡ÛŒÚ† ØªØºÛŒÛŒØ±ÛŒ Ø¯Ø± Â«Ø¯Ø± Ø§Ù†ØªØ¸Ø§Ø±Â» Ø®ÙˆØ¯ Ù†Ù…ÛŒâ€ŒØ¨ÛŒÙ†Ø¯.
  - Ø¯Ø± `apps/agencies/models.py` ÙÛŒÙ„Ø¯ `approval_status` Ø¯Ø± Ù…Ø¯Ù„ `Agency` Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ø±Ø§ `APPROVED` Ù‚Ø±Ø§Ø± Ø¯Ø§Ø¯Ù‡ Ø§Ø³ØªØ› Ø¯Ø± Ø­Ø§Ù„ÛŒ Ú©Ù‡ Ø¯Ø± Ù¾Ù†Ù„ Ù‡Ù†Ú¯Ø§Ù… Ø³Ø§Ø®ØªØŒ ÙˆØ¶Ø¹ÛŒØª Ø¨Ù‡ `PENDING` Ø³Øª Ù…ÛŒâ€ŒØ´ÙˆØ¯. Ø¨Ø±Ø§ÛŒ Ø³Ø§Ø²Ú¯Ø§Ø±ÛŒ Ù…Ù†Ø·Ù‚ÛŒØŒ Ø¨Ù‡ØªØ± Ø§Ø³Øª Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ù…Ø¯Ù„ Ù‡Ù… `PENDING` Ø¨Ø§Ø´Ø¯ ØªØ§ Ù‡ÛŒÚ† Agency Ø¨Ù‡â€ŒØ·ÙˆØ± Ù†Ø§Ø®ÙˆØ§Ø³ØªÙ‡ auto-approved Ù†Ø´ÙˆØ¯.

- **Error Handling & Diagnostics**
  - Ú†Ù†Ø¯ÛŒÙ† Ø¨Ù„Ø§Ú© `except ...: pass` ÙˆØ¬ÙˆØ¯ Ø¯Ø§Ø±Ø¯ Ú©Ù‡ Ø®Ø·Ø§ Ø±Ø§ Ú©Ø§Ù…Ù„Ø§Ù‹ Ù‚ÙˆØ±Øª Ù…ÛŒâ€ŒØ¯Ù‡Ù†Ø¯ Ùˆ Ø¯ÛŒØ¨Ø§Ú¯ Ø±Ø§ Ø³Ø®Øª Ù…ÛŒâ€ŒÚ©Ù†Ù†Ø¯:
    - `apps/common/storage.py` Ø¯Ø± `_save` Ø¨Ø±Ø§ÛŒ ØªØ¨Ø¯ÛŒÙ„ WebP: Ø¯Ø± ØµÙˆØ±Øª Ø®Ø·Ø§ ÙØ§ÛŒÙ„ Ø§ØµÙ„ÛŒ Ø°Ø®ÛŒØ±Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯ (Ø±ÙØªØ§Ø± Ù‚Ø§Ø¨Ù„ Ù‚Ø¨ÙˆÙ„)ØŒ Ø§Ù…Ø§ Ø¨Ø±Ø§ÛŒ Ù„Ø§Ú¯ Ø¨Ù‡ØªØ± Ø§Ø³Øª Ø­Ø¯Ø§Ù‚Ù„ Ø®Ø·Ø§ log Ø´ÙˆØ¯.
    - `apps/common/management/commands/seed_data.py` Ø¯Ø± `_seed_city_area_categories` Ù‡Ù…Ù‡Ù” ExceptionÙ‡Ø§ Ø±Ø§ `pass` Ù…ÛŒâ€ŒÚ©Ù†Ø¯Ø› Ø§ÛŒÙ† Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ Ù…Ø´Ú©Ù„Ø§Øª Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø±Ø§ Ù¾Ù†Ù‡Ø§Ù† Ú©Ù†Ø¯.
    - Ú†Ù†Ø¯ Ø¬Ø§ÛŒ `apps/panel/views.py` Ùˆ `apps/listings/views.py` Ø±ÙˆÛŒ `ValueError` ÙÙ‚Ø· `pass` Ø¯Ø§Ø±Ù†Ø¯ (Ù…Ø«Ù„Ø§Ù‹ Ù‡Ù†Ú¯Ø§Ù… parse Ú©Ø±Ø¯Ù† `int` Ø§Ø² ÙˆØ±ÙˆØ¯ÛŒ) Ú©Ù‡ Ø¯Ø± ØµÙˆØ±Øª ÙˆØ±ÙˆØ¯ÛŒ Ø®Ø±Ø§Ø¨ØŒ Ù…Ø³ÛŒØ± Ø®Ø·Ø§ Ø±Ø§ Ù…Ø¨Ù‡Ù… Ù…ÛŒâ€ŒÚ©Ù†Ø¯.

- **Performance Considerations**
  - Ø¯Ø± `apps/listings/views.py` Ø¨Ø±Ø§ÛŒ Ø³Ø§Ø®Øª Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ ÙÛŒÙ„ØªØ± ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ØŒ Ø¨Ø±Ø§ÛŒ Ù‡Ø± `Attribute` Ø¬Ø¯Ø§Ú¯Ø§Ù†Ù‡ Ø±ÙˆÛŒ `AttributeOption` Ú©ÙˆØ¦Ø±ÛŒ Ø²Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯ (Ø§Ù„Ú¯ÙˆÛŒ N+1) â€” Ø¨Ø±Ø§ÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ù¾Ø± ÙˆÛŒÚ˜Ú¯ÛŒ Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ Ú©Ù†Ø¯ Ø´ÙˆØ¯Ø› Ù…ÛŒâ€ŒØ´ÙˆØ¯ Ø¨Ø§ prefetch ÛŒØ§ Ø¬Ù…Ø¹â€ŒÚ©Ø±Ø¯Ù† Ú©ÙˆØ¦Ø±ÛŒâ€ŒÙ‡Ø§ Ø¨Ù‡ÛŒÙ†Ù‡ Ú©Ø±Ø¯.
  - Ø¯Ø± `_save_listing_attributes_from_post` (`apps/panel/views.py`) Ø¯Ø§Ø®Ù„ Ø­Ù„Ù‚Ù‡Ù” ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ØŒ Ø¨Ø±Ø§ÛŒ Ù‡Ø± ÙˆÛŒÚ˜Ú¯ÛŒ `Attribute.objects.get(pk=attr_id)` ØµØ¯Ø§ Ø²Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯ Ú©Ù‡ Ø¨Ø§ ØªØ¹Ø¯Ø§Ø¯ ÙˆÛŒÚ˜Ú¯ÛŒ Ø¨Ø§Ù„Ø§ Ø¨Ù‡ N+1 ØªØ¨Ø¯ÛŒÙ„ Ù…ÛŒâ€ŒØ´ÙˆØ¯Ø› Ù…ÛŒâ€ŒØªÙˆØ§Ù† Ù‡Ù…Ù‡Ù” AttributeÙ‡Ø§ Ø±Ø§ ÛŒÚ©â€ŒØ¨Ø§Ø±Ù‡ Ú©Ø´ Ú©Ø±Ø¯.

- **Dependency Versioning**
  - Ø¯Ø± `requirements.txt` ÙÙ‚Ø· `Django>=4.2` Ø°Ú©Ø± Ø´Ø¯Ù‡ØŒ Ø¯Ø± Ø­Ø§Ù„ÛŒ Ú©Ù‡ venv ÙØ¹Ù„ÛŒ Ø±ÙˆÛŒ Django 6.0.2 Ø§Ø³ØªØ› Ø¨Ø±Ø§ÛŒ Ø«Ø¨Ø§Øª Ù…Ø­ÛŒØ·â€ŒÙ‡Ø§ Ø¨Ù‡ØªØ± Ø§Ø³Øª Ù†Ø³Ø®Ù‡ Django Ùˆ Ø³Ø§ÛŒØ± Ù¾Ú©ÛŒØ¬â€ŒÙ‡Ø§ Ø¨Ù‡â€ŒØµÙˆØ±Øª Ù…Ø´Ø®Øµ (ÛŒØ§ Ø­Ø¯Ø§Ù‚Ù„ Ø¨Ø§Ø²Ù‡ Ù…Ø­Ø¯ÙˆØ¯) Ù¾ÛŒÙ† Ø´ÙˆÙ†Ø¯.

> **Next Actions (Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ÛŒ):**  
> 1) Ø§Ø¹ØªØ¨Ø§Ø±Ø³Ù†Ø¬ÛŒ `next_url` Ø¨Ø§ `django.utils.http.url_has_allowed_host_and_scheme`ØŒ  
> 2) invalid Ú©Ø±Ø¯Ù† OTP Ù¾Ø³ Ø§Ø² Ø§ÙˆÙ„ÛŒÙ† Ø§Ø³ØªÙØ§Ø¯Ù‡ØŒ  
> 3) Ø§Ø¶Ø§ÙÙ‡ Ú©Ø±Ø¯Ù† Ù‡Ù†Ø¯Ù„ Ø§Ù…Ù† Ø¨Ø±Ø§ÛŒ `int(...)` Ùˆ Ø­Ø°Ù/Ú©Ø§Ù‡Ø´ `except: pass`Ù‡Ø§ÛŒ Ú©Ù„ÛŒØŒ  
> 4) Ù‡Ù…â€ŒØªØ±Ø§Ø² Ú©Ø±Ø¯Ù† Ù¾ÛŒØ´â€ŒÙØ±Ø¶ `Agency.approval_status` Ø¨Ø§ ÙÙ„ÙˆÛŒ Ù¾Ù†Ù„ Ùˆ ØªÙ†Ø¸ÛŒÙ… Ø¯Ù‚ÛŒÙ‚ `ALLOWED_HOSTS` Ø¯Ø± prod.

