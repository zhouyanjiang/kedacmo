#!/usr/bin/env python
# encoding: utf-8
import time
import os
import commands

dicall = {}

def my_get(cmd):
    return commands.getoutput(cmd).split()

def clear():
    os.system("rm -rf xmls sysdevrepo cbb.html")
    os.system("cp ../sample.html cbb.html")


def gen_branches():
    branches = []
    for one in my_get("git branch -a|grep sysdev_"):
        branches.append(one.split("remotes/origin/")[1])
    return branches

def gen_xmls():
    os.system("git clone 172.16.8.9:manifest/sysdevrepo")
    os.chdir("sysdevrepo")
    for one in gen_branches():
        os.system("git checkout %s"%one)
        listp = my_get("find . -path ./tag -prune -o -iname '*.xml' -a -print")
        for two in listp:
            dicall[one] = listp
            path = two[:two.rfind("/")]   
            print path
            print "*"*80
            filename = two[two.rfind("/")+1:]
            os.system("mkdir -p ../xmls/%s/%s"%(one,path))
            os.system("cp %s ../xmls/%s/%s"%(two,one,two))


def gen_info(filename):
    for one in open(filename).readlines():
        if 'info usage="' in one:
            return one.split('"')[1].split('"')[0]
    return "None"

def paixu(list1):
    list2 = []
    for one in list1:
        if "int" in one:
            list2.append(one)
    for one in list1:   
        if "rel" in one:
            list2.append(one)
    for one in list1:
        if one not in list2:
            list2.append(one)
    return list2
    

def gen_html():        
    f = open("cbb.html","a")
    brs = dicall.keys()
    brs = paixu(brs)
    for branch in brs:
        projects = dicall[branch]
        for project in projects:
            f.write('<tr><td>%s</td>'%(branch))
	    f.write('<td class="row"><li><a href="http://172.16.8.9/gitweb/?p=manifest/sysdevrepo.git;a=blob;f=%s;hb=%s" >%s</a></li></td>'%(project[2:],branch,project[2:]))
            print commands.getoutput('pwd')
            infomation = gen_info("xmls/%s/%s"%(branch,project[2:]))
            f.write('<td class="row">%s</td>'%infomation)
            repocode = "repo init -u 172.16.8.9:manifest/sysdevrepo.git -b %s -m %s"%(branch,project[2:])
            f.write("<td>%s</td>"%repocode)
            f.write("</tr>")
    f.write('</table>\n</div>\n<script src="/static/js/jquery.min.js"></script><script src="/static/js/bootstrap.min.js"></script><script src="/static/js/tableExport.js"></script><script src="/static/js/jquery.base64.js"></script><script src="/static/js/bootstrap-table.js"></script><script src="/static/js/bootstrap-table-export.js"></script><br>')
    f.write(time.strftime("最后更新时间：%Y-%m-%d %H:%M:%S"))
    f.write('{% include "common/paginator.html" %}\n')
    f.write('{% endblock %}\n')
    f.close()

if __name__ == '__main__':
    root = '/home/keda/workspace/kedacmo/crontab_scripts/Common_Info'
    os.chdir(root)
    clear()
    os.chdir(root)
    gen_xmls()
    os.chdir(root)
    gen_html()
    os.chdir(root)
    os.system("cp cbb.html ../../templates/sysrepoinfo.html")
