import json
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.agencies.models import Agency, AgencyJoinRequest, EmployeeRemoveRequest
from apps.attributes.models import Attribute, AttributeOption, ListingAttribute
from apps.accounts.models import RoleChangeRequest
from apps.listings.models import Listing
from apps.locations.models import Area, City

from .forms import (
    AgencyCreateForm,
    AgencyJoinRequestForm,
    AgencyProfileForm,
    AttributeForm,
    AttributeOptionFormSet,
    ListingForm,
    RoleChangeRequestForm,
    UserProfileForm,
)


def _get_user_agencies(user):
    """مشاوره‌های املاکی که کاربر مالک آن‌هاست."""
    return Agency.objects.filter(owner=user)


def _get_user_agency(user):
    """اولین مشاوره مالکیت‌شده توسط کاربر (برای سازگاری)."""
    return _get_user_agencies(user).first()


def _get_user_listings_queryset(user):
    """آگهی‌های قابل دسترسی برای کاربر (صاحب مشاوره، کارمند، یا شخصی)."""
    qs = Listing.objects.select_related(
        "city", "area", "category", "created_by"
    ).prefetch_related("images")
    if user.is_superuser or _is_site_admin(user):
        return qs
    agencies = _get_user_agencies(user)
    if agencies.exists():
        return qs.filter(agency__owner=user)
    return qs.filter(created_by=user)


