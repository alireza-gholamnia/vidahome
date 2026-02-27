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

SERVICE_CATEGORIES = [
    ("renovation", "بازسازی", "Renovation"),
    ("interior-design", "طراحی داخلی", "Interior Design"),
    ("legal-consulting", "مشاوره حقوقی", "Legal Consulting"),
]

PROJECT_CATEGORIES = [
    ("project-presale", "پیش‌فروش پروژه", "Project Presale"),
    ("project-tower", "پروژه برج", "Tower Project"),
    ("project-town", "پروژه شهرک", "Town Project"),
]

CONTENT_TAG_CATEGORIES = [
    ("pre-sale", "پیش‌فروش", "Pre Sale"),
    ("luxury", "لوکس", "Luxury"),
    ("sea-view", "ساحلی", "Sea View"),
]

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

# --- توضیحات طولانی شهرها ---
CITY_INTROS = {
    "tehran": """تهران پایتخت ایران و بزرگ‌ترین شهر کشور است. این کلان‌شهر با جمعیت بالغ بر ۸ میلیون نفر، مرکز سیاسی، اقتصادی و فرهنگی ایران به شمار می‌رود. تهران از شمال به کوه‌های البرز و از جنوب به دشت ری محدود می‌شود. بناهای تاریخی متعددی چون کاخ گلستان، برج میلاد و موزه ملی ایران در این شهر قرار دارند. حمل و نقل عمومی شامل مترو، اتوبوس و تاکسی است و فرودگاه بین‌المللی امام خمینی و مهرآباد در نزدیکی شهر واقع شده‌اند.""",
    "isfahan": """اصفهان با لقب نصف جهان، سومین شهر پرجمعیت ایران و یکی از زیباترین شهرهای تاریخی جهان است. میدان نقش جهان، مسجد شیخ لطف‌الله، کاخ چهل‌ستون و سی‌وسه‌پل از معروف‌ترین بناهای آن هستند. اصفهان در مرکز ایران قرار دارد و صنایع دستی آن همچون مینیاتور، قلمزنی و فرش اصفهان شهرت جهانی دارند. زاینده‌رود از میان شهر می‌گذرد و خیابان چهارباغ عباسی یکی از زیباترین خیابان‌های تاریخی کشور است.""",
    "shiraz": """شیراز، شهر شعر و ادب پارسی و مهد تمدن ایران باستان است. آرامگاه حافظ و سعدی، دروازه قرآن، باغ ارم و باغ نارنجستان قوام از جاذبه‌های گردشگری معروف آن هستند. شیراز همچنین به دروازه تخت جمشید و پاسارگاد نزدیک است. هوای معتدل و باغات سرسبز آن شهرت دارد و صنایع دستی مانند خاتم‌کاری و مسگری در آن رونق دارد.""",
    "mashhad": """مشهد، دومین کلان‌شهر ایران و مهم‌ترین شهر مذهبی کشور است. حرم امام رضا (ع) میلیون‌ها زائر سالانه را به خود جذب می‌کند. این شهر در شمال شرقی ایران قرار دارد و مرکز استان خراسان رضوی است. صنعت فرش، زعفران و خشکبار در مشهد رونق دارد. پارک کوهسنگی، آرامگاه فردوسی در طوس و بازار رضا از جمله مکان‌های دیدنی آن هستند.""",
    "tabriz": """تبریز یکی از شهرهای تاریخی و مهم شمال غرب ایران است. بازار تبریز که بزرگ‌ترین بازار مسقف جهان است، در فهرست میراث جهانی یونسکو ثبت شده. مقبرهٔ الشعرا، ارگ علی‌شاه، مسجد کبود و موزه آذربایجان از جاذبه‌های آن هستند. تبریز زادگاه بسیاری از بزرگان ادب و هنر و پایتخت فرش ایران است. آب و هوای سرد و کوهستانی دارد و صنعت چرم و صنایع غذایی در آن فعال است.""",
    "kashan": """کاشان شهری تاریخی در حاشیه دشت کویر است که به باغ‌های فین، خانه‌های تاریخی چون خانه بروجردی‌ها و عباسیان، و صنعت گلاب و عرقیات شهرت دارد. مسجد جامع کاشان و حمام سلطان امیراحمد از بناهای دیدنی آن هستند.""",
    "marvdasht": """مرودشت در نزدیکی شیراز و تخت جمشید قرار دارد. این شهر به عنوان دروازه تخت جمشید شناخته می‌شود و بسیاری از گردشگران از آن به عنوان پایگاه سفر به پرسپولیس استفاده می‌کنند. زمین‌های کشاورزی و باغات مرودشت بسیار حاصل‌خیز است.""",
    "torbat-heydariyeh": """تربت حیدریه شهری در خراسان رضوی و در مسیر مشهد به زاهدان است. این شهر به زعفران و خشکبار معروف است و صنایع دستی مانند قالی و گلیم در آن تولید می‌شود.""",
    "maragheh": """مراغه شهری تاریخی در آذربایجان شرقی است که رصدخانه مراغه (ساخته شده در دوره هلاکوخان) از مهم‌ترین جاذبه‌های آن است. گنبد سرخ و برج مدور از دیگر بناهای تاریخی این شهر هستند.""",
}

