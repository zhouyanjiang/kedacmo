from django.db import models

# Create your models here.
class Modify_Password_Logs(models.Model):
    username = models.CharField(max_length=40)
    ori_pwd = models.CharField(max_length=40)
    new_pwd = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
