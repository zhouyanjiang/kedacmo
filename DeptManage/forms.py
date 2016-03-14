#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from DeptManage.models import DeptManager

class DeptListForm(forms.ModelForm):
    class Meta:
        model = DeptManager
        fields = ('name','owner','fdept','note')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'owner' :  forms.TextInput(attrs={'class':'form-control'}),
            'fdept' : forms.Select(choices=[("","")]+[(x.name,x.name) for x in DeptManager.objects.all()],attrs={'class':'form-control'}),
            'note' :  forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self,*args,**kwargs):
        super(DeptListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'部门名称'
        self.fields['name'].error_messages={'required':u'请输入部门名称'}
        self.fields['owner'].label=u'部门负责人'
        self.fields['owner'].required=False
        self.fields['fdept'].label=u'上级部门'
        self.fields['fdept'].required=False
        self.fields['note'].label=u'备注'
        self.fields['note'].required=False
