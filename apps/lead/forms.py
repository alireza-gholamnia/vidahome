"""فرم‌های لید."""
from django import forms


def _lock_name_fields_on_form(form, disabled_attrs: dict | None = None):
    """نام و نام خانوادگی را غیرقابل ویرایش کن (دیسیبل + readonly). وقتی دیسیبل هستند مقدار در POST نمی‌آید، پس required=False تا اعتبارسنجی خطا ندهد."""
    attrs = disabled_attrs or {"readonly": "readonly", "style": "pointer-events:none; background-color:var(--bs-secondary-bg);"}
    for name in ("first_name", "last_name"):
        form.fields[name].disabled = True
        form.fields[name].required = False
        form.fields[name].widget.attrs.update(attrs)


def _lock_phone_field_on_form(form, disabled_attrs: dict | None = None):
    """فیلد تلفن را غیرقابل ویرایش کن (بعد از لاگین). مقدار در POST نمی‌آید؛ ویو باید از user.phone پر کند."""
    attrs = disabled_attrs or {"readonly": "readonly", "style": "pointer-events:none; background-color:var(--bs-secondary-bg);"}
    form.fields["phone"].disabled = True
    form.fields["phone"].required = False
    form.fields["phone"].widget.attrs.update(attrs)


class ListingLeadForm(forms.Form):
    """فرم استعلام/تماس درباره آگهی — نام و نام خانوادگی جدا؛ بعد از ارسال برای کاربر لاگین پروفایل تکمیل می‌شود."""
    first_name = forms.CharField(
        max_length=60,
        label="نام",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام"}),
    )
    last_name = forms.CharField(
        max_length=60,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام خانوادگی"}),
    )
    phone = forms.CharField(
        max_length=20,
        label="تلفن",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "09xxxxxxxxx"}),
    )
    message = forms.CharField(
        required=False,
        label="پیام",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "پیام یا سؤال خود را بنویسید..."}),
    )

    def __init__(self, *args, **kwargs):
        lock_name_fields = kwargs.pop("lock_name_fields", False)
        lock_phone_field = kwargs.pop("lock_phone_field", False)
        super().__init__(*args, **kwargs)
        if lock_name_fields:
            _lock_name_fields_on_form(self)
        if lock_phone_field:
            _lock_phone_field_on_form(self)


class LandingLeadForm(forms.Form):
    """فرم لید برای لندینگ‌ها و صفحه تماس. با prefix='landing' استفاده شود."""
    first_name = forms.CharField(
        max_length=60,
        label="نام",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام"}),
    )
    last_name = forms.CharField(
        max_length=60,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام خانوادگی"}),
    )
    phone = forms.CharField(
        max_length=20,
        label="تلفن",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "09xxxxxxxxx"}),
    )
    email = forms.EmailField(
        required=False,
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@email.com"}),
    )
    subject = forms.CharField(
        required=False,
        max_length=200,
        label="موضوع",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "موضوع پیام"}),
    )
    message = forms.CharField(
        required=False,
        label="پیام",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "پیام خود را بنویسید..."}),
    )

    def __init__(self, *args, **kwargs):
        lock_name_fields = kwargs.pop("lock_name_fields", False)
        lock_phone_field = kwargs.pop("lock_phone_field", False)
        super().__init__(*args, **kwargs)
        if lock_name_fields:
            _lock_name_fields_on_form(self)
        if lock_phone_field:
            _lock_phone_field_on_form(self)
