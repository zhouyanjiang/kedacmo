from django.db import models

# Create your models here.

class Job_Name(models.Model):
    job_name=models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.job_name
    class Meta:
        ordering=['job_name']

class Job_Ip(models.Model):
    job_ip=models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.ip
    class Meta:
        ordering=['job_ip']

class Job_Ip_Name(models.Model):
    job_name=models.CharField(max_length=100,unique=True)
    job_ip=models.ForeignKey(Job_Ip)

    def __unicode__(self):
        return self.job_name
    class Meta:
        ordering=['job_name']

class Job_List(models.Model):
    job_name=models.CharField(max_length=100,unique=True)
    job_ip=models.CharField(max_length=100)
    def __unicode__(self):
        return self.job_name
    class Meta:
        ordering=['job_name']


class Job_View_List(models.Model):
    job_views=models.CharField(max_length=100,unique=True,primary_key=True)
    def __unicode__(self):
        return self.job_views
    class Meta:
        ordering=['job_views']

class Job_View(models.Model):
    #job_view=models.ForeignKey(Job_View_List)
    job_view=models.CharField(max_length=100)
    job_name=models.CharField(max_length=100)
    def __unicode__(self):
    	#self.job_view,
        return self.job_name
    class Meta:
        ordering=['job_view']

class Job_Build_Item(models.Model):
    job_name=models.ForeignKey(Job_Name)
    build_id=models.CharField(max_length=100)
    build_result=models.CharField(max_length=100)
    build_result_reason=models.CharField(max_length=100)
    def __unicode__(self):
        return self.job_name,self.build_id,self.build_result,self.build_result_reason
    class Meta:
        ordering=['build_id']

		
