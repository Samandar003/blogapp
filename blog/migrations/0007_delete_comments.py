# Generated by Django 4.0.1 on 2022-01-22 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comments_created'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
