VidaHome — Complete Project Description

(Django Monolith + Django Templates)

1) Vision & Philosophy

VidaHome یک پلتفرم حرفه‌ای، مقیاس‌پذیر و SEO-first در حوزه املاک است که با هدف حل مشکلات بنیادی بازار املاک طراحی شده است؛ نه صرفاً ساخت یک وب‌سایت آگهی.

مشکلاتی که VidaHome حل می‌کند:

ساختار ضعیف و غیرمنطقی دسته‌بندی در سایت‌های املاک

فیلترهای محدود، غیرقابل توسعه و وابسته به UI

SEO ناکارآمد، غیرقابل کنترل و وابسته به hardcode

قاطی شدن مفاهیم دامنه‌ای (نوع ملک، نوع معامله، ویژگی‌ها)

ناتوانی در توسعه به شهرها، مناطق و سناریوهای پیچیده

VidaHome از ابتدا با رویکردی سیستمی، الگوریتمی و دیتامحور طراحی شده و تمرکز آن روی Domain Modeling صحیح است.

2) Architecture Overview
Monolithic Django Architecture (Root-based)

پروژه به‌صورت Django Monolith کلاسیک و بدون لایه‌ی اضافی backend پیاده‌سازی شده است.
Django مستقیماً در روت پروژه قرار دارد و مسئول routing، rendering، ORM و SEO است.

vidahome/
├─ manage.py
├─ config/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ wsgi.py
│  ├─ urls.py
│  └─ settings/
│     ├─ __init__.py
│     ├─ base.py
│     ├─ dev.py
│     └─ prod.py
│
├─ apps/
│  ├─ common/
│  ├─ locations/
│  ├─ categories/
│  ├─ attributes/
│  ├─ listings/
│  ├─ blog/
│  └─ seo/
│
├─ templates/
├─ static/
├─ media/
└─ docs/

فلسفه این معماری

سادگی عملیاتی و کاهش پیچیدگی ذهنی

SEO طبیعی و قابل کنترل با Server-Side Rendering

عدم نیاز به hydration، SPA routing یا frontend framework

کنترل کامل HTML خروجی

مناسب بازار ایران و crawl گوگل

3) Rendering Strategy
Django Templates (SSR)

تمام صفحات با Django Templates رندر می‌شوند

HTML کامل در سمت سرور ساخته می‌شود

داده‌ها مستقیم از ORM دریافت می‌شوند

JavaScript صرفاً برای بهبود UX (اختیاری)

نتیجه:

سریع

قابل Crawl

قابل Debug

پایدار

4) URL System (Final & Approved)
Static Pages
/
/about
/contact
/terms
/privacy

Directory Pages
/cities
/categories

Search Engine (Core)
/s
/s/{category}
/s/{city}
/s/{city}/{category}
/s/{city}/{area}
/s/{city}/{area}/{category}

Rules (غیرقابل تغییر)

city / area / category → فقط در URL path

deal → فقط query param (?deal=rent)

attributes → فقط query param

deal پیش‌فرض = buy

هیچ redirect در پروژه Django انجام نمی‌شود

Listing Detail Page
/l/{listingId}-{slug}


ID منبع حقیقت (Source of Truth)

slug صرفاً برای SEO

مستقل از city و category

5) Backend Domain Design (Django Apps)
5.1 locations app (⏳ طراحی دامنه – پیاده‌سازی در فاز بعد)

مدیریت ساختار جغرافیایی.

Entities:

Province

City

Area

Fields مشترک:

name (فارسی)

en_name (انگلیسی)

slug (SEO)

is_active

sort_order

Behavior:

slug از en_name ساخته می‌شود (در Admin)

slug قابل ویرایش است

Area در سطح City یکتا است

کاربرد:

ساخت صفحات /cities

ساخت مسیرهای سرچ

پایه SEO محلی

5.2 categories app (⏳ طراحی شده)

نمایانگر «چه چیزی لیست شده».

Examples:

apartment

villa

land

commercial

Rules:

مستقل از deal

استفاده در URL path

پایدار و کم‌تغییر

5.3 attributes app (⏳ Core System)

سیستم ویژگی‌های پویا (الهام‌گرفته از E-commerce).

Entities:

Attribute

AttributeOption

ListingAttribute

Rules:

Attribute به Category متصل است

انواع:

select

number

boolean

text

اعتبارسنجی سمت سرور

Example:

Category: land
Attributes:
- usage (residential, commercial)
- area_size
- document


«مسکونی» Attribute است، نه Category.

5.4 listings app (⏳ Core Engine)

هسته سیستم.

Listing:

city

area

category

deal (buy | rent)

attributes (dynamic)

images (ordered)

status / publish state

Search Logic:

ترکیب path params + query params

ORM-based filtering

pagination

آماده cache شدن

5.5 seo app (⏳ Strategic Advantage)

SEO کاملاً دیتابیس‌محور.

SEOPage:

path

deal (optional)

title

meta description

h1

content

canonical

noindex

نتیجه:

هزاران landing page بدون hardcode

کنترل کامل SEO از Admin

6) Templates System
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

7) Current Implementation Status (Updated)
Module	Status
Django core (project bootstrap)	✅ Done
Project folder structure	✅ Done
Multi-environment settings (base/dev/prod)	✅ Done
Apps scaffolding (all apps created)	✅ Done
Git repository (fresh init + push)	✅ Done
Locations domain models	❌
Categories domain models	❌
Attributes system	❌
Listings engine	❌
SEO system	❌
Templates implementation	⏳
8) Design Principles (قطعی)

Django-first

Server-side rendering

SEO driven by database

No JS dependency for core UX

Clear domain separation

Query-based filtering

9) Roadmap (Logical Order)

categories app

attributes app

listings engine

search template

SEO system

performance & cache

deployment

10) Project Identity (One-liner)

VidaHome is a Django-based, SEO-first real estate platform designed with a domain-driven architecture to handle complex property data, scalable search, and database-controlled SEO — without frontend frameworks.