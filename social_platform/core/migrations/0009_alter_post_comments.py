# Generated by Django 4.2.6 on 2024-02-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_post_comments_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts', to='core.postcommont'),
        ),
    ]
