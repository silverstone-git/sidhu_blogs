# Generated by Django 4.0.2 on 2022-02-26 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_remove_comment_date_posted_comment_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='no_of_upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.CharField(default='1645854649.8061411', max_length=300),
        ),
    ]
