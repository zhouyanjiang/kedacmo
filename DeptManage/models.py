from django.db import models

# Create your models here.

class DeptManager(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    fdept = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
