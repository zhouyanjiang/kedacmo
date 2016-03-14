#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import time
import commands
import getopt
import getpass
from ftplib import FTP
import urllib
import urllib2
import re
import xlwt
import xlrd
import smtplib
import ldap
import ldap.modlist as modlist
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')

NO_OUT = '>/dev/null 2>&1'
LDAP_HOST = '172.16.6.107'
LDAP_ADMIN = 'cn=admin,dc=test,dc=com'
LDAP_BIND = 'dc=test,dc=com'
LDAP_PASSWD = '123456'
GIT_SYS_HOST = '172.16.8.9'

def get_user():
    return getpass.getuser()

def gen_date():
    return time.strftime('%Y-%m-%d')

def gen_time():
    return time.strftime('%H:%M:%S')

def gen_prelog():
    date = gen_date()
    time1 = gen_time()
    mark = '==='
    return  mark + date + ' ' + time1 + mark

def print_error(message):
    print gen_prelog() + 'ERROR: ' + message
    sys.exit(-1)

def print_warning(message):
    print gen_prelog() + 'WARNING: ' + message

def print_message(message):
    print gen_prelog() + 'LOG: ' + message

def my_successed():
    print_message('Successed!')

def my_sys(cmd):
    os.system('%s %s' % (cmd, NO_OUT))

def my_get(cmd):
    return commands.getoutput(cmd)

def remkdir(path):
    my_sys('rm -rf %s' % path)
    my_sys('mkdir -p %s' % path)

def my_mkdir(path):
    if not os.path.exists(path):
        my_sys('mkdir -p %s' % path)

def gen_lines(filename):
    try:
        return open(filename).readlines()
    except Exception:
        print_error('Open %s Failed!'%filename)

def lists_to_file(LIST, filename):
    f = open(filename, 'wb')
    for one in LIST:
        one = one + '\n'
        f.write(one.encode('utf-8'))
    f.close()

def translate_by_google(STR, CODE):
    values = {
        'hi': CODE,
        'ie': 'UTF-8',
        'text': STR,
        'langpair': 'en|%s' % CODE }
    url = 'http://translate.google.cn/'
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    browser = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
    req.add_header('User-Agent', browser)
    response = urllib2.urlopen(req)
    html = response.read()
    p = re.compile('(?<=TRANSLATED_TEXT=).*?;')
    m = p.search(html)
    out = m.group(0).strip(';')
    return out

def remove_quote(STR):
    if STR.startswith('"') and STR.endswith('"'):
        return STR[1:-1]
    elif STR.startswith("'") and STR.endswith("'"):
        return STR[1:-1]
    else:
        return STR

def sendmail(receiver,message,subject):
    sender = 'sqlmail@kedacom.com'
    smtpserver = '10.5.0.54'
    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['from']='CMOS' 
    msg['to']=receiver 
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(sender, '888')
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def modifyldappassword(username,oldpass,newpass):
    l = ldap.initialize("ldap://%s"%LDAP_HOST)
    l.protocol_version = ldap.VERSION3
    l.simple_bind(LDAP_ADMIN,LDAP_PASSWD)
    searchScope  = ldap.SCOPE_SUBTREE
    searchFiltername = "cn"
    retrieveAttributes = None
    searchFilter = '(' + searchFiltername + "=" + username +')'
    ldap_result_id = l.search(LDAP_BIND, searchScope, searchFilter, retrieveAttributes)
    result_type, result_data = l.result(ldap_result_id,1)
    user = result_data[0][0]
    l.passwd(user,oldpass,newpass)

def resetldappassowrd(username,newpass):
    l = ldap.initialize("ldap://%s"%LDAP_HOST)
    l.protocol_version = ldap.VERSION3
    l.simple_bind(LDAP_ADMIN,LDAP_PASSWD)
    searchScope  = ldap.SCOPE_SUBTREE
    searchFiltername = "cn"
    retrieveAttributes = None
    searchFilter = '(' + searchFiltername + "=" + username +')'
    ldap_result_id = l.search(LDAP_BIND, searchScope, searchFilter, retrieveAttributes)
    result_type, result_data = l.result(ldap_result_id,1)
    user = result_data[0][0]
    oldpass = result_data[0][1]['userPassword'][0]
    old = {'userPassword':oldpass}
    new = {'userPassword':str(newpass)}
    ldif = modlist.modifyModlist(old,new)
    print old,new
    l.modify_s(user,ldif)

def checkldap(username,password):
    l = ldap.initialize("ldap://%s"%LDAP_HOST)
    l.protocol_version = ldap.VERSION3
    l.simple_bind(LDAP_ADMIN,LDAP_PASSWD)
    searchScope  = ldap.SCOPE_SUBTREE
    searchFiltername = "cn"
    retrieveAttributes = None
    searchFilter = '(' + searchFiltername + "=" + username +')'
    ldap_result_id = l.search("dc=test,dc=com", searchScope, searchFilter, retrieveAttributes)
    try:
        result_type, result_data = l.result(ldap_result_id,1)
        user = result_data[0][0]
    except Exception:
        return None
    try:
        mail = result_data[0][1]['mail'][0]
        l.simple_bind_s(user,password)
        return mail
    except Exception:
        return " "

def gen_email(user):
    from UserManage.models import User
    return User.objects.get(username=user).email
