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


---

### Version 2 — Search Namespace + City Landing (Completed)

**Scope:** Establish the `/s/` search namespace and implement the first search landing page: `/s/{city}`.

**What was implemented**
- Implemented the `/s/` URL namespace as the non-negotiable entry for all search-related paths.
- Explicitly **removed** the concept of a “search root page”:
  - Requests to `/s/` (or `/s`) are redirected to the home page (`/`) to avoid thin/meaningless content.
- Implemented the **City Landing** page at:
  - `/s/{city}/`
- City resolution is performed by `City.slug` (globally unique) and only active cities are accessible.
- Implemented a dedicated SSR template for the city landing page as the foundation for future listings, filters, and SEO content injection.

**Architectural intent**
- `/s/` is a **namespace**, not a page.
- Landing pages must only exist when a valid **context** exists (city / area / category). `/s/` alone has no context, so it must not render a page.
- `City.slug` remains globally unique to eliminate routing ambiguity for `/s/{city}`.
- The City Landing is intentionally named `city_landing` (not `search_city`) to keep it future-proof and compatible with database-driven SEO pages.

**Result**
- Search routing foundation is now established and stable.
- `/s/{city}/` is live as the first public search landing page and is ready to be extended with:
  - `/s/{city}/{area}/`
  - `/s/{city}/{category}/`
  - query-param filtering for `deal` and dynamic `attributes`.

**Next step**
➡️ Implement the `categories` domain model and add `/s/{city}/{category}/`.

---

### Version 3 — Area Discovery + Area Landing (Completed)

**Scope:** Extend search paths to support area-level navigation and discovery.

**What was implemented**
- Implemented area discovery on the City Landing page:
  - `/s/{city}/` now lists all active areas of the resolved city for internal linking.
- Implemented Area Landing page:
  - `/s/{city}/{area}/`
- Area resolution is scoped to the resolved city to ensure path consistency and avoid ambiguity.

**Architectural intent**
- City Landing acts as a discovery hub for sub-locations (areas) without introducing province into any URL.
- Area Landing establishes the canonical path structure for future listing results and SEO content injection.
- URL structure remains path-driven for location context; filtering (deal/attributes) will remain query-driven.

**Result**
- Search navigation now supports city → area progression with clean SSR pages.
- The system is ready for connecting listings and adding category paths.

**Next step**
➡️ Implement the `categories` domain model and add `/s/{city}/{category}/`.


---

### Version 4 — Categories Domain (Tree-Based) (Completed)

**Scope:** Implement a stable, extensible category taxonomy with parent/child hierarchy.

**What was implemented**
- Implemented the `Category` domain model as a tree using a self-referential parent relation.
- Categories now support:
  - optional `parent` (for hierarchy)
  - reverse `children` relation (for sub-categories)
- Enforced global uniqueness for `Category.slug` to keep URL paths unambiguous.
- Added safeguards to prevent invalid trees (self-parenting and cyclic parent chains).
- Implemented Django Admin for category management with automatic slug generation.

**Architectural intent**
- Categories represent *what is listed* and remain deal-independent.
- Parent/child hierarchy is for taxonomy and attribute binding; it is not exposed in URL paths.
- Global unique slugs ensure deterministic routing for `/s/{city}/{category}` and related paths.

**Result**
- Category taxonomy is ready for search routing integration and for binding dynamic attributes.

**Next step**
➡️ Implement the resolver and routing strategy for `/s/{slug}/` and `/s/{city}/{category}/` without path ambiguity.


---

### Version 5 — Search URL System Completed (City/Area/Category) (Completed)

**Scope:** Implement the full search path grammar under `/s` as defined in the non-negotiable URL spec.

**What was implemented**
- Implemented `/s` as a namespace-only route:
  - `/s` and `/s/` redirect to `/` (no thin “search root” page).
- Implemented Category Landing:
  - `/s/{category}/` → `category_landing`
- Implemented City Landing:
  - `/s/{city}/` → `city_landing` (lists active areas for discovery and internal linking)
- Implemented City Context Resolver (2nd segment under city):
  - `/s/{city}/{area}/` → Area Landing (resolved first, scoped to city)
  - `/s/{city}/{category}/` → City + Category Landing
- Implemented Area + Category Landing:
  - `/s/{city}/{area}/{category}/` → `area_category`

**Architectural intent**
- `/s` is a routing namespace, not a page.
- Location/category context must be path-based; `deal` and dynamic attributes remain query-param only.
- The route shape `/s/{city}/{x}` is ambiguous by design, so a resolver is required.
  - The resolver prioritizes Area (scoped to city) over Category to preserve location semantics.
- Pages are SSR landings (placeholders for now) and are intentionally named as landings/contexts, not “results”.

**Result**
- The project now supports all required search URL patterns with deterministic resolution:
  - `/s/{category}`
  - `/s/{city}`
  - `/s/{city}/{category}`
  - `/s/{city}/{area}`
  - `/s/{city}/{area}/{category}`
- Ready for the Listings engine integration (ORM filtering + pagination + caching).

**Next step**
➡️ Implement the `Listing` model and connect these paths to real ORM-based search results, keeping `deal` and attributes as query params.
---

### Version 6 — Fix `/s/{slug}` Ambiguity with Single Resolver (Completed)

**Scope:** Resolve routing ambiguity between `/s/{category}` and `/s/{city}`.

**Problem**
- Both `/s/{category}` and `/s/{city}` have identical URL shape and cannot coexist as separate routes.
- Django matched the first pattern, causing `/s/{city}` to incorrectly hit `category_landing` and return 404.

**What was implemented**
- Replaced separate one-segment routes with a single resolver:
  - `/s/{slug}/` → resolves deterministically to:
    1) City landing (if City.slug matches)
    2) Category landing (if Category.slug matches)
    3) 404 otherwise
- Kept existing resolver for two-segment routes:
  - `/s/{city}/{area}/` (Area scoped to city, resolved first)
  - `/s/{city}/{category}/` (Category resolved if no Area match)
- Maintained `/s/` as a namespace-only redirect to `/`.

**Architectural intent**
- URL patterns must remain non-negotiable while avoiding ambiguous Django routing.
- A single resolver preserves clean paths and keeps the system deterministic.
- Location semantics stay dominant (City > Category, Area > Category).

**Result**
- `/s/{city}/` works reliably alongside `/s/{category}/` with no routing conflicts.
- Search URL grammar is now stable and ready for listings integration.

**Next step**
➡️ Implement the `Listing` model and wire real ORM filtering into these landing pages.
