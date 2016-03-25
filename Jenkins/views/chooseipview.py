#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from website.common.CommonPaginator import SelfPaginator
from website.common.common import *

from Jenkins.forms import ChooseIPView
from ServerManage.models import ServerManager
from Jenkins.models import JobBuild
import jenkins
import json
import time
import xml.etree.ElementTree as ET

def ChooseJob(request):
    if request.method == "POST":
        jobip = str(request.POST['job_ip'])
        jobname = str(request.POST['job_name'])
        info = ServerManager.objects.get(ip=jobip).note
        jenkins_user = info.split(":")[0]
        jenkins_pass = info.split(":")[1]
        try:
            lastid = JobBuild.objects.filter(job_ip=jobip).filter(job_name=jobname).latest('id').build_id
            nextid = lastid + 1
        except Exception:
            nextid = 1
        server = jenkins.Jenkins("http://%s:8080"%jobip,jenkins_user,jenkins_pass)
        jenkinsid = server.get_job_info(jobname)['nextBuildNumber']
        for i in range(nextid,jenkinsid):
            try:
                record = JobBuild(job_name=jobname,job_ip=jobip,build_id=i,build_result=server.get_build_info(jobname,i)['result'])
                record.save()
            except Exception:
                pass

        mList = JobBuild.objects.filter(job_ip=jobip).filter(job_name=jobname)
        lst = SelfPaginator(request,mList, 1000)

        kwvars = {
            'lPage':lst,
            'request':request,
        }
        return render_to_response('Jenkins/list.jobbuild.html',kwvars,RequestContext(request))
    else:
        form = ChooseIPView()

    kwvars = {
        'form':form,
        'request':request,
    }
    return render_to_response('Jenkins/choose.job.html',kwvars,RequestContext(request))

def ajax_ip(request):
    st1 = '<option>---</option>'
    st2 = '<option>All</option>'
    jobip = request.GET['ips']
    if jobip:
        info = ServerManager.objects.get(ip=jobip).note
        jenkins_user = info.split(":")[0]
        jenkins_pass = info.split(":")[1]
        server = jenkins.Jenkins("http://%s:8080"%jobip,jenkins_user,jenkins_pass)
        views=server.get_views()
        jobs=server.get_jobs()
        for v in views:
            st1 = st1 + '<option>%s</option>'%v['name']
        for j in jobs:
            st2 = st2 + '<option>%s</option>'%j['name']
        st = [st1,st2]
        return HttpResponse(json.dumps(st), content_type='application/json')

def ajax_view(request):
    st = '<option>All</option>'
    jobip = request.GET['ips']
    jobview = request.GET['views']

    if jobip and jobview != "All":
        info = ServerManager.objects.get(ip=jobip).note
        jenkins_user = info.split(":")[0]
        jenkins_pass = info.split(":")[1]
        server = jenkins.Jenkins("http://%s:8080"%jobip,jenkins_user,jenkins_pass)
        out=server.get_view_config(jobview.encode('utf-8'))
        for one in out.split('<jobNames>')[1].split('</jobNames>')[0].split('<string>')[1:]:
            st = st + '<option>%s</option>'%one.split("</string>")[0]
        return HttpResponse(json.dumps(st), content_type='application/json')