CITY_MAIN_CONTENT_TEMPLATE = """
<p><strong>درباره شهر {fa_name}</strong></p>
<p>{intro}</p>
<p>بازار املاک در {fa_name} همواره فعال بوده و تنوع خوبی از آپارتمان، ویلا، زمین و املاک تجاری را ارائه می‌دهد. با توجه به موقعیت جغرافیایی و امکانات رفاهی، قیمت مسکن در مناطق مختلف متفاوت است. پیشنهاد می‌کنیم قبل از تصمیم‌گیری، از مشاوران املاک معتبر منطقه راهنمایی بگیرید.</p>
<p>دسترسی به مراکز درمانی، مدارس، دانشگاه‌ها و مراکز خرید در انتخاب محل سکونت بسیار مهم است. بسیاری از محلات {fa_name} از امکانات حمل و نقل عمومی مناسبی برخوردارند.</p>
<p>اگر قصد سرمایه‌گذاری یا سکونت در {fa_name} را دارید، می‌توانید از طریق لیست آگهی‌های ما بهترین گزینه‌ها را بررسی و مقایسه کنید.</p>
"""

# --- توضیحات طولانی محلات ---
AREA_INTROS = {
    "tehran_niavaran": """نیاوران در شمال تهران و در منطقه شمیرانات قرار دارد. این محله به کاخ نیاوران، پارک نیاوران و سفارتخانه‌های متعدد معروف است. از محلات مرفه و گران‌قیمت تهران به شمار می‌رود و دسترسی خوبی به اتوبان صیاد شیرازی و خیابان ولیعصر دارد.""",
    "tehran_elahiyeh": """الهیه از محلات قدیمی و گران شمال تهران است. کوچه‌های درخت‌دار، ویلاهای قدیمی و نزدیکی به پاسداران و تجریش از ویژگی‌های آن است. دسترسی به مراکز خرید و رستوران‌های معروف در این منطقه عالی است.""",
    "tehran_zafaranieh": """زعفرانیه در دامنه کوه و با هوای پاک‌تر نسبت به مرکز شهر، یکی از گران‌ترین محلات تهران است. ساختمان‌های نوساز و قدیمی در کنار هم دیده می‌شوند و امکانات رفاهی مناسبی دارد.""",
    "tehran_shemiran": """شمیران نام منطقه‌ای گسترده در شمال تهران است که شامل محلات مختلفی می‌شود. آب و هوای خنک‌تر، فضای سبز بیشتر و دوری از شلوغی مرکز از مزایای زندگی در این منطقه است.""",
    "tehran_pasdaran": """پاسداران یکی از محلات پرطرفدار شرق تهران با دسترسی عالی به اتوبان صیاد شیرازی و همت است. مراکز خرید، بانک‌ها، کلینیک‌ها و مدارس متعددی در این منطقه قرار دارند.""",
    "tehran_vanak": """ونک از محلات مرکزی تهران با دسترسی خوب به مترو و اتوبان است. برج‌های تجاری، مراکز خرید و شرکت‌های بزرگ در اطراف میدان ونک متمرکز شده‌اند. ترافیک در ساعات اوج سنگین است.""",
    "tehran_saadatabad": """سعادت‌آباد در غرب تهران و در منطقه ۲ قرار دارد. جمعیت زیادی در این محله ساکن هستند و امکانات رفاهی، پارک‌ها و مراکز خرید متنوعی دارد. قیمت مسکن نسبت به شمال تهران مناسب‌تر است.""",
    "tehran_ekbatan": """اکباتان یکی از بزرگ‌ترین مجموعه‌های مسکونی تهران در غرب شهر است. سه فاز دارد و امکاناتی مانند مترو، پارک، مدرسه و مراکز خرید در خود محله فراهم است.""",
    "isfahan_jolfa": """جلفا محله تاریخی ارمنی‌نشین اصفهان است. کلیسای وانک، خانه‌های قدیمی و کافه‌های دنج از جاذبه‌های آن هستند. گردشگران بسیاری از این محله بازدید می‌کنند.""",
    "isfahan_chahar-bagh": """چهارباغ به خیابان تاریخی چهارباغ عباسی و میدان نقش جهان نزدیک است. بناهای تاریخی، هتل‌ها و رستوران‌های سنتی در این محدوده قرار دارند.""",
    "isfahan_baharestan": """بهارستان در شرق اصفهان و نزدیک به زاینده‌رود قرار دارد. پارک‌ها و فضای سبز مناسب و دسترسی به مرکز شهر از مزایای آن است.""",
    "shiraz_golestan": """گلستان یکی از محلات پرجمعیت و پررفاه شیراز است. دسترسی به باغ ارم، دانشگاه شیراز و مراکز خرید از ویژگی‌های آن است.""",
    "shiraz_elham": """الهام از محلات نوساز شیراز با امکانات مدرن است. قیمت مسکن در این منطقه نسبت به مرکز شهر مقرون‌به‌صرفه‌تر است.""",
    "shiraz_azadi": """آزادی در نزدیکی میدان آزادی شیراز قرار دارد و دسترسی مناسبی به مرکز شهر و خروجی‌های جاده‌ای دارد.""",
    "mashhad_koohsangi": """کوهسنگی از پارک‌های معروف مشهد و از محلات خوش‌مسیر این شهر است. نزدیکی به حرم و امکانات رفاهی مناسب از مزایای زندگی در این منطقه است.""",
    "mashhad_vakilabad": """وکیل‌آباد در غرب مشهد و نزدیک به باغ وکیل‌آباد قرار دارد. واحدهای مسکونی با تنوع قیمتی در این محله یافت می‌شوند.""",
    "tabriz_valiasr": """ولیعصر خیابان اصلی تبریز و از محلات پرتردد است. مراکز خرید، ادارات و بانک‌ها در این خیابان متمرکزند.""",
    "tabriz_abresan": """ابرسان از محلات قدیمی و پرجمعیت تبریز است. دسترسی به مرکز شهر و بازار تبریز مناسب است.""",
}

