#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
import paramiko
from  jenkins.models  import Job_List,Job_View,Job_View_List
import xml.etree.ElementTree as ET

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


# Create your views here.
def index(request):
	return HttpResponse(u"jenkins info 信息!")

def home(request):
	TutorialList = ["HTML","CSS","jQuery","Python","Django"]
	return render(request,'home.html',{'TutorialList':TutorialList})
def jenkins(request):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("172.16.81.31",22,"root", "kdckdc")
    stdin,stdout,stderr = ssh.exec_command("ls /home/jenkins/jobs/")
    #print stdout.readlines()
    job_list=stdout.readlines()
    ssh.close()
    print job_list
    for j_l in job_list:
        Job_List.objects.get_or_create(job_name=j_l, job_ip="172.16.81.31")

    return render(request,'jenkins.html',{'job_list':job_list})

def get_job_view(request):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("172.16.81.31",22,"root", "kdckdc")
    stdin,stdout,stderr = ssh.exec_command("cat /home/jenkins/config.xml")
    config_file=stdout.readlines()
    ssh.close()
    #print config_file
    str_config_file=''.join(config_file)
    x_root=ET.fromstring(str_config_file)
    for item in x_root.iter('listView'):
        view_list=[]
        for name in item:
            if name.tag=='name':
                #print name.tag,name.text
                view_list.append(name.text)
            if name.tag=='jobNames':
                for str in name.iter('string'):
                    #print str.tag,str.text
                    view_list.append(str.text)
        v_name=view_list[0]
        
        Job_View_List.objects.get_or_create(job_views=v_name)
        view_list.pop(0)
        for v_list in view_list:
            #pass
            print v_name
            print v_list
            Job_View.objects.get_or_create(job_view=v_name,job_name=v_list)
    job_view_lists=Job_View.objects.all().values() 
    #print job_view_lists 
    return render(request,'job_view.html',{'job_view_lists':job_view_lists})

def get_job_item(request):

    #pass
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("172.16.81.31",22,"root", "kdckdc")
    stdin,stdout,stderr = ssh.exec_command("ls /home/jenkins/jobs/20141103_TrueLink_V5R0/builds")
    build_ids=stdout.readlines()
    ssh.close()
    print build_ids
    
