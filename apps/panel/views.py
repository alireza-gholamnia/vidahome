import json
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.agencies.models import (
    Agency,
    AgencyJoinRequest,
    AgencyEmployeeInvite,
    EmployeeRemoveRequest,
)
from apps.attributes.models import Attribute, AttributeOption, ListingAttribute
from apps.accounts.models import RoleChangeRequest, GROUP_ROLE_LABELS
from apps.accounts.roles import (
    assign_user_to_agency,
    clear_user_agency_membership,
    promote_user_to_owner,
    set_exclusive_business_role,
    user_owns_any_agency,
)
from apps.listings.models import Listing
from apps.lead.models import ListingLead, LandingLead
from apps.locations.models import Area, City
from apps.common.sms import normalize_phone

from .forms import (
    AgencyCreateForm,
    AgencyProfileForm,
    AttributeForm,
    AttributeOptionFormSet,
    ListingForm,
    UserProfileForm,
)


def _get_user_agencies(user):
    """مشاوره‌های املاکی که کاربر مالک آن‌هاست."""
    return Agency.objects.filter(owner=user)


def _get_user_agency(user):
    """اولین مشاوره مالکیت‌شده توسط کاربر (برای سازگاری)."""
    return _get_user_agencies(user).first()


def _get_user_active_listing_agencies(user):
    """Active/approved agencies that user can attach listings to."""
    approved_active = {
        "approval_status": Agency.ApprovalStatus.APPROVED,
        "is_active": True,
    }
    if user.is_superuser or _is_site_admin(user):
        return Agency.objects.filter(**approved_active).order_by("name", "id")

    owner_agencies = _get_user_agencies(user).filter(**approved_active).order_by("name", "id")
    if owner_agencies.exists():
        return owner_agencies

    if getattr(user, "agency_id", None):
        return Agency.objects.filter(id=user.agency_id, **approved_active)

    return Agency.objects.none()


def _resolve_listing_agency_for_user(user, selected_agency=None):
    """Resolve target agency for a listing based on user access and optional form selection."""
    agencies = _get_user_active_listing_agencies(user)

    if selected_agency is not None:
        return agencies.filter(id=selected_agency.id).first()

    if getattr(user, "agency_id", None):
        current = agencies.filter(id=user.agency_id).first()
        if current:
            return current

    if agencies.count() == 1:
        return agencies.first()

    return None


def _get_user_listings_queryset(user):
    """آگهی‌های قابل دسترسی برای کاربر (صاحب مشاوره، کارمند، یا شخصی)."""
    qs = Listing.objects.select_related(
        "city", "area", "category", "created_by"
    ).prefetch_related("images")
    if user.is_superuser or _is_site_admin(user):
        return qs
    agency_ids = _get_user_active_listing_agencies(user).values_list("id", flat=True)
    return qs.filter(agency_id__in=agency_ids)


def _can_edit_listing(user, listing):
    """آیا کاربر مجاز به ویرایش این آگهی است؟"""
    if user.is_superuser or _is_site_admin(user):
        return True
    if not listing.agency_id:
        return False
    return _get_user_active_listing_agencies(user).filter(id=listing.agency_id).exists()


def _is_site_admin(user):
    """آیا کاربر ادمین سایت است (سوپرادمین یا گروه site_admin)؟"""
    if user.is_superuser:
        return True
    return user.groups.filter(name="site_admin").exists()




def _can_delete_listing(user, listing):
    """آیا کاربر مجاز به حذف این آگهی است؟ (همان منطق ویرایش)"""
    return _can_edit_listing(user, listing)


def _save_listing_attributes_from_post(listing, post_data):
    """ذخیره مقادیر ویژگی‌ها از POST در ListingAttribute."""
    if not listing.category_id:
        return
    attrs = Attribute.objects.filter(
        categories=listing.category,
        is_active=True,
    ).values_list("id", flat=True)
    for attr_id in attrs:
        key = f"attr_{attr_id}"
        if key not in post_data:
            continue
        val = post_data.get(key)
        attr = Attribute.objects.get(pk=attr_id)
        la, _ = ListingAttribute.objects.get_or_create(
            listing=listing,
            attribute_id=attr_id,
            defaults={"attribute_id": attr_id},
        )
        if attr.value_type == Attribute.ValueType.INTEGER:
            la.value_int = int(val) if val and str(val).strip() else None
            la.value_bool = None
            la.value_str = ""
            la.value_option = None
        elif attr.value_type == Attribute.ValueType.BOOLEAN:
            la.value_bool = val in ("1", "true", "True", "on", "yes")
            la.value_int = None
            la.value_str = ""
            la.value_option = None
        elif attr.value_type == Attribute.ValueType.CHOICE:
            try:
                opt_id = int(val) if val else None
                la.value_option_id = opt_id if opt_id else None
            except (ValueError, TypeError):
                la.value_option_id = None
            la.value_int = None
            la.value_bool = None
            la.value_str = ""
        elif attr.value_type == Attribute.ValueType.STRING:
            la.value_str = (val or "").strip()[:500]
            la.value_int = None
            la.value_bool = None
            la.value_option = None
        la.save()


