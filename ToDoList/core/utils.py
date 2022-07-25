from urllib import request
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.shortcuts import redirect

from core.models import UserValidation


def send_email(request: HttpRequest, validation: UserValidation):
    subject = "Subject"
    message = "Hi there, " + request.user.username + "\nYour code is: " + validation.code
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [request.user.email]

    email = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipent_list)

    return email.send()

def get_validation(user):
    try:
        return UserValidation.objects.get(user=user)
    except:
        return None

def group_required(group_name, redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            required_group = Group.objects.get(name=group_name)
            if(not required_group in request.user.groups.all()):
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function

def logout_required(redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            if(request.user.is_authenticated):
                
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function

def group_unrequired(group_name, redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            required_group = Group.objects.get(name=group_name)
            if(required_group in request.user.groups.all()):
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function