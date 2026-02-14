# Generated manually

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citycategory',
            name='main_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='محتوا با امکان درج و آپلود تصویر'),
        ),
        migrations.AlterField(
            model_name='cityareacategory',
            name='main_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='محتوا با امکان درج و آپلود تصویر'),
        ),
        migrations.CreateModel(
            name='CityCategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/city_category/%Y/%m/')),
                ('alt', models.CharField(blank=True, max_length=180)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_cover', models.BooleanField(default=False)),
                ('is_landing_cover', models.BooleanField(default=False, help_text='کاور صفحه لندینگ')),
                ('is_content_image', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='seo.citycategory')),
            ],
            options={
                'verbose_name': 'تصویر شهر+دسته',
                'verbose_name_plural': 'تصاویر شهر+دسته',
                'ordering': ('sort_order', 'id'),
            },
        ),
        migrations.CreateModel(
            name='CityAreaCategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/area_category/%Y/%m/')),
                ('alt', models.CharField(blank=True, max_length=180)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_cover', models.BooleanField(default=False)),
                ('is_landing_cover', models.BooleanField(default=False, help_text='کاور صفحه لندینگ')),
                ('is_content_image', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city_area_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='seo.cityareacategory')),
            ],
            options={
                'verbose_name': 'تصویر محله+دسته',
                'verbose_name_plural': 'تصاویر محله+دسته',
                'ordering': ('sort_order', 'id'),
            },
        ),
    ]
