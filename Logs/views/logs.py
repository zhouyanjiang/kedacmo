#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator

from Logs.forms import OperatingListForm
from Logs.models import Operating_Logs

from django.db.models import Q



def ListServer(request):
    mList = Operating_Logs.objects.all()
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }
    return render_to_response('Logs/logs.list.html',kwvars,RequestContext(request))



def SearchServer(request):
    s_text=request.GET.get('q','')
    if len(s_text) != 0:
        qset = (
            Q(username__icontains = s_text )|
            Q(time__icontains = s_text)|
            Q(mode__icontains = s_text)|
            Q(note__icontains = s_text)
        )
        results=Operating_Logs.objects.filter(qset).order_by('mode')
    else:
        results = []
    return render_to_response('Logs/logs.search.html',{'s':results})
