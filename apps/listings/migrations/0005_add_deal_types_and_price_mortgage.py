# Generated manually for deal types and price_mortgage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_listing_agency_listing_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price_mortgage',
            field=models.BigIntegerField(
                blank=True,
                help_text='فقط برای نوع «رهن و اجاره»',
                null=True,
                verbose_name='مبلغ رهن',
            ),
        ),
        migrations.AlterField(
            model_name='listing',
            name='deal',
            field=models.CharField(
                choices=[
                    ('buy', 'فروش'),
                    ('rent', 'اجاره'),
                    ('daily_rent', 'اجاره روزانه'),
                    ('mortgage_rent', 'رهن و اجاره'),
                ],
                db_index=True,
                default='buy',
                max_length=16,
                verbose_name='نوع معامله',
            ),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.BigIntegerField(
                blank=True,
                help_text='قیمت اصلی (خرید / اجاره ماهانه / اجاره روزانه / اجاره ماهانه در رهن\u200cواجاره)',
                null=True,
                verbose_name='قیمت',
            ),
        ),
    ]