@login_required(login_url="/accounts/login/")
def dashboard(request):
    """داشبورد پنل کاربری."""
    qs = _get_user_listings_queryset(request.user)
    count = qs.count()
    published = qs.filter(status=Listing.Status.PUBLISHED).count()
    rejected = qs.filter(
        Q(status=Listing.Status.REJECTED)
        | (Q(status=Listing.Status.DRAFT) & ~Q(rejection_reason=""))
    ).count()
    pending_listings = qs.filter(status=Listing.Status.PENDING).count()
    pending_listings_all = 0
    pending_agencies_all = 0
    if _is_site_admin(request.user):
        pending_listings_all = Listing.objects.filter(status=Listing.Status.PENDING).count()
        pending_agencies_all = Agency.objects.filter(approval_status=Agency.ApprovalStatus.PENDING).count()
    return render(
        request,
        "panel/dashboard.html",
        {
            "listings_count": count,
            "published_count": published,
            "rejected_count": rejected,
            "pending_listings": pending_listings,
            "pending_listings_all": pending_listings_all,
            "pending_agencies_all": pending_agencies_all,
            "is_site_admin": _is_site_admin(request.user),
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": None},
            ],
        },
    )


class ListingListView(LoginRequiredMixin, ListView):
    """لیست آگهی‌های کاربر."""
    model = Listing
    template_name = "panel/listing_list.html"
    context_object_name = "listings"
    paginate_by = 12
    login_url = "/accounts/login/"

    def get_queryset(self):
        return _get_user_listings_queryset(self.request.user).order_by("-updated_at", "-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
            {"title": "آگهی‌های من", "url": None},
        ]
        qs = _get_user_listings_queryset(self.request.user)
        context["listings_with_rejection"] = qs.filter(
            Q(status=Listing.Status.REJECTED)
            | (Q(status=Listing.Status.DRAFT) & ~Q(rejection_reason=""))
        ).exists()
        return context


@login_required(login_url="/accounts/login/")
def listing_inquiries(request):
    """استعلام‌های آگهی — فقط برای ادمین سایت. مشاهده و تغییر وضعیت لیدهای آگهی و لندینگ."""
    if not _is_site_admin(request.user):
        messages.warning(request, "دسترسی به استعلام‌های آگهی فقط برای ادمین سایت امکان‌پذیر است.")
        return redirect("panel:dashboard")
    user_listing_ids = _get_user_listings_queryset(request.user).values_list("id", flat=True)
    inquiries = (
        ListingLead.objects.filter(listing_id__in=user_listing_ids)
        .select_related("listing")
        .order_by("-created_at")
    )

    landing_leads = []
    landing_new_count = 0
    is_site_admin = _is_site_admin(request.user)
    if is_site_admin:
        landing_leads = list(LandingLead.objects.all().order_by("-created_at")[:200])
        landing_new_count = LandingLead.objects.filter(status=ListingLead.LeadStatus.NEW).count()

    if request.method == "POST":
        inquiry_id = request.POST.get("inquiry_id")
        new_status = request.POST.get("status")
        if inquiry_id and new_status and new_status in dict(ListingLead.LeadStatus.choices):
            inv = inquiries.filter(pk=int(inquiry_id)).first()
            if inv:
                inv.status = new_status
                inv.save()
                messages.success(request, "وضعیت به‌روز شد.")
                return redirect("panel:listing_inquiries")

        landing_lead_id = request.POST.get("landing_lead_id")
        landing_status = request.POST.get("landing_status")
        if is_site_admin and landing_lead_id and landing_status and landing_status in dict(ListingLead.LeadStatus.choices):
            ll = LandingLead.objects.filter(pk=int(landing_lead_id)).first()
            if ll:
                ll.status = landing_status
                ll.save()
                messages.success(request, "وضعیت لید لندینگ به‌روز شد.")
                return redirect("panel:listing_inquiries")

    new_count = inquiries.filter(status=ListingLead.LeadStatus.NEW).count()
    breadcrumbs = [
        {"title": "صفحه اصلی", "url": "/"},
        {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
        {"title": "استعلام‌های آگهی", "url": None},
    ]
    return render(
        request,
        "panel/listing_inquiries.html",
        {
            "inquiries": inquiries,
            "new_count": new_count,
            "landing_leads": landing_leads,
            "landing_new_count": landing_new_count,
            "is_site_admin": is_site_admin,
            "breadcrumbs": breadcrumbs,
        },
    )


class ListingCreateView(LoginRequiredMixin, CreateView):
    """افزودن آگهی جدید."""
    model = Listing
    form_class = ListingForm
    template_name = "panel/listing_form.html"
    login_url = "/accounts/login/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        city_id = self.request.POST.get("city") if self.request.POST else None
        if city_id:
            kwargs["city_id"] = int(city_id) if str(city_id).isdigit() else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
            {"title": "آگهی‌های من", "url": reverse("panel:listing_list")},
            {"title": "ثبت آگهی", "url": None},
        ]
        context["initial_listing_id"] = None
        context["neshan_api_key"] = getattr(settings, "NESHAN_API_KEY", "") or ""
        attr_post = {}
        if self.request.method == "POST":
            for k, v in self.request.POST.items():
                if k.startswith("attr_"):
                    attr_post[k] = v
        context["attr_post_json"] = json.dumps(attr_post)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        selected_agency = form.cleaned_data.get("agency")
        agency = _resolve_listing_agency_for_user(self.request.user, selected_agency=selected_agency)
        if not agency:
            err = "برای ثبت آگهی باید یک املاک فعال/تأییدشده داشته باشید."
            if "agency" in form.fields:
                form.add_error("agency", err)
            else:
                form.add_error(None, err)
            return self.form_invalid(form)
        obj.agency = agency
        # هر آگهی جدید از پنل همیشه در صف تأیید (حتی ادمین)
        obj.status = Listing.Status.PENDING
        obj.save()
        _save_listing_attributes_from_post(obj, self.request.POST)
        return redirect(reverse("panel:listing_list"))


