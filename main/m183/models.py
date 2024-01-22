from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='0000000000', blank=False)

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    STATUS_CHOICES = [
        ('hidden', 'Hidden'),
        ('published', 'Published'),
        ('deleted', 'Deleted'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='hidden')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content


class LoginAttempt(models.Model):
    username = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    sms_code = models.CharField(max_length=6, null=True, blank=True)
    code_expires = models.DateTimeField(null=True, blank=True)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} at {self.timestamp}"

    @classmethod
    def has_exceeded_limit(cls, username):
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        failed_attempts = cls.objects.filter(username=username, timestamp__gte=five_minutes_ago, failed=True).count()
        return failed_attempts >= 3
