# Generated by Django 4.1.5 on 2024-04-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0012_broiler_region_alias_name_broiler_type_alias_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]