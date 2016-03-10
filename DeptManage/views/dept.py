#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator

from DeptManage.forms import DeptListForm
from DeptManage.models import DeptManager
from Logs.models import Operating_Logs
from django.db.models import Q
import time

def AddDept(request):
    if request.method == "POST":
        form = DeptListForm(request.POST)
        if form.is_valid():
            form.save()
            records = Operating_Logs(username=request.user,mode='Add a dept',note=request.POST['name'],time=time.strftime('%Y-%m-%d %H:%M:%S'))
            records.save()
            return HttpResponseRedirect(reverse('listdepturl'))
    else:
        form = DeptListForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('DeptManage/dept.add.html',kwvars,RequestContext(request))

def ListDept(request):
    mList = DeptManager.objects.all()

    lst = SelfPaginator(request,mList, 10)

    kwvars = {
        'lPage':lst,
        'request':request,
    }
    return render_to_response('DeptManage/dept.list.html',kwvars,RequestContext(request))

def EditDept(request,ID):
    iDept = DeptManager.objects.get(id=ID)
    if request.method == "POST":
        form = DeptListForm(request.POST,instance=iDept)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listdepturl'))
    else:
        form = DeptListForm(instance=iDept)
    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }
    return render_to_response('DeptManage/dept.edit.html',kwvars,RequestContext(request))

def DeleteDept(request,ID):
    DeptManager.objects.filter(id = ID).delete()
    return HttpResponseRedirect(reverse('listdepturl'))

def SearchDept(request):
    s_text=request.GET.get('q','')
    if len(s_text) != 0:
        qset = (
            Q(name__icontains = s_text )|
            Q(level__icontains = s_text)|
            Q(owner__icontains = s_text)
        )
        results=DeptManager.objects.filter(qset).order_by('name')
    else:
        results = []
        #return render_to_response('DeptManage/dept.list.html',{'search_error':'查找内容不存在！'})
    return render_to_response('DeptManage/dept.search.html',{'s':results})
