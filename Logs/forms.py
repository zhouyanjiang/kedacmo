#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from Logs.models import Operating_Logs


class OperatingListForm(forms.ModelForm):
    class Meta:
        model = Operating_Logs
        fields = ('mode','username','time','note')
        widgets = {
            'mode' : forms.TextInput(attrs={'class':'form-control'}),
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'time' :  forms.PasswordInput(attrs={'class':'form-control'}),
            'note' :  forms.PasswordInput(attrs={'class':'form-control'}),
        }
