"""
اسکریپت ساخت تصاویر placeholder با Pillow برای همه موجودیت‌های سایت.
استفاده: python manage.py generate_placeholder_images [--force]

--force: جایگزینی تصاویر قبلی (پیش‌فرض فقط برای موارد بدون تصویر)
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.common.placeholder_images import (
    create_placeholder_image,
    SIZE_COVER,
    SIZE_LANDING,
    SIZE_LOGO,
)


class Command(BaseCommand):
    help = "ساخت تصاویر placeholder برای شهرها، محلات، دسته‌ها، آگهی‌ها، مشاوره‌ها و بلاگ"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="جایگزینی تصاویر قبلی (پیش‌فرض فقط برای موارد بدون تصویر)",
        )

    def handle(self, *args, **options):
        force = options["force"]
        stats = {"cities": 0, "areas": 0, "categories": 0, "listings": 0, "agencies": 0, "city_cats": 0, "area_cats": 0, "blog": 0}

        # --- شهرها ---
        from apps.locations.models import City, CityImage, Area, AreaImage

        for i, city in enumerate(City.objects.all()):
            if force or not city.images.exists():
                if force:
                    city.images.all().delete()
                for is_cover, is_landing in [(True, False), (False, True)]:
                    text = city.en_name
                    w, h = SIZE_LANDING if is_landing else SIZE_COVER
                    content = create_placeholder_image(text, w, h, color_index=i % 6)
                    ci = CityImage(city=city, alt=city.fa_name, is_cover=is_cover, is_landing_cover=is_landing)
                    ci.image.save("cover.png", content, save=True)
                stats["cities"] += 1
        self.stdout.write(f"  Cities: {stats['cities']}")

        # --- محلات ---
        for i, area in enumerate(Area.objects.all()):
            if force or not area.images.exists():
                if force:
                    area.images.all().delete()
                text = f"{area.en_name} - {area.city.en_name}"
                for is_cover, is_landing in [(True, False), (False, True)]:
                    w, h = SIZE_LANDING if is_landing else SIZE_COVER
                    content = create_placeholder_image(text, w, h, font_size=36, color_index=(i + 1) % 6)
                    ai = AreaImage(area=area, alt=area.fa_name, is_cover=is_cover, is_landing_cover=is_landing)
                    ai.image.save("cover.png", content, save=True)
                stats["areas"] += 1
        self.stdout.write(f"  Areas: {stats['areas']}")

        # --- دسته‌بندی‌ها ---
        from apps.categories.models import Category, CategoryImage

        for i, cat in enumerate(Category.objects.all()):
            if force or not cat.images.exists():
                if force:
                    cat.images.all().delete()
                text = cat.en_name
                for is_cover, is_landing in [(True, False), (False, True)]:
                    w, h = SIZE_LANDING if is_landing else SIZE_COVER
                    content = create_placeholder_image(text, w, h, color_index=(i + 2) % 6)
                    ci = CategoryImage(category=cat, alt=cat.fa_name, is_cover=is_cover, is_landing_cover=is_landing)
                    ci.image.save("cover.png", content, save=True)
                stats["categories"] += 1
        self.stdout.write(f"  Categories: {stats['categories']}")

        # --- آگهی‌ها ---
        from apps.listings.models import Listing, ListingImage

        for i, listing in enumerate(Listing.objects.all()):
            if force or not listing.images.exists():
                if force:
                    listing.images.all().delete()
                text = f"{listing.category.en_name} in {listing.city.en_name}"
                content = create_placeholder_image(text, *SIZE_COVER, font_size=32, color_index=(i + 3) % 6)
                li = ListingImage(listing=listing, alt=listing.title[:180], is_cover=True)
                li.image.save("cover.png", content, save=True)
                # یک تصویر اضافی
                content2 = create_placeholder_image(
                    f"{listing.category.en_name} - {listing.city.en_name}",
                    *SIZE_COVER,
                    font_size=28,
                    color_index=(i + 4) % 6,
                )
                li2 = ListingImage(listing=listing, alt=listing.title[:180], is_cover=False, sort_order=1)
                li2.image.save("extra.png", content2, save=True)
                stats["listings"] += 1
        self.stdout.write(f"  Listings: {stats['listings']}")

        # --- مشاوره املاک ---
        from apps.agencies.models import Agency, AgencyImage

        for i, agency in enumerate(Agency.objects.all()):
            if force or not agency.images.exists():
                if force:
                    agency.images.all().delete()
                text = agency.slug or agency.name
                content = create_placeholder_image(text, *SIZE_LANDING, font_size=36, color_index=(i + 4) % 6)
                ai = AgencyImage(agency=agency, alt=agency.name, is_landing_cover=True)
                ai.image.save("cover.png", content, save=True)
                stats["agencies"] += 1
            if force or not agency.logo:
                content = create_placeholder_image(agency.slug or agency.name[:20], *SIZE_LOGO, font_size=24, color_index=(i + 5) % 6)
                agency.logo.save("logo.png", content, save=True)
        self.stdout.write(f"  Agencies: {stats['agencies']}")

        # --- لندینگ شهر+دسته ---
        from apps.seo.models import CityCategory, CityCategoryImage

        for i, cc in enumerate(CityCategory.objects.all()):
            if force or not cc.images.exists():
                if force:
                    cc.images.all().delete()
                text = f"{cc.category.en_name} in {cc.city.en_name}"
                for is_cover, is_landing in [(True, False), (False, True)]:
                    w, h = SIZE_LANDING if is_landing else SIZE_COVER
                    content = create_placeholder_image(text, w, h, font_size=32, color_index=i % 6)
                    cci = CityCategoryImage(city_category=cc, alt=f"{cc.category.fa_name} در {cc.city.fa_name}", is_cover=is_cover, is_landing_cover=is_landing)
                    cci.image.save("cover.png", content, save=True)
                stats["city_cats"] += 1
        self.stdout.write(f"  CityCategory: {stats['city_cats']}")

        # --- لندینگ محله+دسته ---
        from apps.seo.models import CityAreaCategory, CityAreaCategoryImage

        for i, cac in enumerate(CityAreaCategory.objects.all()):
            if force or not cac.images.exists():
                if force:
                    cac.images.all().delete()
                text = f"{cac.category.en_name} in {cac.area.en_name}"
                for is_cover, is_landing in [(True, False), (False, True)]:
                    w, h = SIZE_LANDING if is_landing else SIZE_COVER
                    content = create_placeholder_image(text, w, h, font_size=32, color_index=(i + 1) % 6)
                    caci = CityAreaCategoryImage(city_area_category=cac, alt=f"{cac.category.fa_name} در {cac.area.fa_name}", is_cover=is_cover, is_landing_cover=is_landing)
                    caci.image.save("cover.png", content, save=True)
                stats["area_cats"] += 1
        self.stdout.write(f"  CityAreaCategory: {stats['area_cats']}")

        # --- بلاگ ---
        from apps.blog.models import BlogPost

        for i, post in enumerate(BlogPost.objects.all()):
            if force or not post.cover_image:
                text = post.slug or f"Blog Post {post.id}"
                content = create_placeholder_image(text, *SIZE_LANDING, font_size=36, color_index=(i + 2) % 6)
                post.cover_image.save("cover.png", content, save=True)
                stats["blog"] += 1
        self.stdout.write(f"  Blog posts: {stats['blog']}")

        total = sum(stats.values())
        self.stdout.write(self.style.SUCCESS(f"\nPlaceholder images created/updated for {total} entities."))
