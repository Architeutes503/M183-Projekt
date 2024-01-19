from django.contrib import admin
from .models import Post, Comment, LoginAttempt, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LoginAttempt)
admin.site.register(Profile)