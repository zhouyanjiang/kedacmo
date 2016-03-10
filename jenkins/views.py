#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
import paramiko
from  jenkins.models  import Vieww,Job,Ip,Job_Build_Item
import xml.etree.ElementTree as ET
import re

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
    j_ip=Ip.objects.get(name='172.16.81.31')
    for j_l in job_list:
        j_l=j_l.strip()
        try:
            j_name=Job.objects.get(name=j_l)
        except Job.DoesNotExist:
            Job.objects.get_or_create(name=j_l)
            j_name=Job.objects.get(name=j_l)
        else:
            print "%s this job is exist"  %j_l 
        j_name.ips.add(j_ip)
        j_name.save()
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
        v_name=view_list[0]  #v_name视图名称       
        Vieww.objects.get_or_create(name=v_name)
        j_view=Vieww.objects.get(name=v_name)
        view_list.pop(0)
        for v_list in view_list:
            v_list=v_list.strip()
            print v_name
            print v_list #v_list是（属于这个v_name视图的）job列表中的job名称
            #Job.objects.get_or_create(name=v_list)
            try: 
                j_name=Job.objects.get(name=v_list)
            except Job.DoesNotExist:
               Job.objects.get_or_create(name=v_list) 
               j_name=Job.objects.get(name=v_list)
            else:
                print "%s this job exist"%v_list
            j_name.viewws.add(j_view)
            j_name.save()

    job_view_lists=Job.objects.all().values() 
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
    for id in build_ids:
        id=id.strip()
        m=re.match('\d+$',id)
        if m is not None:
            print m.group()
            print id
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("172.16.81.31",22,"root", "kdckdc")
            str_command="cat /home/jenkins/jobs/20141103_TrueLink_V5R0/builds/%s/build.xml"%id
            stdin,stdout,stderr = ssh.exec_command(str_command)
            build_items=stdout.readlines()
            ssh.close()
            str_build_items=''.join(build_items)
            build_root=ET.fromstring(str_build_items)
            for item_id in build_root.iter('number'):
                print item_id.text #一次构建的ID
            for item_id_info in build_root.iter('displayName'):
                print item_id_info.text #一次构建的ID显示
            for item_result in build_root.iter('result'):
                print item_result.text #一次构建的结果
            j_name=Job.objects.get(name="20141103_TrueLink_V5R0")
            try:
                job_item=Job_Build_Item.objects.get(build_id=item_id_info,build_result=item_result)
            except Job_Build_Item.DoesNotExist:
                Job_Build_Item.objects.get_or_create(job_name=j_name,build_id=item_id_info,build_result=item_result)
                job_item=Job_Build_Item.objects.get(build_id=item_id_info,build_result=item_result)
            else:
                print "% this build_item exist"%item_id
            #job_item.job_name.add(j_name)
            job_item.save()

    job_build_items=Job_Build_Item.objects.all().values()
    print job_build_items
    return render(request,'job_build_items.html',{'job_build_items':job_build_items})
