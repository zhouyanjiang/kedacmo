#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from website.common.CommonPaginator import SelfPaginator
from website.common.common import *
from UserManage.views.permission import PermissionVerify

from django.contrib import auth
from django.contrib.auth import get_user_model
from UserManage.forms import LoginUserForm,ChangePasswordForm,AddUserForm,EditUserForm
from Logs.models import Operating_Logs
from UserManage.models import User
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def LoginUser(request):
    '''用户登录view'''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'GET' and request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = '/'

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)

    kwvars = {
        'request':request,
        'form':form,
        'next':next,
    }

    return render_to_response('UserManage/login.html',kwvars,RequestContext(request))

@login_required
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def ChangePassword(request):
    if request.method=='POST':
        form = ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            user = request.user.username
            origin_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            modifyldappassword(user,origin_password,new_password)
            form.save()
            records = Operating_Logs(username=user,mode='修改密码',note='Success',time=time.strftime('%Y-%m-%d %H:%M:%S'))
            records.save()
            subject = u'修改密码成功'
            message = u'修改密码成功'
            sendmail(gen_email(user),message,subject)
            return HttpResponseRedirect(reverse('logouturl'))
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/password.change.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListUser(request):
    mList = get_user_model().objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('UserManage/user.list.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def AddUser(request):

    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = AddUserForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/user.add.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditUser(request,ID):
    user = get_user_model().objects.get(id = ID)
    
    if request.method=='POST':
        form = EditUserForm(request.POST,instance=user)
        username = request.POST['username']
        newmail = request.POST['email']
        if form.is_valid():
            form.save()
            resetldapemail(username,newmail)
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = EditUserForm(instance=user
        )

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }
    
    return render_to_response('UserManage/user.edit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def DeleteUser(request,ID):
    if ID == '1':
        return HttpResponse(u'超级管理员不允许删除!!!')
    else:
        get_user_model().objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listuserurl'))

@login_required
def SearchUser(request):
    searchname = request.GET.get('q','')
    if len(searchname) != 0:
        user = get_user_model().objects.filter(username=searchname)
        info = ""
        if not user:
            try:
                info = genldapinfo(searchname)
            except Exception:
                info = ""
        email = ""
        if info:
            try:
                email = info[1]['mail'][0]
            except Exception:
                email = " "
        print email
        if email:
            c = User(username=searchname, email=email,is_active=1)
            c.save()
            user = get_user_model().objects.filter(username=searchname)
    else:
        user = []
    
    lst = SelfPaginator(request,user, 10)
    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('UserManage/user.search.html',kwvars,RequestContext(request))


@login_required
@PermissionVerify()
def ResetPassword(request,ID):
    user = get_user_model().objects.get(id = ID)
    newpassword = get_user_model().objects.make_random_password(length=6,allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
    #print '====>ResetPassword:%s-->%s' %(user.username,newpassword)
    user.set_password(newpassword)
    user.save()
    resetldappassowrd(user.username,newpassword)
    subject = u'重置密码成功'
    message = u'新密码:%s'%newpassword
    sendmail(gen_email(user.username),message,subject)
    records = Operating_Logs(username=request.user,mode=u'重置密码',note=u'给用户%s重置密码'%user.username,time=time.strftime('%Y-%m-%d %H:%M:%S'))
    records.save()
    kwvars = {
        'object':user,
        'newpassword':newpassword,
        'request':request,
    }

    return render_to_response('UserManage/password.reset.html',kwvars,RequestContext(request))