AREA_MAIN_TEMPLATE = """
<p><strong>درباره محله {fa_name}</strong></p>
<p>{intro}</p>
<p>بازار مسکن در محله {fa_name} {city_name} طی سال‌های اخیر رونق داشته است. برای خرید یا اجاره ملک در این منطقه، بهتر است چند آگهی را مقایسه کرده و در صورت امکان از محل بازدید حضوری داشته باشید. مشاوران املاک محلی می‌توانند در انتخاب بهترین گزینه به شما کمک کنند.</p>
"""


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
        self._seed_blog(users_data)
        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))

    def _clear_data(self):
        from apps.blog.models import BlogPost, BlogCategory
        from apps.listings.models import Listing, ListingImage
        from apps.seo.models import CityCategory, CityAreaCategory
        from apps.agencies.models import Agency, AgencyImage
        from apps.categories.models import Category, CategoryImage
        from apps.locations.models import Province, City, Area, CityImage, AreaImage

        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()
        ListingImage.objects.all().delete()
        Listing.objects.all().delete()
        CityAreaCategory.objects.all().delete()
        CityCategory.objects.all().delete()
        AgencyImage.objects.all().delete()
        Agency.objects.all().delete()
        CategoryImage.objects.all().delete()
        # حذف اول دسته‌های فرزند (به‌خاطر PROTECT روی parent)
        Category.objects.filter(parent__isnull=False).delete()
        Category.objects.filter(parent__isnull=True).delete()
        AreaImage.objects.all().delete()
        Area.objects.all().delete()
        CityImage.objects.all().delete()
        City.objects.all().delete()
        Province.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()
        Group.objects.all().delete()

        self.stdout.write("Previous data cleared.")

    def _seed_groups(self):
        groups = ["site_admin", "seo_admin", "member", "agency_owner", "agency_employee"]
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
                intro = CITY_INTROS.get(slug, f"شهر {fa} یکی از شهرهای مهم ایران است.")
                main_content = CITY_MAIN_CONTENT_TEMPLATE.format(fa_name=fa, intro=intro)
                c, created = City.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "province": province,
                        "fa_name": fa,
                        "en_name": en,
                        "intro_content": intro,
                        "main_content": main_content.strip(),
                        "sort_order": len(city_map),
                    },
                )
                if not created:
                    c.intro_content = intro
                    c.main_content = main_content.strip()
                    c.save(update_fields=["intro_content", "main_content"])
                city_map[slug] = c

        area_map = {}
        for city_slug, areas in AREAS_DATA.items():
            city = city_map.get(city_slug)
            if not city:
                continue
            for slug, fa, en in areas:
                key = f"{city_slug}_{slug}"
                intro = AREA_INTROS.get(key, f"محله {fa} در {city.fa_name}.")
                main_content = AREA_MAIN_TEMPLATE.format(
                    fa_name=fa, intro=intro, city_name=city.fa_name
                ).strip()
                a, created = Area.objects.get_or_create(
                    city=city,
                    slug=slug,
                    defaults={
                        "fa_name": fa,
                        "en_name": en,
                        "intro_content": intro,
                        "main_content": main_content,
                        "sort_order": len([x for x in area_map if x.startswith(city_slug)]),
                    },
                )
                if not created:
                    a.intro_content = intro
                    a.main_content = main_content
                    a.save(update_fields=["intro_content", "main_content"])
                area_map[key] = a

        self.stdout.write(f"  Provinces: {len(province_map)}, Cities: {len(city_map)}, Areas: {len(area_map)}")
        return {"provinces": province_map, "cities": city_map, "areas": area_map}

    def _seed_categories(self):
        from apps.categories.models import Category

        root_map = {}
        for idx, (slug, fa, en) in enumerate(CATEGORIES_ROOT):
            c, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "fa_name": fa,
                    "en_name": en,
                    "sort_order": idx,
                    "category_type": Category.CategoryType.PROPERTY,
                },
            )
            if not created:
                update_fields = []
                if c.category_type != Category.CategoryType.PROPERTY:
                    c.category_type = Category.CategoryType.PROPERTY
                    update_fields.append("category_type")
                if c.parent_id is not None:
                    c.parent = None
                    update_fields.append("parent")
                if c.fa_name != fa:
                    c.fa_name = fa
                    update_fields.append("fa_name")
                if c.en_name != en:
                    c.en_name = en
                    update_fields.append("en_name")
                if c.sort_order != idx:
                    c.sort_order = idx
                    update_fields.append("sort_order")
                if update_fields:
                    c.save(update_fields=update_fields)
            root_map[slug] = c

        all_cats = list(root_map.values())
        for parent_slug, children in CATEGORIES_CHILD.items():
            parent = root_map.get(parent_slug)
            if not parent:
                continue
            for slug, fa, en in children:
                c, created = Category.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "parent": parent,
                        "fa_name": fa,
                        "en_name": en,
                        "category_type": Category.CategoryType.PROPERTY,
                        "sort_order": len(all_cats),
                    },
                )
                if not created:
                    update_fields = []
                    if c.category_type != Category.CategoryType.PROPERTY:
                        c.category_type = Category.CategoryType.PROPERTY
                        update_fields.append("category_type")
                    if c.parent_id != parent.id:
                        c.parent = parent
                        update_fields.append("parent")
                    if c.fa_name != fa:
                        c.fa_name = fa
                        update_fields.append("fa_name")
                    if c.en_name != en:
                        c.en_name = en
                        update_fields.append("en_name")
                    if update_fields:
                        c.save(update_fields=update_fields)
                all_cats.append(c)

        for data, ctype in (
            (SERVICE_CATEGORIES, Category.CategoryType.SERVICE),
            (PROJECT_CATEGORIES, Category.CategoryType.PROJECT),
            (CONTENT_TAG_CATEGORIES, Category.CategoryType.CONTENT_TAG),
        ):
            for slug, fa, en in data:
                c, created = Category.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "parent": None,
                        "fa_name": fa,
                        "en_name": en,
                        "category_type": ctype,
                        "sort_order": len(all_cats),
                    },
                )
                if not created:
                    update_fields = []
                    if c.category_type != ctype:
                        c.category_type = ctype
                        update_fields.append("category_type")
                    if c.parent_id is not None:
                        c.parent = None
                        update_fields.append("parent")
                    if c.fa_name != fa:
                        c.fa_name = fa
                        update_fields.append("fa_name")
                    if c.en_name != en:
                        c.en_name = en
                        update_fields.append("en_name")
                    if update_fields:
                        c.save(update_fields=update_fields)
                all_cats.append(c)

        self.stdout.write(
            f"  Categories: {len(all_cats)} "
            f"(property={Category.property_queryset().count()}, "
            f"project={Category.objects.filter(category_type=Category.CategoryType.PROJECT).count()}, "
            f"service={Category.objects.filter(category_type=Category.CategoryType.SERVICE).count()}, "
            f"content_tag={Category.objects.filter(category_type=Category.CategoryType.CONTENT_TAG).count()})"
        )
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

        from apps.common.text_utils import slugify_from_title

        agencies = []
        for i, (owner, name) in enumerate(zip(owners[: len(AGENCY_NAMES)], AGENCY_NAMES)):
            slug = slugify_from_title(name, max_length=200) or f"agency-{i+1}"
            agency_intro = (
                f"مشاوره املاک {name} با بیش از پانزده سال سابقه در زمینه خرید، فروش و اجاره املاک مسکونی و تجاری فعالیت می‌کند. "
                f"تیم ما متشکل از مشاوران با تجربه و آشنا به قوانین ملکی است و آماده ارائه مشاوره تخصصی در زمینه معاملات املاک، "
                f"برآورد قیمت، تنظیم قرارداد و انجام تشریفات قانونی به شما عزیزان می‌باشد. با ما در تماس باشید."
            )
            a, created = Agency.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "owner": owner,
                    "phone": _random_phone(),
                    "address": f"تهران، خیابان ولیعصر، پلاک {100 + i}",
                    "intro_content": agency_intro,
                    "is_active": True,
                },
            )
            if not created:
                a.intro_content = agency_intro
                a.save(update_fields=["intro_content"])
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
        property_leaf_categories = list(Category.property_queryset().filter(parent__isnull=False))
        service_categories = list(
            Category.objects.filter(category_type=Category.CategoryType.SERVICE, is_active=True)
        )
        project_categories = list(
            Category.objects.filter(category_type=Category.CategoryType.PROJECT, is_active=True)
        )
        categories = property_leaf_categories + project_categories + service_categories
        if not categories:
            categories = list(Category.listing_queryset())
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

            short_desc = (
                f"ملک در محله {area_name} با امکانات کامل شامل پارکینگ، انباری و آسانسور. "
                f"دسترسی مناسب به مراکز خرید، مترو و اتوبوس. نوساز و آماده تحویل."
            )
            long_desc = (
                f"<p><strong>توضیحات ملک:</strong></p>"
                f"<p>این {category.fa_name} در محله {area_name} واقع شده و از نظر دسترسی به حمل و نقل عمومی، مراکز خرید و امکانات رفاهی در موقعیت مناسبی قرار دارد.</p>"
                f"<p>امکانات واحد شامل پارکینگ، انباری، آسانسور (در صورت وجود)، سیستم گرمایشی مرکزی و امکانات استاندارد می‌باشد. "
                f"سند ملکی شش‌دانگ و تک‌برگ است و امکان بازدید برای مشتریان جدی فراهم است.</p>"
                f"<p>برای دریافت اطلاعات بیشتر و هماهنگی بازدید، با شماره تماس آگهی تماس بگیرید. "
                f"مشاور املاک آماده پاسخگویی به سوالات شما در مورد قیمت، شرایط پرداخت و جزئیات معامله است.</p>"
            )

            agency = random.choice(agencies) if agencies else None
            Listing.objects.create(
                title=title,
                city=city,
                category=category,
                deal=deal,
                area=area,
                status=Listing.Status.PUBLISHED,
                published_at=timezone.now() - timedelta(days=random.randint(0, 90)),
                short_description=short_desc,
                description=long_desc,
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
        categories = list(Category.property_queryset().filter(parent__isnull=True)[:2])
        count = 0
        for city in cities:
            for cat in categories:
                intro = (
                    f"در این صفحه آگهی‌های خرید و فروش و اجاره {cat.fa_name} در {city.fa_name} را مشاهده می‌کنید. "
                    f"تنوع قیمتی و موقعیت‌های مختلف به شما امکان انتخاب بهترین گزینه را می‌دهد. "
                    f"برای کسب اطلاعات بیشتر با مشاور املاک تماس بگیرید."
                )
                main = (
                    f"<p><strong>آگهی‌های {cat.fa_name} در {city.fa_name}</strong></p>"
                    f"<p>بازار املاک {cat.fa_name} در {city.fa_name} طی سال‌های اخیر رونق داشته است. "
                    f"در این بخش لیست به‌روز آگهی‌های {cat.fa_name} در مناطق مختلف {city.fa_name} را می‌بینید. "
                    f"قیمت‌ها بسته به محله، متراژ و امکانات متفاوت است.</p>"
                    f"<p>قبل از تصمیم‌گیری، توصیه می‌کنیم از چند واحد بازدید کنید و با مشاوران معتبر مشورت نمایید. "
                    f"همچنین بررسی سند ملکی و وضعیت مالی فروشنده یا مالک از نکات ضروری است.</p>"
                )
                obj, created = CityCategory.objects.get_or_create(
                    city=city,
                    category=cat,
                    defaults={
                        "intro_content": intro,
                        "main_content": main,
                        "is_active": True,
                    },
                )
                if not created:
                    obj.intro_content = intro
                    obj.main_content = main
                    obj.save(update_fields=["intro_content", "main_content"])
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
            categories = list(Category.property_queryset().filter(parent__isnull=False)[:2])
            for area in areas:
                for cat in categories:
                    try:
                        intro = (
                            f"آگهی‌های {cat.fa_name} در محله {area.fa_name} ({city.fa_name}). "
                            f"در این صفحه لیست واحدهای موجود در این محدوده را مشاهده می‌کنید. "
                            f"محله {area.fa_name} از نظر دسترسی و امکانات رفاهی در وضعیت مناسبی قرار دارد."
                        )
                        main = (
                            f"<p><strong>{cat.fa_name} در محله {area.fa_name}</strong></p>"
                            f"<p>اگر به دنبال {cat.fa_name} در محدوده {area.fa_name} هستید، در این بخش آگهی‌های به‌روز را پیدا می‌کنید. "
                            f"قیمت‌ها بسته به متراژ، طبقه و امکانات واحد متفاوت است. "
                            f"برای بازدید و مذاکره با شماره تماس آگهی‌دهنده ارتباط بگیرید.</p>"
                        )
                        obj, created = CityAreaCategory.objects.get_or_create(
                            city=city,
                            area=area,
                            category=cat,
                            defaults={
                                "intro_content": intro,
                                "main_content": main,
                                "is_active": True,
                            },
                        )
                        if not created:
                            obj.intro_content = intro
                            obj.main_content = main
                            obj.save(update_fields=["intro_content", "main_content"])
                        count += 1
                    except Exception:
                        pass
        self.stdout.write(f"  CityAreaCategory: {count}")

    def _seed_blog(self, users_data):
        from apps.blog.models import BlogCategory, BlogPost
        from apps.locations.models import City, Area
        from apps.categories.models import Category

        cats_data = [
            ("advice", "مشاوره"),
            ("legal", "نکات قانونی"),
            ("market", "بازار مسکن"),
        ]
        for slug, fa in cats_data:
            BlogCategory.objects.get_or_create(slug=slug, defaults={"fa_name": fa, "sort_order": len(cats_data)})

        cities = list(City.objects.all())
        categories = list(Category.property_queryset().filter(parent__isnull=False)[:5]) or list(Category.property_queryset())
        blog_cats = list(BlogCategory.objects.all())
        owners = users_data.get("owners", [])
        author = owners[0] if owners else User.objects.filter(is_staff=True).first()

        BLOG_CONTENT_TEMPLATE = """
        <p>{lead}</p>
        <p>در این مقاله به طور مفصل به این موضوع می‌پردازیم و نکات کاربردی را برای شما بازگو می‌کنیم. امیدواریم این مطلب در تصمیم‌گیری شما مفید واقع شود.</p>
        <h3>مقدمه</h3>
        <p>بازار املاک ایران همواره با فراز و نشیب‌هایی همراه بوده است. آگاهی از قوانین، بررسی موقعیت مکانی و انجام تحقیقات لازم پیش از هر معامله از ضروریات است.</p>
        <h3>نکات کلیدی</h3>
        <p>قبل از هر اقدامی، حتماً سند ملکی را بررسی کنید. اطمینان از اصالت سند، عدم وجود بار مالی و تطابق نقشه با ملک فیزیکی بسیار مهم است. همچنین توصیه می‌کنیم با مشاور املاک معتبر مشورت کنید.</p>
        <h3>جمع‌بندی</h3>
        <p>با رعایت نکات ذکر شده و صبر و حوصله در انتخاب، می‌توانید معامله‌ای مطمئن و به صرفه انجام دهید. موفق باشید.</p>
        """

        posts_data = [
            (
                "راهنمای خرید زمین در تهران",
                "خرید زمین در تهران نیاز به آگاهی از قوانین شهرداری، وضعیت سند و موقعیت منطقه دارد. در این مقاله مراحل و نکات ضروری را شرح می‌دهیم.",
                "advice",
            ),
            (
                "نکات مهم در قرارداد اجاره آپارتمان",
                "قرارداد اجاره باید شامل مواردی مانند مبلغ اجاره، مدت قرارداد، شرایط تمدید و ضمانت باشد. در این مطلب به جزئیات می‌پردازیم.",
                "legal",
            ),
            (
                "وضعیت بازار مسکن شیراز در سال جاری",
                "بررسی روند قیمت مسکن در شیراز و پیش‌بینی آینده بازار. کدام محلات رشد بیشتری داشته‌اند؟",
                "market",
            ),
            (
                "راهنمای خرید ویلا در شمال کشور",
                "خرید ویلا در مناطق شمالی از مازندران تا گیلان. نکات امنیتی، انتخاب زمین و ساخت و ساز.",
                "advice",
            ),
            (
                "چه زمانی برای خرید مسکن مناسب است؟",
                "تحلیل فصل‌های مختلف سال و شرایط اقتصادی برای تعیین بهترین زمان خرید مسکن. توصیه‌های کارشناسان.",
                "market",
            ),
            (
                "سند تک‌برگ و شش‌دانگ چه تفاوتی دارند؟",
                "آشنایی با انواع سند ملکی و implications قانونی هر کدام. چگونه اصالت سند را بررسی کنیم؟",
                "legal",
            ),
            (
                "اجاره کوتاه‌مدت یا بلندمدت؛ کدام بهتر است؟",
                "مقایسه مزایا و معایب اجاره کوتاه‌مدت و بلندمدت از دید مستاجر و مالک.",
                "advice",
            ),
            (
                "راهنمای خرید آپارتمان نوساز",
                "قبل از خرید واحد نوساز چه چیزهایی را چک کنیم؟ سابقه سازنده، وضعیت پایان‌کار و ضمانت نامه.",
                "advice",
            ),
        ]
        for title, excerpt, cat_slug in posts_data:
            bc = next((c for c in blog_cats if c.slug == cat_slug), blog_cats[0] if blog_cats else None)
            city = random.choice(cities) if cities else None
            lcat = random.choice(categories) if categories else None
            content = BLOG_CONTENT_TEMPLATE.format(lead=excerpt).strip()
            post, created = BlogPost.objects.get_or_create(
                title=title,
                defaults={
                    "excerpt": excerpt,
                    "content": content,
                    "status": BlogPost.Status.PUBLISHED,
                    "published_at": timezone.now() - timedelta(days=random.randint(0, 60)),
                    "blog_category": bc,
                    "city": city,
                    "listing_category": lcat,
                    "author": author,
                },
            )
            if not created:
                post.excerpt = excerpt
                post.content = content
                post.save(update_fields=["excerpt", "content"])
        self.stdout.write(f"  Blog: {BlogCategory.objects.count()} categories, {BlogPost.objects.count()} posts")