class ListingUpdateView(LoginRequiredMixin, UpdateView):
    """ویرایش آگهی."""
    model = Listing
    form_class = ListingForm
    template_name = "panel/listing_form.html"
    context_object_name = "listing"
    login_url = "/accounts/login/"

    def get_queryset(self):
        return _get_user_listings_queryset(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not _can_edit_listing(request.user, obj):
            return redirect("panel:listing_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        obj = self.get_object()
        city_id = self.request.POST.get("city") if self.request.POST else (obj.city_id if obj else None)
        if city_id:
            kwargs["city_id"] = int(city_id) if str(city_id).isdigit() else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
            {"title": "آگهی‌های من", "url": reverse("panel:listing_list")},
            {"title": f"ویرایش: {self.object.title[:30]}...", "url": None},
        ]
        context["initial_listing_id"] = self.object.pk if self.object else None
        context["neshan_api_key"] = getattr(settings, "NESHAN_API_KEY", "") or ""
        attr_post = {}
        if self.request.method == "POST":
            for k, v in self.request.POST.items():
                if k.startswith("attr_"):
                    attr_post[k] = v
        context["attr_post_json"] = json.dumps(attr_post)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        selected_agency = form.cleaned_data.get("agency")
        if selected_agency is not None:
            resolved = _resolve_listing_agency_for_user(
                self.request.user,
                selected_agency=selected_agency,
            )
            if not resolved:
                form.add_error("agency", "املاک انتخاب‌شده معتبر نیست.")
                return self.form_invalid(form)
            obj.agency = resolved
        elif not obj.agency_id:
            resolved = _resolve_listing_agency_for_user(self.request.user)
            if not resolved:
                form.add_error(None, "این آگهی باید به یک املاک فعال/تأییدشده متصل باشد.")
                return self.form_invalid(form)
            obj.agency = resolved
        if not _is_site_admin(self.request.user):
            # ویرایش آگهی منتشرشده یا ردشده → همیشه در صف تأیید
            obj.status = Listing.Status.PENDING
        obj.save()
        _save_listing_attributes_from_post(obj, self.request.POST)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("panel:listing_list")


class ListingDeleteView(LoginRequiredMixin, DeleteView):
    """حذف آگهی (فقط برای کاربران مجاز)."""
    model = Listing
    context_object_name = "listing"
    login_url = "/accounts/login/"
    template_name = "panel/listing_confirm_delete.html"

    def get_queryset(self):
        return _get_user_listings_queryset(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not _can_delete_listing(request.user, obj):
            return redirect("panel:listing_list")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"title": "صفحه اصلی", "url": "/"},
            {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
            {"title": "آگهی‌های من", "url": reverse("panel:listing_list")},
            {"title": "حذف آگهی", "url": None},
        ]
        return context

    def get_success_url(self):
        return reverse("panel:listing_list")


@login_required(login_url="/accounts/login/")
def profile_edit(request):
    """ویرایش پروفایل کاربری."""
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("panel:profile_edit")
    else:
        form = UserProfileForm(instance=request.user)
    return render(
        request,
        "panel/profile_edit.html",
        {
            "form": form,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "پروفایل کاربری", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def agency_list(request):
    """لیست املاک‌های مالک (مدل عضو/مالک ساده و بدون تغییر نقش دستی)."""
    agencies = _get_user_agencies(request.user).order_by("name", "id")
    return render(
        request,
        "panel/agency_list.html",
        {
            "agencies": agencies,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مشاوره‌های املاک", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def agency_add(request):
    """افزودن ملک/املاک جدید توسط هر کاربر سایت."""
    if request.method == "POST":
        form = AgencyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.owner = request.user
            agency.approval_status = Agency.ApprovalStatus.PENDING
            agency.save()
            form.save_m2m()
            messages.success(request, "املاک شما ثبت شد و پس از تأیید مدیر سایت فعال می‌شود.")
            return redirect("panel:agency_list")
    else:
        form = AgencyCreateForm()
    return render(
        request,
        "panel/agency_form.html",
        {
            "form": form,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مشاوره‌های املاک", "url": reverse("panel:agency_list")},
                {"title": "افزودن مشاوره املاک", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def agency_edit(request, pk):
    """ویرایش پروفایل املاک — فقط برای مالک همان املاک."""
    agency = get_object_or_404(Agency, pk=pk, owner=request.user)
    if request.method == "POST":
        form = AgencyProfileForm(
            request.POST, request.FILES, instance=agency
        )
        if form.is_valid():
            form.save()
            return redirect("panel:agency_edit", pk=agency.pk)
    else:
        form = AgencyProfileForm(instance=agency)
    return render(
        request,
        "panel/agency_profile.html",
        {
            "form": form,
            "agency": agency,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مشاوره‌های املاک", "url": reverse("panel:agency_list")},
                {"title": f"ویرایش: {agency.name}", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def agency_employees(request):
    """مدیریت همکاران املاک توسط مالک: ارسال دعوت، لغو دعوت، حذف همکار."""
    agencies = _get_user_agencies(request.user).filter(
        approval_status=Agency.ApprovalStatus.APPROVED,
        is_active=True,
    )
    if not agencies.exists():
        messages.info(request, "برای مدیریت همکاران، ابتدا حداقل یک املاک فعال/تأییدشده داشته باشید.")
        return redirect("panel:agency_list")

    from apps.accounts.models import User

    employee_ids = User.objects.filter(agency__in=agencies).values_list("id", flat=True)
    employees = list(
        User.objects.filter(id__in=employee_ids)
        .select_related("agency")
        .order_by("agency__name", "first_name", "username")
    )
    pending_invites = list(
        AgencyEmployeeInvite.objects.filter(
            agency__in=agencies,
            status=AgencyEmployeeInvite.Status.PENDING,
        )
        .select_related("agency", "invited_user")
        .order_by("-created_at")
    )

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        if action == "remove_employee":
            user_id = request.POST.get("user_id")
            try:
                emp = User.objects.get(pk=int(user_id), agency__in=agencies)
                clear_user_agency_membership(emp)
                messages.success(request, "همکار از املاک حذف شد.")
            except (ValueError, User.DoesNotExist):
                messages.error(request, "کارمند انتخاب‌شده معتبر نیست.")
            return redirect("panel:agency_employees")

        if action == "cancel_invite":
            invite_id = request.POST.get("invite_id")
            try:
                invite = AgencyEmployeeInvite.objects.get(
                    pk=int(invite_id),
                    agency__in=agencies,
                    status=AgencyEmployeeInvite.Status.PENDING,
                )
                invite.status = AgencyEmployeeInvite.Status.CANCELED
                invite.responded_at = timezone.now()
                invite.save(update_fields=["status", "responded_at"])
                messages.success(request, "دعوت همکاری لغو شد.")
            except (ValueError, AgencyEmployeeInvite.DoesNotExist):
                messages.error(request, "دعوت انتخاب‌شده معتبر نیست.")
            return redirect("panel:agency_employees")

        if action == "add_employee":
            agency_id = request.POST.get("agency_id")
            identifier = (request.POST.get("identifier") or "").strip()
            if not agency_id or not identifier:
                messages.error(request, "املاک و شناسه کاربر الزامی است.")
                return redirect("panel:agency_employees")

            try:
                agency = agencies.get(pk=int(agency_id))
            except (ValueError, Agency.DoesNotExist):
                messages.error(request, "املاک انتخاب‌شده معتبر نیست.")
                return redirect("panel:agency_employees")

            normalized_phone = normalize_phone(identifier)
            # جستجو بر اساس username یا phone
            target = User.objects.filter(
                Q(username__iexact=identifier)
                | Q(phone__iexact=identifier)
                | Q(phone__iexact=normalized_phone)
            ).first()
            if not target:
                messages.error(request, "کاربری با این نام کاربری/شماره پیدا نشد.")
                return redirect("panel:agency_employees")

            if target.pk == request.user.pk:
                messages.error(request, "نمی‌توانید خودتان را به عنوان همکار اضافه کنید.")
                return redirect("panel:agency_employees")

            if target.is_superuser or target.groups.filter(name="site_admin").exists():
                messages.error(request, "امکان افزودن مدیر سایت به عنوان همکار وجود ندارد.")
                return redirect("panel:agency_employees")

            if user_owns_any_agency(target, approved_only=False):
                messages.error(request, "این کاربر مالک املاک است و نمی‌تواند به عنوان همکار ثبت شود.")
                return redirect("panel:agency_employees")

            if target.agency_id == agency.id:
                messages.info(request, "این کاربر هم‌اکنون همکار همین املاک است.")
                return redirect("panel:agency_employees")

            if AgencyEmployeeInvite.objects.filter(
                invited_user=target,
                agency=agency,
                status=AgencyEmployeeInvite.Status.PENDING,
            ).exists():
                messages.info(request, "برای این کاربر قبلا دعوت همکاری ارسال شده و در انتظار تایید است.")
                return redirect("panel:agency_employees")

            AgencyEmployeeInvite.objects.create(
                invited_user=target,
                agency=agency,
                invited_by=request.user,
                status=AgencyEmployeeInvite.Status.PENDING,
            )
            messages.success(request, "دعوت همکاری ارسال شد. کاربر باید آن را در پنل خود تایید کند.")
            return redirect("panel:agency_employees")

        messages.error(request, "درخواست نامعتبر است.")
        return redirect("panel:agency_employees")

    return render(
        request,
        "panel/agency_employees.html",
        {
            "employees": employees,
            "pending_invites": pending_invites,
            "agencies": agencies,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "کارمندان مشاوره", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def role_change_request(request):
    messages.info(
        request,
        "این بخش غیرفعال شده است. برای مدیریت املاک از «املاک‌های من» و برای همکاری از «همکاران املاک» استفاده کنید.",
    )
    return redirect("panel:dashboard")


def _get_pending_listings_queryset():
    """آگهی‌های در صف تأیید (فقط PENDING)."""
    return Listing.objects.filter(status=Listing.Status.PENDING).select_related(
        "city", "category", "created_by"
    )


@login_required(login_url="/accounts/login/")
def employee_request_join(request):
    """لیست دعوت‌های همکاری کاربر و امکان تایید/رد دعوت."""
    pending_invites_qs = AgencyEmployeeInvite.objects.filter(
        invited_user=request.user,
        status=AgencyEmployeeInvite.Status.PENDING,
    ).select_related("agency", "invited_by").order_by("-created_at")

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        invite_id = request.POST.get("invite_id")
        try:
            invite = AgencyEmployeeInvite.objects.select_related("agency").get(
                pk=int(invite_id),
                invited_user=request.user,
                status=AgencyEmployeeInvite.Status.PENDING,
            )
        except (TypeError, ValueError, AgencyEmployeeInvite.DoesNotExist):
            messages.error(request, "دعوت انتخاب‌شده معتبر نیست.")
            return redirect("panel:employee_request_join")

        if action == "accept_invite":
            agency = invite.agency
            if (
                agency.approval_status != Agency.ApprovalStatus.APPROVED
                or not agency.is_active
            ):
                invite.status = AgencyEmployeeInvite.Status.REJECTED
                invite.responded_at = timezone.now()
                invite.save(update_fields=["status", "responded_at"])
                messages.error(request, "این دعوت معتبر نیست (املاک فعال/تأییدشده نیست) و رد شد.")
                return redirect("panel:employee_request_join")

            if user_owns_any_agency(request.user, approved_only=False):
                invite.status = AgencyEmployeeInvite.Status.REJECTED
                invite.responded_at = timezone.now()
                invite.save(update_fields=["status", "responded_at"])
                messages.error(request, "شما مالک املاک هستید و امکان پذیرش دعوت همکاری ندارید.")
                return redirect("panel:employee_request_join")

            assign_user_to_agency(request.user, agency)
            invite.status = AgencyEmployeeInvite.Status.ACCEPTED
            invite.responded_at = timezone.now()
            invite.save(update_fields=["status", "responded_at"])

            AgencyEmployeeInvite.objects.filter(
                invited_user=request.user,
                status=AgencyEmployeeInvite.Status.PENDING,
            ).exclude(pk=invite.pk).update(
                status=AgencyEmployeeInvite.Status.REJECTED,
                responded_at=timezone.now(),
            )

            messages.success(request, "دعوت همکاری تایید شد و عضویت شما فعال گردید.")
            return redirect("panel:employee_my_agency")

        if action == "reject_invite":
            invite.status = AgencyEmployeeInvite.Status.REJECTED
            invite.responded_at = timezone.now()
            invite.save(update_fields=["status", "responded_at"])
            messages.info(request, "دعوت همکاری رد شد.")
            return redirect("panel:employee_request_join")

        messages.error(request, "درخواست نامعتبر است.")
        return redirect("panel:employee_request_join")

    invite_history = AgencyEmployeeInvite.objects.filter(
        invited_user=request.user,
    ).exclude(status=AgencyEmployeeInvite.Status.PENDING).select_related(
        "agency", "invited_by"
    ).order_by("-created_at")[:30]

    return render(
        request,
        "panel/employee_request_join.html",
        {
            "pending_invites": list(pending_invites_qs),
            "invite_history": list(invite_history),
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "دعوت‌های همکاری", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def employee_my_agency(request):
    """نمایش اطلاعات مشاوره‌ای که کاربر عضو آن است — فقط برای کارمندان با user.agency."""
    if not request.user.agency_id:
        return redirect("panel:dashboard")
    agency = request.user.agency
    return render(
        request,
        "panel/employee_my_agency.html",
        {
            "agency": agency,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "اطلاعات مشاوره املاک", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def approve_dashboard(request):
    """داشبورد تأیید — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")

    tab = request.GET.get("tab", "pending")
    if tab not in ("pending", "rejected", "approved", "employees"):
        tab = "pending"

    pending_listings_qs = _get_pending_listings_queryset().order_by("-updated_at")
    pending_listings_count = pending_listings_qs.count()
    pending_listings = list(pending_listings_qs[:50])

    pending_agencies_qs = Agency.objects.filter(
        approval_status=Agency.ApprovalStatus.PENDING
    ).select_related("owner").order_by("-id")
    pending_agencies_count = pending_agencies_qs.count()
    pending_agencies = list(pending_agencies_qs[:50])

    rejected_listings_qs = Listing.objects.filter(
        Q(status=Listing.Status.REJECTED)
        | (Q(status=Listing.Status.DRAFT) & ~Q(rejection_reason=""))
    ).select_related("city", "category", "created_by").order_by("-updated_at")
    rejected_listings_count = rejected_listings_qs.count()
    rejected_listings = list(rejected_listings_qs[:50])

    # آگهی‌های تأیید شده (منتشرشده)
    approved_listings_qs = Listing.objects.filter(
        status=Listing.Status.PUBLISHED
    ).select_related("city", "category", "created_by").order_by("-published_at", "-id")
    approved_listings_count = approved_listings_qs.count()
    approved_listings = list(approved_listings_qs[:50])

    # کارمندان (کاربران با agency)
    from apps.accounts.models import User

    employees_qs = User.objects.filter(agency__isnull=False).select_related(
        "agency"
    ).order_by("agency__name", "first_name", "username")
    employees_count = employees_qs.count()
    employees = list(employees_qs[:100])

    return render(
        request,
        "panel/approve_dashboard.html",
        {
            "tab": tab,
            "pending_listings": pending_listings,
            "pending_listings_count": pending_listings_count,
            "pending_agencies": pending_agencies,
            "pending_agencies_count": pending_agencies_count,
            "rejected_listings": rejected_listings,
            "rejected_listings_count": rejected_listings_count,
            "approved_listings": approved_listings,
            "approved_listings_count": approved_listings_count,
            "employees": employees,
            "employees_count": employees_count,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "تأیید موارد", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def approve_listing(request, pk):
    """تأیید و انتشار آگهی — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    listing = get_object_or_404(
        Listing.objects.prefetch_related("images", "attribute_values__attribute", "attribute_values__value_option")
        .select_related("city", "area", "category", "created_by", "agency"),
        pk=pk,
        status__in=(Listing.Status.DRAFT, Listing.Status.PENDING, Listing.Status.REJECTED),
    )
    action = request.POST.get("action")
    if action == "approve":
        listing.status = Listing.Status.PUBLISHED
        listing.rejection_reason = ""
        from django.utils import timezone

        listing.published_at = timezone.now()
        listing.save()
        return redirect("panel:approve_dashboard")
    elif action == "reject":
        listing.status = Listing.Status.REJECTED
        listing.rejection_reason = (request.POST.get("rejection_reason") or "").strip()
        listing.save()
        return redirect("panel:approve_dashboard")
    return render(request, "panel/approve_listing.html", {"listing": listing})


@login_required(login_url="/accounts/login/")
def approve_join_request(request, pk):
    """تأیید یا رد درخواست عضویت کارمند — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    join_req = get_object_or_404(
        AgencyJoinRequest, pk=pk, status=AgencyJoinRequest.Status.PENDING
    )
    action = request.POST.get("action")
    if action == "approve":
        if (
            join_req.agency.approval_status != Agency.ApprovalStatus.APPROVED
            or not join_req.agency.is_active
        ):
            join_req.status = AgencyJoinRequest.Status.REJECTED
            from django.utils import timezone

            join_req.reviewed_at = timezone.now()
            join_req.save(update_fields=["status", "reviewed_at"])
            messages.error(request, "این مشاوره فعال/تأیید شده نیست و درخواست عضویت رد شد.")
            return redirect("panel:approve_dashboard")

        # نقش‌ها انحصاری هستند؛ کاربری که مالک مشاوره است نباید کارمند شود.
        if user_owns_any_agency(join_req.user, approved_only=False):
            join_req.status = AgencyJoinRequest.Status.REJECTED
            from django.utils import timezone

            join_req.reviewed_at = timezone.now()
            join_req.save(update_fields=["status", "reviewed_at"])
            messages.error(request, "این کاربر مالک مشاوره است و امکان تأیید به عنوان کارمند ندارد.")
            return redirect("panel:approve_dashboard")

        assign_user_to_agency(join_req.user, join_req.agency)
        join_req.status = AgencyJoinRequest.Status.APPROVED
        from django.utils import timezone

        join_req.reviewed_at = timezone.now()
        join_req.save()
        # با تأیید یک درخواست، بقیه درخواست‌های باز کاربر بسته می‌شوند.
        AgencyJoinRequest.objects.filter(
            user=join_req.user,
            status=AgencyJoinRequest.Status.PENDING,
        ).exclude(pk=join_req.pk).update(
            status=AgencyJoinRequest.Status.REJECTED,
            reviewed_at=timezone.now(),
        )
        return redirect("panel:approve_dashboard")
    elif action == "reject":
        join_req.status = AgencyJoinRequest.Status.REJECTED
        from django.utils import timezone

        join_req.reviewed_at = timezone.now()
        join_req.save()
        return redirect("panel:approve_dashboard")
    return redirect("panel:approve_dashboard")


@login_required(login_url="/accounts/login/")
def approve_remove_request(request, pk):
    """تأیید یا رد درخواست حذف کارمند — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    req = get_object_or_404(
        EmployeeRemoveRequest, pk=pk, status=EmployeeRemoveRequest.Status.PENDING
    )
    action = request.POST.get("action")
    if action == "approve":
        # فقط در صورتی که کارمند هنوز در همان مشاوره است
        if req.user.agency_id == req.agency_id:
            clear_user_agency_membership(req.user)
        req.status = EmployeeRemoveRequest.Status.APPROVED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect("panel:approve_dashboard")
    elif action == "reject":
        req.status = EmployeeRemoveRequest.Status.REJECTED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect("panel:approve_dashboard")
    return redirect("panel:approve_dashboard")


@login_required(login_url="/accounts/login/")
def approve_role_change_request(request, pk):
    """تأیید یا رد درخواست تغییر نقش — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    req = get_object_or_404(
        RoleChangeRequest, pk=pk, status=RoleChangeRequest.Status.PENDING
    )
    action = request.POST.get("action")
    if action == "approve":
        # اگر کاربر مالک مشاوره باشد، نباید به نقش کارمند تغییر کند.
        if (
            req.requested_role == RoleChangeRequest.RequestedRole.AGENCY_EMPLOYEE
            and user_owns_any_agency(req.user, approved_only=False)
        ):
            req.status = RoleChangeRequest.Status.REJECTED
            from django.utils import timezone

            req.reviewed_at = timezone.now()
            req.save(update_fields=["status", "reviewed_at"])
            messages.error(request, "این کاربر مالک مشاوره است و نمی‌تواند نقش کارمند بگیرد.")
            return redirect("panel:approve_dashboard")

        if req.requested_role == RoleChangeRequest.RequestedRole.AGENCY_OWNER:
            promote_user_to_owner(req.user)
        else:
            set_exclusive_business_role(req.user, RoleChangeRequest.RequestedRole.AGENCY_EMPLOYEE)

        req.status = RoleChangeRequest.Status.APPROVED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect("panel:approve_dashboard")
    elif action == "reject":
        req.status = RoleChangeRequest.Status.REJECTED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect("panel:approve_dashboard")
    return redirect("panel:approve_dashboard")


@login_required(login_url="/accounts/login/")
def employee_manage_agency(request, user_id):
    """تغییر یا حذف مشاوره کارمند — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    from apps.accounts.models import User

    emp = get_object_or_404(User, pk=user_id)
    if not emp.agency_id:
        return redirect("panel:approve_dashboard")
    if request.method == "POST":
        new_agency_id = request.POST.get("agency")
        if new_agency_id == "" or new_agency_id == "remove":
            clear_user_agency_membership(emp)
        else:
            try:
                agency = Agency.objects.get(
                    pk=int(new_agency_id),
                    approval_status=Agency.ApprovalStatus.APPROVED,
                    is_active=True,
                )
                assign_user_to_agency(emp, agency)
            except (ValueError, Agency.DoesNotExist):
                pass
        return redirect(reverse("panel:approve_dashboard") + "?tab=employees")
    agencies = Agency.objects.filter(
        approval_status=Agency.ApprovalStatus.APPROVED,
        is_active=True,
    ).order_by("name")
    return render(
        request,
        "panel/employee_manage_agency.html",
        {
            "emp": emp,
            "agencies": agencies,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "تأیید موارد", "url": reverse("panel:approve_dashboard")},
                {"title": "مدیریت کارمند", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def approve_agency(request, pk):
    """تأیید یا رد مشاوره املاک — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    agency = get_object_or_404(Agency, pk=pk, approval_status=Agency.ApprovalStatus.PENDING)
    action = request.POST.get("action")
    if action == "approve":
        agency.approval_status = Agency.ApprovalStatus.APPROVED
        agency.is_active = True
        agency.save()
        promote_user_to_owner(agency.owner)
        return redirect("panel:approve_dashboard")
    elif action == "reject":
        agency.approval_status = Agency.ApprovalStatus.REJECTED
        agency.save()
        return redirect("panel:approve_dashboard")
    return render(request, "panel/approve_agency.html", {"agency": agency})


# --- مدیریت ویژگی‌ها (فقط ادمین سایت) ---


@login_required(login_url="/accounts/login/")
def attribute_list(request):
    """لیست ویژگی‌ها — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    attributes = Attribute.objects.prefetch_related("categories", "options").order_by("sort_order", "id")
    return render(
        request,
        "panel/attribute_list.html",
        {
            "attributes": attributes,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مدیریت ویژگی‌ها", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def attribute_add(request):
    """افزودن ویژگی جدید — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    if request.method == "POST":
        form = AttributeForm(request.POST, request.FILES)
        formset = AttributeOptionFormSet(request.POST, instance=Attribute())
        if form.is_valid():
            attr = form.save(commit=False)
            attr.slug = f"attr-{uuid.uuid4().hex[:12]}"  # موقت برای ذخیره اول
            attr.save()
            attr.slug = str(attr.id)
            attr.save(update_fields=["slug"])
            form.save_m2m()
            formset = AttributeOptionFormSet(request.POST, instance=attr)
            if formset.is_valid():
                formset.save()
                messages.success(request, "ویژگی با موفقیت ذخیره شد.")
                return redirect("panel:attribute_list")
            else:
                attr.delete()  # rollback
                form = AttributeForm(request.POST, request.FILES)
                formset = AttributeOptionFormSet(request.POST, instance=Attribute())
                err = formset.non_form_errors()
                messages.error(request, f"خطا در گزینه‌ها: {err}" if err else "خطا در گزینه‌ها.")
    else:
        form = AttributeForm()
        formset = AttributeOptionFormSet(instance=Attribute())
    return render(
        request,
        "panel/attribute_form.html",
        {
            "form": form,
            "formset": formset,
            "object": None,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مدیریت ویژگی‌ها", "url": reverse("panel:attribute_list")},
                {"title": "افزودن ویژگی", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def attribute_edit(request, pk):
    """ویرایش ویژگی — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    attr = get_object_or_404(Attribute, pk=pk)
    if request.method == "POST":
        form = AttributeForm(request.POST, request.FILES, instance=attr)
        formset = AttributeOptionFormSet(request.POST, instance=attr)
        if form.is_valid() and formset.is_valid():
            attr = form.save(commit=False)
            attr.slug = str(attr.id)
            attr.save()
            form.save_m2m()
            formset.save()
            messages.success(request, "ویژگی با موفقیت ذخیره شد.")
            return redirect("panel:attribute_edit", pk=attr.pk)
        else:
            if not form.is_valid():
                for field, errs in form.errors.items():
                    for e in errs:
                        messages.error(request, f"فیلد «{form.fields.get(field, type('', (), {'label': field}))}»: {e}" if hasattr(form.fields.get(field), 'label') else f"{field}: {e}")
            if not formset.is_valid():
                err = formset.non_form_errors()
                if err:
                    for e in err:
                        messages.error(request, str(e))
                for i, f in enumerate(formset.forms):
                    if f.errors:
                        for field, errs in f.errors.items():
                            for e in errs:
                                messages.error(request, f"گزینه {i+1} ({field}): {e}")
    else:
        form = AttributeForm(instance=attr)
        formset = AttributeOptionFormSet(instance=attr)
    return render(
        request,
        "panel/attribute_form.html",
        {
            "form": form,
            "formset": formset,
            "object": attr,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مدیریت ویژگی‌ها", "url": reverse("panel:attribute_list")},
                {"title": f"ویرایش: {attr.name}", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def attribute_delete(request, pk):
    """حذف ویژگی — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")
    attr = get_object_or_404(Attribute, pk=pk)
    if request.method == "POST":
        attr.delete()
        return redirect("panel:attribute_list")
    return render(
        request,
        "panel/attribute_confirm_delete.html",
        {
            "object": attr,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "مدیریت ویژگی‌ها", "url": reverse("panel:attribute_list")},
                {"title": f"حذف: {attr.name}", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def reverse_geocode_json(request):
    """تبدیل مختصات به شهر/محله با سرویس نشان؛ برگرداندن city_id و area_id برای فرم آگهی."""
    lat = request.GET.get("lat", "").strip()
    lng = request.GET.get("lng", "").strip()
    if not lat or not lng:
        return JsonResponse({"city_id": None, "area_id": None, "error": "lat and lng required"})

    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except ValueError:
        return JsonResponse({"city_id": None, "area_id": None, "error": "invalid coordinates"})

    api_key = getattr(settings, "NESHAN_SERVICE_API_KEY", "") or getattr(settings, "NESHAN_API_KEY", "")
    if not api_key:
        return JsonResponse({"city_id": None, "area_id": None, "error": "NESHAN_SERVICE_API_KEY not set"})

    url = f"https://api.neshan.org/v5/reverse?lat={lat_f}&lng={lng_f}"
    req = Request(url, headers={"Api-Key": api_key})
    try:
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except (HTTPError, URLError, json.JSONDecodeError) as e:
        return JsonResponse({"city_id": None, "area_id": None, "error": str(e)})

    if data.get("status") != "OK":
        return JsonResponse({
            "city_id": None, "area_id": None,
            "error": data.get("status", "unknown") or "Neshan API error"
        })

    city_name = (data.get("city") or "").strip()
    neighbourhood = (data.get("neighbourhood") or "").strip()

    city_id = None
    area_id = None

    if city_name:
        city = City.objects.filter(fa_name__iexact=city_name, is_active=True).first()
        if not city:
            city = City.objects.filter(fa_name__icontains=city_name, is_active=True).first()
        if city:
            city_id = city.id
            if neighbourhood and city_id:
                area = Area.objects.filter(
                    city_id=city_id,
                    is_active=True,
                ).filter(
                    Q(fa_name__iexact=neighbourhood) | Q(fa_name__icontains=neighbourhood)
                ).first()
                if area:
                    area_id = area.id

    return JsonResponse({"city_id": city_id, "area_id": area_id, "city_name": city_name, "neighbourhood": neighbourhood})


def areas_json(request):
    """برگرداندن محله‌های یک شهر به صورت JSON برای پر کردن select."""
    city_id = request.GET.get("city_id", "").strip()
    if not city_id:
        return JsonResponse([], safe=False)
    try:
        cid = int(city_id)
    except ValueError:
        return JsonResponse([], safe=False)
    areas = list(
        Area.objects.filter(city_id=cid, is_active=True)
        .order_by("sort_order", "id")
        .values("id", "fa_name")
    )
    return JsonResponse(areas, safe=False)


@login_required(login_url="/accounts/login/")
def attributes_json(request):
    """ویژگی‌های مربوط به یک دسته‌بندی برای فرم آگهی."""
    category_id = request.GET.get("category_id", "").strip()
    listing_id = request.GET.get("listing_id", "").strip()
    if not category_id:
        return JsonResponse([], safe=False)
    try:
        cid = int(category_id)
    except ValueError:
        return JsonResponse([], safe=False)
    attrs = Attribute.objects.filter(
        categories__id=cid,
        is_active=True,
    ).order_by("sort_order", "id").distinct()
    current_values = {}
    if listing_id:
        try:
            lid = int(listing_id)
            if _get_user_listings_queryset(request.user).filter(id=lid).exists():
                for lav in ListingAttribute.objects.filter(
                    listing_id=lid
                ).select_related("attribute", "value_option"):
                    # استخراج مقدار از هر فیلدی که پر شده (مستقل از value_type)
                    if lav.value_int is not None:
                        current_values[lav.attribute_id] = lav.value_int
                    elif lav.value_bool is not None:
                        current_values[lav.attribute_id] = lav.value_bool
                    elif lav.value_str:
                        current_values[lav.attribute_id] = lav.value_str
                    elif lav.value_option_id is not None:
                        current_values[lav.attribute_id] = lav.value_option_id
        except ValueError:
            pass
    result = []
    for attr in attrs:
        item = {
            "id": attr.id,
            "name": attr.name,
            "value_type": attr.value_type,
            "unit": attr.unit or "",
        }
        if attr.value_type == Attribute.ValueType.CHOICE:
            item["options"] = list(
                AttributeOption.objects.filter(attribute=attr)
                .order_by("sort_order", "id")
                .values("id", "value")
            )
            item["current_value"] = current_values.get(attr.id)
        else:
            item["options"] = None
            item["current_value"] = current_values.get(attr.id)
        result.append(item)
    return JsonResponse(result, safe=False)


