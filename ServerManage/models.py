from django.db import models

# Create your models here.
class ServerStatus(models.Model):
    ip = models.GenericIPAddressField(max_length=255, unique=True,db_index=True)
    is_active = models.BooleanField(default=False)
    cpuinfo = models.CharField(max_length=255)
    meminfo = models.CharField(max_length=255)
    diskinfo = models.CharField(max_length=255)
    boottime = models.CharField(max_length=255)
    ldapstatus = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s(%s)' %(self.cpuinfo,self.meminfo)

class ServerManager(models.Model):
    ip = models.GenericIPAddressField(max_length=255, unique=True,db_index=True)
    logname = models.CharField(max_length=40)
    passwd = models.CharField(max_length=40)
    servertype = models.CharField(max_length=255)
    serveruse = models.CharField(max_length=255)
    #status = models.ForeignKey(ServerStatus,null=True,blank=True)

    def __unicode__(self):
        return self.ip
