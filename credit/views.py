# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import *

#from __future__ import unicode_literals
# Create your views here.


def index(request):
    return render(request, "index.html")


def logIn(request):
    name = request.POST['username'].split(" ")[0]
    pwd = request.POST['password']
    context = {}
    try:
        usr = Member.objects.get(first_name=name)
    except (KeyError, Member.DoesNotExist):
        context['errors'] = True
        return render(request, "form.html", context)
    else:
        if (usr.pwd == pwd):
            usr.logged_in = True
            usr.save()
            request.session['member_id'] = usr.id
            request.session.set_expiry(0)
            return HttpResponseRedirect(reverse('credit:index'))
        else:
            return render(request, "form.html", context)

def form(request):
    	return render(request, 'form.html')


def logOut(request):
    try:
        m_id = request.session['member_id']
    except KeyError:
        pass
    else:
        m = Member.objects.get(pk=m_id)
        m.logged_in = False
        m.save()
        del request.session['member_id']
        return render(request, "index.html")


def signUp(request):
    fname = request.POST.get('firstname','')
    lname = request.POST.get('lastname','')
    mail = request.POST.get('emailsignup','')
    password = request.POST.get('passwordsignup','')
    pwd2 = request.POST.get('passwordsignup_confirm','')
    context = {}

    if (password != pwd2):
        context['wrong'] = True
        return render(request, "form.html", context)
    else:
        mem = Member.objects.create(
            first_name=fname, last_name=lname, email=mail, pwd=password, logged_in=True)
        from twilio.rest import Client
        # Your Account SID from twilio.com/console
        account_sid = "AC0ecf8751edaaa7efa663b8ee5adfb9ce"
        # Your Auth Token from twilio.com/console
        auth_token  = "3195155aea2c94c1130a9b1dbe9147ef"

        client = Client(account_sid, auth_token)
        import random
        pin = random.randint(999, 9999)
        msg = "welcome "+fname+"  "+lname+" your secret pin is  " + str(pin)
        message = client.messages.create(
            to="+201550328883", 
            from_="+17175469588",
            body=msg)
        return HttpResponseRedirect(reverse('credit:index'))

    return HttpResponse("signup")
