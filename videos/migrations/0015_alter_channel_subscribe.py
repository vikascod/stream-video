# Generated by Django 4.2.2 on 2023-06-06 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_alter_channel_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='subscribe',
            field=models.ManyToManyField(blank=True, related_name='subscribed_by', to='videos.channel'),
        ),
    ]
