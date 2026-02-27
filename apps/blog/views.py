from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Count, Q
from django.utils.html import strip_tags

from .models import BlogPost, BlogCategory


def _get_categories():
    """دسته‌بندی‌های فعال با تعداد پست منتشر شده."""
    return BlogCategory.objects.filter(is_active=True).annotate(
        post_count=Count("posts", filter=Q(posts__status=BlogPost.Status.PUBLISHED))
    ).order_by("sort_order", "id")


def _build_seo_for_blog(request, obj, *, default_title: str, default_desc: str):
    is_noindex = (not getattr(obj, "allow_index", True)) or getattr(obj, "seo_noindex", False)
    canonical = getattr(obj, "seo_canonical", None) or request.build_absolute_uri()

    return {
        "seo_title": (getattr(obj, "seo_title", None) or default_title).strip(),
        "seo_meta_description": (getattr(obj, "seo_meta_description", None) or default_desc).strip(),
        "seo_h1": (getattr(obj, "seo_h1", None) or default_title).strip(),
        "seo_canonical": canonical.strip(),
        "seo_robots": "noindex, follow" if is_noindex else "index, follow",
    }


def blog_index(request):
    """صفحه لیست پست‌های بلاگ."""
    posts = (
        BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
        .select_related("blog_category", "author", "city", "listing_category")
        .order_by("-published_at", "-id")
    )
    categories = _get_categories()

    paginator = Paginator(posts, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    seo = {
        "seo_title": "بلاگ | VidaHome",
        "seo_meta_description": "مقالات و راهنماهای املاک",
        "seo_h1": "بلاگ",
        "seo_canonical": request.build_absolute_uri("/blog/"),
        "seo_robots": "index, follow",
    }

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "بلاگ", "url": None},
    ]

    return render(
        request,
        "pages/blog_index.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "breadcrumbs": breadcrumbs,
            **seo,
        },
    )


def blog_category(request, slug):
    """لیست پست‌های یک دسته‌بندی بلاگ."""
    cat = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    posts = (
        BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED, blog_category=cat)
        .select_related("blog_category", "author", "city", "listing_category")
        .order_by("-published_at", "-id")
    )
    categories = _get_categories()

    paginator = Paginator(posts, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    seo = _build_seo_for_blog(
        request, cat,
        default_title=f"{cat.fa_name} | بلاگ VidaHome",
        default_desc=f"مقالات دسته {cat.fa_name}",
    )

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "بلاگ", "url": "/blog/"},
        {"title": cat.fa_name, "url": None},
    ]

    total_posts = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED).count()

    return render(
        request,
        "pages/blog_category.html",
        {
            "category": cat,
            "page_obj": page_obj,
            "categories": categories,
            "total_posts": total_posts,
            "breadcrumbs": breadcrumbs,
            **seo,
        },
    )


def blog_post_detail(request, slug):
    """صفحه تک پست بلاگ."""
    post = (
        BlogPost.objects
        .select_related("blog_category", "author", "city", "area", "listing_category")
        .filter(slug=slug, status=BlogPost.Status.PUBLISHED)
        .first()
    )

    if not post:
        raise Http404()

    seo = _build_seo_for_blog(
        request, post,
        default_title=f"{post.title} | VidaHome",
        default_desc=post.excerpt[:160] if post.excerpt else f"مقاله {post.title}",
    )
    seo["seo_canonical"] = request.build_absolute_uri(post.get_absolute_url())
    seo["seo_og_type"] = "article"
    if post.cover_image:
        seo["seo_og_image"] = request.build_absolute_uri(post.cover_image.url)

    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "بلاگ", "url": "/blog/"},
    ]
    if post.blog_category:
        breadcrumbs.append({"title": post.blog_category.fa_name, "url": post.blog_category.get_absolute_url()})
    breadcrumbs.append({"title": post.title, "url": None})

    recent_posts = (
        BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
        .exclude(pk=post.pk)
        .select_related("blog_category", "author")
        .order_by("-published_at", "-id")[:6]
    )
    categories = _get_categories()

    article_schema = {
        "@type": "Article",
        "headline": post.title,
        "description": (post.excerpt or "")[:200],
        "datePublished": post.published_at.isoformat() if post.published_at else "",
        "dateModified": post.updated_at.isoformat() if hasattr(post, "updated_at") and post.updated_at else "",
        "mainEntityOfPage": request.build_absolute_uri(post.get_absolute_url()),
        "author": {
            "@type": "Person",
            "name": post.author.get_full_name() if post.author else "VidaHome",
        },
        "publisher": {
            "@type": "Organization",
            "name": "VidaHome",
        },
    }
    if post.cover_image:
        article_schema["image"] = [request.build_absolute_uri(post.cover_image.url)]
    if post.excerpt:
        article_schema["articleSection"] = post.excerpt[:80]
    content_text = strip_tags(post.content or "").strip()
    if content_text:
        article_schema["articleBody"] = content_text[:5000]

    return render(
        request,
        "pages/blog_post_detail.html",
        {
            "post": post,
            "breadcrumbs": breadcrumbs,
            "landing_links": post.get_landing_links(),
            "recent_posts": recent_posts,
            "categories": categories,
            "extra_schema_json_ld": [article_schema],
            **seo,
        },
    )
