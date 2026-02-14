# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_cityimage_is_landing_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='cityimage',
            name='caption',
            field=models.CharField(blank=True, help_text='لیبل نمایشی — برای تصاویر محتوا مفید است', max_length=200),
        ),
        migrations.AddField(
            model_name='cityimage',
            name='is_content_image',
            field=models.BooleanField(default=False, help_text='تصاویر محتوا — برای درج در محتوای ریچ‌تکست شهر'),
        ),
        migrations.AlterField(
            model_name='cityimage',
            name='alt',
            field=models.CharField(blank=True, help_text='متن جایگزین برای سئو و دسترسی‌پذیری', max_length=180),
        ),
        migrations.AlterField(
            model_name='cityimage',
            name='image',
            field=models.ImageField(upload_to='uploads/cities/%Y/%m/'),
        ),
    ]
