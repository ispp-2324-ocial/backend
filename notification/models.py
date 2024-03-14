from django.db import models
from user.models import OcialClient, OcialUser

class Notification(models.Model):
    user_sender=models.ForeignKey(OcialClient,null=True,blank=True,related_name='user_sender',on_delete=models.CASCADE)
    user_receiver=models.ForeignKey(OcialUser,null=True,blank=True,related_name='user_receiver',on_delete=models.CASCADE)
    status=models.CharField(max_length=264,null=True,blank=True,default="unread")
    type_of_notification=models.CharField(max_length=264,null=True,blank=True)
