from django.db import models

# Create your models here.
class JobBuild(models.Model):
    job_name=models.CharField(max_length=255)
    job_ip=models.IPAddressField()
    job_view=models.CharField(max_length=255)
    job_project=models.CharField(max_length=255)
    build_id=models.IntegerField(max_length=255)
    build_result=models.CharField(max_length=255)
    build_result_reason=models.CharField(max_length=255)

    def __unicode__(self):
        return self.build_id,self.build_result,self.build_result_reason
    class Meta:
        ordering=['build_id']

