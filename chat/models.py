from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"Chat {self.id}"

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    chat = models.ForeignKey(Chat, related_name='Messages', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Message {self.id} - Chat {self.chat_id}"