def _can_edit_listing(user, listing):
    """آیا کاربر مجاز به ویرایش این آگهی است؟"""
    if user.is_superuser or _is_site_admin(user):
        return True
    if listing.created_by_id == user.id:
        return True
    if listing.agency_id and Agency.objects.filter(owner=user, id=listing.agency_id).exists():
        return True
    return False


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
            {"title": "ثبت ملک جدید", "url": None},
        ]
        context["initial_listing_id"] = None
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
        agency = form.cleaned_data.get("agency")
        if not agency:
            agency = getattr(self.request.user, "agency", None) or _get_user_agency(self.request.user)
        if agency:
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
        attr_post = {}
        if self.request.method == "POST":
            for k, v in self.request.POST.items():
                if k.startswith("attr_"):
                    attr_post[k] = v
        context["attr_post_json"] = json.dumps(attr_post)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        agency = form.cleaned_data.get("agency")
        if agency:
            obj.agency = agency
        was_published = self.object.status == Listing.Status.PUBLISHED
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
    """ویرایش اطلاعات شخصی کاربر."""
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
                {"title": "ویرایش پروفایل", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def agency_list(request):
    """لیست مشاوره‌های املاک کاربر (صاحب مشاوره)."""
    agencies = _get_user_agencies(request.user)
    if not agencies.exists():
        if request.user.groups.filter(name="agency_owner").exists():
            return redirect("panel:agency_add")
        return redirect("panel:dashboard")
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
    """افزودن مشاوره املاک جدید (فقط برای صاحب مشاوره)."""
    if not request.user.groups.filter(name="agency_owner").exists():
        return redirect("panel:dashboard")
    if request.method == "POST":
        form = AgencyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.owner = request.user
            agency.approval_status = Agency.ApprovalStatus.PENDING
            agency.save()
            form.save_m2m()
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
    """ویرایش پروفایل مشاوره املاک."""
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
    """لیست کارمندان مشاوره‌های مالک و امکان درخواست حذف — فقط صاحب مشاوره."""
    agencies = _get_user_agencies(request.user).filter(
        approval_status=Agency.ApprovalStatus.APPROVED,
        is_active=True,
    )
    if not agencies.exists():
        return redirect("panel:dashboard")

    from apps.accounts.models import User

    employee_ids = User.objects.filter(
        agency__in=agencies
    ).values_list("id", flat=True)
    employees = list(
        User.objects.filter(id__in=employee_ids)
        .select_related("agency")
        .order_by("agency__name", "first_name", "username")
    )

    # درخواست‌های حذف در انتظار برای هر کارمند
    pending_removes = set(
        EmployeeRemoveRequest.objects.filter(
            user_id__in=employee_ids,
            status=EmployeeRemoveRequest.Status.PENDING,
            requested_by=request.user,
        ).values_list("user_id", flat=True)
    )

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            try:
                emp = User.objects.get(pk=int(user_id), agency__in=agencies)
                if EmployeeRemoveRequest.objects.filter(
                    user=emp,
                    agency=emp.agency,
                    status=EmployeeRemoveRequest.Status.PENDING,
                ).exists():
                    pass  # قبلاً درخواست داده
                else:
                    EmployeeRemoveRequest.objects.create(
                        user=emp,
                        agency=emp.agency,
                        requested_by=request.user,
                        status=EmployeeRemoveRequest.Status.PENDING,
                    )
                    pending_removes.add(emp.id)
            except (ValueError, User.DoesNotExist):
                pass
        return redirect("panel:agency_employees")

    return render(
        request,
        "panel/agency_employees.html",
        {
            "employees": employees,
            "pending_removes": pending_removes,
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
    """درخواست تغییر نقش به صاحب مشاوره یا کارمند مشاوره — برای تمام کاربران."""
    if request.method == "POST":
        form = RoleChangeRequestForm(request.POST, user=request.user)
        if form.is_valid():
            role = form.cleaned_data.get("requested_role")
            if not role:
                form.add_error(
                    "requested_role",
                    "شما هم‌اکنون هر دو نقش صاحب مشاوره و کارمند مشاوره را دارید.",
                )
            else:
                # جلوگیری از درخواست نقش‌ای که کاربر هم‌اکنون دارد
                if request.user.groups.filter(name=role).exists():
                    form.add_error(
                        "requested_role",
                        "شما هم‌اکنون این نقش را دارید.",
                    )
                elif RoleChangeRequest.objects.filter(
                    user=request.user,
                    requested_role=role,
                    status=RoleChangeRequest.Status.PENDING,
                ).exists():
                    form.add_error(
                        "requested_role",
                        "درخواست مشابه برای این نقش در انتظار تأیید دارید.",
                    )
                else:
                    RoleChangeRequest.objects.create(
                        user=request.user,
                        requested_role=role,
                        message=form.cleaned_data.get("message", ""),
                        status=RoleChangeRequest.Status.PENDING,
                    )
                    return redirect("panel:role_change_request")
    else:
        form = RoleChangeRequestForm(user=request.user)
    requests_qs = RoleChangeRequest.objects.filter(user=request.user).order_by("-created_at")[:20]
    # آیا کاربر نقش‌ای برای درخواست دارد؟ (هنوز یکی از دو نقش را ندارد)
    existing = set(request.user.groups.values_list("name", flat=True))
    can_request_role = any(
        r not in existing for r in ["agency_owner", "agency_employee"]
    )
    return render(
        request,
        "panel/role_change_request.html",
        {
            "form": form,
            "requests": list(requests_qs),
            "can_request_role": can_request_role,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "درخواست تغییر نقش", "url": None},
            ],
        },
    )


def _get_pending_listings_queryset():
    """آگهی‌های در صف تأیید (فقط PENDING)."""
    return Listing.objects.filter(status=Listing.Status.PENDING).select_related(
        "city", "category", "created_by"
    )


@login_required(login_url="/accounts/login/")
def employee_request_join(request):
    """درخواست عضویت در مشاوره املاک — فقط برای کاربران با نقش کارمند."""
    if not request.user.groups.filter(name="agency_employee").exists():
        return redirect("panel:dashboard")
    if request.user.agency_id:
        return render(
            request,
            "panel/employee_request_join.html",
            {
                "already_member": True,
                "agency": request.user.agency,
                "breadcrumbs": [
                    {"title": "صفحه اصلی", "url": "/"},
                    {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                    {"title": "درخواست عضویت در مشاوره", "url": None},
                ],
            },
        )
    if request.method == "POST":
        form = AgencyJoinRequestForm(request.POST, user=request.user)
        if form.is_valid():
            agency = form.cleaned_data["agency"]
            if AgencyJoinRequest.objects.filter(
                user=request.user, agency=agency, status=AgencyJoinRequest.Status.PENDING
            ).exists():
                form.add_error("agency", "درخواست مشابه در انتظار تأیید دارید.")
            else:
                AgencyJoinRequest.objects.create(
                    user=request.user,
                    agency=agency,
                    status=AgencyJoinRequest.Status.PENDING,
                )
                return redirect("panel:employee_request_join")
    else:
        form = AgencyJoinRequestForm(user=request.user)
    requests = AgencyJoinRequest.objects.filter(user=request.user).select_related(
        "agency"
    ).order_by("-created_at")[:20]
    return render(
        request,
        "panel/employee_request_join.html",
        {
            "form": form,
            "requests": requests,
            "breadcrumbs": [
                {"title": "صفحه اصلی", "url": "/"},
                {"title": "پنل کاربری", "url": reverse("panel:dashboard")},
                {"title": "درخواست عضویت در مشاوره", "url": None},
            ],
        },
    )


@login_required(login_url="/accounts/login/")
def approve_dashboard(request):
    """داشبورد تأیید — فقط ادمین سایت."""
    if not _is_site_admin(request.user):
        return redirect("panel:dashboard")

    tab = request.GET.get("tab", "pending")
    if tab not in ("pending", "rejected", "approved", "join_requests", "employees", "remove_requests", "role_change"):
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

    # درخواست‌های عضویت کارمند
    join_requests_qs = AgencyJoinRequest.objects.filter(
        status=AgencyJoinRequest.Status.PENDING
    ).select_related("user", "agency").order_by("-created_at")
    join_requests_count = join_requests_qs.count()
    join_requests = list(join_requests_qs[:50])

    # کارمندان (کاربران با agency)
    from apps.accounts.models import User

    employees_qs = User.objects.filter(agency__isnull=False).select_related(
        "agency"
    ).order_by("agency__name", "first_name", "username")
    employees_count = employees_qs.count()
    employees = list(employees_qs[:100])

    # درخواست‌های حذف کارمند (توسط صاحب مشاوره)
    remove_requests_qs = EmployeeRemoveRequest.objects.filter(
        status=EmployeeRemoveRequest.Status.PENDING
    ).select_related("user", "agency", "requested_by").order_by("-created_at")
    remove_requests_count = remove_requests_qs.count()
    remove_requests = list(remove_requests_qs[:50])

    role_change_qs = RoleChangeRequest.objects.filter(
        status=RoleChangeRequest.Status.PENDING
    ).select_related("user").order_by("-created_at")
    role_change_count = role_change_qs.count()
    role_change_requests = list(role_change_qs[:50])

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
            "join_requests": join_requests,
            "join_requests_count": join_requests_count,
            "employees": employees,
            "employees_count": employees_count,
            "remove_requests": remove_requests,
            "remove_requests_count": remove_requests_count,
            "role_change_requests": role_change_requests,
            "role_change_count": role_change_count,
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
        from django.contrib.auth.models import Group

        # اگر کاربر از قبل عضو این مشاوره است، فقط وضعیت را تأیید می‌کنیم
        if join_req.user.agency_id != join_req.agency_id:
            join_req.user.agency = join_req.agency
            join_req.user.save()
        emp_group = Group.objects.filter(name="agency_employee").first()
        if emp_group and not join_req.user.groups.filter(name="agency_employee").exists():
            join_req.user.groups.add(emp_group)
        join_req.status = AgencyJoinRequest.Status.APPROVED
        from django.utils import timezone

        join_req.reviewed_at = timezone.now()
        join_req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=join_requests")
    elif action == "reject":
        join_req.status = AgencyJoinRequest.Status.REJECTED
        from django.utils import timezone

        join_req.reviewed_at = timezone.now()
        join_req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=join_requests")
    return redirect(reverse("panel:approve_dashboard") + "?tab=join_requests")


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
            req.user.agency = None
            req.user.save()
        req.status = EmployeeRemoveRequest.Status.APPROVED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=remove_requests")
    elif action == "reject":
        req.status = EmployeeRemoveRequest.Status.REJECTED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=remove_requests")
    return redirect(reverse("panel:approve_dashboard") + "?tab=remove_requests")


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
        from django.contrib.auth.models import Group

        # اگر کاربر از قبل این نقش را دارد، فقط وضعیت را تأیید می‌کنیم (تغییر گروهی انجام نمی‌شود)
        if not req.user.groups.filter(name=req.requested_role).exists():
            group = Group.objects.filter(name=req.requested_role).first()
            if group:
                req.user.groups.add(group)
        req.status = RoleChangeRequest.Status.APPROVED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=role_change")
    elif action == "reject":
        req.status = RoleChangeRequest.Status.REJECTED
        from django.utils import timezone

        req.reviewed_at = timezone.now()
        req.save()
        return redirect(reverse("panel:approve_dashboard") + "?tab=role_change")
    return redirect(reverse("panel:approve_dashboard") + "?tab=role_change")


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
            emp.agency = None
            emp.save()
        else:
            try:
                agency = Agency.objects.get(
                    pk=int(new_agency_id),
                    approval_status=Agency.ApprovalStatus.APPROVED,
                )
                emp.agency = agency
                emp.save()
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
