# Generated by Django 3.2.12 on 2022-05-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Shipping Cost'),
        ),
    ]
