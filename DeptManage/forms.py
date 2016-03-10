#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from DeptManage.models import DeptManager


class DeptListForm(forms.ModelForm):
    class Meta:
        model = DeptManager
        fields = ('name','level','owner')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'level' : forms.TextInput(attrs={'class':'form-control'}),
            'owner' :  forms.PasswordInput(attrs={'class':'form-control'}),
        }
    def __init__(self,*args,**kwargs):
        super(DeptListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'部门名称'
        self.fields['name'].error_messages={'required':u'请输入部门名称'}
        self.fields['level'].label=u'部门级别'
        self.fields['level'].required=False
        self.fields['owner'].label=u'部门负责人'
        self.fields['owner'].required=False
