from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chat(models.Model):
    class ChatType(models.TextChoices):
        DIRECT ="direct"
        GROUP="group"
        PRIVATE="private"


    title=models.CharField(max_length=100,blank=True, null=True)
    chat_image=models.ImageField(max_length=100,blank=True, null=True)
    users=models.ManyToManyField(User)
    type=models.CharField(max_length=10,choices=ChatType.choices, default=ChatType.DIRECT)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)



class Message(models.Model):
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE)
    message=models.TextField()
    reply=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='replies')
    seen=models.BooleanField(default=False)

    created_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
