# Generated by Django 4.2.3 on 2023-07-26 09:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='overview',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]