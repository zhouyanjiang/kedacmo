#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from Jenkins.models import JobBuild
from ServerManage.models import ServerManager

class ChooseIPView(forms.ModelForm):
    class Meta:
        model = JobBuild
        fields = ('job_ip','job_view','job_name')
        widgets = {
            'job_ip' : forms.Select(choices=[("","")]+[(x.ip,x.ip) for x in ServerManager.objects.filter(serveruse=u'应用服务器')],attrs={'class':'form-control'}),
            'job_view' : forms.Select(choices=[(u'---',u'---')],attrs={'class':'form-control'}),
            'job_name' : forms.Select(choices=[(u'All',u'All')],attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(ChooseIPView,self).__init__(*args,**kwargs)
        self.fields['job_ip'].label=u'IP'
        self.fields['job_ip'].required=True
        self.fields['job_view'].label=u'View'
        self.fields['job_view'].required=False
        self.fields['job_name'].label=u'Job'
        self.fields['job_name'].required=False
