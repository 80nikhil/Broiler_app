# Generated by Django 4.1.5 on 2024-04-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0002_ctype_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctype_data',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False),
        ),
    ]
