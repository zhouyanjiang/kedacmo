#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from website.common.common import *

from DeptManage.forms import DeptListForm
from DeptManage.models import DeptManager
from Logs.models import Operating_Logs
from django.db.models import Q
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def AddDept(request):
    if request.method == "POST":
        form = DeptListForm(request.POST)
        if form.is_valid():
            print gen_macro("EMAIL")
            print gen_macro("AAA")
            form.save()
            records = Operating_Logs(username=request.user,mode=u'新建部门',note=request.POST['name'],time=time.strftime('%Y-%m-%d %H:%M:%S'))
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
    cond = request.GET.get('q','')
    if len(cond) != 0:
        if ":" not in cond:
            qset = (
                Q(name__icontains = cond )|
                Q(fdept__icontains = cond)|
                Q(owner__icontains = cond)|
                Q(note__icontains = cond)
            )
        else:
            try:
                k=cond.split(":")[0]
                v=cond.split(":")[1]
                if k == 'name':qset = Q(name = v)
                if k == 'fdept':qset = Q(fdept = v)
                if k == 'owner':qset = Q(owner = v)
                if k == 'note':qset = Q(note = v)
            except Exception:
                return 0
        results=DeptManager.objects.filter(qset).order_by('name')
        print results
    else:
        results = []
    lst = SelfPaginator(request,results, 10)
    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('DeptManage/dept.search.html',kwvars,RequestContext(request))
