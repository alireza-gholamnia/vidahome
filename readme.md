````md
# VidaHome — Complete Project Description
**Django Monolith + Django Templates**

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

## 2. Architecture Overview
### Monolithic Django Architecture (Root-based)

پروژه به‌صورت **Django Monolith کلاسیک** و بدون لایه‌ی اضافی backend پیاده‌سازی شده است.  
Django مستقیماً در روت پروژه قرار دارد و مسئول **routing، rendering، ORM و SEO** است.

```text
vidahome/
├─ manage.py
├─ config/
│  ├─ asgi.py
│  ├─ wsgi.py
│  ├─ urls.py
│  └─ settings/
│     ├─ base.py
│     ├─ dev.py
│     └─ prod.py
├─ apps/
│  ├─ common/
│  ├─ locations/
│  ├─ categories/
│  ├─ attributes/
│  ├─ listings/
│  ├─ blog/
│  └─ seo/
├─ templates/
├─ static/
├─ media/
└─ docs/
````

### Architectural Rationale

* سادگی عملیاتی و کاهش پیچیدگی ذهنی
* SEO طبیعی و قابل کنترل با Server-Side Rendering
* عدم نیاز به hydration، SPA routing یا frontend framework
* کنترل کامل HTML خروجی
* مناسب crawl گوگل و بازار ایران

---

## 3. Rendering Strategy

### Django Templates (SSR)

* Full server-side HTML rendering
* Data fetched directly from ORM
* JavaScript is optional and UX-only

**Result**

* Fast
* Crawlable
* Debuggable
* Stable

---

## 4. URL System (Final & Non-Negotiable)

### Static Pages

```text
/
/about
/contact
/terms
/privacy
```

### Directory Pages

```text
/cities
/categories
```

### Search Engine (Core)

```text
/s
/s/{category}
/s/{city}
/s/{city}/{category}
/s/{city}/{area}
/s/{city}/{area}/{category}
```

### Rules

* `city / area / category` → URL path only
* `deal` → query param only (`?deal=rent`)
* `attributes` → query params only
* Default deal = `buy`
* ❌ No redirects allowed in backend

### Listing Detail Page

```text
/l/{listingId}-{slug}
```

* ID = source of truth
* slug = SEO only
* Independent from city/category paths

---

## 5. Backend Domain Design (Planned)

### 5.1 locations

**Purpose:** Geographical hierarchy and local SEO.

* Hierarchy: Province → City → Area
* Used for:

  * `/cities` directory pages
  * Search routing
  * Local SEO foundations

### 5.2 categories

**Purpose:** Define *what is listed*.

* Examples:

  * apartment
  * villa
  * land
  * commercial
* Rules:

  * Stable
  * Deal-independent
  * Used directly in URL path

### 5.3 attributes

**Purpose:** Dynamic, category-based attribute system (E-commerce inspired).

* Attribute types:

  * select
  * number
  * boolean
  * text
* Server-side validation
* Category-bound

**Example**

```text
Category: land
Attributes:
- usage (residential, commercial)
- area_size
- document
```

> “Residential” is an **attribute**, not a category.

### 5.4 listings

**Purpose:** Core search engine.

* Fields:

  * city
  * area
  * category
  * deal (buy | rent)
  * dynamic attributes
  * ordered images
  * publish state
* Search logic:

  * Path params + query params
  * ORM-based filtering
  * Pagination
  * Cache-ready

### 5.5 seo

**Purpose:** Fully database-driven SEO system.

* SEOPage fields:

  * path
  * deal (optional)
  * title
  * meta description
  * h1
  * content
  * canonical
  * noindex

**Result**

* Thousands of landing pages
* Zero hardcoded SEO
* Full admin-level control

---

## 6. Templates System (Planned)

```text
templates/
├─ base.html
├─ partials/
│  ├─ header.html
│  ├─ footer.html
│  └─ filters.html
├─ pages/
│  ├─ home.html
│  ├─ cities.html
│  ├─ categories.html
│  ├─ search.html
│  └─ listing_detail.html
└─ errors/
   └─ 404.html
```

---

## 📘 Documentation & Update Protocol (MANDATORY)

This README is a **living document** and the only authoritative reference for this project.

### Update Rules

* After **every meaningful commit**, a new entry **must** be added to the Change Log below.
* Each entry must clearly describe:

  * What was implemented or changed
  * Why it was implemented (architectural intent)
  * What the next logical step is

Any AI reading this file must be able to **continue development without asking clarifying questions**.

---

## 🧱 Project Change Log (Single Source of Truth)

### Version 0 — Project Bootstrap (Completed)

**Scope:** Infrastructure & architectural foundation.

**Work done**

* Django monolithic project initialized (root-based).
* Clean, scalable folder structure created.
* Multi-environment settings implemented (`base / dev / prod`).
* All domain apps scaffolded (no business logic yet).
* Git repository freshly initialized and pushed.
* Architecture, rules, and roadmap documented here.

**Result**
The project is structurally stable and ready for domain-driven implementation.

**Next step**
➡️ Implement **location** domain model (first real business logic).

---

## Project Identity

**VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO — without frontend frameworks.**

```
```

---
---

### Version 1 — Locations Domain & Cities Directory (Completed)

**Scope:** Foundational geographical domain and first public discovery page.

**What was implemented**

- Implemented the **Locations domain model** with three explicit entities:
  - **Province**: backend-only geographical taxonomy (not exposed in URLs).
  - **City**: primary public location unit, exposed in URLs (`/s/{city}`) with a globally unique slug.
  - **Area**: sub-location scoped to a city, exposed in URLs (`/s/{city}/{area}`) with per-city uniqueness.
- Enforced all critical domain rules at the **database level** using constraints to prevent invalid or ambiguous data.
- Implemented Django Admin interfaces for managing provinces, cities, and areas, including automatic slug generation.
- Established a **root-based template architecture** for SSR and SEO control.
- Implemented the `/cities/` directory page to list all active cities as the first public entry point.
- Completed the first full vertical slice: database → ORM → view → template → URL.

**Architectural intent**

- Province is intentionally excluded from the URL structure to keep routing simple and stable while remaining available for internal organization and future expansion.
- City slugs are globally unique to eliminate routing ambiguity.
- Area slugs are unique per city to align with path-based search URLs.
- All pages are rendered server-side to ensure crawlability, performance, and predictable HTML output.

**Result**

- The location system is stable, extensible, and SEO-safe.
- URL rules are strictly enforced by the database.
- The project now has a reliable foundation for search and listings.

**Next step**

➡️ Implement the search entry page for `/s/{city}`.
