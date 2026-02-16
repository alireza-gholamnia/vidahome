from django import forms
from django.forms import inlineformset_factory

from apps.agencies.models import Agency, AgencyJoinRequest
from apps.accounts.models import User, RoleChangeRequest
from apps.attributes.models import Attribute, AttributeOption
from apps.listings.models import Listing
from apps.locations.models import Area, City
from apps.categories.models import Category


class ListingForm(forms.ModelForm):
    """فرم افزودن/ویرایش آگهی در پنل کاربری"""

    class Meta:
        model = Listing
        fields = [
            "title",
            "city",
            "area",
            "category",
            "deal",
            "status",
            "short_description",
            "description",
            "price",
            "price_mortgage",
            "price_unit",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "عنوان آگهی"}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "area": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "deal": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "short_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "خلاصه کوتاه"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control w-100", "rows": 6, "style": "width: 100%; min-width: 100%;"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "قیمت"}),
            "price_mortgage": forms.NumberInput(attrs={"class": "form-control", "placeholder": "مبلغ رهن"}),
            "price_unit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "تومان", "value": "تومان"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        city_id = kwargs.pop("city_id", None)
        super().__init__(*args, **kwargs)
        self.fields["area"].required = False
        self.fields["area"].queryset = Area.objects.none()
        self.fields["price"].required = False
        self.fields["price_mortgage"].required = False
        self.fields["short_description"].required = False
        self.fields["description"].required = False
        # پر کردن محله‌ها بر اساس شهر
        cid = city_id or (self.instance.city_id if self.instance else None)
        if cid:
            self.fields["area"].queryset = Area.objects.filter(city_id=cid).order_by("sort_order", "id")
        self.fields["city"].queryset = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")
        self.fields["category"].queryset = Category.objects.filter(is_active=True).order_by("sort_order", "fa_name")
        # ثبت جدید: همه کاربران فقط «درخواست تأیید و انتشار». ویرایش: کاربر عادی همین گزینه.
        is_new = not self.instance or not self.instance.pk
        is_restricted = is_new or not (self.user.is_superuser or (self.user and self.user.groups.filter(name="site_admin").exists()))
        if self.user and is_restricted:
            self.fields["status"].choices = [
                (Listing.Status.PENDING, "درخواست تأیید و انتشار"),
            ]
            if is_new:
                self.fields["status"].initial = Listing.Status.PENDING
        # فیلد مشاوره برای صاحب مشاوره با چند آژانس
        if self.user:
            agencies = Agency.objects.filter(owner=self.user)
            if agencies.count() > 1:
                self.fields["agency"] = forms.ModelChoiceField(
                    queryset=agencies,
                    required=False,
                    label="مشاوره املاک",
                    widget=forms.Select(attrs={"class": "form-select"}),
                )


class UserProfileForm(forms.ModelForm):
    """فرم ویرایش اطلاعات شخصی کاربر."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "email", "avatar")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام خانوادگی"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "۰۹۱۲۳۴۵۶۷۸۹", "dir": "ltr"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@email.com"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }


class AgencyCreateForm(forms.ModelForm):
    """فرم ایجاد مشاوره املاک جدید توسط صاحب مشاوره."""

    class Meta:
        model = Agency
        fields = ("name", "phone", "address", "intro_content", "logo", "cities")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام مشاوره املاک"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "تلفن", "dir": "ltr"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "آدرس"}),
            "intro_content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "cities": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cities"].queryset = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")


class AgencyProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل مشاوره املاک (برای صاحب مشاوره)."""

    class Meta:
        model = Agency
        fields = ("name", "phone", "address", "intro_content", "main_content", "logo", "cities")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام مشاوره املاک"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "تلفن", "dir": "ltr"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "آدرس"}),
            "intro_content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "cities": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cities"].queryset = City.objects.filter(is_active=True).order_by("sort_order", "fa_name")


class AgencyJoinRequestForm(forms.ModelForm):
    """فرم درخواست عضویت در مشاوره املاک به عنوان کارمند."""

    class Meta:
        model = AgencyJoinRequest
        fields = ("agency",)
        widgets = {
            "agency": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Agency.objects.filter(
            approval_status=Agency.ApprovalStatus.APPROVED,
            is_active=True,
        ).order_by("name")
        if user:
            pending_agency_ids = AgencyJoinRequest.objects.filter(
                user=user, status=AgencyJoinRequest.Status.PENDING
            ).values_list("agency_id", flat=True)
            qs = qs.exclude(id__in=pending_agency_ids)
        self.fields["agency"].queryset = qs


class RoleChangeRequestForm(forms.ModelForm):
    """فرم درخواست تغییر نقش به صاحب مشاوره یا کارمند مشاوره."""

    class Meta:
        model = RoleChangeRequest
        fields = ("requested_role", "message")
        widgets = {
            "requested_role": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "توضیح دلیل درخواست و زمینه فعالیت خود را بنویسید...",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # حذف نقش‌هایی که کاربر از قبل دارد
            existing_roles = set(user.groups.values_list("name", flat=True))
            choices = [
                (k, v)
                for k, v in RoleChangeRequest.RequestedRole.choices
                if k not in existing_roles
            ]
            self.fields["requested_role"].choices = choices
            if not choices:
                self.fields["requested_role"].choices = [("", "--- شما هر دو نقش را دارید ---")]
                self.fields["requested_role"].required = False  # تا validation خطا ندهد


class AttributeForm(forms.ModelForm):
    """فرم تعریف/ویرایش ویژگی ملک (فقط ادمین سایت). اسلاگ به‌صورت خودکار از id پر می‌شود."""

    class Meta:
        model = Attribute
        fields = (
            "name",
            "value_type",
            "unit",
            "icon",
            "categories",
            "sort_order",
            "is_active",
            "is_filterable",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "مثال: تعداد اتاق"}),
            "value_type": forms.Select(attrs={"class": "form-select"}),
            "unit": forms.TextInput(attrs={"class": "form-control", "placeholder": "مثال: اتاق، متر"}),
            "icon": forms.FileInput(attrs={"accept": ".png,.svg"}),
            "categories": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_filterable": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categories"].required = False
        self.fields["categories"].queryset = Category.objects.filter(is_active=True).order_by("sort_order", "fa_name")
        self.fields["categories"].error_messages = {
            "invalid_choice": "دسته‌بندی انتخاب‌شده معتبر نیست. صفحه را رفرش کرده و دوباره امتحان کنید.",
            "invalid_list": "مقدار دسته‌بندی نامعتبر است.",
        }


AttributeOptionFormSet = inlineformset_factory(
    Attribute,
    AttributeOption,
    fields=("value", "sort_order"),
    extra=0,
    can_delete=True,
    validate_min=False,
    widgets={
        "value": forms.TextInput(attrs={"class": "form-control", "placeholder": "مقدار"}),
        "sort_order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
    },
)
