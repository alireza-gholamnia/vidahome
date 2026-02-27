import json

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import strip_tags

register = template.Library()


def _abs_url(request, value):
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    if value.startswith("//"):
        return f"{request.scheme}:{value}"
    return request.build_absolute_uri(value)


def _clean_text(value, fallback=""):
    text = strip_tags(value or fallback or "").replace("\n", " ").strip()
    return " ".join(text.split())


@register.simple_tag(takes_context=True)
def absolute_url(context, value):
    request = context.get("request")
    if not request:
        return value or ""
    return _abs_url(request, value)


@register.simple_tag(takes_context=True)
def pagination_url(context, page_number):
    request = context.get("request")
    if not request:
        return ""
    params = request.GET.copy()
    params["page"] = page_number
    return f"{request.path}?{params.urlencode()}"


@register.simple_tag(takes_context=True)
def build_seo_graph(context):
    request = context.get("request")
    if not request:
        return ""

    site_name = getattr(settings, "SITE_NAME", "VidaHome")
    default_desc = getattr(settings, "SEO_DEFAULT_DESCRIPTION", "")
    site_url = getattr(settings, "SITE_URL", "").rstrip("/") or request.build_absolute_uri("/").rstrip("/")

    canonical = context.get("seo_canonical") or request.build_absolute_uri()
    title = _clean_text(context.get("seo_title"), site_name)
    description = _clean_text(context.get("seo_meta_description"), default_desc)

    graph = []

    webpage = {
        "@type": "WebPage",
        "name": title,
        "url": canonical,
    }
    if description:
        webpage["description"] = description
    graph.append(webpage)

    org_logo_path = getattr(settings, "SEO_ORGANIZATION_LOGO_PATH", static("img/logo/logo-dark.svg"))
    org = {
        "@type": "Organization",
        "name": getattr(settings, "SEO_ORGANIZATION_NAME", site_name),
        "url": site_url,
    }
    if org_logo_path:
        org["logo"] = _abs_url(request, org_logo_path)
    graph.append(org)

    breadcrumbs = context.get("breadcrumbs") or []
    if breadcrumbs:
        items = []
        position = 1
        for crumb in breadcrumbs:
            label = _clean_text(crumb.get("title", ""))
            if not label:
                continue
            url = crumb.get("url")
            items.append(
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": label,
                    "item": _abs_url(request, url) if url else canonical,
                }
            )
            position += 1
        if items:
            graph.append(
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": items,
                }
            )

    faq_items = context.get("faq_items") or []
    faq_entities = []
    for faq in faq_items:
        question = _clean_text(faq.get("question", ""))
        answer = _clean_text(faq.get("answer", ""))
        if question and answer:
            faq_entities.append(
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                }
            )
    if faq_entities:
        graph.append({"@type": "FAQPage", "mainEntity": faq_entities})

    extra_schema = context.get("extra_schema_json_ld")
    if isinstance(extra_schema, dict):
        extra_schema = [extra_schema]
    if isinstance(extra_schema, list):
        for item in extra_schema:
            if isinstance(item, dict):
                cloned = dict(item)
                cloned.pop("@context", None)
                graph.append(cloned)

    if not graph:
        return ""
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": graph,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
