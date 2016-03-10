#-*- coding: UTF-8 -*- 
from django.db import models

# Create your models here.

#jenkins ip
class Ip(models.Model):
    name=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

#视图
class Vieww(models.Model):
    name=models.CharField(max_length=100)
    ips=models.ManyToManyField(Ip)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

#job名称
class Job(models.Model):
    name=models.CharField(max_length=100)
    ips=models.ManyToManyField(Ip)
    viewws=models.ManyToManyField(Vieww)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

#job编译信息
class Job_Build_Item(models.Model):
    job_name=models.ForeignKey(Job)
    build_id=models.CharField(max_length=100)
    build_result=models.CharField(max_length=100)
    build_result_reason=models.CharField(max_length=100)
    def __unicode__(self):
        return self.build_id,self.build_result,self.build_result_reason
    class Meta:
        ordering=['build_id']

		
