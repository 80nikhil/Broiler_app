# Generated by Django 4.1.5 on 2024-04-10 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0003_alter_ctype_data_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctype_data',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
