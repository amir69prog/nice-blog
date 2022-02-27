# Generated by Django 4.0.2 on 2022-02-27 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_reading_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date_created', '-date_updated')},
        ),
        migrations.AlterField(
            model_name='post',
            name='reading_time',
            field=models.DurationField(help_text='Please enter the reading time as `seconds`'),
        ),
    ]