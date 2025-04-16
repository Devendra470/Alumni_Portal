from django.db import models

# Create your models here.
class Student(models.Model):
    role=models.CharField(max_length=10)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=128)
    graduation_year=models.IntegerField(null=True,blank=True)
    degree=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.first_name

class Alumni(models.Model):
    role=models.CharField(max_length=10)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=128)
    graduation_year=models.IntegerField(null=True,blank=True)
    degree=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.first_name

    