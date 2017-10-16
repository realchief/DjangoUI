# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django import forms

from . import models
from .models import Customer

class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'email', 'first_name', 'last_name', 'is_superuser', 'date_joined', 'group')
    list_filter = BaseUserAdmin.list_filter
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'last_login')
        }),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def group(self, obj):
        if not obj:
            return None
        groups = obj.groups.values_list('name', flat=True)
        if len(groups) <= 0:
            return None
        return groups[0].encode('utf-8')

class Evaluation_UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date_joined', 'email_activities',]
    fieldsets = (
        ('Personal info', {
            'fields': ('name', 'company_name', 'email', 'phone_number',)
        }),
        ('License info', {
            'fields': ('license_requirements', 'interest_product', 'time_frame',)
        }),
        ('Permissions', {
            'fields': ('is_subscribed', 'email_activities',)
        }),
        ('Note', {
            'fields': ('note_use',)
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class LicenseAllowanceAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'user_id', 'total_product', 'registered_product',]
    fieldsets = (
        ('Customer info', {
            'fields': ('user_id',)
        }),
        ('Product info', {
            'fields': ('product_id', 'total_product', 'registered_product',)
        }),
    )
    ordering = ('product_id',)
    filter_horizontal = ()

class LicenseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'key', 'user_email', 'system_hash', 'number_licenses', 'date_joined',]
    fieldsets = (
        ('Customer info', {
            'fields': ('user_email',)
        }),
        ('License info', {
            'fields': ('product_name', 'key', 'system_hash', 'number_licenses',)
        }),
    )
    search_fields = ('user_email',)
    ordering = ('user_email',)
    filter_horizontal = ()

class LabelLicenseRequirementAdmin(admin.ModelAdmin):
    list_display = ['list_id', 'name']

class LabelInterestProductAdmin(admin.ModelAdmin):
    list_display = ['list_id', 'name']

class LabelPurchaseTimeFrameAdmin(admin.ModelAdmin):
    list_display = ['list_id', 'name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']


admin.site.register(models.Customer, UserAdmin)
admin.site.register(models.License_Allowance, LicenseAllowanceAdmin)
admin.site.register(models.License_Registration, LicenseRegistrationAdmin)
admin.site.register(models.Evaluation_User, Evaluation_UserAdmin)
admin.site.register(models.Label_License_Requirement, LabelLicenseRequirementAdmin)
admin.site.register(models.Label_Interest_Product, LabelInterestProductAdmin)
admin.site.register(models.Label_Purchase_Time_Frame, LabelPurchaseTimeFrameAdmin)
admin.site.register(models.Product, ProductAdmin)
