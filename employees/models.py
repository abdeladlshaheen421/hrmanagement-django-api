from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.conf import settings
# Create your models here.


class Employee(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Attendence(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True,null=True)
