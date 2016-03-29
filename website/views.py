#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from Logs.models import Login_Logs

@login_required
def Home(request):
   record = Login_Logs.objects.get(username=request.user.username)
   a = locals()
   a['lastlogintime'] = record.logintime
   a['count'] = record.count
   return render_to_response('home.html',a,RequestContext(request))

def About(request):
   return render_to_response('about.html',locals(),RequestContext(request))

def Index(request):
   return render_to_response('index.html',locals(),RequestContext(request))

def SysRepoInfo(request):
   return render_to_response('sysrepoinfo.html',locals(),RequestContext(request))

def SysBranchInfo(request):
   return render_to_response('sysbranchinfo.html',locals(),RequestContext(request))
