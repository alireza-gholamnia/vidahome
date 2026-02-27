from django.db import migrations, models


_PHONE_DIGIT_TRANSLATION = str.maketrans(
    {
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
    }
)


def _normalize_phone(value: str) -> str:
    if not value:
        return ""
    normalized_input = str(value).translate(_PHONE_DIGIT_TRANSLATION)
    digits = "".join(ch for ch in normalized_input if ch.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("98") and len(digits) >= 10:
        return "0" + digits[2:]
    if digits.startswith("9") and len(digits) == 10:
        return "0" + digits
    if not digits:
        return ""
    return digits if digits.startswith("0") else "0" + digits


def normalize_and_deduplicate_user_phones(apps, schema_editor):
    User = apps.get_model("accounts", "User")

    for user in User.objects.exclude(phone="").only("id", "phone").iterator():
        normalized = _normalize_phone(user.phone)
        if normalized != user.phone:
            User.objects.filter(pk=user.pk).update(phone=normalized)

    seen = set()
    duplicate_ids = []
    for user in User.objects.exclude(phone="").order_by("id").values("id", "phone").iterator():
        phone = user["phone"]
        if phone in seen:
            duplicate_ids.append(user["id"])
        else:
            seen.add(phone)

    if duplicate_ids:
        User.objects.filter(id__in=duplicate_ids).update(phone="")


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_rolechangerequest_uniq_pending_rolechange_user_role"),
    ]

    operations = [
        migrations.RunPython(normalize_and_deduplicate_user_phones, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                condition=~models.Q(phone=""),
                fields=("phone",),
                name="uniq_accounts_user_phone_nonempty",
            ),
        ),
    ]
