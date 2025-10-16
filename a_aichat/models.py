from django.db import models
from django.contrib.auth.models import User
import uuid

class AIChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chats')
    message = models.TextField()
    is_user_message = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
        
    def __str__(self):
        return f"{self.user.username} - {'User' if self.is_user_message else 'AI'} - {self.created}"

class HelperChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helper_chats')
    message = models.TextField()
    is_user_message = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
        
    def __str__(self):
        return f"{self.user.username} - {'User' if self.is_user_message else 'Helper'} - {self.created}"


class TravelChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_chats')
    message = models.TextField()
    is_user_message = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return f"{self.user.username} - {'User' if self.is_user_message else 'Travel'} - {self.created}"
    
