from django.db import models
from django.contrib.auth.models import User
from  django import forms



class RoomNumber(models.Model):

    roomNo=models.CharField(max_length=120,null=True,unique=False)
    STATUS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    seat=models.CharField(max_length=120,null=True,choices=STATUS)
    def __str__(self):
          return f"{self.roomNo} - {self.seat}"


class UserProfile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True,blank=True)
    Room_No=models.OneToOneField(RoomNumber,null=True,on_delete=models.SET_NULL)
    Phone=models.CharField(max_length=100,null=True,unique=True)
    Email=models.EmailField(max_length=100,null=True,unique=True)
    profile_pic=models.ImageField(null=True,blank=True)
    ID_NO=models.IntegerField(null=True,blank=True,unique=True)
    Batch=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name
# .now how will i show the RoomNumber options in the html page form 


class Complain(models.Model):
    name = models.CharField(max_length=255)
    registration_no = models.IntegerField()
    room_no = models.CharField(max_length=50)
    complaint = models.TextField()
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.name}"
    
class News (models.Model):
    news=models.CharField(max_length=255)
    def __str__(self):
        return  self.news




