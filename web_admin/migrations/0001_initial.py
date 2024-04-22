# Generated by Django 4.1.5 on 2024-04-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ftype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('abbreviation', models.CharField(max_length=150)),
                ('ctype', models.CharField(max_length=150)),
                ('createdate', models.DateTimeField()),
                ('bActive', models.BooleanField(default=True)),
            ],
        ),
    ]
