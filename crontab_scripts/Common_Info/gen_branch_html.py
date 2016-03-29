#!/usr/bin/env python
# encoding: utf-8
import time
import os
import commands

dicall = {}
dicpeople = {}

def my_get(cmd):
    return commands.getoutput(cmd).split("\n")

def clear():
    os.system("rm -rf branch.html")
    os.system("cp ../sample_branch.html  branch.html")

def gen_branches():
    repository = []
    for one in my_get("ssh 172.16.8.9 gerrit ls-projects|grep sysdev/"):
        repository.append(one)
    for one in repository:
	for two in  my_get("ssh 172.16.8.9 gerrit ls-user-refs --only-refs-heads -p %s -u caiyan"%one):
            try:
	        two = two.split("refs/heads/")[1].split()
		dicall.setdefault(one,[]).append(two)
            except Exception:
		print "ERROR %s"%one

def gen_people():
    repository = []
    for one in my_get("ssh 172.16.8.9 gerrit ls-projects|grep sysdev/"):
        repository.append(one)
    for one in repository:
	for two in my_get("ssh 172.16.8.9 gerrit ls-members %s/submit"%one):
	    two = two.split()[-1].split("@")[0]
	    if two == 'email':
 	        pass
	    else:
		dicpeople.setdefault(one,[]).append(two)

def gen_html():        
    f = open("branch.html","a")
    projects = dicall.keys()
    for project in projects:
	people = dicpeople[project]
	people = ','.join(people)
        branches = dicall[project]
        for branch in branches:
	    branch = ','.join(branch)
            f.write('<tr><td>%s</td>'%(project))
	    f.write('<td>%s</td>'%(branch))
            f.write("<td><font size='1' color='green'>%s</font></td>"%people)
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
    gen_branches()
    os.chdir(root)
    gen_people()
    os.chdir(root)
    gen_html()
    os.chdir(root)
    os.system("cp  branch.html ../../templates/sysbranchinfo.html")
