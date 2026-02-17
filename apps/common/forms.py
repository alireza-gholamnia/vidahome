"""فرم‌های عمومی."""
from django import forms


class ContactForm(forms.Form):
    """فرم تماس با ما."""
    name = forms.CharField(
        max_length=120,
        label="نام",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی"}),
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@email.com"}),
    )
    phone = forms.CharField(
        required=False,
        max_length=20,
        label="تلفن",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "09xxxxxxxxx"}),
    )
    subject = forms.CharField(
        required=False,
        max_length=200,
        label="موضوع",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "موضوع پیام"}),
    )
    message = forms.CharField(
        label="پیام",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "پیام خود را بنویسید..."}),
    )
