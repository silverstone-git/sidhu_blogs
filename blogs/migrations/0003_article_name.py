# Generated by Django 4.0.1 on 2022-01-13 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_reader_saved_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='name',
            field=models.CharField(default='origin_13_jan_2022', max_length=300),
        ),
    ]