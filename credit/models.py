# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    pwd = models.CharField(max_length=200)
    logged_in = models.BooleanField(default=False)
    balance = models.IntegerField(default = 100)
    # upload_date=models.DateTimeField(auto_now_add =True)

    def __str__ (self):
        return self.last_name

class transaction(models.Model):
    amount = models.IntegerField()
    token  = models.IntegerField()
    user_one =  models.ForeignKey(Member,related_name="firstparty", on_delete=models.CASCADE)
    user_two =  models.ForeignKey(Member,related_name="sectparty", on_delete=models.CASCADE)
    status = models.IntegerField()
    t_type = models.IntegerField()
    done = models.IntegerField(default = 0)
