# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Evaluation_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, db_column='name')),
                ('email', models.EmailField(unique=True, max_length=254, db_column='email')),
                ('company_name', models.CharField(default='', max_length=255, db_column='company_name')),
                ('phone_number', models.CharField(default='', max_length=255, db_column='phone_number')),
                ('license_requirements', models.CharField(default='', max_length=255, db_column='license_requirements')),
                ('interest_product', models.CharField(default='', max_length=255, db_column='interest_product')),
                ('time_frame', models.CharField(default='', max_length=255, db_column='time_frame')),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined')),
                ('is_subscribed', models.BooleanField(default=False, db_column='is_subscribed')),
                ('note_use', models.TextField(default='', db_column='note_use')),
                ('email_activities', models.IntegerField(default=1, max_length=11, db_column='email_activities')),
            ],
            options={
                'db_table': 'evaluation_user',
            },
        ),
        migrations.CreateModel(
            name='Label_Interest_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list_id', models.IntegerField(max_length=30, db_column='list_id')),
                ('name', models.CharField(max_length=30, db_column='name')),
            ],
            options={
                'db_table': 'label_interest_product',
            },
        ),
        migrations.CreateModel(
            name='Label_License_Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list_id', models.IntegerField(max_length=30, db_column='list_id')),
                ('name', models.CharField(max_length=30, db_column='name')),
            ],
            options={
                'db_table': 'label_license_requirement',
            },
        ),
        migrations.CreateModel(
            name='Label_Purchase_Time_Frame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list_id', models.IntegerField(max_length=30, db_column='list_id')),
                ('name', models.CharField(max_length=30, db_column='name')),
            ],
            options={
                'db_table': 'label_purchase_time_frame',
            },
        ),
        migrations.CreateModel(
            name='License_Allowance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField(default=0, max_length=11, db_column='product_id')),
                ('user_id', models.IntegerField(default=0, max_length=11, db_column='user_id')),
                ('total_product', models.CharField(default=0, max_length=30, db_column='total_product')),
                ('registered_product', models.CharField(default=0, max_length=30, db_column='registered_product')),
            ],
            options={
                'db_table': 'license_allowance',
            },
        ),
        migrations.CreateModel(
            name='License_Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.TextField(max_length=30, db_column='key')),
                ('product_id', models.EmailField(max_length=254, db_column='product_id')),
                ('user_email', models.CharField(max_length=254, db_column='user_email')),
                ('system_hash', models.CharField(max_length=254, db_column='system_hash')),
                ('product_name', models.CharField(default='', max_length=254, db_column='product_name')),
                ('number_licenses', models.IntegerField(max_length=11, db_column='number_licenses')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
            ],
            options={
                'db_table': 'license_registration',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254, db_column='name')),
                ('type', models.CharField(default='', max_length=254, db_column='type')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
