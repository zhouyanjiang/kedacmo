from django.db import models

# Create your models here.
class Login_Logs(models.Model):
    username = models.CharField(max_length=40)
    logintime = models.CharField(max_length=40,null=True)
    count = models.IntegerField(max_length=11,null=True)


class Modify_Password_Logs(models.Model):
    username = models.CharField(max_length=40)
    ori_pwd = models.CharField(max_length=40)
    new_pwd = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
