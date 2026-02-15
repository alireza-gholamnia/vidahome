"""
اسکریپت seed برای پر کردن دیتابیس با داده‌های واقعی.
استفاده: python manage.py seed_data [--clear]
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

User = get_user_model()


# --- داده‌های ثابت ---
PROVINCES_DATA = [
    ("tehran", "تهران", "Tehran"),
    ("isfahan", "اصفهان", "Isfahan"),
    ("shiraz", "شیراز", "Shiraz"),
    ("mashhad", "مشهد", "Mashhad"),
    ("tabriz", "تبریز", "Tabriz"),
]

CITIES_DATA = {
    "tehran": [
        ("tehran", "تهران", "Tehran"),
    ],
    "isfahan": [
        ("isfahan", "اصفهان", "Isfahan"),
        ("kashan", "کاشان", "Kashan"),
    ],
    "shiraz": [
        ("shiraz", "شیراز", "Shiraz"),
        ("marvdasht", "مرودشت", "Marvdasht"),
    ],
    "mashhad": [
        ("mashhad", "مشهد", "Mashhad"),
        ("torbat-heydariyeh", "تربت حیدریه", "Torbat Heydariyeh"),
    ],
    "tabriz": [
        ("tabriz", "تبریز", "Tabriz"),
        ("maragheh", "مراغه", "Maragheh"),
    ],
}

AREAS_DATA = {
    "tehran": [
        ("niavaran", "نیاوران", "Niavaran"),
        ("elahiyeh", "الهیه", "Elahiyeh"),
        ("zafaranieh", "زعفرانیه", "Zafaranieh"),
        ("shemiran", "شمیران", "Shemiran"),
        ("pasdaran", "پاسداران", "Pasdaran"),
        ("vanak", "ونک", "Vanak"),
        ("saadatabad", "سعادت‌آباد", "Saadatabad"),
        ("ekbatan", "اکباتان", "Ekbatan"),
    ],
    "isfahan": [
        ("jolfa", "جلفا", "Jolfa"),
        ("chahar-bagh", "چهارباغ", "Chahar Bagh"),
        ("baharestan", "بهارستان", "Baharestan"),
    ],
    "shiraz": [
        ("golestan", "گلستان", "Golestan"),
        ("elham", "الهام", "Elham"),
        ("azadi", "آزادی", "Azadi"),
    ],
    "mashhad": [
        ("koohsangi", "کوهسنگی", "Koohsangi"),
        ("vakilabad", "وکیل‌آباد", "Vakilabad"),
    ],
    "tabriz": [
        ("valiasr", "ولیعصر", "Valiasr"),
        ("abresan", "ابرسان", "Abresan"),
    ],
}

CATEGORIES_ROOT = [
    ("apartment", "آپارتمان", "Apartment"),
    ("villa", "ویلا", "Villa"),
    ("land", "زمین", "Land"),
    ("commercial", "تجاری", "Commercial"),
]

CATEGORIES_CHILD = {
    "apartment": [
        ("apartment-2room", "آپارتمان دو خوابه", "2-Room Apartment"),
        ("apartment-3room", "آپارتمان سه خوابه", "3-Room Apartment"),
        ("apartment-duplex", "آپارتمان دوبلکس", "Duplex Apartment"),
    ],
    "villa": [
        ("villa-standard", "ویلا استاندارد", "Standard Villa"),
        ("villa-luxury", "ویلا لاکچری", "Luxury Villa"),
    ],
    "land": [
        ("land-residential", "زمین مسکونی", "Residential Land"),
        ("land-agricultural", "زمین کشاورزی", "Agricultural Land"),
    ],
    "commercial": [
        ("shop", "مغازه", "Shop"),
        ("office", "دفتر", "Office"),
    ],
}

LISTING_TITLES_BUY = [
    "آپارتمان نوساز در {area} با بالکن و پارکینگ",
    "ویلا کلاسیک با حیاط و باغچه در {area}",
    "زمین آماده ساخت با سند شش‌دانگ در {area}",
    "آپارتمان دو خوابه شمالی در {area}",
    "مغازه با ویترین در {area}",
    "آپارتمان سه خوابه با آسانسور در {area}",
]

LISTING_TITLES_RENT = [
    "اجاره آپارتمان مبله در {area}",
    "اجاره کوتاه مدت ویلا در {area}",
    "اجاره مغازه با موقعیت عالی در {area}",
]

AGENCY_NAMES = [
    "مشاوره املاک کیان",
    "دفتر املاک پرشیا",
    "آژانس املاک آرش",
    "مشاوره املاک سایه",
]

INTRO_TEMPLATES = [
    "منطقه {name} یکی از محلات پرطرفدار و دارای دسترسی مناسب به مراکز تجاری و حمل و نقل عمومی است.",
    "محله {name} با امکانات رفاهی و فضای سبز مناسب، گزینه مناسبی برای سکونت است.",
]


def _random_phone():
    return f"0{random.randint(911, 999)}{random.randint(1000000, 9999999)}"


def _random_price_buy():
    return random.choice([
        random.randint(3_000_000_000, 8_000_000_000),
        random.randint(800_000_000, 2_500_000_000),
    ])


def _random_price_rent():
    return random.randint(15_000_000, 80_000_000)


class Command(BaseCommand):
    help = "پر کردن دیتابیس با داده‌های نمونه واقعی"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="پاک کردن داده‌های قبلی قبل از seed (به جز superuser)",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear_data()

        self._seed_groups()
        self._seed_locations()
        self._seed_categories()
        users_data = self._seed_users()
        agencies_data = self._seed_agencies(users_data)
        self._seed_listings(agencies_data)
        self._seed_city_categories()
        self._seed_city_area_categories()
        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))

    def _clear_data(self):
        from apps.listings.models import Listing, ListingImage
        from apps.seo.models import CityCategory, CityAreaCategory
        from apps.agencies.models import Agency, AgencyImage
        from apps.categories.models import Category, CategoryImage
        from apps.locations.models import Province, City, Area, CityImage, AreaImage

        ListingImage.objects.all().delete()
        Listing.objects.all().delete()
        CityAreaCategory.objects.all().delete()
        CityCategory.objects.all().delete()
        AgencyImage.objects.all().delete()
        Agency.objects.all().delete()
        CategoryImage.objects.all().delete()
        Category.objects.all().delete()
        AreaImage.objects.all().delete()
        Area.objects.all().delete()
        CityImage.objects.all().delete()
        City.objects.all().delete()
        Province.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()
        Group.objects.all().delete()

        self.stdout.write("Previous data cleared.")

    def _seed_groups(self):
        groups = ["site_admin", "seo_admin", "member", "independent_agent", "agency_owner", "agency_employee"]
        for g in groups:
            Group.objects.get_or_create(name=g)
        self.stdout.write(f"  Groups: {len(groups)}")

    def _seed_locations(self):
        from apps.locations.models import Province, City, Area

        province_map = {}
        for slug, fa, en in PROVINCES_DATA:
            p, _ = Province.objects.get_or_create(
                slug=slug,
                defaults={"fa_name": fa, "en_name": en, "sort_order": len(province_map)},
            )
            province_map[slug] = p

        city_map = {}
        for prov_slug, cities in CITIES_DATA.items():
            province = province_map[prov_slug]
            for slug, fa, en in cities:
                c, _ = City.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "province": province,
                        "fa_name": fa,
                        "en_name": en,
                        "intro_content": f"شهر {fa} یکی از شهرهای مهم ایران است.",
                        "sort_order": len(city_map),
                    },
                )
                city_map[slug] = c

        area_map = {}
        for city_slug, areas in AREAS_DATA.items():
            city = city_map.get(city_slug)
            if not city:
                continue
            for slug, fa, en in areas:
                a, _ = Area.objects.get_or_create(
                    city=city,
                    slug=slug,
                    defaults={
                        "fa_name": fa,
                        "en_name": en,
                        "intro_content": f"محله {fa} در {city.fa_name}.",
                        "sort_order": len([x for x in area_map if x.startswith(city_slug)]),
                    },
                )
                area_map[f"{city_slug}_{slug}"] = a

        self.stdout.write(f"  Provinces: {len(province_map)}, Cities: {len(city_map)}, Areas: {len(area_map)}")
        return {"provinces": province_map, "cities": city_map, "areas": area_map}

    def _seed_categories(self):
        from apps.categories.models import Category

        root_map = {}
        for slug, fa, en in CATEGORIES_ROOT:
            c, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"fa_name": fa, "en_name": en, "sort_order": len(root_map)},
            )
            root_map[slug] = c

        all_cats = list(root_map.values())
        for parent_slug, children in CATEGORIES_CHILD.items():
            parent = root_map.get(parent_slug)
            if not parent:
                continue
            for slug, fa, en in children:
                c, _ = Category.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "parent": parent,
                        "fa_name": fa,
                        "en_name": en,
                        "sort_order": len(all_cats),
                    },
                )
                all_cats.append(c)

        self.stdout.write(f"  Categories: {len(all_cats)}")
        return all_cats

    def _seed_users(self):
        member_grp = Group.objects.filter(name="member").first()
        owner_grp = Group.objects.filter(name="agency_owner").first()
        employee_grp = Group.objects.filter(name="agency_employee").first()

        owners = []
        for i, name in enumerate(["رضا محمدی", "سارا احمدی", "علی کریمی", "مریم حسینی"]):
            username = f"owner{i+1}"
            u, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": name.split()[0],
                    "last_name": name.split()[1] if len(name.split()) > 1 else "",
                    "phone": _random_phone(),
                    "is_verified": random.choice([True, False]),
                },
            )
            u.set_password("test1234")
            u.save()
            if owner_grp:
                u.groups.add(owner_grp)
            owners.append(u)

        employees = []
        for i, name in enumerate(["امیر زارعی", "نرگس رضایی", "کامران نوری", "فاطمه موسوی", "حسین صادقی"]):
            username = f"emp{i+1}"
            u, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": name.split()[0],
                    "last_name": name.split()[1] if len(name.split()) > 1 else "",
                    "phone": _random_phone(),
                },
            )
            u.set_password("test1234")
            u.save()
            if employee_grp:
                u.groups.add(employee_grp)
            employees.append(u)

        for i in range(3):
            username = f"user{i+1}"
            u, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": f"کاربر{i+1}",
                    "last_name": "تست",
                    "phone": _random_phone(),
                },
            )
            u.set_password("test1234")
            u.save()
            if member_grp:
                u.groups.add(member_grp)

        self.stdout.write(f"  Users: {len(owners) + len(employees) + 3}")
        return {"owners": owners, "employees": employees}

    def _seed_agencies(self, users_data):
        from apps.locations.models import City
        from apps.agencies.models import Agency

        owners = users_data["owners"]
        employees = users_data["employees"]
        cities = list(City.objects.all())

        agencies = []
        for i, (owner, name) in enumerate(zip(owners[: len(AGENCY_NAMES)], AGENCY_NAMES)):
            slug = name.replace(" ", "-").replace("‌", "-").lower()[:50]
            slug = "".join(c if c.isalnum() or c == "-" else "" for c in slug)
            slug = slug or f"agency-{i+1}"
            a, _ = Agency.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "owner": owner,
                    "phone": _random_phone(),
                    "address": f"تهران، خیابان ولیعصر، پلاک {100 + i}",
                    "intro_content": f"مشاوره املاک {name} با سال‌ها تجربه در خرید و فروش املاک.",
                    "is_active": True,
                },
            )
            if cities:
                a.cities.add(*random.sample(cities, min(2, len(cities))))
            agencies.append(a)

        for agency, emp in zip(agencies, employees[: len(agencies)]):
            emp.agency = agency
            emp.save()

        self.stdout.write(f"  Agencies: {len(agencies)}")
        return agencies

    def _seed_listings(self, agencies):
        from apps.listings.models import Listing
        from apps.locations.models import City, Area
        from apps.categories.models import Category

        cities = list(City.objects.all())
        categories = list(Category.objects.filter(parent__isnull=False)) or list(Category.objects.all())
        if not cities or not categories:
            self.stdout.write(self.style.WARNING("  Listings: Skipped (need City and Category)"))
            return

        deals = [Listing.Deal.BUY, Listing.Deal.RENT]
        count = 0
        for _ in range(60):
            city = random.choice(cities)
            areas = list(Area.objects.filter(city=city))
            area = random.choice(areas) if areas else None
            category = random.choice(categories)
            deal = random.choice(deals)

            if deal == Listing.Deal.BUY:
                title_tpl = random.choice(LISTING_TITLES_BUY)
                price = _random_price_buy()
                price_unit = "تومان"
            else:
                title_tpl = random.choice(LISTING_TITLES_RENT)
                price = _random_price_rent()
                price_unit = "تومان / ماه"

            area_name = area.fa_name if area else city.fa_name
            title = title_tpl.format(area=area_name)

            agency = random.choice(agencies) if agencies else None
            Listing.objects.create(
                title=title,
                city=city,
                category=category,
                deal=deal,
                area=area,
                status=Listing.Status.PUBLISHED,
                published_at=timezone.now() - timedelta(days=random.randint(0, 90)),
                short_description=f"ملک در محله {area_name} با امکانات کامل.",
                description=f"<p>توضیحات کامل برای {title}</p>",
                price=price,
                price_unit=price_unit,
                agency=agency,
                created_by=agency.owner if agency else None,
            )
            count += 1

        self.stdout.write(f"  Listings: {count}")

    def _seed_city_categories(self):
        from apps.seo.models import CityCategory
        from apps.locations.models import City
        from apps.categories.models import Category

        cities = list(City.objects.all()[:3])
        categories = list(Category.objects.filter(parent__isnull=True)[:2])
        count = 0
        for city in cities:
            for cat in categories:
                _, created = CityCategory.objects.get_or_create(
                    city=city,
                    category=cat,
                    defaults={
                        "intro_content": f"آگهی‌های {cat.fa_name} در {city.fa_name}.",
                        "is_active": True,
                    },
                )
                if created:
                    count += 1
        self.stdout.write(f"  CityCategory: {count}")

    def _seed_city_area_categories(self):
        from apps.seo.models import CityAreaCategory
        from apps.locations.models import City, Area
        from apps.categories.models import Category

        cities = list(City.objects.all()[:2])
        count = 0
        for city in cities:
            areas = list(Area.objects.filter(city=city)[:2])
            categories = list(Category.objects.filter(parent__isnull=False)[:2])
            for area in areas:
                for cat in categories:
                    try:
                        _, created = CityAreaCategory.objects.get_or_create(
                            city=city,
                            area=area,
                            category=cat,
                            defaults={
                                "intro_content": f"Aghahi haye {cat.fa_name} dar {area.fa_name}.",
                                "is_active": True,
                            },
                        )
                        if created:
                            count += 1
                    except Exception:
                        pass
        self.stdout.write(f"  CityAreaCategory: {count}")
