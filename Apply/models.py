from django.db import models

# Create your models here.

class ApplyGit(models.Model):
    serverIp = models.CharField(max_length=255)
    gitName = models.CharField(max_length=255)
    authority = models.CharField(max_length=255)
    operator = models.CharField(max_length=255)
    applicant = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    starttime = models.CharField(max_length=255)
    endtime = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __unicode__(self):
        return self.serverIp
