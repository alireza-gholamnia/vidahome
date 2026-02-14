# Generated manually for CityImage

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_area_allow_index_area_intro_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cities/%Y/%m/')),
                ('alt', models.CharField(blank=True, max_length=180)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_cover', models.BooleanField(default=False, help_text='تصویر اصلی برای کارت و بنر شهر')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='locations.city')),
            ],
            options={
                'verbose_name': 'تصویر شهر',
                'verbose_name_plural': 'تصاویر شهر',
                'ordering': ('sort_order', 'id'),
            },
        ),
        migrations.AddIndex(
            model_name='cityimage',
            index=models.Index(fields=['city', 'sort_order'], name='loc_cityimg_city_sort_idx'),
        ),
        migrations.AddIndex(
            model_name='cityimage',
            index=models.Index(fields=['city', 'is_cover'], name='loc_cityimg_city_cover_idx'),
        ),
    ]
