#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from Apply.models import ApplyGit
from ServerManage.models import ServerManager

class ApplyGitForm(forms.ModelForm):
    class Meta:
        model = ApplyGit
        fields = ('serverIp','gitName','authority','reason')
        widgets = {
            'serverIp' : forms.Select(choices=[("","")]+[(x.ip,x.ip) for x in ServerManager.objects.all()],attrs={'class':'form-control'}),
            'gitName' : forms.Select(choices=[(u'-',u'请选择仓库')],attrs={'class':'form-control'}),
            'authority' : forms.Select(choices=((u'-',u'请选择权限'),(u'read',u'读取和提交'),(u'submit',u'审核'),(u'tag',u'tag提交')),attrs={'class':'form-control'}),
            'reason' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(ApplyGitForm,self).__init__(*args,**kwargs)
        self.fields['serverIp'].label=u'IP'
        self.fields['serverIp'].required=True
        self.fields['gitName'].label=u'Git'
        self.fields['gitName'].required=False
        self.fields['authority'].label=u'权限种类'
        self.fields['authority'].required=False
        self.fields['reason'].label=u'申请理由'
        self.fields['reason'].required=False
