#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from website.common.common import *

from Apply.forms import ApplyGitForm
from Apply.models import ApplyGit
import json

def ApplyGit(request):
    if request.method == "POST":
        form = ApplyGitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('applygiturl'))
    else:
        form = ApplyGitForm()
    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('Apply/apply.git.html',kwvars,RequestContext(request))

def ajax_dict(request):
    ips = request.GET['ips']
    st = '<option>请选择仓库</option>'
    if ips:
        gits = my_get('ssh %s gerrit ls-projects'%ips).split()
        for git in gits:
            st = st + '<option>%s</option>'%git
        return HttpResponse(json.dumps(st), content_type='application/json')
