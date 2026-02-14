# Generated manually

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_allow_index_category_intro_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='main_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='محتوا با امکان درج و آپلود تصویر'),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/categories/%Y/%m/')),
                ('alt', models.CharField(blank=True, max_length=180)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_cover', models.BooleanField(default=False, help_text='تصویر کارت دسته‌بندی')),
                ('is_landing_cover', models.BooleanField(default=False, help_text='کاور صفحه لندینگ')),
                ('is_content_image', models.BooleanField(default=False, help_text='تصاویر محتوا')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='categories.category')),
            ],
            options={
                'verbose_name': 'تصویر دسته‌بندی',
                'verbose_name_plural': 'تصاویر دسته‌بندی',
                'ordering': ('sort_order', 'id'),
            },
        ),
    ]
