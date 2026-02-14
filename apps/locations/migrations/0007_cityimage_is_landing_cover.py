# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_rename_loc_cityimg_city_sort_idx_locations_c_city_id_b12a11_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cityimage',
            name='is_landing_cover',
            field=models.BooleanField(default=False, help_text='عکس کاور صفحه لندینگ شهر — نمایش در بالای صفحه شهر'),
        ),
        migrations.AlterField(
            model_name='cityimage',
            name='is_cover',
            field=models.BooleanField(default=False, help_text='تصویر شاخص برای کارت شهر در صفحه لیست شهرها'),
        ),
    ]
