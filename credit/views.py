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
    logged_in = checkAuth(request)
    return render(request, "index.html",context={'log':logged_in})

def dashboard(request):
    logged_in = checkAuth(request)
    if logged_in == False:
        redirect('credit:logIn')
    else:
        m = Member.objects.get(pk=logged_in)
        return render(request,'dashboard.html',context={'member':m})


def checkAuth(request):
    try:
        m = request.session['member_id']
    except:
        return 0
    return m
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
    fname = request.POST.get('firstname', '')
    lname = request.POST.get('lastname', '')
    mail = request.POST.get('emailsignup', '')
    password = request.POST.get('passwordsignup', '')
    pwd2 = request.POST.get('passwordsignup_confirm', '')
    context = {}

    if (password != pwd2):
        context['wrong'] = True
        return render(request, "form.html", context)
    else:
        mem = Member.objects.create(
            first_name=fname, last_name=lname, email=mail, pwd=password, logged_in=True)

        return HttpResponseRedirect(reverse('credit:index'))

    return HttpResponse("signup")


def send(request):
    if request.method == 'POST':
        import random
        pin = random.randint(999, 9999)
        amount = request.POST.get('amount', '')
        sent_to = request.POST.get('user', '')
        s_to = Member.objects.get(first_name=sent_to)
        trans = transaction.objects.create(amount=int(amount), token=pin, status=0, done=0,
                                           t_type=0, user_one=Member.objects.get(pk=request.session['member_id']), user_two=s_to)
        return HttpResponseRedirect(reverse('credit:verf',kwargs={'trans_id':trans.id}))
    else:
        return render(request, 'send.html')


def recieve(request):
    if request.method == 'POST':
        import random
        pin = random.randint(999, 9999)
        from twilio.rest import Client
        # Your Account SID from twilio.com/console
        account_sid = "AC0ecf8751edaaa7efa663b8ee5adfb9ce"
        # Your Auth Token from twilio.com/console
        auth_token = "3195155aea2c94c1130a9b1dbe9147ef"

        client = Client(account_sid, auth_token)
        import random
        pin = random.randint(999, 9999)
  
        amount = request.POST.get('amount', '')
        sent_to = request.POST.get('user', '')
        msg = "code to confirm payment with amount "+amount+ " pin is  " + str(pin)
        message = client.messages.create(
            to="+201550328883",
            from_="+17175469588",
            body=msg)
        s_to = Member.objects.get(first_name=sent_to)
        trans = transaction.objects.create(amount=int(amount), token=pin, status=0, done=0,
                                           t_type=1, user_one=Member.objects.get(pk=request.session['member_id']), user_two=s_to)
        return redirect('credit:verf', trans_id=trans.id)
    else:
        return render(request, 'recieve.html')

def verf(request,trans_id):
    trans = transaction.objects.get(pk=trans_id)
    one = Member.objects.get(pk=trans.user_one.id)
    two = Member.objects.get(pk=trans.user_two.id)
    if trans.done == 1: 
        redirect('index')
    else:
        if request.method == 'POST':
            pin = request.POST.get("pin","")
            print "this is "+pin
            if int(pin) == trans.token:
                trans.status=1
                trans.done = 1
                trans.save()
                if trans.t_type == 0:
                    one.balance = one.balance-trans.amount
                    one.save()
                    two.balance = two.balance + trans.amount
                    two.save()
                else:
                    one.balance = one.balance+trans.amount
                    one.save()
                    two.balance = two.balance - trans.amount
                    two.save()
            else:
                redirect('index')
        else:
            return render(request,'verfiy.html',context={'t_id':trans_id})
