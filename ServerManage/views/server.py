#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator

from ServerManage.forms import ServerListForm
from ServerManage.models import ServerManager
from Logs.models import Operating_Logs
from django.db.models import Q
import time

def AddServer(request):
    if request.method == "POST":
        form = ServerListForm(request.POST)
        if form.is_valid():
            form.save()
            records = Operating_Logs(username=request.user,mode='增添服务器',note=request.POST['ip'],time=time.strftime('%Y-%m-%d %H:%M:%S'))
            records.save()
            return HttpResponseRedirect(reverse('listserverurl'))
    else:
        form = ServerListForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('ServerManage/server.add.html',kwvars,RequestContext(request))

def ListServer(request):
    mList = ServerManager.objects.all()

    lst = SelfPaginator(request,mList, 10)

    kwvars = {
        'lPage':lst,
        'request':request,
    }
    return render_to_response('ServerManage/server.list.html',kwvars,RequestContext(request))

def EditServer(request,ID):
    iServer = ServerManager.objects.get(id=ID)
    if request.method == "POST":
        form = ServerListForm(request.POST,instance=iServer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listserverurl'))
    else:
        form = ServerListForm(instance=iServer)
    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }
    return render_to_response('ServerManage/server.edit.html',kwvars,RequestContext(request))

def DeleteServer(request,ID):
    ServerManager.objects.filter(id = ID).delete()
    return HttpResponseRedirect(reverse('listserverurl'))

def SearchServer(request):
    s_text=request.GET.get('q','')
    if len(s_text) != 0:
        qset = (
            Q(ip__icontains = s_text )|
            Q(logname__icontains = s_text)|
            Q(servertype__icontains = s_text)|
            Q(serveruse__icontains = s_text)
        )
        results=ServerManager.objects.filter(qset).order_by('ip')
    else:
        results = []
    lst = SelfPaginator(request, results , 10)
    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('ServerManage/server.search.html',kwvars,RequestContext(request))
