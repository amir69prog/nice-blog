# Generated by Django 4.0.2 on 2022-02-19 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(help_text='Please enter your phone number as a following template\nuse one of these: [09120000000 | +9891200000000 | 00989120000000]', max_length=14, unique=True, validators=[django.core.validators.RegexValidator(code='phone_number_validator', message='Phone number is not correct', regex='^(0|\\+98|0098)9[0-9]{9}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
