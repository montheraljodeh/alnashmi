from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class NewUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stuts = models.CharField(max_length=100)

class Addtecher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    stuts = models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=100)

class student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    techer=models.ForeignKey(Addtecher,on_delete=models.CASCADE)
    stuts = models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=100)
    idsec=models.CharField(max_length=100)
    grade=models.CharField(max_length=100)
    date=models.DateField(blank=True,null=True)


class addstudent(models.Model):
    user = models.ForeignKey(Addtecher, on_delete=models.CASCADE, null=True)
    feed = models.ForeignKey(student, on_delete=models.CASCADE, null=True)



    
class Notifications(models.Model):
    title=models.CharField(max_length=256)
    message=models.TextField()
    viewied=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class message(models.Model):
    std1=models.CharField(max_length=100)
    t2=models.CharField(max_length=100)
    date1=models.DateField()
    reson=models.CharField(max_length=100)




class atdence(models.Model):
    sdtid=models.ForeignKey(student, on_delete=models.CASCADE, null=True)
    techerid = models.ForeignKey(Addtecher, on_delete=models.CASCADE, null=True)
    date=models.DateField(blank=True,null=True)
    stuts=models.CharField(max_length=100)

class rateandexam(models.Model):
    stduentid = models.ForeignKey(student, on_delete=models.CASCADE, null=True)
    techerid = models.ForeignKey(Addtecher, on_delete=models.CASCADE, null=True)
    Surah=models.CharField(max_length=100)
    pagenumber=models.IntegerField()
    date=models.DateField(blank=True, null=True)
    behavior=models.IntegerField()
    points=models.IntegerField()

class addadmin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    stuts = models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=100)



# Create your models here.
class StudentForm1(models.Model):
    Addtecher = models.ForeignKey(Addtecher, on_delete=models.CASCADE, null=True)
    stduentid = models.ForeignKey(student, on_delete=models.CASCADE, null=True)
    date=models.DateField(blank=True, null=True)
    file = models.FileField()  # for creating file input

    class Meta:
        db_table = "student"












