# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class AuthUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    """
    Used for all authenticated user (influencers, brands, assistants, superuser, etc...)
    """

    first_name = models.CharField( ('first name'), max_length=30, blank=True)
    last_name = models.CharField( ('last name'), max_length=30, blank=True)
    email = models.EmailField( ('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField( ('staff status'), default=False,
                                   help_text= ('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField( ('active'), default=True,
                                    help_text= ('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField( ('date joined'), auto_now_add=True)
    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'customer'

class Evaluation_User(models.Model):

    name = models.CharField(max_length=30, db_column="name")
    email = models.EmailField(max_length=254, unique=True, db_column="email")
    company_name = models.CharField(max_length=255, db_column="company_name", default="")
    phone_number = models.CharField(max_length=255, db_column="phone_number", default="")
    license_requirements = models.CharField(max_length=255, db_column="license_requirements", default="")
    interest_product = models.CharField(max_length=255, db_column="interest_product", default="")
    time_frame = models.CharField(max_length=255, db_column="time_frame", default="")
    date_joined = models.DateTimeField(auto_now_add=True, db_column="date_joined")
    is_subscribed = models.BooleanField(default=False, db_column="is_subscribed")
    note_use = models.TextField(db_column="note_use", default="")
    email_activities = models.IntegerField(max_length=11, db_column="email_activities", default=1)

    class Meta:
        db_table = 'evaluation_user'

class Label_License_Requirement(models.Model):

    list_id = models.IntegerField(max_length=30, db_column="list_id")
    name = models.CharField(max_length=30, db_column="name")

    class Meta:
        db_table = 'label_license_requirement'

class Label_Interest_Product(models.Model):
    list_id = models.IntegerField(max_length=30, db_column="list_id")
    name = models.CharField(max_length=30, db_column="name")

    class Meta:
        db_table = 'label_interest_product'

class Label_Purchase_Time_Frame(models.Model):

    list_id = models.IntegerField(max_length=30, db_column="list_id")
    name = models.CharField(max_length=30, db_column="name")

    class Meta:
        db_table = 'label_purchase_time_frame'

class License_Allowance(models.Model):

    product_id = models.IntegerField(max_length=11, db_column="product_id", default=0)
    user_id = models.IntegerField(max_length=11, db_column="user_id", default=0)
    total_product = models.CharField(max_length=30, db_column="total_product", default=0)
    registered_product = models.CharField(max_length=30, db_column="registered_product", default=0)

    class Meta:
        db_table = 'license_allowance'

class License_Registration(models.Model):

    key = models.TextField(max_length=30, db_column="key")
    product_id = models.EmailField(max_length=254, db_column="product_id")
    user_email = models.CharField(max_length=254, db_column="user_email")
    system_hash = models.CharField(max_length=254, db_column="system_hash")
    product_name = models.CharField(max_length=254, db_column="product_name", default="")
    number_licenses = models.IntegerField(max_length=11, db_column="number_licenses")
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)

    class Meta:
        db_table = 'license_registration'

class Product(models.Model):

    name = models.CharField(max_length=254, db_column="name")
    type = models.CharField(max_length=254, db_column="type", default="")

    class Meta:
        db_table = 'product'