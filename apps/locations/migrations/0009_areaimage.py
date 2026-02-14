# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_cityimage_caption_cityimage_is_content_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/areas/%Y/%m/')),
                ('alt', models.CharField(blank=True, max_length=180)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_cover', models.BooleanField(default=False, help_text='تصویر کارت محله')),
                ('is_landing_cover', models.BooleanField(default=False, help_text='کاور صفحه لندینگ محله')),
                ('is_content_image', models.BooleanField(default=False, help_text='تصاویر محتوا')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='locations.area')),
            ],
            options={
                'verbose_name': 'تصویر محله',
                'verbose_name_plural': 'تصاویر محله',
                'ordering': ('sort_order', 'id'),
            },
        ),
    ]
