# Generated by Django 4.1.5 on 2024-04-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0006_alter_broiler_type_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='broiler_region',
            name='broilertype_c',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]