from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    name= models.CharField(max_length=56,null=True,blank=True)
    email= models.EmailField(max_length=56,null=True,blank=True)
    password= models.CharField(max_length=256,null=True,blank=True)
    picture= models.ImageField(null=True,blank=True)
    paypal_email= models.EmailField(max_length=56,null=True,blank=True)
    balance= models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return f"{self.name},  {self.paypal_email}"

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return f"{self.name}"
class Language(models.Model):
    language_name = models.CharField(max_length=256)
    def __str__(self):
        return f"{self.language_name}"

class Level(models.Model):
    level_number = models.IntegerField()
    def __str__(self):
        return f"{self.level_number}"

class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    Win_Payment = models.IntegerField(null=False,blank=False,default=5)
    def __str__(self):
        return f"{self.category}, {self.language}, {self.level},"

class Question(models.Model):
    question = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(null=True, blank=True)
    option_a =  models.CharField(max_length=56,null=True,blank=False)
    option_b =  models.CharField(max_length=56,null=True,blank=False)
    option_c =  models.CharField(max_length=56,null=True,blank=False)
    option_d =  models.CharField(max_length=56,null=True,blank=False)
    ans_key =  models.CharField(max_length=56,null=True,blank=False)
    asked =  models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question}"

class Completed_Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField(blank=False,null=False)
    def __str__(self):
        return f"{self.user},{self.category},{self.level}"

from datetime import datetime

class Status(models.Model):
    status = models.CharField(max_length=10,null=True,blank=False)
    def __str__(self):
        return f"{self.status}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    payment = models.CharField(max_length=56,null=True,blank=False)
    date =  models.DateTimeField(default=datetime.now())
    def __str__(self):
        return f"{self.payment},  {self.payment_status}"