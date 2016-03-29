#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from ServerManage.models import ServerManager


class ServerListForm(forms.ModelForm):
    class Meta:
        model = ServerManager
        fields = ('ip','logname','passwd','servertype','serveruse','bitwide','note')
        widgets = {
            'ip' : forms.TextInput(attrs={'class':'form-control'}),
            'logname' : forms.TextInput(attrs={'class':'form-control'}),
            'passwd' :  forms.PasswordInput(attrs={'class':'form-control'}),
            'servertype' : forms.Select(choices=((u'----',u'请选择类型'),(u'Windows XP',u'Windows XP'),(u'Windows 7',u'Windows 7'),(u'CentOS 5.6',u'CentOS 5.6'),(u'CentOS 6.6',u'CentOS 6.6'),(u'Ubuntu 14.04',u'Ubuntu 14.04'),(u'Ubuntu 12.04',u'Ubuntu 12.04'),(u'Redhat 4.4',u'Redhat 4.4'),(u'Redhat 5.2 ',u'Redhat 5.2')),attrs={'class':'form-control'}),
            'serveruse' : forms.Select(choices=((u'----',u'请选择用途'),(u'编译机',u'编译机'),(u'SVN 源码机',u'SVN 源码机'),(u'Git 源码机',u'Git 源码机'),(u'版本机',u'版本机'),(u'应用服务器',u'应用服务器')),attrs={'class':'form-control'}),
            'bitwide' : forms.RadioSelect(choices=((u'32位',u'32位'),(u'64位',u'64位')),attrs={'class':'list-inline'}),
            'note' : forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            #'status' : forms.HiddenInput,
        }
    def __init__(self,*args,**kwargs):
        super(ServerListForm,self).__init__(*args,**kwargs)
        self.fields['ip'].label=u'机器IP'
        self.fields['ip'].error_messages={'required':u'请输入机器IP'}
        self.fields['logname'].label=u'登录账号'
        self.fields['logname'].required=False
        self.fields['passwd'].label=u'密码'
        self.fields['passwd'].required=False
        self.fields['servertype'].label=u'服务器类型'
        self.fields['servertype'].required=False
        self.fields['bitwide'].label=u'CPU位宽'
        self.fields['bitwide'].required=False
        self.fields['serveruse'].label=u'服务器用途'
        self.fields['serveruse'].required=False
        self.fields['note'].label=u'备注'
        self.fields['note'].required=False


    #if ip:
    #    s = ServerManager.objects.filter(ip = ip)
