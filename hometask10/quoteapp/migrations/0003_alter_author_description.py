# Generated by Django 4.2.3 on 2023-07-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0002_alter_author_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
