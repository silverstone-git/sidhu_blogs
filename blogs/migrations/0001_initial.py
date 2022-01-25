# Generated by Django 4.0.1 on 2022-01-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=122)),
                ('content', models.CharField(max_length=900000)),
                ('date_posted', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('date_posted', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=122)),
                ('email_address', models.EmailField(max_length=254)),
                ('description', models.CharField(max_length=300)),
                ('level', models.CharField(default='novice', max_length=20)),
                ('no_of_comments', models.IntegerField(default=0)),
            ],
        ),
    ]
