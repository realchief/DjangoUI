# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

from os.path import expanduser

from .models import *
from .forms import LoginForm

import subprocess
import time
import re

admin_emails = settings.ADMIN_EMAIL_LIST

# Create your views here.c

def login(request):
    redirect_to = request.POST.get('next_',
                                   request.GET.get('next', 'main:auth_key_register'))
    if request.user.is_authenticated():
        return redirect(redirect_to)
    if request.method == "POST":

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            auth.login(request, form.get_user())
            return redirect(redirect_to)
    else:
        form = LoginForm(request, initial={'next_': redirect_to})

    return render(request, 'pages/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('main:login')

def free_key_generate(request):

    license_requirements_list = Label_License_Requirement.objects.all()
    interest_products_list = Label_Interest_Product.objects.all()
    time_frame_list = Label_Purchase_Time_Frame.objects.all()

    context = {
        'license_requirements_list': license_requirements_list,
        'interest_products_list': interest_products_list,
        'time_frame_list': time_frame_list,
    }

    return render(request, 'pages/eval_request.html', context)

def free_key_generate_ajax(request):

    name = request.GET.get('name')
    email = request.GET.get('email')
    company_name = request.GET.get('company_name')
    phone_number = request.GET.get('phone_number')
    note_use = request.GET.get('note_use')
    license_requirements = request.GET.get('license_requirements')
    product_interest = request.GET.get('product_interest')
    time_frame = request.GET.get('time_frame')

    if Evaluation_User.objects.filter(email=email).exists():

        evaluation_user = Evaluation_User.objects.get(email=email)
        email_activities = evaluation_user.email_activities

        if email_activities > 1:
            try:

                key = get_free_license_key(email)

                evaluation_user.email_activities = email_activities - 1
                evaluation_user.save()

                send_mail_customer(email, key, name)
                send_mail_admin(name, email, phone_number, company_name,
                                license_requirements, product_interest, time_frame, note_use)

                return JsonResponse({
                    'status': 'ok',
                    'message': 'An evaluation key has been emailed to you! '
                               'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                               'for technical assistance and licensing questions.',
                })
            except ValueError:
                return JsonResponse({
                    'status': 'failed',
                    'message': 'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                               'for assistance or questions with your evaluation.',
                })
        else:
            return JsonResponse({
                'status': 'failed',
                'message': 'This e-mail address already been used to register an evaluation. '
                           'Please contact info@openalpr.com to request an extension on your previous evaluation.',
            })

    else:

        try:
            key = get_free_license_key(email)

            new_customer = Evaluation_User(
                name=name, email=email,
                company_name=company_name,
                phone_number=phone_number,
                license_requirements=license_requirements,
                interest_product=product_interest,
                time_frame=time_frame,
                note_use=note_use,
                is_subscribed=0
            )

            new_customer.save()

            send_mail_customer(email, key, name)
            send_mail_admin(name, email, phone_number, company_name,
                            license_requirements, product_interest, time_frame, note_use)

            return JsonResponse({
                'status': 'ok',
                'message': 'An evaluation key has been emailed to you! '
                           'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                           'for technical assistance and licensing questions.',
            })
        except ValueError:
            return JsonResponse({
                'status': 'failed',
                'message': 'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                           'for assistance or questions with your evaluation.',
            })

def auth_key_generate_ajax(request):
    allowed_product_id = request.GET.get('allowed_product_id')
    email = request.user.email
    system_id = request.GET.get('system_id')
    license_register= request.GET.get('license_register')

    try:
        allowed_product = License_Allowance.objects.get(id=allowed_product_id)

        product_id = allowed_product.product_id

        product = Product.objects.get(id=product_id)

        product_name = product.name
        product_type = product.type

        key = get_auth_license_key(system_id, license_register, product_type)

        new_license = License_Registration(
            key=key,
            user_email=email,
            system_hash=system_id,
            number_licenses=license_register,
            product_id=allowed_product_id,
            product_name=product_name,
        )

        new_license.save()

        allowed_product = License_Allowance.objects.get(id=allowed_product_id)
        allowed_product.registered_product = int(allowed_product.registered_product) + int(license_register)
        allowed_product.save()

        send_mail_admin_register(
            email=email,
            product_name=product_name,
            key=key,
            system_hash=system_id,
            licenses_register=license_register,
        )

        return JsonResponse({
            'status': 'ok',
            'message': 'An evaluation key has been registered! '
                       'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                       'for technical assistance and licensing questions.',
        })
    except ValueError:
        return JsonResponse({
            'status': 'failed',
            'message': 'Please <a href="http://www.openalpr.com/contact-us.html"> Contact-Us </a> '
                       'for assistance or questions with your evaluation.',
        })

def product_license_detail(request, product_id):

    licenses = License_Registration.objects.filter(product_id=product_id, user_email=request.user.email)
    allowed_product = License_Allowance.objects.get(id=product_id)
    product_id = allowed_product.product_id
    product = Product.objects.get(id=product_id)
    product_name = product.name

    context = {
        'product_name': product_name,
        'licenses': licenses,
    }

    return render(request, 'pages/product_license_detail.html', context)

def auth_key_register(request):

    if not request.user.is_authenticated():
        return redirect('main:login')

    user_id = request.user.id
    allowed_products = License_Allowance.objects.filter(user_id=user_id)

    for allowed_product in allowed_products:
        product_id = allowed_product.product_id
        product = Product.objects.get(id=product_id)
        product_name = product.name
        allowed_product.product_name = product_name

    context = {
        'allowed_products': allowed_products
    }
    return render(request, 'pages/license_register.html', context)

def chunkstring(string, length):

    return (string[0+i:length+i] for i in range(0, len(string), length))

def send_mail_customer(email, key, name):
    subject = "OpenALPR License Key"
    to = [email]
    from_email = 'info@openalpr.com'

    ctx = {
        'license_key': key,
        'first_name': name
    }

    message = get_template('email_template_customer_body.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

def send_mail_admin(name, email, phone_number, company_name,
                    license_requirements, product_interest, time_frame, note_use):
    subject = "OpenALPR License Key"
    to = admin_emails
    from_email = 'info@openalpr.com'

    ctx = {
        'first_name': name,
        'email': email,
        'phone_number': phone_number,
        'company_name': company_name,
        'license_requirements': license_requirements,
        'product_interest': product_interest,
        'note_use': note_use,
        'time_frame': time_frame
    }

    message = get_template('email_template_admin_body.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

def send_mail_admin_register(email, key, product_name,
                    licenses_register, system_hash):
    subject = "OpenALPR License Key"
    to = admin_emails
    from_email = 'info@openalpr.com'

    ctx = {
        'email': email,
        'key': key,
        'product_name': product_name,
        'licenses_register': licenses_register,
        'system_hash': system_hash,
    }

    message = get_template('email_template_admin_register_body.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

def get_free_license_key(email):

    license_expire_date_epoch = int(time.time()) + 1296000
    home_dir = expanduser("~")

    system_hash = re.sub('[^a-zA-Z0-9]', '_', email)
    system_hash = list(chunkstring(system_hash, 20))[0]

    cmd_string = '{home_dir}/licensemaker --system_hash {system_hash} --num_licenses {num_licenses} --license_type ' \
                 '{license_type} --maintenance_expires {maintenance_expires} --license_expires {license_expires} -s' \
        .format(home_dir=home_dir,
                system_hash=system_hash,
                num_licenses='2',
                license_type='3',
                maintenance_expires='2524604400',
                license_expires=str(license_expire_date_epoch))

    key = subprocess.Popen(
        cmd_string,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    ).stdout.read()

    return key

def get_auth_license_key(system_id, license_register, product_type):

    license_expire_date_epoch = int(time.time()) + 1296000
    home_dir = expanduser("~")

    cmd_string = '{home_dir}/licensemaker --system_hash {system_hash} --num_licenses {num_licenses} --license_type ' \
                 '{license_type} --maintenance_expires {maintenance_expires} --license_expires {license_expires} -s' \
        .format(home_dir=home_dir,
                system_hash=system_id,
                num_licenses=license_register,
                license_type=product_type,
                maintenance_expires='2524604400',
                license_expires=str(license_expire_date_epoch))

    key = subprocess.Popen(
        cmd_string,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    ).stdout.read()

    return key